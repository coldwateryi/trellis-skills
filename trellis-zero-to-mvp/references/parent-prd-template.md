# Parent PRD Template

```markdown
# <Project Title>

## Goal

Deliver the project described by the source requirements document. The parent task owns overall scope, requirement IDs, dependency plan, MVP boundary, and final acceptance definition. Child tasks own independently verifiable capabilities.

## Source Requirement Document

- Path: <requirements document path>
- Version: <version or date>
- Owner: <business or technical owner>

## Project Contract Lock

This section locks local implementation contracts. All child PRDs, `design.md`, and `implement.md` must follow it. If it changes, update this section and relevant README/spec first.

| Item | Value |
| --- | --- |
| Project Contract Profile | <java-ruoyi-crud/typescript-cli-framework/frontend-spa/python-service/custom> |
| Profile Evidence | <README/spec/code paths> |

| Contract Item | Profile Field | Adopted Value | Evidence Path | Forbidden Tokens |
| --- | --- | --- | --- | --- |
| <item> | <profile field> | <specific path/name/API/command/module or not-applicable> | <path> | <tokens or none> |

## Full Platform Scope vs Current MVP Boundary

| Scope Block | Full Platform Requirement | Current MVP Handling | Difference/Risk |
| --- | --- | --- | --- |
| <PC/IOC/integration/mobile/report/etc.> | <source scope> | <TASK/MERGED/OUT_OF_SCOPE/BLOCKED> | <risk> |

## Requirement IDs

| ID | Requirement Summary | Coverage Status | Child Task / Baseline / Scope Note | Covering AC | Implementation Status |
| --- | --- | --- | --- | --- | --- |
| REQ-001 | <summary> | TASK | <task slug> | AC-001 | PLANNED |

Allowed coverage statuses: `TASK`, `MERGED`, `BASELINE`, `OUT_OF_SCOPE`, `BLOCKED`.
Allowed implementation statuses: `PLANNED`, `IN_PROGRESS`, `DONE`, `PARTIAL`, `BLOCKED`, `VERIFIED`.

For requirements already satisfied by existing code, set child task to `none` and cite evidence in Existing Baseline Summary.
If a requirement is merged, write the target child task here and explain in Task Merge/Split Record.

## Requirement Coverage Summary

Counts must come from mechanical MVP Coverage Matrix statistics.

| Category | Count | Notes |
| --- | --- | --- |
| Source requirement count | <n> | Source-verifiable requirements extracted |
| Current MVP covered | <n> | `TASK` + `MERGED` + `BASELINE` |
| Independent child tasks | <n> | `TASK` |
| Merged coverage | <n> | `MERGED` |
| Existing baseline coverage | <n> | `BASELINE` |
| Current out of scope | <n> | `OUT_OF_SCOPE` |
| Blocked | <n> | `BLOCKED` |

## Task Merge/Split Record

| Requirement ID | Source Point | Handling | Target Task / Baseline / Scope | Covering AC | Reason | Risk |
| --- | --- | --- | --- | --- | --- | --- |
| REQ-001 | <point> | MERGED | <task slug> | AC-001 | <reason> | <risk> |

## Backlog / Later Scope

Every `OUT_OF_SCOPE` requirement must appear here.

| Requirement ID | Source Point | Exclusion Reason | Recommended Stage | Conditions to Re-enter Scope | Depends on MVP Tasks |
| --- | --- | --- | --- | --- | --- |
| REQ-999 | <point> | <reason> | MVP+1/V2/BLOCKED | <conditions> | <task ids> |

## Existing Baseline Summary

Use this when development started before Trellis planning:

| Requirement ID | Existing Capability | Evidence | Remaining Work |
| --- | --- | --- | --- |
| REQ-001 | <capability or "none"> | <code/test/spec paths> | <none/test gap/behavior gap> |

## Child Task Planning Progress

This table must cover every current MVP `TASK` child task. The parent task cannot claim planning complete while non-terminal rows remain.

| Task ID | Requirement IDs | Batch | Parallel Group | Planning Status | Real Directory | Gate | Blocker / Next Step |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T01 | REQ-001 | B01 | G01 | READY_TO_CONFIRM/GATED_PASS/BLOCKED/OUT_OF_SCOPE | <task.py output dir or pending> | PASS/FAIL/N/A | <notes> |

## Batch Completion Rollup

| Batch | Task IDs | Goal | Status | Remaining Non-Terminal | Next Step |
| --- | --- | --- | --- | --- | --- |
| B01 | T01,T02 | <goal> | planned/ready/gated/blocked | <n> | <notes> |

## Task Dependency Graph

```text
T0 requirements traceability
  -> T1 foundation
    -> T2 core capability
      -> T3 business loop
  -> T-final validation
```

## Delivery Strategy

1. Complete requirement tracing and technical planning.
2. Implement foundations and contracts.
3. Implement the MVP core business loop.
4. Add secondary capabilities only after dependencies complete.
5. Finish with validation and acceptance reporting.

## Definition of Done

- [ ] Every requirement ID has a status.
- [ ] All current MVP `TASK` child tasks are complete, blocked, or explicitly out of scope; not just P0/P1.
- [ ] Every requirement ID has test mapping or documented manual verification reason.
- [ ] Lint, typecheck, and required tests pass.
- [ ] Final acceptance report uses PASS / FAIL / PARTIAL / NOT TESTED / BLOCKED.
- [ ] Docs and run instructions are updated if behavior changed.

## Out of Scope

- <items explicitly excluded from MVP>

## Artifact Gate

After task creation, this section must pass. Counts must come from `scripts/trellis_zero_gate.py` or equivalent mechanical scan, not model judgment.

```bash
python <skill-dir>/scripts/trellis_zero_gate.py \
  --tasks .trellis/tasks \
  --parent-task-json <parent-task-dir>/task.json \
  --parent-prd <parent-task-dir>/prd.md \
  --jsonl-mode <required|optional|inline>
```

| Check | Result | Notes |
| --- | --- | --- |
| scanned_tasks | <n> | <task count scanned> |
| jsonl_mode | <required/optional/inline> | <from Codex dispatch_mode or artifact matrix> |
| placeholder_hits | <0/n> | `{Entity}`, `<path>`, `TBD`, `depends`, etc. |
| angle_placeholder_hits | <0/n> | Generic `<...>` placeholders |
| jsonl_seed_hits | <0/n> | `_example` JSONL |
| contract_mismatch_hits | <0/n> | Project Contract Lock mismatch |
| forbidden_token_hits | <0/n> | Contract Snapshot forbidden tokens |
| coverage_count_mismatch_hits | <0/n> | Requirement coverage statistics mismatch |
| high_complexity_missing_artifacts | <0/n> | High complexity missing `design.md` / `implement.md` |
| missing_declared_artifacts | <0/n> | Declared required but missing files |
| declared_gate_mismatch_hits | <0/n> | Parent PRD declared values differ from scan |
| external_config_hits | <0/n> | `YOUR_KEY`, pending external config |
| result | PASS/FAIL | <fix action or blocker on FAIL> |

## Notes

- Strict dependencies live in child task `Dependencies` sections.
- Existing capabilities may be referenced as baseline dependencies in child tasks.
- Parent/child links organize scope but do not replace dependency documentation.
- Child task names, paths, APIs, commands, packages/modules, routes, tables, and permission models must match Project Contract Lock.
```
