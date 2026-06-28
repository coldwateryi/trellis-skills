# Task Creation Checklist

Use this after the user confirms the complete read-only plan.

## Before Creating Tasks

- [ ] Source requirements document path is known.
- [ ] `.trellis/workflow.md` was read if present; `.trellis/config.yaml`, `.trellis/.version`, `.trellis/.developer` were checked if present.
- [ ] `.trellis/config.yaml` `codex.dispatch_mode` was read; `inline` uses `jsonl_mode=inline`, sub-agent or JSONL-required contexts use `jsonl_mode=required`.
- [ ] Relevant `.trellis/spec/` files are fresh enough, or a spec-refresh/bootstrap task is planned.
- [ ] Project Contract Profile is selected with evidence and rejected-profile reasons.
- [ ] Project Contract Lock exists; applicable profile fields have adopted values and evidence paths; non-applicable fields are `not-applicable`.
- [ ] RuoYi/Java fields were not applied to CLI, SDK, frontend, Python service, or custom framework projects.
- [ ] Any `CONTRACT_CONFLICT` was confirmed by the user before task creation.
- [ ] Contract Snapshot and forbidden tokens exist; child task candidates have been checked against them.
- [ ] Child task candidates follow Project Contract Lock and do not mix naming/path/API systems.
- [ ] Existing Implementation Baseline is complete when the repo already has manual implementation.
- [ ] `DONE` requirements have no implementation tasks.
- [ ] `UNTESTED` requirements create only test coverage tasks.
- [ ] `PARTIAL` requirements create only gap-closing tasks.
- [ ] Requirement IDs are stable and bound to source requirements.
- [ ] Full Requirement Matrix and MVP Coverage Matrix are separate.
- [ ] Full platform scope vs MVP boundary is explained.
- [ ] Every `REQ-xxx` has coverage status: `TASK`, `MERGED`, `BASELINE`, `OUT_OF_SCOPE`, or `BLOCKED`.
- [ ] Every `MERGED` requirement names target child task and covering AC.
- [ ] Every `BASELINE` requirement has code/test evidence.
- [ ] Every `OUT_OF_SCOPE` requirement is in Backlog with reason, recommended stage, recovery conditions, and dependencies.
- [ ] Task merge/split record is complete.
- [ ] Subtask Planning Ledger covers every MVP Coverage Matrix `TASK`.
- [ ] Batch Completion Rollup lists B01/B02/... Task IDs, dependency layers, parallel groups, and batch goals.
- [ ] All MVP child tasks are `READY_TO_CONFIRM`, `BLOCKED`, or `OUT_OF_SCOPE`; planning is not P0/P1 only.
- [ ] No `UNASSIGNED_MVP_REQ`, `UNBATCHED_TASK`, `P0P1_ONLY_PLAN`, or `DEFERRED_PRD_WITHOUT_PLAN`.
- [ ] User confirmed the complete MVP task tree, all batches, Backlog boundary, Blocked items, and creation scope.
- [ ] Each child task has acceptance criteria, test requirements, and explicit dependencies.
- [ ] Trellis task dependencies and existing baseline dependencies are separate.
- [ ] Logical planning IDs (`T01`, `REQ-001`) are distinct from real `task.py create` directories.
- [ ] Every child task has complexity; high complexity is split or requires design/implement artifacts.
- [ ] Small Model Mode granularity is satisfied or explicitly blocked for user confirmation.
- [ ] Sub-agent planning was used or serially simulated when trigger conditions apply.
- [ ] Every child PRD has no unresolved `<...>`, `{Entity}`, `TBD`, `depends`, or external config placeholders.
- [ ] Every child PRD includes Project Contract Reference, behavior constraints, acceptance criteria, dependencies, and implementation plan location.
- [ ] In Trellis 0.6+ projects, detailed file plan, ordered steps, and self-check commands are in `implement.md`; only low-complexity PRD-only tasks use PRD compact appendix.
- [ ] Planning artifact matrix lists `prd.md`, `design.md`, `implement.md`, `implement.jsonl`, `check.jsonl`, `jsonl_mode`, and reasons for every child task.
- [ ] Medium/high complexity tasks include or require `design.md` and `implement.md`.
- [ ] High complexity tasks are not PRD-only.
- [ ] `implement.jsonl` / `check.jsonl` are not seed-only; for `optional/inline`, seeds are deleted or matrix marks `NOT_NEEDED_WITH_REASON`.
- [ ] Parent PRD coverage counts come from mechanical MVP Coverage Matrix statistics.
- [ ] Stage State Packet counts match matrices and ledger.

## Commands

```bash
python ./.trellis/scripts/task.py create "<parent title>" --slug <parent-slug>
python ./.trellis/scripts/task.py create "<child title>" --slug <child-slug> --parent "<parent-task-dir>"
```

Record every `task.py create` stdout path and use it as the only trusted artifact path.

If `task.py create` reports no developer is set, stop and ask the user to initialize Trellis:

```bash
trellis init -u <name>
```

Include project platform flags when appropriate, such as `--codex`.

Use legacy fallback only when Trellis CLI is unavailable:

```bash
python ./.trellis/scripts/init_developer.py <name>
```

or ask the user for an assignee to pass with `--assignee`.

## After Creating Tasks

- [ ] Every created task directory contains `task.json`.
- [ ] Subtask Planning Ledger is backfilled with real directories.
- [ ] Parent `prd.md` is written to the real parent directory.
- [ ] Every child `prd.md` is written to the real child directory.
- [ ] No side directory without `task.json` holds a complete PRD.
- [ ] Required `design.md`, `implement.md`, `implement.jsonl`, and `check.jsonl` are written according to artifact matrix.
- [ ] No `prd.md` says an artifact is required while the real directory lacks it.
- [ ] No high-complexity PRD-only task remains.
- [ ] `python ./.trellis/scripts/task.py list` shows the parent/child relationship.
- [ ] New artifacts contain no unresolved placeholders.
- [ ] JSONL seed scan has no blocking seeds, or `jsonl_mode=inline/optional` raw seeds are explained.
- [ ] Contract forbidden-token scan is clean.
- [ ] `design.md` / `implement.md` semantic anchors match corresponding PRD.
- [ ] Project Contract Check confirms names, paths, APIs, commands, packages/modules, routes, tables, and permission models match parent Contract Lock.
- [ ] Small Model Grain Check still passes.
- [ ] External config scan is clean or values are `FIXED`, `BASELINE`, `BLOCKED`, or `OUT_OF_SCOPE`.
- [ ] Deterministic Gate script is run and its JSON is the only Artifact Gate evidence:

```bash
python <skill-dir>/scripts/trellis_zero_gate.py \
  --tasks .trellis/tasks \
  --parent-task-json <parent-task-dir>/task.json \
  --parent-prd <parent-task-dir>/prd.md \
  --jsonl-mode <required|optional|inline>
```

- [ ] Add `--forbidden-token`, `--forbidden-regex`, or `--contract-mismatch-regex` as required by Contract Snapshot.
- [ ] Artifact Gate output includes `scanned_tasks`, `jsonl_mode`, `placeholder_hits`, `angle_placeholder_hits`, `jsonl_seed_hits`, `forbidden_token_hits`, `contract_mismatch_hits`, `coverage_count_mismatch_hits`, `high_complexity_missing_artifacts`, `missing_declared_artifacts`, `declared_gate_mismatch_hits`, `external_config_hits`, and `result`.
- [ ] Parent PRD declared Gate counts match script output.
- [ ] If Artifact Gate is `FAIL` or `PENDING`, do not claim the task tree is executable.
- [ ] Only when Development Recommendation Gate is `PASS`, output the first recommended task.
- [ ] Output task tree, dependency-ordered plan, blocked tasks, and parallelizable tasks.
- [ ] Do not start implementation.
