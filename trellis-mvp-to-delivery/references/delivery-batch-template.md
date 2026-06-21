# Delivery Batch Template

Use this template to plan exactly one delivery batch per `trellis-mvp-to-delivery` run. Copy batch details into `.trellis/delivery-state.md` and into task PRDs where relevant.

## Batch Metadata

- batch_id: `<delivery-batch-001>`
- round: `<number>`
- priority: `P0 | P1 | P2 | P3`
- risk: `low | medium | high`
- mode: `L1 | L2 | L3`
- audit_scope: `full | delta`

## Included Gaps

| REQ ID | Gap | Planned Task | Reason Included | Risk |
| --- | --- | --- | --- | --- |
| REQ-001 | `<specific gap>` | `<task slug>` | `<dependency, priority, or blocker reason>` | low/medium/high |

## Excluded Gaps

| REQ ID | Reason |
| --- | --- |
| REQ-002 | `<deferred because...>` |

## Batch Limits

- max_gap_tasks: `3`
- max_high_risk_tasks: `1`
- worktree_required: `true`
- verifier_required: `true`
- max_fix_attempts_per_task: `2`
- max_debug_rounds_per_task: `3`

## Sequencing Rules

- Do not mix foundation contracts, business behavior, UI display, and final validation in the same batch when their dependencies differ.
- P0 foundation/API/schema gaps should run before P1 business behavior.
- Final acceptance is its own batch and depends on all P0/P1 gaps being DONE or explicitly deferred by a human.
- Test-only `UNTESTED` gaps can share a batch only when they protect the same feature area.

## Stop Conditions

- Any critical review issue.
- Any verifier failure after 2 attempts.
- Same requirement reopened twice.
- Human blocker appears.
- A task requires files outside its File Manifest.

## Next Action

- action: `create-tasks | update-existing-tasks | continue-existing-batch | early-exit | pause-human-needed | final-acceptance`
- reason: `<specific reason>`
