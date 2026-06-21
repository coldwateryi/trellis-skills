# Delivery Run Log Template

Append one JSON object per run to `.trellis/delivery-run-log.jsonl`. Do not rewrite old entries.

## JSONL Entry Shape

```json
{
  "run_id": "2026-06-21T12:00:00Z",
  "skill": "trellis-mvp-to-delivery",
  "mode": "L1",
  "round": 1,
  "audit_scope": "full",
  "baseline_commit": "abc123",
  "head_commit": "def456",
  "requirements_changed": 0,
  "open_gaps": 4,
  "tasks_created": 0,
  "tasks_updated": 0,
  "tasks_completed": 0,
  "critical_review_issues": 0,
  "debug_escalations": 0,
  "carry_over_requirements": 0,
  "tokens_estimate": 120000,
  "outcome": "audit-only",
  "next_action": "confirm-batch"
}
```

## Outcome Values

- `audit-only`
- `batch-planned`
- `tasks-created`
- `tasks-updated`
- `no-op`
- `pause-human-needed`
- `final-acceptance-ready`
- `rebaseline-required`

## Token Budget Defaults

- L1 audit-only: max `120k` tokens/run
- L2 assisted batch: max `350k` tokens/run
- L3 controlled loop: max `500k` tokens/day
- max batches/day: `1`
- max gap tasks/run: `3`
- max carry-over rounds/REQ: `2`
