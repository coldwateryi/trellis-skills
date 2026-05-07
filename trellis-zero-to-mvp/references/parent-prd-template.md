# Parent PRD Template

```markdown
# <Project Title>

## Goal

Deliver the project described by the source requirements document. The parent task owns the overall scope, requirement IDs, dependency plan, and final acceptance definition. Child tasks own implementation of independently verifiable capabilities.

## Source Requirement Document

- Path: <requirements document path>
- Version: <version or date>
- Owner: <business or technical owner>

## Requirement IDs

| ID | Requirement Summary | Child Task | Status |
| --- | --- | --- | --- |
| REQ-001 | <summary> | <task slug> | PLANNED |

Allowed statuses: `PLANNED`, `IN_PROGRESS`, `DONE`, `PARTIAL`, `BLOCKED`, `VERIFIED`.

## Task Dependency Graph

```text
T0 requirements traceability
  -> T1 foundation
    -> T2 core capability
      -> T3 business loop
  -> T-final validation
```

## Delivery Strategy

1. Complete traceability and technical planning.
2. Implement foundations and contracts.
3. Implement the core MVP business loop.
4. Add secondary capabilities only when their dependencies are complete.
5. Finish with validation and acceptance reporting.

## Definition of Done

- [ ] Every requirement ID has a status.
- [ ] All MVP P0/P1 requirements are complete.
- [ ] Every requirement ID has a test mapping or documented manual verification reason.
- [ ] Lint, typecheck, and required tests pass.
- [ ] Final acceptance report uses PASS / FAIL / PARTIAL / NOT TESTED.
- [ ] Docs and run instructions are updated if behavior changed.

## Out of Scope

- <items explicitly excluded from MVP>

## Notes

- Strict dependencies live in child task `Dependencies` sections.
- Parent/child links organize scope but do not replace dependency documentation.
```
