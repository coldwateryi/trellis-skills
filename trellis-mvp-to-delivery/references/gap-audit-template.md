# MVP Gap Audit Template

Use this template for the first pass after an MVP exists. Do not write code or create tasks until the user confirms the audit.

## Trellis Workflow Context

| Item | Value | Notes |
| --- | --- | --- |
| Trellis version/source | <from `.trellis/.version` or "unknown"> | <beta/current/legacy signal> |
| Workflow contract | <path to `.trellis/workflow.md` or "not present"> | <artifact requirements found> |
| Config | <path to `.trellis/config.yaml` or "not present"> | <relevant options> |
| Developer identity | <from `.trellis/.developer` or "not initialized"> | <action needed if missing> |
| Spec freshness | <fresh/stale/missing/unknown> | <spec files read or refresh task needed> |

## Delivery Loop Metadata

| Item | Value | Notes |
| --- | --- | --- |
| Loop mode | <L1/L2/L3> | <why this mode> |
| Audit scope | <full/delta> | <first run must be full> |
| MVP baseline commit | <git-sha> | <source of baseline> |
| Last audited commit | <git-sha or none> | <from delivery state if present> |
| Current round | <number> | <from delivery state or 1> |
| Early-exit eligible | <yes/no> | <reason> |

## Execution Profile

| Profile | Value |
| --- | --- |
| Expected execution model | <e.g. qwen3.6 35b local / GPT-5.5 / Opus 4.8> |
| Planning depth | <standard / small-model-safe / high-risk> |
| Regression risk level | <low/medium/high> |

## Requirements Traceability Matrix

| ID | Requirement | Current Status | Related Code | Existing Tests | Gap | Suggested Task |
| --- | --- | --- | --- | --- | --- | --- |
| REQ-001 |  | UNCLEAR |  |  |  |  |

Allowed statuses:

- `DONE`: Fully implemented and tested.
- `PARTIAL`: Partially implemented.
- `MISSING`: Not implemented.
- `UNTESTED`: Implemented but missing adequate tests.
- `UNCLEAR`: Requirement is not clear enough to implement.

Evidence rules:

- `DONE` requires implementation evidence and test evidence.
- `UNTESTED` requires implementation evidence and a clear test gap.
- `PARTIAL` requires evidence for what works and what is missing.
- `MISSING` requires no implementation evidence or only unrelated scaffolding.
- `UNCLEAR` requires a blocking question or ambiguity statement.

## MVP Completion Summary

- Complete:
- Partial:
- Missing:
- Implemented but untested:
- Unclear:

## Blocking Questions

List only questions that block implementation. Do not ask questions answerable from the repository or source requirements.

## Task Plan

| Order | Task Slug | Title | Requirement IDs | Depends On | Acceptance Criteria | Automated Tests Required | Priority | Complexity | Planning Artifacts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 |  |  |  |  |  |  | P0 | low | prd.md |

## Delivery Batch Recommendation

Use `delivery-batch-template.md` to recommend at most one batch for this run.

| Batch ID | Scope | Included REQs | Excluded REQs | Risk | Next Action |
| --- | --- | --- | --- | --- | --- |
| delivery-batch-001 | <P0 foundation / P1 core behavior / regression / final acceptance> | <REQ list> | <REQ list + reason> | low/medium/high | create-tasks/update-existing-tasks/pause |

Complexity (assessed against the execution model's capability; drives split granularity and PRD detail):

- `low`: standard CRUD, config, an existing example to copy. A weak model can do it independently.
- `medium`: some business validation or cross-table logic; needs explicit implementation steps. A weak model can do it with a detailed PRD.
- `high`: complex transactions, concurrency, cross-module consistency, heavy implicit domain knowledge. A weak model cannot do it independently — split further, or pin every step in the PRD until no reasoning is needed.

Task planning rules:

1. One task closes one tightly related group of gaps.
2. Do not mix foundation contracts with UI presentation unless they are inseparable.
3. Do not mix feature implementation with final validation.
4. Each feature task includes its own basic tests.
5. The final validation task depends on all functional tasks.

For every medium/high complexity gap-closing task, also draft the required Trellis 0.6 beta planning artifacts using `planning-artifacts-template.md`.

## Confirmation Request

End with:

```text
Confirm this gap audit, delivery state update, and selected batch? If yes, I will create or update Trellis tasks and PRDs for this batch without implementing features yet.
```
