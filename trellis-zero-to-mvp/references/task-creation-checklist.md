# Task Creation Checklist

Use this after the user confirms the complete read-only plan.

## Before Creating Tasks

- [ ] Source requirements document path is known.
- [ ] `.trellis/workflow.md` was read if present; `.trellis/config.yaml`, `.trellis/.version`, `.trellis/.developer` were checked if present.
- [ ] `.trellis/config.yaml` `codex.dispatch_mode` was read; `inline` uses `jsonl_mode=inline`, sub-agent or JSONL-required contexts use `jsonl_mode=required`.
- [ ] Relevant `.trellis/spec/` files are fresh enough, or a spec-refresh/bootstrap task is planned before implementation tasks.
- [ ] Project Contract Profile is selected with evidence and rejected-profile reasons.
- [ ] Project Contract Lock exists; applicable profile fields have adopted values and evidence paths; non-applicable fields are `not-applicable`.
- [ ] RuoYi/Java fields were not applied to CLI, SDK, frontend, Python service, or custom framework projects.
- [ ] Any `CONTRACT_CONFLICT` was confirmed by the user before task creation.
- [ ] Contract Snapshot and forbidden tokens exist; child task candidates have been scanned and fixed against forbidden tokens.
- [ ] Child task candidates follow Project Contract Lock and do not mix naming systems, table prefixes, routes, or package paths.
- [ ] Existing Implementation Baseline is complete when the repo already has manual implementation.
- [ ] `DONE` requirements have no implementation child tasks.
- [ ] `UNTESTED` requirements create only test coverage tasks.
- [ ] `PARTIAL` requirements create only gap-closing tasks for missing behavior.
- [ ] Requirement IDs are stable.
- [ ] `REQ-xxx` binds source requirement behavior and does not change meaning when tasks merge, split, or reorder.
- [ ] Source requirement list is complete and every point has `REQ-xxx`.
- [ ] Full Requirement Matrix and MVP Coverage Matrix are separate; MVP coverage count is not reported as original source requirement count.
- [ ] Full platform scope vs current MVP boundary is explained.
- [ ] Every `REQ-xxx` has coverage status: `TASK`, `MERGED`, `BASELINE`, `OUT_OF_SCOPE`, or `BLOCKED`.
- [ ] Every `MERGED` requirement names target child task and covering AC.
- [ ] Every `BASELINE` requirement has existing implementation evidence.
- [ ] Every `OUT_OF_SCOPE` requirement has an exclusion reason and will be shown during confirmation.
- [ ] Every `OUT_OF_SCOPE` requirement is in Backlog with recommended stage, recovery conditions, and MVP dependencies.
- [ ] Task merge/split record is complete and task-count changes have reasons.
- [ ] MVP boundary is clear.
- [ ] Subtask Planning Ledger covers every MVP Coverage Matrix `TASK`.
- [ ] Batch Completion Rollup lists B01/B02/... Task IDs, dependency layers, parallel groups, and batch goals.
- [ ] All MVP child tasks are `READY_TO_CONFIRM`, `BLOCKED`, or `OUT_OF_SCOPE`; planning is not P0/P1 only.
- [ ] No `UNASSIGNED_MVP_REQ`, `UNBATCHED_TASK`, `P0P1_ONLY_PLAN`, or `DEFERRED_PRD_WITHOUT_PLAN`.
- [ ] User confirmed the complete MVP task tree, all batch plans, Backlog boundary, Blocked items, and creation scope.
- [ ] Each child task has acceptance criteria.
- [ ] Each child task has test requirements.
- [ ] Dependencies are explicit.
- [ ] Trellis task dependencies and existing baseline dependencies are separate.
- [ ] Logical planning IDs such as `T01`, `REQ-001`, and `<child-slug>` are distinct from real Trellis task directories returned by `task.py create`.
- [ ] Every child task has complexity; high-complexity tasks are split smaller or every step is pinned.
- [ ] Small Model Mode: each child task covers only one entity CRUD, one endpoint group, one state transition, one frontend page, or one backend aggregate query.
- [ ] Small Model Mode: no child task combines multiple primary entities, multiple CRUD sets, CRUD + state machine + report, backend flow + mini-app page, map/GIS + multi-table aggregation + advanced analytics.
- [ ] Small Model Mode: no oversized task is exempted by model reasoning about coupling; retained merges have explicit user confirmation.
- [ ] Small Model Mode: max 8 executable child tasks and max 5 full high-quality PRDs per batch; if exceeded, all batches are indexed, not only P0/P1.
- [ ] If using a small model and expected child tasks exceed 15, batch planning is used; non-first-batch MVP tasks still have title, REQ coverage, dependencies, complexity, artifact needs, and expected batch.
- [ ] If sub-agents are available, batch/domain Agent Packets were dispatched; otherwise `agent_mode: unavailable_fallback_serial` is recorded.
- [ ] Every child PRD has no unresolved `<...>` placeholders or `TBD/as needed` expressions.
- [ ] Every child PRD has no `{Entity}`, `{domain}`, `{entity}`, `<PageComponent>`, or similar template residue.
- [ ] Every child PRD has no `YOUR_KEY`, `API_KEY_HERE`, or unresolved external config; external config is `FIXED`, `BASELINE`, `BLOCKED`, or `OUT_OF_SCOPE`.
- [ ] Every child task title, business domain, primary entity, table name, route, and file list are consistent; references to other tasks list dependencies or baseline reason.
- [ ] Every child task has Project Contract Reference or equivalent contract reference that matches parent Project Contract Lock.
- [ ] Every child PRD has reference implementation paths, behavior constraints, acceptance criteria, dependencies, Project Contract Reference, and implementation plan location.
- [ ] Every child PRD has a `Task Impact Matrix`, and impact decisions match task type, semantic anchors, and file plan.
- [ ] If any impact surface is `yes`, the corresponding `design.md` section and `implement.md` plan section are prepared.
- [ ] In Trellis 0.6+ projects, detailed file plan, ordered steps, and self-check commands are in `implement.md`; only low-complexity PRD-only tasks with local workflow evidence use PRD compact appendix.
- [ ] Planning Artifact Matrix lists `prd.md`, `design.md`, `implement.md`, `implement.jsonl`, `check.jsonl`, `jsonl_mode`, and reasons for each child task.
- [ ] Medium/high complexity child tasks include or require `design.md`, `implement.md`, `implement.jsonl`, and `check.jsonl` according to workflow and risk.
- [ ] High complexity tasks are not PRD-only; if still high complexity, they require `design.md` + `implement.md`, otherwise they are split smaller and complexity is updated.
- [ ] If workflow requires `design.md` for medium/high tasks, `implement.md` is also prepared or a clear not-needed reason exists.
- [ ] `implement.jsonl` / `check.jsonl`, if present, are not seed-only; for `jsonl_mode=optional/inline`, seed files are deleted or marked `NOT_NEEDED_WITH_REASON` in the artifact matrix.
- [ ] Tasks involving database, API, UI, permission, dictionary, state, validation, transaction, external interface, or test strategy do not miss matching design-surface sections.
- [ ] Acceptance criteria are machine-checkable or individually tickable assertions.
- [ ] Parent PRD coverage counts come from mechanical MVP Coverage Matrix statistics.
- [ ] Small-model or long complex tasks output Stage State Packet; state packet counts match matrices and ledger.

## Commands

```bash
python ./.trellis/scripts/task.py create "<parent title>" --slug <parent-slug>
python ./.trellis/scripts/task.py create "<child title>" --slug <child-slug> --parent "<parent-task-dir>"
```

Record every `task.py create` stdout path and use it as the only trusted artifact path. Do not construct directories from slug, date, or Task ID.

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
- [ ] Subtask Planning Ledger is backfilled with real directories from `task.py create` output.
- [ ] Parent `prd.md` is written to the real parent directory.
- [ ] Every child `prd.md` is written to the real child directory.
- [ ] No complete PRD is written into side directories such as `.trellis/tasks/<logical-task-id>/` or `.trellis/tasks/tXX-*/` without `task.json`.
- [ ] No `<task-dir>/prd/` subdirectory is used as PRD container; PRD path is `<task-dir>/prd.md`.
- [ ] Required `design.md`, `implement.md`, `implement.jsonl`, and `check.jsonl` are written according to artifact matrix and live in the same real task directory.
- [ ] No `prd.md` says an artifact is required while the real directory lacks it.
- [ ] No high-complexity PRD-only task remains; if no extra artifact exists, task has been split and parent merge/split record explains it.
- [ ] `python ./.trellis/scripts/task.py list` shows the parent and all child tasks with correct parent/child relationship.
- [ ] New parent/child `prd.md` files contain no `TBD`, `<...>`, `to be provided`, or `as needed`.
- [ ] Placeholder scan is empty:

```bash
rg -n '\{Entity\}|\{domain\}|\{entity\}|<PageComponent>|<Task Title>|<path>|TBD|to be provided|as needed|depending on situation' .trellis/tasks/*/*.md
```

- [ ] Generic angle placeholder scan is empty or every hit has an explicit non-placeholder explanation:

```bash
rg -n '<[A-Za-z0-9_.:/ -]+>' .trellis/tasks/*/*.{md,jsonl}
```

- [ ] JSONL seed scan is clean; if it hits, new-task JSONL is filled with real context or explained as not needed:

```bash
rg -n '"_example"' .trellis/tasks/*/*.jsonl
```

- [ ] Contract forbidden-token scan is clean. Replace `<forbidden-token-regex>` with the regex generated from Contract Snapshot:

```bash
rg -n '<forbidden-token-regex>' .trellis/tasks/*/*.{md,jsonl}
```

- [ ] Spot-check every `design.md` / `implement.md`: title, semantic anchors, file plan, routes/APIs/commands/tables/state objects match the corresponding `prd.md` and do not copy another task.
- [ ] Project Contract Check passes: names, paths, APIs, commands, packages/modules, routes, tables, and permission models match parent Project Contract Lock.
- [ ] Design Surface Check passes: every PRD impact surface marked `yes` has matching sections in both `design.md` and `implement.md`.
- [ ] Small Model Grain Check passes; if a new task violates one-entity/interface/state/page/query granularity, split or block.
- [ ] External config scan is clean or values are `FIXED`, `BASELINE`, `BLOCKED`, or `OUT_OF_SCOPE`:

```bash
rg -n 'YOUR_KEY|API_KEY_HERE|to be provided|pending config|placeholder key' .trellis/tasks/*/*.{md,jsonl}
```

- [ ] Output Artifact Gate result: `scanned_tasks`, `placeholder_hits`, `jsonl_seed_hits`, `forbidden_token_hits`, `contract_mismatch_hits`, `coverage_count_mismatch_hits`, `high_complexity_missing_artifacts`, `missing_declared_artifacts`, `design_surface_prd_without_matrix`, `design_surface_missing_hits`, `external_config_hits`, `result: PASS/FAIL`.
- [ ] Run deterministic Gate script and use its JSON as the only Artifact Gate evidence:

```bash
python <skill-dir>/scripts/trellis_zero_gate.py \
  --tasks .trellis/tasks \
  --parent-task-json <parent-task-dir>/task.json \
  --parent-prd <parent-task-dir>/prd.md \
  --jsonl-mode <required|optional|inline>
```

- [ ] Add `--forbidden-token` or `--forbidden-regex` if Contract Snapshot defines forbidden tokens.
- [ ] Output Artifact Gate result: `scanned_tasks`, `placeholder_hits`, `angle_placeholder_hits`, `jsonl_seed_hits`, `forbidden_token_hits`, `contract_mismatch_hits`, `coverage_count_mismatch_hits`, `high_complexity_missing_artifacts`, `missing_declared_artifacts`, `design_surface_prd_without_matrix`, `design_surface_missing_hits`, `declared_gate_mismatch_hits`, `external_config_hits`, `result: PASS/FAIL`.
- [ ] Parent PRD declared Gate values match script output; if not, use script output and failure code `DECLARED_GATE_MISMATCH`.
- [ ] If Artifact Gate is `FAIL` or `PENDING`, do not claim the task tree is executable; fix or explicitly block.
- [ ] Created task statuses are updated to `CREATED`, `ARTIFACTS_WRITTEN`, `GATED_PASS`, or `BLOCKED`.
- [ ] If any current MVP child remains uncreated, unwritten, or not Gate-passed, final report uses `BATCH_INCOMPLETE` and does not recommend development.
- [ ] Only when Development Recommendation Gate is `PASS`, output the first recommended task.
- [ ] Output task tree.
- [ ] Output dependency-ordered plan.
- [ ] Output blocked tasks.
- [ ] Output parallelizable tasks.
- [ ] Do not start implementation.
