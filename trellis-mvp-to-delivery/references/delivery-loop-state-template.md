# Delivery Loop State Template

Copy this template to `.trellis/delivery-state.md` on the first `trellis-mvp-to-delivery` run. Update it at the end of every delivery loop run. This file is the durable memory spine for repeated MVP-to-delivery loops.

## Baseline

- source_requirements: `<path>`
- mvp_baseline_commit: `<git-sha>`
- last_audited_commit: `<git-sha>`
- loop_mode: `L1`
- current_round: `1`
- max_rounds: `6`
- current_batch_id: `<none-or-batch-id>`

## Requirement Status

| REQ ID | Status | Implementation Evidence | Test Evidence | Gap Task | Last Changed Round | Carry-over Count |
| --- | --- | --- | --- | --- | --- | --- |
| REQ-001 | DONE/PARTIAL/MISSING/UNTESTED/UNCLEAR | `<path-or-none>` | `<path-or-none>` | `<task-or-none>` | 1 | 0 |

## Current Batch

- batch_id: `<delivery-batch-001>`
- scope: `<P0 foundation gaps / P1 core behavior / regression closure / final acceptance>`
- selected_reqs:
  - `<REQ-xxx>`
- excluded_this_round:
  - `<REQ-yyy>: <reason>`

## Blockers

| Item | Reason | Needed From Human | Since Round |
| --- | --- | --- | --- |
| `<REQ-xxx or task>` | `<why blocked>` | `<decision or input needed>` | 1 |

## Human Decisions

- `<date>`: `<decision and scope impact>`

## Budget Snapshot

- max_batches_per_day: `1`
- max_gap_tasks_per_run: `3`
- max_high_risk_tasks_per_run: `1`
- max_carry_over_rounds_per_req: `2`
- max_verifier_failures_per_task: `2`

## Next Loop Recommendation

- action: `continue-next-batch | early-exit | pause-human-needed | run-final-acceptance | rebaseline-required`
- reason: `<specific reason>`
- next_audit_scope: `full | delta | none`
