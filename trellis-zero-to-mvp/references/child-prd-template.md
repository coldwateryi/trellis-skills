# Child PRD Template

## Authoring Rules

This PRD is filled during planning and may be implemented by a capability-limited local model. It must pin requirements, contracts, boundaries, acceptance, and dependencies, but it must not replace Trellis 0.6+ `design.md` / `implement.md`.

- Replace every `<...>` placeholder with a concrete value.
- Do not leave `{Entity}`, `{domain}`, `{entity}`, `<PageComponent>`, `TBD`, `depends`, or equivalent template residue.
- By default, PRD contains requirements, constraints, scope, dependencies, and acceptance. Technical design goes in `design.md`; file plan, ordered steps, self-check commands, rollback, and review gates go in `implement.md`.
- Only low-complexity tasks may keep a compact execution appendix in PRD, and only when the local workflow permits PRD-only and the artifact matrix says `implement.md: not required`.
- Every reasoning decision (naming, paths, API/command/route, schema, state branch, external config) must be pinned during planning; PRD pins behavior contract, `design.md` / `implement.md` pin technical placement.
- Child tasks must reference the parent Project Contract Lock. Do not invent names, paths, APIs, commands, packages/modules, routes, tables, or permission models.
- Copy relevant Contract Snapshot adopted values and forbidden tokens. PRD, `design.md`, `implement.md`, and JSONL must not hit forbidden tokens.
- In Small Model Mode, one child task covers only one primary entity CRUD, one endpoint group, one state transition, one frontend page, or one backend aggregate query.
- External config and third-party keys must be `FIXED`, `BASELINE`, `BLOCKED`, or `OUT_OF_SCOPE`. Do not leave `YOUR_KEY`, `API_KEY_HERE`, or "to be provided".

## Template

```markdown
# <Task Title>

## Requirement IDs

- REQ-001
- AC-001

## Goal

Implement or validate this independently verifiable MVP capability.

## Project Contract Reference

Copy the contract items this task must follow from the parent Project Contract Lock. If this task needs a different name/path/API, update the parent contract first and explain why.

| Contract Item | Profile Field | This Task Uses | Parent Evidence Path |
| --- | --- | --- | --- |
| <item> | <profile field> | <specific path/name/API/command/module or not-applicable> | <path> |

### Contract Snapshot Check

| Check | Value |
| --- | --- |
| Required adopted values | <paths/names/APIs/commands/modules/routes/tables/permissions> |
| Forbidden tokens for this task | <tokens; none if none> |
| Scan scope | This PRD, design.md, implement.md, implement.jsonl, check.jsonl |
| Handling | Any hit makes Artifact Gate FAIL; fix before execution |

## Semantic Anchors

Use concrete values. Keep these consistent with Project Contract Reference, acceptance criteria, `design.md`, and `implement.md`. Write `not-applicable` for irrelevant fields instead of applying another tech stack.

| Item | Value |
| --- | --- |
| Project Contract Profile | <selected profile> |
| Business / Capability Domain | <e.g. site / cli-task-create / workflow-template / auth-page> |
| Primary Object / Entity / Interface | <specific name or not-applicable> |
| User-Visible Entry | <page path / CLI command / API endpoint / SDK function / workflow section> |
| Data or State Object | <table / schema / config key / state block / not-applicable> |
| Code Landing Summary | <module, package, workspace, template, or not-applicable> |
| Permission / Auth Model | <permission prefix / guard / config / not-applicable> |
| Adjacent Domains This Task Must Not Touch | <domains unless listed as dependencies> |

## Small Model Granularity Check

| Check | Result |
| --- | --- |
| Task granularity | <one entity CRUD / endpoint group / state transition / frontend page / backend aggregate query> |
| Primary object count | <n, usually 1 in Small Model Mode> |
| Independent capability count | <n, usually 1 in Small Model Mode> |
| Includes high-complexity combination | <yes/no; if yes, explain why not split> |
| Needs split | <no/yes; yes unless user explicitly approved merge> |

## Gap Source

- Requirement status before this task: <PARTIAL/MISSING/UNTESTED>
- Task action: <gap-task/new-task/test-only>
- Existing baseline dependencies:
  - <existing:path-or-capability, or "none">
- Trellis task dependencies:
  - <task slug or "none">
- Scope rule: this task must not recreate behavior already listed in Existing Implementation Baseline.

## Current Gap

- Current implementation: <existing behavior or none>
- Gap: <missing behavior>
- Risk: <why this matters>

## Complexity and Planning Artifacts

- Complexity: <low/medium/high, assessed against execution model capability>
- Execution model assumption: <qwen3.6 35b local / GPT-5.5 / Opus 4.8>
- Batch: <B01/B02/...>
- Parallel group: <G01/G02/...; none if not parallel>
- Ledger status: <must match parent Subtask Planning Ledger>
- Artifact matrix row: <copy this task's row from planning artifact matrix>
- Required artifacts:
  - `prd.md`: required
  - `design.md`: <required/not required and reason>
  - `implement.md`: <required/not required and reason>
  - `implement.jsonl`: <required/not required and reason; jsonl_mode=required/optional/inline>
  - `check.jsonl`: <required/not required and reason; jsonl_mode=required/optional/inline>
- Trellis 0.6+ artifact boundary: <file plan, steps, and self-check commands are in implement.md; or low-complexity PRD-only appendix>
- Spec freshness: <which `.trellis/spec/` files were read; if stale, name refresh task>

## Context Manifest

The execution model must read these before editing:

| Kind | Path | Purpose |
| --- | --- | --- |
| Existing example | <path> | <pattern to copy> |
| Contract/spec | <path> | <API/schema/state rules> |
| Test example | <path> | <test style to copy> |

## Decision Table

Pin every decision that would otherwise require execution-time reasoning:

| Decision | Selected Option | Reason | Affected File or Artifact |
| --- | --- | --- | --- |
| <naming/schema/state branch/API/command choice> | <exact choice> | <reason> | <prd/design/implement or paths> |

## External Config and Open Items

All external config must be fixed or excluded. Do not leave placeholders.

If a `BLOCKED` external config is required for implementation, this task must be `BLOCKED` or the dependent behavior must be out of scope. Executable tasks can only implement behavior that does not depend on unresolved config.

| Config / External Dependency | Status | Planning Handling | Execution Behavior |
| --- | --- | --- | --- |
| <map key / third-party API / hardware protocol> | FIXED/BASELINE/BLOCKED/OUT_OF_SCOPE | <config name, evidence, or exclusion reason> | <exact behavior> |

## Reference Implementation

During execution, prefer copying these examples and replacing only this task's names/fields:

- Business/interface example: <path or "none, build from design.md / implement.md">
- Data/state/config example: <schema / mapper / template / config / workflow path or none>
- UI/CLI/SDK example: <page, component, command, SDK API, or template path or none>
- Replacement notes: <replace Xxx with Yyy; detailed file replacement is in implement.md>

## Implementation Plan Location

Trellis 0.6+ stores detailed file plans in `implement.md` by default. This section only states where execution planning lives, to avoid PRD and `implement.md` drifting.

| Item | Value |
| --- | --- |
| File plan location | `implement.md` / this PRD compact appendix |
| Ordered steps location | `implement.md` / this PRD compact appendix |
| Self-check commands location | `implement.md` / this PRD compact appendix |
| PRD-only evidence | <low complexity + local workflow permits + artifact matrix says implement.md not required; otherwise not-applicable> |

### PRD-only Compact Execution Appendix (low complexity only)

Delete this subsection for non-PRD-only tasks and fill `implement.md` instead.

| Action | File Path | Notes |
| --- | --- | --- |
| New/Modify | <path> | <what this file does; do not fill for non-PRD-only tasks> |

1. <only for PRD-only: concrete action; otherwise write "see implement.md">

```bash
<only for PRD-only: self-check command; otherwise write "see implement.md">
```

## Mount Points

These make the capability visible. Rule: "if this line disappears, the feature disappears from the user/system point of view."

| Mount Point | Type | Location | Exact Wiring Action |
| --- | --- | --- | --- |
| <name> | route registration / config entry / event subscription / DI binding / menu entry / CLI registration / SDK export | <path> | <exact action> |

## Behavior Constraints

- <required behavior as a decidable assertion>
- <boundary condition behavior for empty/oversized/duplicate input>
- <error handling: exact error code/message>
- <compatibility requirement: behavior that must not break>

## Acceptance Criteria

Use machine-checkable or individually tickable assertions:

- [ ] REQ-001 is fully implemented for this task scope.
- [ ] <build/compile command> passes.
- [ ] <specific call/command/page action + input> returns <exact expectation>.
- [ ] <failure path> returns <exact error code/message>.
- [ ] Existing MVP behavior is not broken.
- [ ] Required tests pass.

## Automated Tests Required

### Unit Tests

- <test point: method + input + expected output>

### Integration Tests

- <test point>

### Regression Tests

- <test point>

### E2E / Smoke Tests

- <test point>

## Dependencies

- Trellis task dependencies:
  - <task slug or none>
- Existing baseline dependencies:
  - <existing:path-or-capability or none>
- Reason:
  - <why this dependency exists>

## Unlocks

- <tasks unlocked by this work>

## Out of Scope

- <explicit exclusions>
- <anything that cannot be pinned during planning and must not be left to execution model discretion>

## Forbidden

- Do not create base/utility classes that already exist; reuse the existing ones referenced above.
- Do not touch files outside the `implement.md` file plan; PRD-only low-complexity tasks must stay inside the compact appendix file list.
- Do not introduce dependencies or frameworks not listed in `design.md` / `implement.md`.
- Do not change Project Contract Reference names, paths, APIs, commands, packages/modules, routes, tables, or permission models.
- Do not use Contract Snapshot forbidden tokens.
- Do not implement adjacent domains opportunistically; adjacent work needs dependency or separate task.
- Do not leave `YOUR_KEY`, `API_KEY_HERE`, `TBD`, `depends`, `as needed`, or unresolved placeholders.
- <other project-specific red lines>

## Technical Notes

- Related files:
- Existing patterns:
- Relevant specs:
- Risks:
```
