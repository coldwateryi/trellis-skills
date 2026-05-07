# MVP Gap Audit Template

Use this template for the first pass after an MVP exists. Do not write code or create tasks until the user confirms the audit.

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

| Order | Task Slug | Title | Requirement IDs | Depends On | Acceptance Criteria | Automated Tests Required | Priority |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 |  |  |  |  |  |  | P0 |

Task planning rules:

1. One task closes one tightly related group of gaps.
2. Do not mix foundation contracts with UI presentation unless they are inseparable.
3. Do not mix feature implementation with final validation.
4. Each feature task includes its own basic tests.
5. The final validation task depends on all functional tasks.

## Confirmation Request

End with:

```text
Confirm this gap audit and delivery task plan? If yes, I will create Trellis tasks and PRDs without implementing features yet.
```
