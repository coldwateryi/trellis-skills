# Gate Definitions

This file is the single source of truth for `trellis-zero-to-mvp` Gates. Other templates may reference these Gates, but should not redefine conflicting pass conditions.

## Failure Codes

| Code | Meaning | Handling |
| --- | --- | --- |
| `MATRIX_INCOMPLETE` | Full Requirement Matrix does not cover all source-verifiable requirements | Continue requirement extraction |
| `CONTRACT_CONFLICT` | README/spec/code contracts conflict and are not resolved | Block and ask user to choose |
| `CONTRACT_SNAPSHOT_MISSING` | Contract Snapshot or forbidden tokens are missing | Fill contract snapshot |
| `UNASSIGNED_MVP_REQ` | MVP `TASK` requirement has no target child task | Add task mapping |
| `UNBATCHED_TASK` | Child task lacks batch | Assign B01/B02/... |
| `P0P1_ONLY_PLAN` | Only P0/P1 planned while MVP `TASK` items remain unplanned | Continue later batches |
| `DEFERRED_PRD_WITHOUT_PLAN` | Later batch lacks PRD draft or artifact needs | Add planning draft |
| `SMALL_MODEL_GRAIN_FAIL` | Child task violates Small Model Mode granularity | Split or block for explicit user merge approval |
| `ARTIFACT_MATRIX_INCOMPLETE` | Planning artifact matrix lacks tasks or reasons | Complete matrix |
| `DESIGN_SURFACE_MISSING` | A child task declares an involved design surface but lacks matching `design.md` or `implement.md` sections | Fill design-surface sections or fix the impact matrix |
| `DATABASE_SCHEMA_MISSING` | Database/data model is involved but table design or migration plan is missing | Fill Database Schema Design and Database Migration Plan |
| `API_CONTRACT_MISSING` | API is involved but request/response/error/permission contract or implementation plan is missing | Fill API Contract Design and API Implementation Plan |
| `INTER_MODULE_CONTRACT_MISSING` | Inter-module interaction is involved but call boundaries, transaction boundary, or failure strategy are missing | Fill Inter-Module Interaction Design and Wiring Plan |
| `EXTERNAL_INTERFACE_CONTRACT_MISSING` | External system is involved but protocol, auth, config, timeout, fallback, or mock strategy is missing | Fill External System Interface Design and Adapter Plan |
| `UI_DESIGN_MISSING` | Page/UI is involved but project style, page structure, table/form, or state design is missing | Fill UI Design and Style Contract and UI Implementation Plan |
| `UI_STYLE_CONTRACT_MISMATCH` | UI design conflicts with Project Contract Lock or current project style | Fix according to reference page and design system |
| `PERMISSION_CONTRACT_MISSING` | Permission/data scope is involved but backend permission, frontend button permission, menu, or data scope rule is missing | Fill Permission and Data Scope Design |
| `DATA_SCOPE_RULE_MISSING` | Data scope is involved but department/role/tenant filtering rule is missing | Fill data scope rule |
| `DICT_CONTRACT_MISSING` | Dictionary/enum is involved but dict type and values are missing | Fill Dictionary and State Design |
| `STATE_TRANSITION_MISSING` | State transition is involved but allowed transitions, roles, preconditions, and illegal behavior are missing | Fill state-machine design |
| `QUERY_CONTRACT_MISSING` | Query list is involved but query fields, match mode, sorting, or pagination rules are missing | Fill Query and Import Export Design |
| `EXPORT_IMPORT_CONTRACT_MISSING` | Import/export is involved but fields, permission, template, or error handling is missing | Fill import/export design |
| `VALIDATION_CONTRACT_MISSING` | Form/API input is involved but frontend/backend/business validation is missing | Fill Validation and Error Semantics |
| `ERROR_SEMANTICS_MISSING` | Concrete error message, code, or failure response shape is missing | Fill error semantics |
| `TRANSACTION_CONTRACT_MISSING` | Multiple writes/state transition/batch processing is involved but transaction boundary is missing | Fill transaction design |
| `IDEMPOTENCY_CONTRACT_MISSING` | Callback/sync/duplicate submission is involved but idempotency strategy is missing | Fill idempotency design |
| `ASYNC_JOB_CONTRACT_MISSING` | Scheduled/async job is involved but trigger, lock, or failure handling is missing | Fill Async Job and Event Design |
| `EVENT_CONTRACT_MISSING` | Event/message is involved but topic/payload/consumer/failure strategy is missing | Fill event design |
| `AUDIT_LOG_CONTRACT_MISSING` | Admin operation or external call is involved but logging/audit design is missing | Fill Audit and Logging Design |
| `SENSITIVE_LOGGING_RISK` | Logs may record sensitive data but masking strategy is missing | Fill masking rules |
| `DATA_INIT_CONTRACT_MISSING` | Menu/dictionary/config initialization is involved but initialization design is missing | Fill Data Initialization and Migration Design |
| `MIGRATION_COMPATIBILITY_MISSING` | Table field/data migration is involved but existing-data compatibility or rollback strategy is missing | Fill migration compatibility design |
| `TEST_STRATEGY_MISSING` | Test strategy design is missing | Fill Test Strategy Design |
| `AC_TEST_MAPPING_MISSING` | AC is not mapped to concrete tests or manual acceptance | Fill AC-to-test mapping |
| `PERFORMANCE_CONSTRAINT_MISSING` | Report/import/aggregation/large list is involved but performance/capacity constraints are missing | Fill Performance and Capacity Design |
| `SECURITY_CONTRACT_MISSING` | Security-sensitive entry is involved but security constraints are missing | Fill Security and Sensitive Data Design |
| `SENSITIVE_DATA_POLICY_MISSING` | Sensitive data is involved but display/export/log masking policy is missing | Fill sensitive-data policy |
| `CONFIG_CONTRACT_MISSING` | Config is involved but config name, default, missing behavior, or environment difference is missing | Fill Configuration Design |
| `FRAMEWORK_CONVENTION_MISSING` | Framework generation/directory/base class/annotation is involved but project convention is missing | Fill Framework Convention Design |
| `MANUAL_ACCEPTANCE_UNCLEAR` | Manual acceptance is required but preconditions, steps, pass criteria, or evidence are missing | Fill Manual Acceptance Design |
| `OPS_DOC_CONTRACT_MISSING` | Config/deploy/scheduled/external system is involved but documentation/ops handoff is missing | Fill Documentation and Operations Handoff |
| `MISSING_DECLARED_ARTIFACT` | Declared artifact is absent from real task directory | Write artifact or fix declaration |
| `PLACEHOLDER_HIT` | Artifact contains template placeholders or unresolved expressions | Replace with concrete values |
| `JSONL_SEED_HIT` | JSONL still contains `_example` seed row | Fill real context or delete/explain not needed |
| `JSONL_MODE_MISMATCH` | JSONL mode conflicts with `.trellis/config.yaml` or artifact matrix | Fix `required/optional/inline` mode and rerun Gate |
| `CONTRACT_TOKEN_HIT` | Forbidden token appears | Fix according to Contract Snapshot |
| `COVERAGE_COUNT_MISMATCH` | Coverage statistics do not match mechanical matrix counts | Recount and fix parent PRD |
| `MECHANICAL_GATE_MISSING` | Gate result lacks command/script evidence or is hand-filled | Run mechanical scan and use real output |
| `DECLARED_GATE_MISMATCH` | Parent PRD declared Gate counts differ from mechanical scan | Use mechanical scan as truth |
| `STATE_DRIFT` | Stage State Packet disagrees with matrices, ledgers, or real directories | Drift Reset |
| `DEVELOPMENT_NOT_READY` | Development recommendation threshold is not met | Do not recommend development |

## Gate Output Format

Every Gate uses this output shape:

```yaml
gate:
  name: <Gate Name>
  result: PASS | FAIL
  failure_codes:
    - <code>
  evidence:
    - <file/table/row>
  next_action: <specific fix or next batch action>
```

Gate evidence cannot be pure prose. Counts, file existence, placeholders, JSONL seeds, forbidden tokens, and Artifact Gate must cite command output, script output, matrix rows, or real file paths. Missing mechanical evidence makes the Gate `FAIL` with `MECHANICAL_GATE_MISSING`.

## Requirement Ledger Gate

Inputs:

- Source requirements.
- Source requirement list.
- Full Requirement Matrix.
- MVP Coverage Matrix.
- Backlog.

PASS conditions:

- Every source requirement has a stable `REQ-xxx`.
- Every acceptance point has a stable `AC-xxx`.
- Full Requirement Matrix covers all source-verifiable requirements.
- MVP Coverage Matrix status is one of `TASK`, `MERGED`, `BASELINE`, `OUT_OF_SCOPE`, `BLOCKED`.
- Mechanical count of `TASK + MERGED + BASELINE + OUT_OF_SCOPE + BLOCKED` equals Full Requirement Matrix rows.
- Every `OUT_OF_SCOPE` requirement enters Backlog.

If FAIL, do not draft full child PRDs.

## Contract Gate

Inputs:

- Project Contract Lock.
- Contract Snapshot.
- README, AGENTS, `.trellis/spec/`, and existing code evidence.

PASS conditions:

- Project Contract Profile is selected with evidence and rejected-profile reasons.
- Contract Lock uses selected profile fields; every applicable field has adopted value and evidence path.
- Non-applicable fields are explicitly `not-applicable`; Java/RuoYi fields are not applied to CLI, SDK, frontend, Python service, or custom projects.
- `forbidden_tokens` come from conflicts, old wrong tasks, framework-default misreads, or values inconsistent with README/spec/code.
- No unresolved `CONTRACT_CONFLICT`.

If FAIL, do not create tasks.

## Full MVP Planning Gate

Inputs:

- Full Requirement Matrix.
- MVP Coverage Matrix.
- Subtask Planning Ledger.
- Batch Completion Rollup.
- Planning artifact matrix.
- Parent/child PRD drafts.

PASS conditions:

- Every MVP `TASK` coverage row has target Task ID.
- Every `MERGED` row names target child task and covering AC.
- Every Task ID has title, REQ coverage, dependencies, priority, batch, parallel group, complexity, Small Model granularity, acceptance criteria, PRD draft, and artifact needs.
- Every Task ID has a `Task Impact Matrix`; if any surface is `yes`, the planning artifact matrix requires `design.md` and `implement.md` and lists the corresponding sections.
- Every MVP child task status is `READY_TO_CONFIRM`, `BLOCKED`, or `OUT_OF_SCOPE`.
- No `UNASSIGNED_MVP_REQ`, `UNBATCHED_TASK`, `P0P1_ONLY_PLAN`, or `DEFERRED_PRD_WITHOUT_PLAN`.
- Planning artifact matrix covers all current MVP `TASK` child tasks in Subtask Planning Ledger.
- Stage State Packet `total_mvp_tasks`, `ready_to_confirm`, `blocked`, `out_of_scope`, and `non_terminal` match mechanical Subtask Planning Ledger counts.

If FAIL, continue planning the next batch; do not ask for confirmation.

## Batch Completeness Gate

Inputs:

- Subtask Planning Ledger.
- Batch Completion Rollup.

PASS conditions:

- Every MVP `TASK` child task has a batch.
- Every batch lists Task IDs, goal, dependency layer, parallel group, status, remaining non-terminal count, and next step.
- No batch exceeds Small Model Mode limits.
- Later batches are not merely "to be planned"; they have frozen boundaries, REQ coverage, dependencies, complexity, and artifact needs.

If FAIL, output `BATCH_INCOMPLETE`.

## Design Surface Gate

Inputs:

- Child PRD `Task Impact Matrix`.
- `design.md`.
- `implement.md`.
- `references/design-surface-template.md`.

PASS conditions:

- Every child PRD contains a `Task Impact Matrix`.
- If any surface has `Involved = yes`, `design.md` exists and contains the design section declared in the matrix.
- If any surface has `Involved = yes`, `implement.md` exists and contains the implementation-plan section declared in the matrix.
- Matrix failure codes match the mapping in `design-surface-template.md`.
- For `java-ruoyi-crud` CRUD/fullstack/frontend/backend tasks, common surfaces such as database, API, UI, permissions, query, validation, and tests must not all be marked `no` without reason.

The first mechanical Gate only checks "declared yes -> section exists". If the model incorrectly marks an obviously involved surface as `no`, self-review must report the risk; later versions can add keyword inference.

## Pre-Confirmation Gate

Inputs:

- Requirement Ledger Gate result.
- Contract Gate result.
- Full MVP Planning Gate result.
- Batch Completeness Gate result.

PASS conditions:

- All above Gates are `PASS`.
- User confirmation summary can cover the complete MVP task tree, all batches, Backlog, Blocked items, and creation scope.

If FAIL, do not ask the user to confirm.

## Task Creation Gate

Inputs:

- User confirmation record.
- `task.py create` output.
- Subtask Planning Ledger.

PASS conditions:

- User confirmed complete planning.
- Parent and all confirmed-scope children were created through `task.py create`.
- Every real directory contains `task.json`.
- Logical Task ID -> real task directory mapping is backfilled.
- No side directory without `task.json` holds PRD.

If FAIL, do not write artifacts.

## Artifact Gate

Inputs:

- Real task directories.
- Parent/child `prd.md`.
- `design.md`, `implement.md`, `implement.jsonl`, `check.jsonl`.
- Planning artifact matrix.
- Contract Snapshot.
- `scripts/trellis_zero_gate.py` output or equivalent mechanical scan.

Recommended command:

```bash
python <skill-dir>/scripts/trellis_zero_gate.py \
  --tasks .trellis/tasks \
  --parent-task-json <parent-task-dir>/task.json \
  --parent-prd <parent-task-dir>/prd.md \
  --jsonl-mode <required|optional|inline>
```

If Contract Snapshot defines forbidden tokens, add `--forbidden-token '<token>'` or `--forbidden-regex '<regex>'`. If a project-contract conflict cannot be simplified to forbidden tokens, add `--contract-mismatch-regex '<regex>'`.

PASS conditions:

- `scanned_tasks` equals parent plus child tasks in scope.
- `placeholder_hits = 0`.
- `angle_placeholder_hits = 0`.
- `jsonl_seed_hits = 0`. Only `jsonl_mode=required` blocks on seeds; `optional` / `inline` must still output raw seed examples and matrix explanations for deletion or not-needed reason.
- `forbidden_token_hits = 0`.
- `contract_mismatch_hits = 0`.
- `coverage_count_mismatch_hits = 0`.
- `high_complexity_missing_artifacts = 0`.
- `missing_declared_artifacts = 0`.
- `design_surface_prd_without_matrix = 0`.
- `design_surface_missing_hits = 0`.
- `declared_gate_mismatch_hits = 0`.
- `external_config_hits = 0`.
- Mechanical output `result = PASS`.

FAIL or PENDING means do not claim the task tree is executable.

## Development Recommendation Gate

Inputs:

- Subtask Planning Ledger.
- Artifact Gate result.
- Blocked task list.

PASS conditions:

- Artifact Gate is `PASS`.
- Every created current-MVP child task is `GATED_PASS`, `BLOCKED`, or `OUT_OF_SCOPE`.
- No unexplained non-terminal task remains.
- A recommended task's dependencies are satisfied or are existing baselines.

If FAIL, output `development_ready: false`; do not recommend starting development.
