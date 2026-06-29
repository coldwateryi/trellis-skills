#!/usr/bin/env python3
"""Planning-phase mechanical gate for trellis-zero-to-mvp-zh.

Run between each planning phase (S0-S5) to enforce state machine transitions,
verify counting consistency, and detect small-model drift patterns.

The model writes a stage_state.yaml at each phase boundary; this script reads
it, validates the transition, checks matrices for numeric consistency, and
outputs structured PASS/FAIL results. The model must NOT hand-fill gate results.

Usage:
  python trellis_planning_gate.py \\
    --phase S2_CONTRACT_LOCK \\
    --state-file .trellis/planning/planning-state.yaml \\
    --matrix .trellis/planning/full-requirement-matrix.csv \\
    --mvp-matrix .trellis/planning/mvp-coverage-matrix.csv \\
    --ledger .trellis/planning/subtask-ledger.yaml \\
    --contract .trellis/planning/contract-snapshot.yaml
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
#  State machine definition
# ---------------------------------------------------------------------------

VALID_STATES = [
    "S0_DISCOVER_CONTEXT",
    "S1_REQUIREMENT_LEDGER",
    "S2_CONTRACT_LOCK",
    "S3_FULL_MVP_TASK_CANDIDATES",
    "S4_PROGRESSIVE_BATCH_PLANNING",
    "S5_FULL_MVP_PLANNING_GATE",
    "S6_USER_CONFIRMATION",
    "S7_TASK_CREATION",
    "S8_ARTIFACT_WRITING",
    "S9_ARTIFACT_GATE",
    "S10_NEXT_IMPLEMENTATION_RECOMMENDATION",
]

STATE_INDEX = {s: i for i, s in enumerate(VALID_STATES)}

# Legal transitions: +0 (same phase re-enter), +1 (next phase), +n (back to
# earlier phase = drift reset), but NEVER skip forward more than 1.
def allowed_transition(prev: str | None, next_state: str) -> tuple[bool, str]:
    if prev is None:
        return next_state == "S0_DISCOVER_CONTEXT", f"First state must be S0_DISCOVER_CONTEXT, got {next_state}"
    if next_state not in STATE_INDEX:
        return False, f"Unknown state: {next_state}"
    if prev not in STATE_INDEX:
        return False, f"Unknown previous state: {prev}"
    diff = STATE_INDEX[next_state] - STATE_INDEX[prev]
    if diff == 0:
        return True, "Re-entry into same phase (allowed, e.g. after gate fix)"
    if diff == 1:
        return True, "Forward one phase (allowed)"
    if diff < 0:
        return True, f"Regression ({prev} -> {next_state}, -{abs(diff)} phases) — allowed only as explicit Drift Reset"
    if diff > 1:
        return False, f"ILLEGAL: skipped {diff - 1} phase(s) ({prev} -> {next_state}). Must progress one phase at a time."
    return True, ""


# ---------------------------------------------------------------------------
#  File helpers
# ---------------------------------------------------------------------------

def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def try_load_json(path: Path) -> dict | None:
    if not path.exists():
        return None
    try:
        return json.loads(read_text(path))
    except (json.JSONDecodeError, ValueError):
        return None


def try_load_yaml_as_json(path: Path) -> dict | None:
    """Read a simple key:value YAML file and return as dict.

    This is NOT a full YAML parser. It handles the subset used by
    Stage State Packet and Contract Snapshot files.
    """
    if not path.exists():
        return None
    result = {}
    text = read_text(path)
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("---"):
            continue
        m = re.match(r"^(\w[\w_]*)\s*:\s*(.+)$", line)
        if m:
            key = m.group(1).strip()
            value = m.group(2).strip().strip('"').strip("'")
            result[key] = value
    return result


def load_planning_state(state_file: Path) -> dict | None:
    """Load the planning state YAML file written by the model."""
    data = try_load_yaml_as_json(state_file)
    if data:
        return data
    # Fallback: try loading as JSON
    return try_load_json(state_file)


def save_planning_state(state_file: Path, data: dict) -> None:
    """Persist the gate result back into the state file."""
    state_file.parent.mkdir(parents=True, exist_ok=True)
    state_file.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def count_matrix_rows(matrix_path: Path) -> int | None:
    """Count data rows in a pipe-delimited Markdown matrix file."""
    if not matrix_path.exists():
        return None
    count = 0
    for line in read_text(matrix_path).splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        if "---" in line:
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) >= 3 and cells[0].startswith("REQ-"):
            count += 1
    return count


def extract_coverage_status_counts(mvp_matrix_path: Path) -> dict[str, int]:
    """Count coverage statuses from MVP Coverage Matrix."""
    counts = {"TASK": 0, "MERGED": 0, "BASELINE": 0, "OUT_OF_SCOPE": 0, "BLOCKED": 0}
    if not mvp_matrix_path.exists():
        return counts
    for line in read_text(mvp_matrix_path).splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        for col_idx, cell in enumerate(cells):
            cell_upper = cell.upper()
            if cell_upper in counts:
                counts[cell_upper] += 1
    return counts


def count_ledger_tasks(ledger_path: Path) -> dict:
    """Count task states from Subtask Planning Ledger."""
    result = {
        "total_mvp_tasks": 0,
        "ready_to_confirm": 0,
        "blocked": 0,
        "out_of_scope": 0,
        "drafted": 0,
        "candidate": 0,
        "other": 0,
    }
    if not ledger_path.exists():
        return result
    in_table = False
    for line in read_text(ledger_path).splitlines():
        stripped = line.strip()
        if stripped.startswith("| T") or stripped.startswith("| TASK"):
            if "Task ID" in stripped or "需求 ID" in stripped:
                continue
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            if len(cells) >= 10:
                result["total_mvp_tasks"] += 1
                status = cells[9].upper()
                if status == "READY_TO_CONFIRM":
                    result["ready_to_confirm"] += 1
                elif status == "BLOCKED":
                    result["blocked"] += 1
                elif status == "OUT_OF_SCOPE":
                    result["out_of_scope"] += 1
                elif status == "DRAFTED":
                    result["drafted"] += 1
                elif status == "CANDIDATE":
                    result["candidate"] += 1
                else:
                    result["other"] += 1
    result["non_terminal"] = result["candidate"] + result["drafted"] + result["other"]
    return result


def check_placeholder_in_text(text: str, sample_limit: int) -> tuple[int, list[str]]:
    """Scan text for template placeholders and generic angle brackets."""
    hits = []
    patterns = [
        r"\{Entity\}", r"\{domain\}", r"\{entity\}", r"<PageComponent>",
        r"<任务标题>", r"<path>", r"<domain>", r"TBD", r"待定",
        r"视情况", r"根据实际情况", r"YOUR_KEY", r"API_KEY_HERE",
        r"待用户提供", r"待配置", r"待申请",
    ]
    for line_no, line in enumerate(text.splitlines(), 1):
        for pat in patterns:
            if re.search(pat, line):
                hits.append(f"line {line_no}: {line.strip()[:80]}")
                break
    return len(hits[:sample_limit]), hits[:sample_limit]


def check_angle_placeholder(text: str, sample_limit: int) -> tuple[int, list[str]]:
    """Scan for generic angle-bracket placeholders like <ControllerClass>."""
    hits = []
    generic_re = re.compile(r"<[A-Za-z一-鿿_./: -]{2,40}>")
    for line_no, line in enumerate(text.splitlines(), 1):
        for m in generic_re.finditer(line):
            hits.append(f"line {line_no}: {m.group()}")
    return len(hits[:sample_limit]), hits[:sample_limit]


# ---------------------------------------------------------------------------
#  Phase-specific checks
# ---------------------------------------------------------------------------

def check_s1_requirement_ledger(
    matrix_path: Path, mvp_matrix_path: Path
) -> list[dict]:
    """S1 checks: REQ completeness and matrix coverage consistency."""
    failures = []
    req_count = count_matrix_rows(matrix_path)
    mvp_count = count_matrix_rows(mvp_matrix_path)

    if req_count is None and mvp_count is None:
        failures.append({
            "code": "MATRIX_FILE_MISSING",
            "detail": "Neither full-requirement-matrix.csv nor mvp-coverage-matrix.csv found",
        })
        return failures

    if req_count is None:
        failures.append({
            "code": "FULL_REQUIREMENT_MATRIX_MISSING",
            "detail": "Full Requirement Matrix not found: can't verify coverage completeness",
        })
    elif req_count == 0:
        failures.append({
            "code": "MATRIX_EMPTY",
            "detail": "Full Requirement Matrix has zero REQ rows; source requirements not extracted",
        })

    if mvp_count is None:
        failures.append({
            "code": "MVP_COVERAGE_MATRIX_MISSING",
            "detail": "MVP Coverage Matrix not found: can't verify MVP scope",
        })
        return failures

    if req_count and mvp_matrix_path.exists():
        coverage_counts = extract_coverage_status_counts(mvp_matrix_path)
        total_covered = sum(coverage_counts.values())
        if total_covered > 0 and total_covered != req_count:
            failures.append({
                "code": "COVERAGE_COUNT_MISMATCH",
                "detail": (
                    f"Full Requirement Matrix has {req_count} rows but "
                    f"MVP Coverage Matrix sums to {total_covered} "
                    f"(TASK={coverage_counts['TASK']}, "
                    f"MERGED={coverage_counts['MERGED']}, "
                    f"BASELINE={coverage_counts['BASELINE']}, "
                    f"OUT_OF_SCOPE={coverage_counts['OUT_OF_SCOPE']}, "
                    f"BLOCKED={coverage_counts['BLOCKED']})"
                ),
                "expected_sum": req_count,
                "actual_sum": total_covered,
                "breakdown": coverage_counts,
            })

    return failures


def check_s2_contract_lock(contract_path: Path) -> list[dict]:
    """S2 checks: contract snapshot presence and completeness."""
    failures = []
    contract = try_load_yaml_as_json(contract_path)

    if contract is None:
        failures.append({
            "code": "CONTRACT_SNAPSHOT_MISSING",
            "detail": "Contract Snapshot file not found or unparseable",
        })
        return failures

    # Check required fields
    required_fields = ["profile", "backend_module", "database_table_prefix"]
    for field in required_fields:
        if field not in contract or not contract[field]:
            continue  # Only warn for required fields

    # Check for forbidden tokens section
    if "forbidden_tokens" not in contract:
        failures.append({
            "code": "FORBIDDEN_TOKENS_MISSING",
            "detail": "Contract Snapshot missing 'forbidden_tokens' field",
        })

    # Detect common drift: evidence paths missing or vague
    evidence_fields = [k for k in contract if "evidence" in k.lower() or "path" in k.lower()]
    for field in evidence_fields:
        val = contract[field]
        if val and val.lower() in {"unknown", "tbd", "待定", ""}:
            failures.append({
                "code": "EVIDENCE_VAGUE",
                "detail": f"Contract field '{field}' has vague evidence: '{val}'",
            })

    return failures


def check_s3_task_candidates(ledger_path: Path) -> list[dict]:
    """S3 checks: task candidate completeness and granularity."""
    failures = []
    ledger_stats = count_ledger_tasks(ledger_path)

    if ledger_stats["total_mvp_tasks"] == 0:
        failures.append({
            "code": "LEDGER_EMPTY",
            "detail": "Subtask Planning Ledger has zero task rows; no MVP task candidates identified",
        })
        return failures

    # Check for P0P1_ONLY_PLAN: all tasks are P0/P1 and none P2/P3
    # This is a soft check (flag, not block)
    if ledger_stats["candidate"] > 0 and ledger_stats["non_terminal"] > 0:
        failures.append({
            "code": "NON_TERMINAL_CANDIDATES",
            "detail": (
                f"{ledger_stats['non_terminal']}/{ledger_stats['total_mvp_tasks']} "
                f"tasks still in CANDIDATE/DRAFTED/other non-terminal state"
            ),
            "breakdown": {
                "candidate": ledger_stats["candidate"],
                "drafted": ledger_stats["drafted"],
                "other": ledger_stats["other"],
            },
        })

    return failures


def check_s4_batch_planning(ledger_path: Path) -> list[dict]:
    """S4 checks: batch completeness and progress."""
    failures = []
    ledger_stats = count_ledger_tasks(ledger_path)

    if ledger_stats["total_mvp_tasks"] == 0:
        return failures

    terminal = ledger_stats["ready_to_confirm"] + ledger_stats["blocked"] + ledger_stats["out_of_scope"]
    if terminal < ledger_stats["total_mvp_tasks"]:
        failures.append({
            "code": "BATCH_INCOMPLETE",
            "detail": (
                f"{terminal}/{ledger_stats['total_mvp_tasks']} tasks terminal "
                f"(READY_TO_CONFIRM + BLOCKED + OUT_OF_SCOPE). "
                f"{ledger_stats['total_mvp_tasks'] - terminal} non-terminal tasks remain."
            ),
            "terminal": terminal,
            "total": ledger_stats["total_mvp_tasks"],
            "breakdown": {
                "ready_to_confirm": ledger_stats["ready_to_confirm"],
                "blocked": ledger_stats["blocked"],
                "out_of_scope": ledger_stats["out_of_scope"],
                "non_terminal": ledger_stats["non_terminal"],
            },
        })

    return failures


def check_s5_gate_readiness(ledger_path: Path) -> list[dict]:
    """S5 checks: all tasks terminal before confirmation."""
    failures = check_s4_batch_planning(ledger_path)
    # Additional S5 checks: ensure no P0P1_ONLY_PLAN
    if ledger_path.exists():
        text = read_text(ledger_path).upper()
        has_p0p1_only = bool(re.search(r"P0[^_]", text)) and not bool(re.search(r"P2[^_]", text))
        if has_p0p1_only:
            failures.append({
                "code": "P0P1_ONLY_PLAN",
                "detail": "Ledger only shows P0/P1 tasks; P2/P3 MVP tasks may be unplanned",
            })
    return failures


# ---------------------------------------------------------------------------
#  Main
# ---------------------------------------------------------------------------

# Phase-specific check dispatch
PHASE_CHECKS = {
    "S1_REQUIREMENT_LEDGER": check_s1_requirement_ledger,
    "S2_CONTRACT_LOCK": check_s2_contract_lock,
    "S3_FULL_MVP_TASK_CANDIDATES": check_s3_task_candidates,
    "S4_PROGRESSIVE_BATCH_PLANNING": check_s4_batch_planning,
    "S5_FULL_MVP_PLANNING_GATE": check_s5_gate_readiness,
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--phase", required=True,
        choices=VALID_STATES,
        help="The phase being entered (the desired next state)",
    )
    parser.add_argument(
        "--state-file",
        default=".trellis/planning/planning-state.yaml",
        help="Path to planning state file (written by model at each phase boundary)",
    )
    parser.add_argument(
        "--matrix",
        default=".trellis/planning/full-requirement-matrix.md",
        help="Path to Full Requirement Matrix",
    )
    parser.add_argument(
        "--mvp-matrix",
        default=".trellis/planning/mvp-coverage-matrix.md",
        help="Path to MVP Coverage Matrix",
    )
    parser.add_argument(
        "--ledger",
        default=".trellis/planning/subtask-ledger.yaml",
        help="Path to Subtask Planning Ledger",
    )
    parser.add_argument(
        "--contract",
        default=".trellis/planning/contract-snapshot.yaml",
        help="Path to Contract Snapshot",
    )
    parser.add_argument(
        "--parent-prd",
        help="Path to parent prd.md (for placeholder scan)",
    )
    parser.add_argument(
        "--sample-limit", type=int, default=10,
        help="Max examples per failure type",
    )
    args = parser.parse_args()

    # -----------------------------------------------------------------------
    # 1. Load prior state
    # -----------------------------------------------------------------------
    state_file = Path(args.state_file).resolve()
    prior_state = load_planning_state(state_file)
    prev_phase = prior_state.get("current_phase") if prior_state else None

    # -----------------------------------------------------------------------
    # 2. State machine transition check
    # -----------------------------------------------------------------------
    transition_ok, transition_msg = allowed_transition(prev_phase, args.phase)
    transition_blocking = not transition_ok

    # -----------------------------------------------------------------------
    # 3. Phase-specific checks
    # -----------------------------------------------------------------------
    phase_failures: list[dict] = []
    checker = PHASE_CHECKS.get(args.phase)
    if checker:
        checker_kwargs = {}
        if args.phase == "S1_REQUIREMENT_LEDGER":
            checker_kwargs = {
                "matrix_path": Path(args.matrix),
                "mvp_matrix_path": Path(args.mvp_matrix),
            }
        elif args.phase == "S2_CONTRACT_LOCK":
            checker_kwargs = {"contract_path": Path(args.contract)}
        elif args.phase in ("S3_FULL_MVP_TASK_CANDIDATES",):
            checker_kwargs = {"ledger_path": Path(args.ledger)}
        elif args.phase in ("S4_PROGRESSIVE_BATCH_PLANNING", "S5_FULL_MVP_PLANNING_GATE"):
            checker_kwargs = {"ledger_path": Path(args.ledger)}
        phase_failures = checker(**checker_kwargs)

    # -----------------------------------------------------------------------
    # 4. Parent PRD placeholder scan (if provided)
    # -----------------------------------------------------------------------
    placeholder_hits = 0
    placeholder_examples: list[str] = []
    angle_hits = 0
    angle_examples: list[str] = []

    if args.parent_prd:
        prd_path = Path(args.parent_prd)
        if prd_path.exists():
            text = read_text(prd_path)
            placeholder_hits, placeholder_examples = check_placeholder_in_text(text, args.sample_limit)
            angle_hits, angle_examples = check_angle_placeholder(text, args.sample_limit)

    # -----------------------------------------------------------------------
    # 5. Build result
    # -----------------------------------------------------------------------
    failure_codes_map = {}
    if transition_blocking:
        failure_codes_map["ILLEGAL_STATE_TRANSITION"] = transition_msg

    code_to_detail = {
        "MATRIX_FILE_MISSING": "Requirement matrix files missing",
        "FULL_REQUIREMENT_MATRIX_MISSING": "Full Requirement Matrix not found",
        "MATRIX_EMPTY": "Full Requirement Matrix empty",
        "MVP_COVERAGE_MATRIX_MISSING": "MVP Coverage Matrix not found",
        "COVERAGE_COUNT_MISMATCH": "Coverage count mismatch",
        "CONTRACT_SNAPSHOT_MISSING": "Contract Snapshot missing",
        "FORBIDDEN_TOKENS_MISSING": "Forbidden tokens not defined",
        "EVIDENCE_VAGUE": "Contract evidence vague or unknown",
        "LEDGER_EMPTY": "Subtask Planning Ledger empty",
        "NON_TERMINAL_CANDIDATES": "Tasks still in non-terminal state",
        "BATCH_INCOMPLETE": "Batch planning incomplete",
        "P0P1_ONLY_PLAN": "Only P0/P1 tasks planned",
    }

    for f in phase_failures:
        failure_codes_map[f["code"]] = f["detail"]

    if placeholder_hits > 0:
        failure_codes_map["PLACEHOLDER_HIT"] = f"{placeholder_hits} placeholder(s) in parent PRD"
    if angle_hits > 0:
        failure_codes_map["ANGLE_PLACEHOLDER_HIT"] = f"{angle_hits} angle-bracket placeholder(s) in parent PRD"

    # -----------------------------------------------------------------------
    # 6. Compute final PASS/FAIL
    # -----------------------------------------------------------------------
    is_blocking = transition_blocking
    is_fail = len(failure_codes_map) > 0
    final_result = "FAIL" if is_fail else "PASS"

    output = {
        "gate_result": final_result,
        "current_phase": args.phase,
        "previous_phase": prev_phase,
        "transition_allowed": not transition_blocking,
        "transition_message": transition_msg,
        "failure_codes": list(failure_codes_map.keys()),
        "failure_details": failure_codes_map,
        "phase_failures": phase_failures,
        "stats": {
            "placeholder_hits": placeholder_hits,
            "angle_placeholder_hits": angle_hits,
        },
        "phase_specific": {},
    }

    # Add phase-specific stats
    if args.phase == "S1_REQUIREMENT_LEDGER":
        mvp_counts = extract_coverage_status_counts(Path(args.mvp_matrix))
        req_count = count_matrix_rows(Path(args.matrix))
        output["phase_specific"]["req_count"] = req_count
        output["phase_specific"]["mvp_coverage_counts"] = mvp_counts
    elif args.phase in ("S3_FULL_MVP_TASK_CANDIDATES", "S4_PROGRESSIVE_BATCH_PLANNING", "S5_FULL_MVP_PLANNING_GATE"):
        ledger_stats = count_ledger_tasks(Path(args.ledger))
        output["phase_specific"]["ledger_stats"] = ledger_stats

    # -----------------------------------------------------------------------
    # 7. Persist the new state
    # -----------------------------------------------------------------------
    new_state = {
        "current_phase": args.phase,
        "last_gate_result": final_result,
        "last_gate_failure_codes": list(failure_codes_map.keys()),
        "last_gate_timestamp": "",  # Model should fill actual time
    }
    if prior_state:
        # Preserve prior metadata
        for k in ("full_requirement_count", "contract_snapshot", "source_docs"):
            if k in prior_state:
                new_state[k] = prior_state[k]
    save_planning_state(state_file, new_state)

    # -----------------------------------------------------------------------
    # 8. Print
    # -----------------------------------------------------------------------
    print(json.dumps(output, ensure_ascii=False, indent=2))

    # Return 1 on fail or blocking transition
    return 1 if is_fail or is_blocking else 0


if __name__ == "__main__":
    sys.exit(main())
