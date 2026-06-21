# Delivery Task PRD Template

## Authoring Rules (read during planning)

This PRD is filled in by a strong model during the **planning phase** and may be implemented by a capability-limited local model (e.g. offline qwen) during the **execution phase**. Therefore:

- Replace every `<...>` placeholder with a **concrete value**. Never leave a placeholder or "TBD / depends" for the execution phase.
- Do not just describe "what behavior to build". State "which file to touch, which existing example to copy, in what order, and how to self-check".
- Reasoning decisions — bug classification, which branch to take, which annotation — must be pinned down during planning. The execution phase only performs mechanical copying.
- If a point cannot be pinned down during planning, put it in `Out of Scope` or split it into a separate task. Do not leave it to the execution model's discretion.

## Template

```markdown
# <Task Title>

## Requirement IDs

- REQ-001
- AC-001

## Goal

Close the verified gap for these requirements without expanding unrelated scope.

## Current Gap

- Current status: <DONE/PARTIAL/MISSING/UNTESTED/UNCLEAR>
- Evidence:
  - Code:
  - Tests:
- Gap:
- Risk:

## Delivery Loop Controls

- Delivery batch: <delivery-batch-id>
- Loop mode: <L1/L2/L3>
- Worktree required: <yes/no; yes for L2/L3 implementation work>
- Verifier required: <yes/no; yes for any code-changing task>
- Implementation skill: `trellis-implement-tdd`
- Debug skill: `trellis-debug-systematic`
- Review skill: `trellis-review-twostage`
- Human gate: <required/not required and reason>
- Max fix attempts: <default 2>
- Max debug hypothesis rounds: <default 3>
- Rollback trigger:
  - verifier critical issue
  - test regression
  - file outside File Manifest changed
  - MVP compatibility contract broken
- State update required:
  - update `.trellis/delivery-state.md`
  - append `.trellis/delivery-run-log.jsonl`

## Complexity and Planning Artifacts

- Complexity: <low/medium/high, assessed against the execution model capability>
- Execution model assumption: <e.g. qwen3.6 35b local / GPT-5.5 / Opus 4.8>
- Required artifacts:
  - `prd.md`: required
  - `design.md`: <required/not required and reason>
  - `implement.md`: <required/not required and reason>
  - `implement.jsonl`: <required/not required and reason>
  - `check.jsonl`: <required/not required and reason>
- Spec freshness: <which `.trellis/spec/` files were read; if stale, name the spec-refresh task>

## Context Manifest

The execution model must read these before editing:

| Kind | Path | Purpose |
| --- | --- | --- |
| MVP code | <path> | <behavior to preserve or extend> |
| Existing test | <path> | <regression or style reference> |
| Contract/spec | <path> | <API/schema/state rules> |

## Decision Table

Pin every decision that would otherwise require reasoning during execution:

| Decision | Selected Option | Reason | Affected Files |
| --- | --- | --- | --- |
| <bug branch/naming/schema/API choice> | <exact choice> | <why> | <paths> |

## MVP Compatibility Contract

| Existing Behavior | Evidence | Must Preserve? | Regression Check |
| --- | --- | --- | --- |
| <behavior> | <path/test> | yes | <command/test> |

## Reference Implementation

During execution, prefer copying the existing examples below, replacing only the entity/fields/naming for this task:

- Backend example: <path to an existing file to copy; if none, write "none, build from scratch per Technical Notes">
- Data-layer example: <path to existing Mapper / SQL / interface contract>
- Frontend example: <path to existing page/component to copy>
- Replacement notes: <replace Xxx in the example with this task's Yyy; field mapping in File Manifest>

## File Manifest

| Action | File Path | Notes |
| --- | --- | --- |
| New | <path> | <what this file does> |
| Modify | <path> | <where to add what> |

If a data structure is involved, attach a field table:

| Field | Type | Constraint | Notes |
| --- | --- | --- | --- |
| <name> | <type> | <not-null/unique/default> | <meaning> |

## Implementation Steps

Execute in order; each step is independently verifiable. Steps must be concrete actions, not abstract goals:

1. <e.g. run DDL/migration>
2. <e.g. copy the Reference Implementation, replace entity and fields per File Manifest>
3. <e.g. add <specific validation/branch> in <specific method>; pin which branch is taken>
4. <e.g. compile passes>

## Behavior Constraints

- <behavior to implement or test, written as a decidable assertion>
- <boundary condition: exact behavior for empty/oversized/duplicate input>
- <error handling: exact error code/message returned on failure>
- <compatibility or migration notes>

## Acceptance Criteria

Write as machine-checkable or individually tickable assertions; avoid subjective phrasing like "correctly implemented":

- [ ] Requirement IDs listed above reach the expected status.
- [ ] <build/compile command> passes.
- [ ] <specific call + input> returns <exact expectation>.
- [ ] <failure path> returns <exact error code and message>.
- [ ] Existing MVP behavior is preserved unless explicitly changed.
- [ ] Required tests are added or updated.
- [ ] Lint, typecheck, and relevant tests pass.

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

### Manual Verification

- <only if automation is not suitable; explain why>

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
- Do not implement outside the required worktree when `Worktree required` is yes.
- Do not mark this task complete without `trellis-review-twostage` passing; the implementer must not grade its own work.
- <other project-specific red lines>

## Technical Notes

- Related files:
- Existing patterns:
- Relevant specs:
- Risks:
```
