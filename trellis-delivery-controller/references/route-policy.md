# Route Policy

## Stage Selection Table

| Project state | Next stage | Skill |
| --- | --- | --- |
| Requirements exist, but no `.trellis/tasks/` or no MVP task tree | `zero-to-mvp-readonly` | `trellis-zero-to-mvp` |
| `zero-to-mvp` read-only analysis exists and user confirmed scope | `zero-to-mvp-create-tasks` | `trellis-zero-to-mvp` |
| MVP is complete and `.trellis/delivery-state.md` is missing | `mvp-to-delivery-full-audit` | `trellis-mvp-to-delivery` |
| Delivery state exists and source requirements changed | `mvp-to-delivery-full-audit` | `trellis-mvp-to-delivery` |
| Delivery state exists, requirements did not change, and related code/tests/tasks changed | `mvp-to-delivery-delta-audit` | `trellis-mvp-to-delivery` |
| Delivery state exists, requirements did not change, and nothing relevant changed | `early-exit` | `trellis-mvp-to-delivery` |
| Confirmed current_batch exists but gap tasks are not created or updated | `delivery-batch-planning` | `trellis-mvp-to-delivery` |
| Ready subtask exists, dependencies are satisfied, implementation has not started | `implement-tdd` | `trellis-implement-tdd` |
| TDD or self-check fails with a stable failure signal | `debug-systematic` | `trellis-debug-systematic` |
| Subtask ACs and self-checks are green, but review is missing | `review-twostage-stage1` | `trellis-review-twostage` |
| Stage 1 passed, code quality review is missing | `review-twostage-stage2` | `trellis-review-twostage` |
| All P0/P1 gaps are DONE or explicitly deferred by a human | `final-acceptance` | `trellis-mvp-to-delivery` |
| Scope, schema, auth, payment, infra, or security decisions are unclear | `pause-human-needed` | none |

## Routing Principles

- Choose exactly one next stage.
- When multiple stages may apply, handle the earliest unmet safety gate first.
- For post-MVP full/delta/early-exit decisions, read `delivery-loop-routing.md`.
- Do not judge completion from chat memory; read file evidence.
- If there is a failure signal, debug before implementing new ACs.
- If review has a critical issue, fix the marked issue before advancing task state.
- If strong-model judgment is needed but unavailable, pause and output an evidence pack.

## Evidence Pack

When pausing for a strong model or human, output:

- Task directory.
- Requirement and AC IDs.
- Relevant `prd.md`, `design.md`, `implement.md`, and `check.jsonl` paths.
- Current diff summary.
- Commands run and results.
- Failure log or review issue.
- Recommended next stage.
