# Delivery Loop Policy

Use this policy before each `trellis-mvp-to-delivery` run to choose loop mode, audit scope, early-exit behavior, and stop conditions.

## Loop Modes

| Mode | Name | Allowed Actions | Human Gate |
| --- | --- | --- | --- |
| L1 | Audit only | Full/delta gap audit, state/log update, batch recommendation | Always before task creation |
| L2 | Assisted delivery | Create/update confirmed gap tasks, one batch per run, worktree + verifier required | Required for high risk, schema, auth, payments, security |
| L3 | Controlled continuous loop | Same as L2 with explicit prior approval, strict early-exit, max one batch/day | Required for critical findings or scope changes |

Default to L1 when `.trellis/delivery-state.md` is missing.

## Audit Scope Selection

Use **full audit** when:

- `.trellis/delivery-state.md` does not exist.
- The source requirements document changed.
- `mvp_baseline_commit` or `last_audited_commit` is missing.
- Final acceptance failed.
- A human requested rebaseline.

Use **delta audit** when:

- Delivery state exists.
- Source requirements are unchanged.
- Only implementation files, tests, or related Trellis tasks changed since `last_audited_commit`.
- Open gaps already have requirement IDs and task links.

Use **early exit** when:

- No relevant files changed since `last_audited_commit`.
- No open blocker changed.
- No gap task status changed.
- No requirement evidence changed.

When early-exiting, update `.trellis/delivery-run-log.jsonl` with `outcome: "no-op"` and do not re-run full audit or create tasks.

## Batch Limits

- Max batches per run: `1`
- Max gap tasks per run: `3`
- Max high-risk tasks per run: `1`
- Max debug hypothesis rounds per task: `3`
- Max verifier failures per task: `2`
- Max carry-over rounds per REQ: `2`

## Stop And Escalate

Pause the loop and ask the user when:

- The same `REQ-*` carries over for more than 2 rounds without status progress.
- The same task fails verifier or review twice.
- `trellis-review-twostage` reports any critical issue.
- `trellis-debug-systematic` exceeds 3 hypothesis/fix rounds.
- A task needs files outside the File Manifest.
- A requirement, schema, security, payment, auth, or infrastructure decision is ambiguous.
- Full audit and delivery state disagree about a DONE/PARTIAL/MISSING status.

## Round Cap

Typical delivery loops should converge in 3-6 outer rounds. If `current_round > max_rounds`, stop and recommend re-scoping, rebaseline, or human review.
