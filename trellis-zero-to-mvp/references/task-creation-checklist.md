# Task Creation Checklist

Use this checklist after the user confirms the read-only analysis.

## Before Creating Tasks

- [ ] The source requirements document path is known.
- [ ] `.trellis/workflow.md` was read if present; `.trellis/config.yaml`, `.trellis/.version`, and `.trellis/.developer` were checked if present.
- [ ] Relevant `.trellis/spec/` files are fresh enough, or a spec-refresh/bootstrap task is planned before implementation work.
- [ ] Requirement IDs are stable.
- [ ] MVP boundary is explicit.
- [ ] Task split is confirmed by the user.
- [ ] Every child task has acceptance criteria.
- [ ] Every child task has required tests.
- [ ] Dependencies are explicit.
- [ ] Every child task is annotated with complexity (low/medium/high); high-complexity tasks are split further or have every step pinned down in the PRD.
- [ ] Every `<...>` placeholder in each child PRD is replaced with a concrete value; no "TBD / depends".
- [ ] Each child PRD includes reference implementation paths, a file manifest, ordered implementation steps, and self-check commands.
- [ ] Medium/high complexity child tasks include or explicitly require `design.md`, `implement.md`, `implement.jsonl`, and `check.jsonl` according to project workflow and risk.
- [ ] Acceptance criteria are written as machine-checkable or individually tickable assertions.

## Commands

```bash
python ./.trellis/scripts/task.py create "<parent title>" --slug <parent-slug>
python ./.trellis/scripts/task.py create "<child title>" --slug <child-slug> --parent "<parent-task-dir>"
```

If `task.py create` reports that no developer is set, stop and ask the user to initialize Trellis with:

```bash
trellis init -u <name>
```

Include the platform flag used by the project when appropriate, such as `--codex`.

Use the legacy fallback only when the Trellis CLI is unavailable:

```bash
python ./.trellis/scripts/init_developer.py <name>
```

or to provide the assignee that should be used with `--assignee`.

## After Creating Tasks

- [ ] Write parent `prd.md`.
- [ ] Write each child `prd.md`.
- [ ] Write or draft `design.md`, `implement.md`, `implement.jsonl`, and `check.jsonl` for child tasks whose complexity/risk requires them and whose workflow supports them.
- [ ] Output task tree.
- [ ] Output dependency-ordered execution plan.
- [ ] Output blocked task list.
- [ ] Output parallelizable task list.
- [ ] Do not start implementation.
