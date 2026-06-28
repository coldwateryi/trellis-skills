#!/usr/bin/env python3
"""Deterministic artifact gate for trellis-zero-to-mvp-zh outputs.

The planner model must not hand-fill gate counts. Run this script after task
creation and artifact writing, then copy the resulting counts into the final
Artifact Gate report.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path


PLACEHOLDER_RE = re.compile(
    r"\{Entity\}|\{domain\}|\{entity\}|<PageComponent>|<任务标题>|"
    r"<path>|<domain>|<valid-token>|<token>|<why>|TBD|待定|视情况|"
    r"根据实际情况|YOUR_KEY|API_KEY_HERE|待用户提供|待配置|待申请"
)

EXTERNAL_CONFIG_RE = re.compile(
    r"YOUR_KEY|API_KEY_HERE|待用户提供|待配置|待申请|待开通|待获取|"
    r"placeholder key|replace with.*key",
    re.IGNORECASE,
)

GENERIC_ANGLE_RE = re.compile(r"<[A-Za-z0-9_.:/ -]+>")

NEEDS_DESIGN_RE = re.compile(
    r"design\.md\s*[:：]?\s*(需要|required)|必要产物.*design\.md|写prd\.md\+design\.md",
    re.IGNORECASE,
)

NEEDS_IMPLEMENT_RE = re.compile(
    r"implement\.md\s*[:：]?\s*(需要|required)|必要产物.*implement\.md",
    re.IGNORECASE,
)

HIGH_COMPLEXITY_RE = re.compile(r"复杂度\s*[:：]\s*高")
MEDIUM_COMPLEXITY_RE = re.compile(r"复杂度\s*[:：]\s*中")
DESIGN_SURFACE_SECTION_RE = re.compile(
    r"^##\s+任务影响面矩阵\s*$", re.MULTILINE
)
MARKDOWN_HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.MULTILINE)

YES_VALUES = {"是", "yes", "y", "true", "1", "涉及", "需要"}


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def first_examples(values: list[str], limit: int) -> list[str]:
    return values[:limit]


def task_dirs(tasks_root: Path) -> list[Path]:
    return sorted(p.parent for p in tasks_root.glob("*/task.json") if p.is_file())


def scoped_task_dirs(tasks_root: Path, parent_task_json: Path | None) -> list[Path]:
    if parent_task_json is None or not parent_task_json.exists():
        return task_dirs(tasks_root)
    try:
        data = json.loads(read_text(parent_task_json))
    except json.JSONDecodeError:
        return task_dirs(tasks_root)

    dirs = [parent_task_json.parent]
    children = data.get("children")
    if isinstance(children, list):
        for child in children:
            if isinstance(child, str):
                child_dir = tasks_root / child
                if (child_dir / "task.json").exists():
                    dirs.append(child_dir)
    return sorted(dict.fromkeys(dirs))


def scan_files(
    tasks_root: Path,
    dirs: list[Path],
    forbidden_patterns: list[re.Pattern[str]],
    contract_mismatch_patterns: list[re.Pattern[str]],
    sample_limit: int,
    jsonl_mode: str,
) -> dict:
    md_files = sorted(path for task_dir in dirs for path in task_dir.glob("*.md"))
    jsonl_files = sorted(path for task_dir in dirs for path in task_dir.glob("*.jsonl"))

    placeholder_hits: list[str] = []
    external_config_hits: list[str] = []
    angle_placeholder_hits: list[str] = []
    forbidden_hits: list[str] = []
    contract_mismatch_hits: list[str] = []
    jsonl_seed_hits: list[str] = []

    for path in md_files + jsonl_files:
        text = read_text(path)
        for lineno, line in enumerate(text.splitlines(), 1):
            if PLACEHOLDER_RE.search(line):
                placeholder_hits.append(f"{rel(path, tasks_root)}:{lineno}")
            elif GENERIC_ANGLE_RE.search(line):
                angle_placeholder_hits.append(f"{rel(path, tasks_root)}:{lineno}")
            if EXTERNAL_CONFIG_RE.search(line):
                external_config_hits.append(f"{rel(path, tasks_root)}:{lineno}")
            for pattern in forbidden_patterns:
                if pattern.search(line):
                    forbidden_hits.append(f"{rel(path, tasks_root)}:{lineno}")
            for pattern in contract_mismatch_patterns:
                if pattern.search(line):
                    contract_mismatch_hits.append(f"{rel(path, tasks_root)}:{lineno}")

    for path in jsonl_files:
        text = read_text(path)
        if '"_example"' in text:
            jsonl_seed_hits.append(rel(path, tasks_root))

    blocking_jsonl_seed_hits = jsonl_seed_hits if jsonl_mode == "required" else []

    return {
        "prd_files": len([p for p in md_files if p.name == "prd.md"]),
        "design_files": len([p for p in md_files if p.name == "design.md"]),
        "implement_files": len([p for p in md_files if p.name == "implement.md"]),
        "jsonl_files": len(jsonl_files),
        "jsonl_mode": jsonl_mode,
        "placeholder_hits": len(placeholder_hits),
        "placeholder_examples": first_examples(placeholder_hits, sample_limit),
        "external_config_hits": len(external_config_hits),
        "external_config_examples": first_examples(external_config_hits, sample_limit),
        "angle_placeholder_hits": len(angle_placeholder_hits),
        "angle_placeholder_examples": first_examples(angle_placeholder_hits, sample_limit),
        "jsonl_seed_hits": len(blocking_jsonl_seed_hits),
        "jsonl_seed_hits_raw": len(jsonl_seed_hits),
        "jsonl_seed_examples": first_examples(blocking_jsonl_seed_hits, sample_limit),
        "jsonl_seed_examples_raw": first_examples(jsonl_seed_hits, sample_limit),
        "forbidden_token_hits": len(forbidden_hits),
        "forbidden_token_examples": first_examples(forbidden_hits, sample_limit),
        "contract_mismatch_hits": len(contract_mismatch_hits),
        "contract_mismatch_examples": first_examples(contract_mismatch_hits, sample_limit),
    }


def declared_artifact_scan(
    tasks_root: Path,
    dirs: list[Path],
    parent_dir: Path | None,
    sample_limit: int,
) -> dict:
    missing_declared: list[str] = []
    high_complexity_missing: list[str] = []

    for task_dir in dirs:
        if parent_dir is not None and task_dir == parent_dir:
            continue
        prd = task_dir / "prd.md"
        if not prd.exists():
            continue
        text = read_text(prd)
        needs_design = bool(NEEDS_DESIGN_RE.search(text))
        needs_implement = bool(NEEDS_IMPLEMENT_RE.search(text))
        is_high = bool(HIGH_COMPLEXITY_RE.search(text))
        is_medium = bool(MEDIUM_COMPLEXITY_RE.search(text))

        if needs_design and not (task_dir / "design.md").exists():
            missing_declared.append(f"{rel(task_dir, tasks_root)}:design.md")
        if needs_implement and not (task_dir / "implement.md").exists():
            missing_declared.append(f"{rel(task_dir, tasks_root)}:implement.md")

        if is_high:
            if not (task_dir / "design.md").exists():
                high_complexity_missing.append(f"{rel(task_dir, tasks_root)}:design.md")
            if not (task_dir / "implement.md").exists():
                high_complexity_missing.append(f"{rel(task_dir, tasks_root)}:implement.md")
        elif is_medium and needs_design and not (task_dir / "design.md").exists():
            high_complexity_missing.append(f"{rel(task_dir, tasks_root)}:design.md")

    return {
        "missing_declared_artifacts": len(missing_declared),
        "missing_declared_examples": first_examples(missing_declared, sample_limit),
        "high_complexity_missing_artifacts": len(high_complexity_missing),
        "high_complexity_missing_examples": first_examples(high_complexity_missing, sample_limit),
    }


def markdown_section(text: str, heading_pattern: re.Pattern[str]) -> str:
    marker = heading_pattern.search(text)
    if not marker:
        return ""
    next_heading = re.search(r"^##\s+", text[marker.end() :], re.MULTILINE)
    if not next_heading:
        return text[marker.end() :]
    return text[marker.end() : marker.end() + next_heading.start()]


def parse_markdown_table(section: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in section.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or "---" in stripped:
            continue
        parts = [part.strip() for part in stripped.strip("|").split("|")]
        if len(parts) >= 5:
            rows.append(parts)
    if rows and rows[0][0] in {"影响面", "Surface"}:
        rows = rows[1:]
    return rows


def heading_from_location(location: str) -> tuple[str | None, str | None]:
    value = location.strip().strip("`")
    if not value or value.lower() in {"none", "not-applicable", "不适用"}:
        return None, None
    if "#" not in value:
        return value, None
    filename, heading = value.split("#", 1)
    return filename.strip() or None, heading.strip() or None


def has_heading(path: Path, heading: str | None) -> bool:
    if not path.exists():
        return False
    if not heading:
        return True
    text = read_text(path)
    normalized = heading.strip().lower()
    for match in MARKDOWN_HEADING_RE.finditer(text):
        candidate = match.group(1).strip().lower()
        if candidate == normalized:
            return True
    return False


def design_surface_scan(
    tasks_root: Path,
    dirs: list[Path],
    parent_dir: Path | None,
    sample_limit: int,
) -> dict:
    missing: list[str] = []
    declared_count = 0
    satisfied_count = 0
    prd_with_matrix = 0
    prd_without_matrix: list[str] = []

    for task_dir in dirs:
        if parent_dir is not None and task_dir == parent_dir:
            continue
        prd = task_dir / "prd.md"
        if not prd.exists():
            continue
        text = read_text(prd)
        section = markdown_section(text, DESIGN_SURFACE_SECTION_RE)
        if not section:
            prd_without_matrix.append(rel(prd, tasks_root))
            continue
        prd_with_matrix += 1
        for row in parse_markdown_table(section):
            surface, involved, design_location, implement_location, *rest = row
            if involved.strip().lower() not in YES_VALUES:
                continue
            declared_count += 1
            row_missing: list[str] = []

            design_file, design_heading = heading_from_location(design_location)
            if design_file:
                design_path = task_dir / design_file
                if not has_heading(design_path, design_heading):
                    row_missing.append(f"{design_file}#{design_heading or ''}")

            implement_file, implement_heading = heading_from_location(implement_location)
            if implement_file:
                implement_path = task_dir / implement_file
                if not has_heading(implement_path, implement_heading):
                    row_missing.append(f"{implement_file}#{implement_heading or ''}")

            if row_missing:
                missing.append(
                    f"{rel(task_dir, tasks_root)}:{surface}: missing {', '.join(row_missing)}"
                )
            else:
                satisfied_count += 1

    return {
        "design_surface_prd_with_matrix": prd_with_matrix,
        "design_surface_prd_without_matrix": len(prd_without_matrix),
        "design_surface_prd_without_matrix_examples": first_examples(
            prd_without_matrix, sample_limit
        ),
        "design_surface_declared_count": declared_count,
        "design_surface_satisfied_count": satisfied_count,
        "design_surface_missing_hits": len(missing),
        "design_surface_missing_examples": first_examples(missing, sample_limit),
    }


def requirement_section(text: str) -> str:
    marker = re.search(r"^##\s+需求 ID\s*$", text, re.MULTILINE)
    if not marker:
        return ""
    next_heading = re.search(r"^##\s+", text[marker.end() :], re.MULTILINE)
    if not next_heading:
        return text[marker.end() :]
    return text[marker.end() : marker.end() + next_heading.start()]


def coverage_scan(parent_prd: Path | None) -> dict:
    if parent_prd is None or not parent_prd.exists():
        return {
            "coverage_rows": None,
            "coverage_status_counts": {},
            "coverage_count_mismatch_hits": 0,
            "coverage_count_examples": [],
        }

    text = read_text(parent_prd)
    section = requirement_section(text)
    status_counts: Counter[str] = Counter()
    rows = 0
    for line in section.splitlines():
        if not line.startswith("| REQ-"):
            continue
        parts = [part.strip() for part in line.strip().split("|")]
        if len(parts) < 5:
            continue
        rows += 1
        status_counts[parts[3]] += 1

    mismatches: list[str] = []
    summary_match = re.search(r"\|\s*原始功能点总数\s*\|\s*(\d+)\s*\|", text)
    if summary_match and rows and int(summary_match.group(1)) != rows:
        mismatches.append(
            f"原始功能点总数={summary_match.group(1)} but requirement rows={rows}"
        )

    declared_gate = re.search(r"\|\s*coverage_count_mismatch_hits\s*\|\s*(\d+)\s*\|", text)
    if declared_gate and int(declared_gate.group(1)) == 0 and mismatches:
        mismatches.append("declared coverage_count_mismatch_hits=0 despite mismatch")

    return {
        "coverage_rows": rows,
        "coverage_status_counts": dict(status_counts),
        "coverage_count_mismatch_hits": len(mismatches),
        "coverage_count_examples": mismatches,
    }


def declared_gate_mismatch(parent_prd: Path | None, actual: dict) -> dict:
    if parent_prd is None or not parent_prd.exists():
        return {"declared_gate_mismatch_hits": 0, "declared_gate_mismatch_examples": []}

    text = read_text(parent_prd)
    key_map = {
        "placeholder_hits": actual.get("placeholder_hits", 0),
        "angle_placeholder_hits": actual.get("angle_placeholder_hits", 0),
        "jsonl_seed_hits": actual.get("jsonl_seed_hits", 0),
        "forbidden_token_hits": actual.get("forbidden_token_hits", 0),
        "contract_mismatch_hits": actual.get("contract_mismatch_hits", 0),
        "coverage_count_mismatch_hits": actual.get("coverage_count_mismatch_hits", 0),
        "high_complexity_missing_artifacts": actual.get("high_complexity_missing_artifacts", 0),
        "missing_declared_artifacts": actual.get("missing_declared_artifacts", 0),
        "design_surface_prd_without_matrix": actual.get(
            "design_surface_prd_without_matrix", 0
        ),
        "design_surface_missing_hits": actual.get("design_surface_missing_hits", 0),
        "external_config_hits": actual.get("external_config_hits", 0),
    }

    mismatches: list[str] = []
    for key, observed in key_map.items():
        match = re.search(rf"\|\s*{re.escape(key)}\s*\|\s*(\d+)\s*\|", text)
        if match and int(match.group(1)) != observed:
            mismatches.append(f"{key}: declared {match.group(1)} observed {observed}")

    return {
        "declared_gate_mismatch_hits": len(mismatches),
        "declared_gate_mismatch_examples": mismatches,
    }


def expected_task_count(parent_task_json: Path | None) -> int | None:
    if parent_task_json is None or not parent_task_json.exists():
        return None
    try:
        data = json.loads(read_text(parent_task_json))
    except json.JSONDecodeError:
        return None
    children = data.get("children")
    if isinstance(children, list):
        return 1 + len(children)
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tasks", required=True, help="Path to .trellis/tasks")
    parser.add_argument("--parent-task-json", help="Path to parent task.json")
    parser.add_argument("--parent-prd", help="Path to parent prd.md")
    parser.add_argument(
        "--jsonl-mode",
        choices=["required", "optional", "inline"],
        default="required",
        help=(
            "required blocks on _example JSONL seeds; optional and inline report raw "
            "seed examples without failing the gate"
        ),
    )
    parser.add_argument("--forbidden-token", action="append", default=[])
    parser.add_argument("--forbidden-regex", action="append", default=[])
    parser.add_argument(
        "--contract-mismatch-regex",
        action="append",
        default=[],
        help="Regex for project-contract mismatch patterns not covered by forbidden tokens",
    )
    parser.add_argument("--sample-limit", type=int, default=10)
    args = parser.parse_args()

    tasks_root = Path(args.tasks).resolve()
    if not tasks_root.exists():
        print(json.dumps({"result": "FAIL", "error": f"tasks root not found: {tasks_root}"}))
        return 2

    forbidden_patterns = [re.compile(re.escape(token)) for token in args.forbidden_token]
    forbidden_patterns.extend(re.compile(pattern) for pattern in args.forbidden_regex)
    contract_mismatch_patterns = [
        re.compile(pattern) for pattern in args.contract_mismatch_regex
    ]

    parent_task_json = Path(args.parent_task_json).resolve() if args.parent_task_json else None
    parent_prd = Path(args.parent_prd).resolve() if args.parent_prd else None
    dirs = scoped_task_dirs(tasks_root, parent_task_json)

    file_counts = scan_files(
        tasks_root,
        dirs,
        forbidden_patterns,
        contract_mismatch_patterns,
        args.sample_limit,
        args.jsonl_mode,
    )
    artifact_counts = declared_artifact_scan(
        tasks_root,
        dirs,
        parent_task_json.parent if parent_task_json else None,
        args.sample_limit,
    )
    design_surface_counts = design_surface_scan(
        tasks_root,
        dirs,
        parent_task_json.parent if parent_task_json else None,
        args.sample_limit,
    )
    coverage_counts = coverage_scan(parent_prd)

    result = {
        "tasks_root": str(tasks_root),
        "scanned_tasks": len(dirs),
        "expected_tasks": expected_task_count(parent_task_json),
        **file_counts,
        **artifact_counts,
        **design_surface_counts,
        **coverage_counts,
    }
    result.update(declared_gate_mismatch(parent_prd, result))

    if result["expected_tasks"] is not None and result["expected_tasks"] != result["scanned_tasks"]:
        result["scanned_task_mismatch_hits"] = 1
        result["scanned_task_mismatch_examples"] = [
            f"expected {result['expected_tasks']} from parent children but scanned {result['scanned_tasks']}"
        ]
    else:
        result["scanned_task_mismatch_hits"] = 0
        result["scanned_task_mismatch_examples"] = []

    fail_keys = [
        "placeholder_hits",
        "angle_placeholder_hits",
        "jsonl_seed_hits",
        "forbidden_token_hits",
        "contract_mismatch_hits",
        "coverage_count_mismatch_hits",
        "high_complexity_missing_artifacts",
        "missing_declared_artifacts",
        "design_surface_prd_without_matrix",
        "design_surface_missing_hits",
        "declared_gate_mismatch_hits",
        "external_config_hits",
        "scanned_task_mismatch_hits",
    ]
    result["failure_codes"] = [key for key in fail_keys if result.get(key, 0)]
    result["result"] = "FAIL" if result["failure_codes"] else "PASS"

    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 1 if result["failure_codes"] else 0


if __name__ == "__main__":
    sys.exit(main())
