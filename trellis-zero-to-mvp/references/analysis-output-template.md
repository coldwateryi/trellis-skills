# Zero to MVP Analysis Output Template

Use this template for the read-only analysis. Do not create tasks or write code during this phase.

## Project Goal Summary

Write 5-10 bullets describing what the requirements document asks the project to deliver.

## Requirements Traceability Matrix

| ID | Requirement | Current Status | Related Code | Existing Tests | Gap | Suggested Task |
| --- | --- | --- | --- | --- | --- | --- |
| REQ-001 |  | MISSING |  |  |  |  |

Allowed statuses:

- `DONE`: Fully implemented and tested.
- `PARTIAL`: Partially implemented.
- `MISSING`: Not implemented.
- `UNTESTED`: Implemented but missing adequate tests.
- `UNCLEAR`: Requirement is not clear enough to implement.

## Module Dependency Graph

| Module | Responsibility | Depends On | Used By | Risks |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## Task Split

| Task ID | Title | Goal | Type | Depends On | Priority | Parallelizable | Acceptance Criteria | Likely Areas |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T0 |  |  | docs | none | P0 | no |  |  |

Allowed task types: `backend`, `frontend`, `fullstack`, `docs`, `test`, `infra`.

Priority rules:

- `P0`: Blocks other modules or core correctness.
- `P1`: Core business loop.
- `P2`: Experience, reports, notifications, enhancements.
- `P3`: Non-essential optimization.

Sorting rules:

1. Put data structures, API contracts, and configuration first.
2. Put blocking modules before modules that depend on them.
3. Pull high-risk unknowns earlier.
4. Put UI polish, documentation, and experience enhancements later.
5. Do not mark mutually dependent tasks as parallel.

## Recommended MVP Development Order

1. `<task-id>`: `<reason>`
2. `<task-id>`: `<reason>`

## Parent Task PRD Draft

Draft the parent PRD using `parent-prd-template.md`.

## Child Task PRD Drafts

For each child task, draft the PRD using `child-prd-template.md`.

## Confirmation Request

End with:

```text
Confirm this task split and MVP boundary? If yes, I will create the Trellis parent task, child tasks, and PRDs without writing application code.
```
