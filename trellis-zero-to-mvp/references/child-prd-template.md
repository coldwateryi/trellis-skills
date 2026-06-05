# Child PRD Template

## Authoring Rules (read during planning)

This PRD is filled in by a strong model during the **planning phase** and may be implemented by a capability-limited local model (e.g. offline qwen) during the **execution phase**. Therefore:

- Replace every `<...>` placeholder with a **concrete value**. Never leave a placeholder or "TBD / depends" for the execution phase.
- Do not just describe "what behavior to build". State "which file to touch, which existing example to copy, in what order, and how to self-check".
- Anything requiring reasoning (which annotation, which branch, naming, table schema) must be decided during planning. The execution phase only performs mechanical copying.
- If a point cannot be pinned down during planning, put it in `Out of Scope` or split it into a separate task. Do not leave it to the execution model's discretion.

## Template

```markdown
# <Task Title>

## Requirement IDs

- REQ-001
- AC-001

## Goal

Implement or validate this independently verifiable capability for the MVP.

## Current Gap

- Current implementation: <existing behavior or none>
- Gap: <missing behavior>
- Risk: <why this matters>

## Reference Implementation

During execution, prefer copying the existing examples below, replacing only the entity/fields/naming for this task:

- Backend example: <path to an existing file to copy, e.g. .../XxxController.java; if none, write "none, build from scratch per Technical Notes">
- Data-layer example: <path to existing Mapper / SQL / interface contract>
- Frontend example: <path to existing page/component to copy>
- Replacement notes: <replace Xxx in the example with this task's Yyy; field mapping in File Manifest>

## File Manifest

List every file this task touches, marking new/modified, with exact paths:

| Action | File Path | Notes |
| --- | --- | --- |
| New | <path> | <what this file does> |
| Modify | <path> | <where to add what, e.g. "append Y after method X"> |

If a data structure is involved, attach a field table:

| Field | Type | Constraint | Notes |
| --- | --- | --- | --- |
| <name> | <type> | <not-null/unique/default> | <meaning> |

## Implementation Steps

Execute in order; each step is independently verifiable. Steps must be concrete actions, not abstract goals:

1. <e.g. create data structure / run DDL>
2. <e.g. copy the Reference Implementation example, replace entity and fields per File Manifest>
3. <e.g. add <specific validation/branch> in <specific method>; pin which branch is taken>
4. <e.g. compile passes>

## Requirements

- <required behavior, written as a decidable assertion>
- <boundary condition: exact behavior for empty/oversized/duplicate input>
- <error handling: exact error code/message returned on failure>
- <compatibility requirement: behavior that must not break>

## Acceptance Criteria

Write as machine-checkable or individually tickable assertions; avoid subjective phrasing like "correctly implemented":

- [ ] REQ-001 is fully implemented for this task scope.
- [ ] <build/compile command> passes.
- [ ] <specific call + input> returns <exact expectation>.
- [ ] <failure path, e.g. duplicate/invalid input> returns <exact error code and message>.
- [ ] Existing MVP behavior is not broken.
- [ ] Required tests pass.

## Self-Check Commands

Commands the execution phase can run after each step to confirm locally, no human judgment needed:

```bash
<e.g. mvn -pl <module> compile>
<e.g. mvn -pl <module> test -Dtest=<TestClass>>
<e.g. curl -X POST <url> -d '<payload>'  # expect ...>
```

## Automated Tests Required

### Unit Tests

- <test point: method under test + input + expected output>

### Integration Tests

- <test point>

### Regression Tests

- <test point>

### E2E / Smoke Tests

- <test point>

## Dependencies

- Depends on:
  - <task slug or none>
- Reason:
  - <why this dependency exists>

## Unlocks

- <tasks unlocked by this work>

## Out of Scope

- <explicit exclusions>
- <any point that cannot be pinned down during planning and must not be left to the execution model>

## Forbidden

Negative constraints for the execution model, to stop it improvising:

- Do not create base/utility classes that already exist; reuse the existing ones the Reference Implementation points to.
- Do not touch files outside the File Manifest.
- Do not introduce new dependencies or frameworks not listed in Technical Notes.
- <other project-specific red lines>

## Technical Notes

- Related files:
- Existing patterns:
- Relevant specs:
- Risks:
```
