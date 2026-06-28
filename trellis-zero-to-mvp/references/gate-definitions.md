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
| `MISSING_DECLARED_ARTIFACT` | Declared artifact is absent from real task directory | Write artifact or fix declaration |
| `PLACEHOLDER_HIT` | Artifact contains template placeholders or unresolved expressions | Replace with concrete values |
| `JSONL_SEED_HIT` | JSONL still contains `_example` seed row | Fill real context or delete/explain not needed |
| `JSONL_MODE_MISMATCH` | JSONL mode conflicts with `.trellis/config.yaml` or artifact matrix | Fix `required/optional/inline` mode and rerun Gate |
| `CONTRACT_TOKEN_HIT` | Forbidden token appears | Fix according to Contract Snapshot |
| `COVERAGE_COUNT_MISMATCH` | Coverage statistics do not match mechanical matrix counts | Recount and fix parent PRD |
| `MECHANICAL_GATE_MISSING` | Gate result lacks command/script evidence or is hand-filled | Run mechanical scan |
| `DECLARED_GATE_MISMATCH` | Parent PRD declared Gate counts differ from mechanical scan | Use mechanical scan as truth |
| `STATE_DRIFT` | Stage State Packet disagrees with matrices, ledgers, or real directories | Drift Reset |
| `DEVELOPMENT_NOT_READY` | Development recommendation threshold is not met | Do not recommend development |

## Gate Output Format

```yaml
gate:
  name: <Gate Name>
  result: PASS | FAIL
  failure_codes:
    - <code>
  evidence:
    - <file/table/row/command output>
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

- Project Contract Profile.
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
- Every MVP child task status is `READY_TO_CONFIRM`, `BLOCKED`, or `OUT_OF_SCOPE`.
- No `UNASSIGNED_MVP_REQ`, `UNBATCHED_TASK`, `P0P1_ONLY_PLAN`, or `DEFERRED_PRD_WITHOUT_PLAN`.
- Planning artifact matrix covers all current MVP `TASK` child tasks in Subtask Planning Ledger.
- Stage State Packet counts match mechanical Subtask Planning Ledger counts.

If FAIL, continue planning; do not ask for confirmation.

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

## Pre-Confirmation Gate

Inputs:

- Requirement Ledger Gate.
- Contract Gate.
- Full MVP Planning Gate.
- Batch Completeness Gate.

PASS conditions:

- All above Gates are `PASS`.
- User confirmation summary covers the complete MVP task tree, all batches, Backlog, Blocked items, and creation scope.

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

Add `--forbidden-token`, `--forbidden-regex`, or `--contract-mismatch-regex` when Contract Snapshot requires them.

PASS conditions:

- `scanned_tasks` equals parent plus child tasks in scope.
- `placeholder_hits = 0`.
- `angle_placeholder_hits = 0`.
- `jsonl_seed_hits = 0`. Only `jsonl_mode=required` blocks on seeds; `optional` / `inline` must still output raw seed examples and matrix explanations.
- `forbidden_token_hits = 0`.
- `contract_mismatch_hits = 0`.
- `coverage_count_mismatch_hits = 0`.
- `high_complexity_missing_artifacts = 0`.
- `missing_declared_artifacts = 0`.
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
