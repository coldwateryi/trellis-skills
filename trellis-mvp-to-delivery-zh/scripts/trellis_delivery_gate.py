#!/usr/bin/env python3
"""Delivery state gate for trellis-mvp-to-delivery-zh.

Validates delivery-state.md state machine transitions and detects
small-model drift patterns during MVP-to-delivery loops.

Usage:
  python trellis_delivery_gate.py \\
    --phase S4_UPDATE_STATE \\
    --state-file .trellis/delivery-state.md
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


VALID_STATES = [
    "S0_LOAD_STATE",
    "S1_DETERMINE_LOOP",
    "S2_DISCOVER_EVIDENCE",
    "S3_GAP_AUDIT",
    "S4_UPDATE_STATE",
    "S5_PICK_BATCH",
    "S6_CONFIRM",
    "S7_CREATE_TASKS",
    "S8_RUN_LOG",
    "S9_PLAN_TESTS",
    "S10_FINAL_ACCEPTANCE",
]

STATE_INDEX = {s: i for i, s in enumerate(VALID_STATES)}


def allowed_transition(prev: str | None, next_state: str) -> tuple[bool, str]:
    if prev is None:
        return next_state == "S0_LOAD_STATE", f"First state must be S0_LOAD_STATE, got {next_state}"
    if next_state not in STATE_INDEX:
        return False, f"Unknown state: {next_state}"
    if prev not in STATE_INDEX:
        return False, f"Unknown previous state: {prev}"
    diff = STATE_INDEX[next_state] - STATE_INDEX[prev]
    if diff == 0:
        return True, "Re-entry into same phase (allowed)"
    if diff == 1:
        return True, "Forward one phase (allowed)"
    if diff < 0:
        return True, f"Regression ({prev} -> {next_state}, -{abs(diff)} phases) — allowed as Drift Reset"
    if diff > 1:
        return False, f"ILLEGAL: skipped {diff - 1} phase(s) ({prev} -> {next_state})"
    return True, ""


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def parse_state_file(path: Path) -> dict | None:
    if not path.exists():
        return None
    text = read_text(path)
    result = {}
    in_yaml_block = False
    for line in text.splitlines():
        if line.strip().startswith("stage_state:"):
            in_yaml_block = True
            continue
        if in_yaml_block:
            if line.strip().startswith("---"):
                break
            if not line.strip() or line.strip().startswith("#"):
                continue
            m = re.match(r"^\s*(\w[\w_]*)\s*:\s*(.+)$", line)
            if m:
                key = m.group(1).strip()
                value = m.group(2).strip().strip('"').strip("'")
                result[key] = value
    return result


def parse_delivery_state(path: Path) -> dict | None:
    if not path.exists():
        return None
    text = read_text(path)
    result = {}
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


def check_delivery_state(state_path: Path) -> list[dict]:
    failures = []
    state = parse_delivery_state(state_path)

    if state is None:
        failures.append({
            "code": "DELIVERY_STATE_MISSING",
            "detail": "delivery-state.md not found or unparseable",
        })
        return failures

    required_fields = ["loop_mode", "current_round", "next_loop_recommendation"]
    for field in required_fields:
        if field not in state:
            failures.append({
                "code": f"STATE_FIELD_MISSING",
                "detail": f"Required field '{field}' missing from delivery-state.md",
            })

    if "loop_mode" in state and state["loop_mode"] not in ("L1", "L2", "L3"):
        failures.append({
            "code": "INVALID_LOOP_MODE",
            "detail": f"loop_mode must be L1/L2/L3, got {state['loop_mode']}",
        })

    if "next_loop_recommendation" in state:
        valid = ("continue-next-batch", "early-exit", "pause-human-needed",
                 "run-final-acceptance", "rebaseline-required")
        if state["next_loop_recommendation"] not in valid:
            failures.append({
                "code": "INVALID_NEXT_ACTION",
                "detail": f"next_loop_recommendation must be one of {valid}, got {state['next_loop_recommendation']}",
            })

    if "carry_over" in state:
        try:
            co = int(state["carry_over"])
            if co > 3:
                failures.append({
                    "code": "HIGH_CARRY_OVER",
                    "detail": f"Carry-over count {co} exceeds threshold of 3; may require pause-human-needed",
                })
        except (ValueError, TypeError):
            pass

    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--phase", required=True,
        choices=VALID_STATES,
        help="The phase being entered",
    )
    parser.add_argument(
        "--state-file",
        default=".trellis/delivery-state.md",
        help="Path to .trellis/delivery-state.md",
    )
    args = parser.parse_args()

    state_file = Path(args.state_file).resolve()
    prev_phase = None

    # Try to get previous phase from stage_state block in delivery-state.md
    stage_info = parse_state_file(state_file)
    if stage_info and "state" in stage_info:
        prev_phase = stage_info["state"]

    # State machine transition check
    transition_ok, transition_msg = allowed_transition(prev_phase, args.phase)
    transition_blocking = not transition_ok

    # Phase-specific checks
    phase_failures: list[dict] = []

    if args.phase in ("S4_UPDATE_STATE", "S5_PICK_BATCH", "S6_CONFIRM"):
        phase_failures = check_delivery_state(state_file)

    # Build result
    failure_codes_map = {}
    if transition_blocking:
        failure_codes_map["ILLEGAL_STATE_TRANSITION"] = transition_msg
    for f in phase_failures:
        failure_codes_map[f["code"]] = f["detail"]

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
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 1 if is_fail or is_blocking else 0


if __name__ == "__main__":
    sys.exit(main())