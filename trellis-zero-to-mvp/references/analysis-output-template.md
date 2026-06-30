# Zero to MVP Analysis Output Template

> **Small model note:** This template covers output formats for S1-S10. Do not attempt to fill everything at once. Each section is tagged with its applicable phase:
> - `[S0]` Discovery Phase
> - `[S1]` Requirement Ledger Phase
> - `[S2]` Contract Lock Phase
> - `[S3]` Task Candidate Phase
> - `[S4]` Batch Planning Phase
> - `[S5]` Gating Phase
> - `[S6]` User Confirmation Phase
> - `[S7]` Task Creation Phase
> - `[S8]` Artifact Writing Phase
> - `[S9]` Artifact Gate Phase
> - `[ALL]` All Phases

## [S0] Project Goal Summary

Write 5-10 bullets describing what the requirements document asks the project to deliver.

## [S2] Project Contract Profile

Read `project-contract-profiles.md` first and select a profile from repository evidence. Do not apply RuoYi/Java CRUD fields to CLI, SDK, frontend, Python service, or custom framework projects.

```yaml
project_contract_profile:
  selected: <java-ruoyi-crud|typescript-cli-framework|frontend-spa|python-service|custom>
  secondary_profiles:
    - <profile or none>
  evidence:
    - <path:reason>
  rejected_profiles:
    - profile: <name>
      reason: <why not applicable>
```

## [S2] Project Contract Lock

Lock implementation contracts from user requirements, README, module README, AGENTS.md, `.trellis/spec/`, and existing code. Later artifacts must follow this table and cannot switch naming systems.

| Contract Item | Profile Field | adopted_value | evidence_path | forbidden_tokens | Notes |
| --- | --- | --- | --- | --- | --- |
| <item> | <profile field> | <specific value or not-applicable> | <path> | <tokens or none> | <notes> |

Example fields by profile, use only those that apply:

- `java-ruoyi-crud`: backend module, Java entity naming, table prefix, Controller package/route, Service/Mapper/XML, frontend API/Views, permission prefix, SQL organization.
- `typescript-cli-framework`: workspace package manager, package layout, CLI entrypoints, SDK public API, template source paths, generated destinations, workflow state blocks, platform configurators, script templates, test/build commands.
- `frontend-spa`: routes, page components, shared components, API client, state management, design system, auth guard, test/build commands.
- `python-service`: package layout, app/CLI entrypoint, router/command paths, service modules, schema/model paths, config policy, test/lint/typecheck commands.

### Contract Snapshot and Forbidden Tokens

Convert Project Contract Lock into a mechanically scannable snapshot. `forbidden_tokens` must come from conflicts, old wrong tasks, framework-default misreads, or values inconsistent with README/spec/code.

| Profile Field | Adopted Value (must use) | Forbidden Tokens | Evidence Path | Notes |
| --- | --- | --- | --- | --- |
| <field> | <specific path/command/API/name> | <conflict tokens or none> | <path> | <notes> |

Rule: if parent/child PRDs, `design.md`, `implement.md`, or JSONL hit a forbidden token, Artifact Gate must FAIL.

### CONTRACT_CONFLICT (if any)

| Conflict | Source A | Source B | Recommended Value | Risk | Blocking |
| --- | --- | --- | --- | --- | --- |
| <name/path/prefix> | <path/value> | <path/value> | <value> | <risk> | <yes/no> |

If a conflict blocks planning, do not create tasks; ask the user to confirm the adopted contract first.

## [S1] Existing Implementation Baseline

Use this section when the repository already contains manually implemented functionality or Trellis/spec was initialized after development started.

| Existing Capability | Evidence Type | Code Evidence | Test Evidence | Requirement IDs Covered | Baseline Dependency Name | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| <capability> | code/test/spec/task | <exact path> | <exact path or "none"> | REQ-001 | existing:<capability-or-file> | <reuse constraints> |

Rules:

- Source requirements are the source of truth; existing code and `.trellis/spec/` are evidence, not substitute requirements.
- If a requirement is `DONE`, do not create an implementation task for that scope.
- If a requirement is `UNTESTED`, create only a test-coverage task unless implementation evidence is weak.
- If a requirement is `PARTIAL`, create a gap-closing task for missing behavior only.
- If a requirement is `MISSING`, create a new implementation task.

## [S0] Trellis Workflow Context

| Item | Value | Notes |
| --- | --- | --- |
| Trellis version/source | <from `.trellis/.version` or "unknown"> | <0.6+/legacy signal> |
| Workflow contract | <`.trellis/workflow.md` path or "not present"> | <artifact requirements found> |
| Config | <`.trellis/config.yaml` path or "not present"> | <relevant options> |
| Codex dispatch_mode | <inline/sub-agent/unknown/not-codex> | <JSONL Gate mode: inline/required/optional> |
| Developer identity | <from `.trellis/.developer` or "not initialized"> | <action needed if missing> |
| Spec freshness | <fresh/stale/missing/unknown> | <spec files read or refresh task needed> |

## [ALL] Execution Model Profile

| Item | Value |
| --- | --- |
| Expected execution model | <e.g. qwen3.6 35b local / GPT-5.5 / Opus 4.8> |
| Planning depth | <standard / small-model-safe / high-risk> |
| Task granularity rule | <how small tasks must be> |
| Small Model Mode | <enabled/disabled; trigger reason> |
| Batch limit | <e.g. max 8 executable tasks, max 5 full PRDs per batch> |
| Batch planning requirement | <if over limit, list all B01/B02/... batches; never stop at P0/P1> |

## [ALL] Stage State Packet

Required for small/local models, long complex tasks, more than 8 candidates, or context recovery. Values come from matrices, ledger, and real directories; unknown values are allowed only during discovery.

```yaml
stage_state:
  state: <S0_DISCOVER_CONTEXT...S10_NEXT_IMPLEMENTATION_RECOMMENDATION>
  source_docs:
    - <path>
  contract_snapshot: <present/missing/path>
  full_requirement_count: <number or unknown>
  mvp_coverage_counts:
    TASK: <n>
    MERGED: <n>
    BASELINE: <n>
    OUT_OF_SCOPE: <n>
    BLOCKED: <n>
  subtask_ledger:
    total_mvp_tasks: <n>
    ready_to_confirm: <n>
    blocked: <n>
    out_of_scope: <n>
    non_terminal: <n>
  current_batch: <Bxx or none>
  next_legal_action: <one action>
  stop_gate_failures:
    - <none or failure codes>
```

Rules:

- `next_legal_action` can contain only one action.
- If `stop_gate_failures` is non-empty, do not ask for user confirmation, create tasks, or recommend development.
- If Stage State Packet disagrees with Full Requirement Matrix, MVP Coverage Matrix, Subtask Planning Ledger, or real directories, output `STATE_DRIFT` and do Drift Reset.

## [S1] Source Requirement List

Extract every verifiable source requirement. `REQ-xxx` is the stable identity; task merge/split/reorder cannot change its meaning.

| Source Section | Source Requirement | Stable ID | Summary | Notes |
| --- | --- | --- | --- | --- |
| <chapter/page/title> | <source point> | REQ-001 | <one-line summary> | <context> |

## [S1] Full Requirement Matrix

This table reflects source truth only. Every source-verifiable requirement must have one row.

| ID | Source Section/Point | Requirement Summary | Implementation Status | Related Code | Existing Tests | Gap |
| --- | --- | --- | --- | --- | --- | --- |
| REQ-001 | <section/point> | <summary> | MISSING | <path or none> | <path or none> | <gap> |

Allowed statuses:

- `DONE`: fully implemented and tested.
- `PARTIAL`: partially implemented.
- `MISSING`: not implemented.
- `UNTESTED`: implemented but lacks enough tests.
- `UNCLEAR`: requirement is too unclear to implement.

## [S1] MVP Coverage Matrix

> **Mechanical constraint:** `TASK + MERGED + BASELINE + OUT_OF_SCOPE + BLOCKED` = Full Requirement Matrix row count

This table describes how the current MVP handles each full requirement. Do not report MVP coverage count as the original source requirement count.

After generation, mechanically count `TASK`, `MERGED`, `BASELINE`, `OUT_OF_SCOPE`, and `BLOCKED`; their sum must equal Full Requirement Matrix rows. Reuse these counts in the parent PRD. Do not hand-estimate them again.

| ID | Requirement Summary | Coverage Status | Task Action | Target Task/Baseline/Scope Note | Covering AC | MVP/Backlog Note |
| --- | --- | --- | --- | --- | --- | --- |
| REQ-001 | <summary> | TASK | new-task | T01 | AC-001 | MVP |

Coverage status:

- `TASK`: create an independent child task.
- `MERGED`: merge into another child task; name the target task and covering AC.
- `BASELINE`: covered by existing implementation; cite baseline evidence.
- `OUT_OF_SCOPE`: not in current MVP; explain why and surface during user confirmation.
- `BLOCKED`: blocked; explain issue and next step.

Task actions:

- `none`: requirement is `DONE`; keep as baseline evidence.
- `test-only`: requirement is `UNTESTED`; create only a test-coverage task, not reimplementation.
- `gap-task`: requirement is `PARTIAL`; implement only missing behavior.
- `new-task`: requirement is `MISSING`; create a new implementation task.
- `clarify`: requirement is `UNCLEAR`; ask a blocking question or create a clarification task before implementation.

## [S1-S2] Full Platform Scope vs MVP Boundary

| Scope Block | Full Platform Requirement | Current MVP Handling | Difference/Risk |
| --- | --- | --- | --- |
| <PC/IOC/integration/mobile/report/etc.> | <source scope> | <TASK/MERGED/OUT_OF_SCOPE> | <risk> |

## [S3] Task Merge/Split Record

Every source requirement that is not an independent task must have a destination here.

| Requirement ID | Source Point | Handling | Target Task/Baseline/Scope | Covering AC | Reason | Risk |
| --- | --- | --- | --- | --- | --- | --- |
| REQ-001 | <point> | MERGED | T03 | AC-003-01 | <why> | <risk> |

Handling values: `SPLIT`, `MERGED`, `BASELINE`, `OUT_OF_SCOPE`, `BLOCKED`.

## Backlog / Later Scope

Every `OUT_OF_SCOPE` requirement must appear here and must not disappear from traceability.

| Requirement ID | Source Point | Exclusion Reason | Recommended Stage | Conditions to Re-enter Scope | Depends on MVP Tasks |
| --- | --- | --- | --- | --- | --- |
| REQ-999 | <point> | <reason> | MVP+1/V2/BLOCKED | <conditions> | <task ids> |

## Module Dependency Graph

| Module | Responsibility | Depends On | Used By | Risks |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## [S3] Task Split

Small Model Mode rules:

0. The model must not self-exempt oversized tasks using "strongly coupled", "same flow", or "splitting would increase dependencies" as justification. Only user-confirmed merges are allowed, with explicit risk notes.
1. Each child task covers at most one entity's CRUD, one endpoint group, one state transition, one front-end page, or one backend aggregate query.
2. A candidate containing multiple primary entities, multiple CRUD sets, CRUD + state machine + report, backend flow + mini-app page, or map/GIS + multi-table aggregation + advanced analytics must be split.
3. Max 8 executable tasks per batch, max 5 full PRDs per batch. P0/P1 is priority, not completeness.
4. High-complexity tasks must be split to low/medium, or require `design.md` + `implement.md` + JSONL.

| Task ID | Title | Goal | Type | Requirement IDs | Source Status | Depends On | Baseline Dependencies | Priority | Complexity | Small Model Granularity | Planning Artifacts | Parallelizable | Acceptance Criteria | Likely Areas |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T01 |  |  | docs | REQ-001 | MISSING | none | none | P0 | low | one entity CRUD / one endpoint group / one state transition / one page / one aggregate query | prd.md | no |  |  |

Allowed task types: `backend`, `frontend`, `fullstack`, `cli`, `sdk`, `template`, `workflow`, `script`, `docs`, `test`, `infra`.

Complexity is assessed against execution-model capability and determines split granularity and PRD detail:

- `low`: standard CRUD/config, or a direct example to copy. Weak model can complete independently.
- `medium`: some business validation or cross-table logic; needs explicit implementation steps. Weak model can complete with detailed PRD.
- `high`: complex transaction/concurrency/cross-module consistency or much implicit domain knowledge. Weak model is unlikely to complete independently; split into low/medium tasks or pin every step in PRD/design/implement so no reasoning is needed.

Priority rules:

- `P0`: blocks other modules or core correctness.
- `P1`: core business loop.
- `P2`: experience, reports, notifications, enhancements.
- `P3`: non-essential optimization.

Ordering rules:

1. Data structures, API contracts, and config first.
2. Tasks that block other modules before dependent tasks.
3. High-risk and unknown-heavy tasks early for validation.
4. UI polish, docs, and experience enhancements later.
5. Do not mark mutually dependent tasks as parallelizable.

Small Model Mode rules:

0. The model must not keep oversized tasks by claiming "strong coupling", "same flow", or "splitting adds dependencies" on its own. Only explicitly user-approved merges are exceptions, and the risk column must record them.

1. A child task covers at most one primary entity CRUD, one endpoint group, one state transition, one frontend page, or one backend aggregate query.
2. Split tasks that combine multiple primary entities, multiple CRUD sets, CRUD + state machine + report, backend flow + mini-app page, map/GIS + multi-table aggregation + advanced analytics.
3. Max 8 executable tasks per batch and max 5 full PRDs per batch. If over limit, plan a complete batch index first. P0/P1 is priority, not completion of full planning.
4. High complexity tasks must be split into low/medium tasks or require `design.md` + `implement.md` + JSONL context.

Existing implementation rules:

1. Do not create child tasks for `DONE` requirements.
2. Create `test` tasks for `UNTESTED` requirements only when tests are missing.
3. Create gap-closing tasks for `PARTIAL` requirements; task title must name the missing behavior, not the already implemented behavior.
4. When a task depends on existing capability, write it as `existing:src/auth/session.ts` or equivalent in Baseline Dependencies.
5. Do not disguise existing baseline dependencies as new Trellis tasks.

## [S4] Subtask Planning Ledger

The ledger is the only state source for progressive planning. Every MVP Coverage Matrix row with `TASK` status must have a row. Do not keep only the current batch.

| Task ID | Requirement IDs | Title | Priority | Batch | Dependencies | Parallel Group | Owner Agent | Planning Status | PRD Status | design/implement Status | Artifact Gate | Real Directory | Next Step |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T01 | REQ-001 | <title> | P0 | B01 | none | G01 | main/agent-a | CANDIDATE/DRAFTED/READY_TO_CONFIRM/USER_CONFIRMED/CREATED/ARTIFACTS_WRITTEN/GATED_PASS/BLOCKED/OUT_OF_SCOPE | missing/draft/ready/written | not-needed/draft/ready/written | PENDING/PASS/FAIL/N/A | <task.py output dir or pending> | <next action> |

Status rules:

- `CANDIDATE`: candidate task identified, but boundary, dependencies, or artifacts are not frozen.
- `DRAFTED`: draft exists, but Full MVP Planning Gate has not passed.
- `READY_TO_CONFIRM`: task boundary, REQ coverage, dependencies, acceptance, PRD draft, and artifact needs are frozen and can enter user confirmation.
- `USER_CONFIRMED`: user confirmed this task belongs to the current creation scope.
- `CREATED`: real directory was created through `task.py create` and ledger was backfilled.
- `ARTIFACTS_WRITTEN`: all declared planning artifacts were written.
- `GATED_PASS`: Artifact Gate passed.
- `BLOCKED`: clear blocker, owner, and recovery condition exist.
- `OUT_OF_SCOPE`: entered Backlog; not created for current MVP.

Before confirmation, all MVP `TASK` child tasks must be `READY_TO_CONFIRM`, `BLOCKED`, or `OUT_OF_SCOPE`. If any are `CANDIDATE` or `DRAFTED`, output `BATCH_INCOMPLETE` and continue planning the next batch.

## [S4] Batch Completion Rollup

| Batch | Task IDs | Goal | Status | READY_TO_CONFIRM | BLOCKED | OUT_OF_SCOPE | Remaining Non-Terminal | Next Batch Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B01 | T01,T02,T03 | P0 foundations | planned/in-progress/ready/blocked | <n> | <n> | <n> | <n> | <continue B02 or none> |

Completion rule:

- `all_mvp_task_count` equals current MVP `TASK` rows in Subtask Planning Ledger.
- `ready_or_terminal_count = READY_TO_CONFIRM + BLOCKED + OUT_OF_SCOPE`.
- Only when `ready_or_terminal_count == all_mvp_task_count` may output `ALL_SUBTASK_PLANNING_COMPLETE`.
- Otherwise output `BATCH_INCOMPLETE`, list next-batch Task IDs, unfinished reasons, and the main agent's next action.

## [S4] Agent Dispatch Plan (if triggered)

When candidate child tasks exceed batch limits, business domains exceed 3, full PRD drafts exceed 5, or the user requests multi-agent planning, output this according to `subagent-planning-template.md`:

| Agent | Input Scope | Output Scope | Status | Failure Code |
| --- | --- | --- | --- | --- |
| requirement-ledger-agent | <REQ range> | <matrix review> | planned/running/done/blocked | <none/code> |
| batch-split-agent | <MVP TASK range> | <batch split> | planned/running/done/blocked | <none/code> |
| gate-check-agent | <all drafts> | <Gate PASS/FAIL> | planned/running/done/blocked | <none/code> |

## [S5] Planning Artifact Matrix

Fill this before creating Trellis tasks. This matrix is the basis for post-creation file existence checks; `task.py create` does not automatically fill `design.md` or `implement.md`.

| Task ID | Real Directory | Title | Complexity | prd.md | design.md | implement.md | implement.jsonl | check.jsonl | jsonl_mode | Write Status | Gate Result | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T01 | <task.py output dir> | <title> | <low/medium/high> | required | <required/not required> | <required/not required> | <required/not required> | <required/not required> | required/optional/inline | WRITTEN/NOT_NEEDED_WITH_REASON/BLOCKED | PASS/FAIL/PENDING | <workflow, complexity, model capability reason> |

Rules:

- Every child task has `prd.md`.
- High complexity cannot be PRD-only; split or require `design.md` + `implement.md`.
- If project workflow or nearby task directories contain `implement.jsonl` / `check.jsonl`, the matrix must state JSONL mode: `required` (sub-agent or stable context preload is truly required), `optional` (can delete or explain not needed), or `inline` (Codex inline, not a planning-readiness gate). Seed-only JSONL is not enough.
- Files marked required must exist in real `task.py create` directories after creation.
- `Write Status = WRITTEN` must mean the file exists in the real directory. `NOT_NEEDED_WITH_REASON` must explain why it is not needed. `BLOCKED` must prevent executable reporting.

## [S5] MVP Recommended Development Order

Output this only after Full MVP Planning Gate passes. It must cover every current MVP `TASK` child task. If it covers only the created batch, rename the section to `This Batch Execution Order` and do not recommend starting development.

1. `<task-id>`: `<reason>`
2. `<task-id>`: `<reason>`

## [S5] Artifact Gate Plan

After task creation, run and report:

| Check | Handling on Hit |
| --- | --- |
| `_example` JSONL | Fill real context, delete and explain not needed, or block |
| `{Entity}` / `<path>` / `TBD` / `to be provided` / `as needed` | Replace with concrete values |
| `YOUR_KEY` / `API_KEY_HERE` / unresolved external config | Mark `FIXED`, `BASELINE`, `BLOCKED`, or `OUT_OF_SCOPE` |
| Contract mismatch or forbidden token | Fix to Contract Snapshot; do not let model-invented names override README/spec |
| High complexity missing `design.md` / `implement.md` | Add artifacts or split task |
| PRD/design/implement semantic anchors disagree | Stop and fix |
| Task impact surface is `yes` but design/implementation section is missing | Fill the matching `design.md` / `implement.md` sections or fix the Task Impact Matrix |

Recommended command:

```bash
python <skill-dir>/scripts/trellis_zero_gate.py \
  --tasks .trellis/tasks \
  --parent-task-json <parent-task-dir>/task.json \
  --parent-prd <parent-task-dir>/prd.md \
  --jsonl-mode <required|optional|inline>
```

Add `--forbidden-token` or `--forbidden-regex` if Contract Snapshot has forbidden tokens. Do not hand-fill PASS before running mechanical scan.

## [S9] Artifact Gate Output Fields

After creating tasks, output these fields. `result` can only be `PASS` or `FAIL`; do not report executable readiness with `PENDING`.

| Field | Meaning | PASS Condition |
| --- | --- | --- |
| scanned_tasks | New tasks scanned | Equals parent + child count |
| placeholder_hits | Template/unresolved expression hits | 0 |
| angle_placeholder_hits | Generic `<...>` placeholder hits | 0 |
| jsonl_seed_hits | Blocking `_example` JSONL hits | 0 |
| forbidden_token_hits | Contract Snapshot forbidden token hits | 0 |
| contract_mismatch_hits | Project Contract Lock mismatch hits | 0 |
| coverage_count_mismatch_hits | Coverage statistics mismatch | 0 |
| high_complexity_missing_artifacts | Missing design/implement for complex task | 0 |
| missing_declared_artifacts | Declared required but missing files | 0 |
| design_surface_prd_without_matrix | Child PRD missing Task Impact Matrix | 0 |
| design_surface_missing_hits | Task Impact Matrix says a surface is involved but matching design/implementation sections are missing | 0 |
| declared_gate_mismatch_hits | Parent PRD Gate values differ from scan | 0 |
| external_config_hits | Unresolved external config/key placeholders | 0 |
| result | Overall result | PASS only when all blocking counts are 0 |

## [S6] Pre-Confirmation Gate

Fill this before outputting a confirmation request. If any item fails, do not ask for confirmation; continue planning or fix.

| Check | Result | Evidence / Next Step |
| --- | --- | --- |
| Requirement Ledger Gate | PASS/FAIL | <evidence> |
| Contract Gate | PASS/FAIL | <evidence> |
| Full MVP Planning Gate | PASS/FAIL | <evidence> |
| Batch Completeness Gate | PASS/FAIL | <evidence> |
| UNASSIGNED_MVP_REQ | 0/<n> | <REQ IDs> |
| UNBATCHED_TASK | 0/<n> | <Task IDs> |
| P0P1_ONLY_PLAN | false/true | <notes> |
| DEFERRED_PRD_WITHOUT_PLAN | 0/<n> | <Task IDs> |
| ALL_SUBTASK_PLANNING_COMPLETE | PASS/FAIL | <notes> |

If failing, output:

```yaml
planning_status:
  full_mvp_planning_gate: FAIL
  development_ready: false
  failure_codes:
    - <code>
  next_action: <next batch or fix action>
```

## Parent Task PRD Draft

Use `parent-prd-template.md`.

## Child Task PRD Drafts

Use `child-prd-template.md` for every child task.

For every medium/high complexity child task, also use `planning-artifacts-template.md` to draft required Trellis 0.6+ planning artifacts.

## Confirmation Request

Only when Pre-Confirmation Gate is `PASS`, end with:

```text
Please confirm the complete MVP task tree, all batch plans, Backlog boundary, Blocked items, and first creation scope. If confirmed, I will create the Trellis parent task, all planned child tasks, and their required PRD/design/implement/JSONL artifacts without writing application code.
```
