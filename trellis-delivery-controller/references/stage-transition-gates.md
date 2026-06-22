# Stage Transition Gates

## Automatically Allowed

- Read requirements, code, tests, `.trellis/`, and related specs.
- Detect the current stage and next skill.
- Execute TDD, systematic debugging, and Stage 1 spec compliance for subtasks within confirmed scope.
- Enter systematic debugging when self-check fails, up to 3 hypothesis/fix rounds.
- Recommend task-state advancement after review passes.
- Early-exit when delivery state exists and nothing relevant changed.

## Must Pause

- Before creating or modifying Trellis task trees after first read-only analysis.
- Before creating gap tasks after the first full audit and gap matrix.
- When work needs files outside the File Manifest.
- When requirements, schema, auth, payment, security, or infrastructure decisions are unclear.
- When verifier fails twice.
- When debugging exceeds 3 rounds and still fails.
- When review reports a critical issue.
- When Stage 2 code quality review needs a strong model but only a small model is available.
- When the outer delivery loop exceeds 6 rounds.
- When the same `REQ-*` has no progress for 2 rounds.
- Before any destructive git operation, commit, push, tag, or release unless the user explicitly authorized it.

## Stage Completion Conditions

| Stage | Completion condition |
| --- | --- |
| `zero-to-mvp-readonly` | RTM, MVP boundary, task split, and PRD drafts are produced |
| `zero-to-mvp-create-tasks` | Trellis parent/child tasks and PRDs are created; no application code is written |
| `mvp-to-delivery-full-audit` | Complete Requirements Gap Matrix and delivery state are prepared |
| `mvp-to-delivery-delta-audit` | Only affected REQs and run log are updated |
| `delivery-batch-planning` | Current batch tasks are created/updated; implementation has not started |
| `implement-tdd` | Every AC has red/green records and self-checks are green |
| `debug-systematic` | Original failing command is green, or escalation is documented |
| `review-twostage-stage1` | Spec compliance review has no critical issue |
| `review-twostage-stage2` | Strong model or human code-quality review is complete with no blocking issue |
| `final-acceptance` | In-scope REQs have acceptance evidence or explicit human deferral |
