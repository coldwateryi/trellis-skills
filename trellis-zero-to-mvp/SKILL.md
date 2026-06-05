---
name: trellis-zero-to-mvp
description: Create a Trellis MVP task tree from a full requirements document. Use when Codex receives a product brief, requirements document, PRD, or large feature request for a new project or major capability and needs to do read-only analysis, assign stable REQ/AC IDs, build a traceability matrix, split scope into parent and child Trellis tasks, draft PRDs, and plan dependency-ordered MVP delivery before any coding starts.
---

# Trellis Zero to MVP

## Overview

Turn a raw requirements document into an MVP-sized Trellis delivery plan. The output is a confirmed parent task plus independently verifiable child tasks, not application code.

## Guardrails

- Do not write business code.
- Do not create Trellis tasks until the user confirms the read-only analysis.
- Do not split tasks by files. Split by independently verifiable business or technical capability.
- Size tasks to the execution model's capability: if the execution phase may use a capability-limited local model (e.g. offline qwen), split finer — one child task per entity's CRUD set or per endpoint — and annotate complexity.
- Assign stable requirement IDs before task planning: `REQ-001`, `REQ-002`, `AC-001`.
- Every child task must include requirement IDs, acceptance criteria, tests, dependencies, unlocks, out-of-scope items, and technical notes.
- A PRD is an execution spec the execution model copies from, not an intent description. During planning, replace every `<...>` placeholder with a concrete value (exact file paths, copyable existing examples, ordered implementation steps, machine-checkable acceptance assertions, self-check commands). Never leave reasoning to the execution phase.
- Every decision requiring reasoning (which annotation, which branch, naming, table schema, which example to copy) must be pinned down during planning. Points that cannot be pinned go to out-of-scope or a separate task, never to the execution model's discretion.
- Treat Trellis parent/child links as task structure only. Write strict dependencies in each child `prd.md`.
- If `task.py create` fails because the developer identity is not initialized, stop and tell the user to run `python ./.trellis/scripts/init_developer.py <name>` or provide an explicit assignee.

## Workflow

### 1. Discover Inputs

Locate and read:

- The source requirements document.
- README or project overview files.
- Existing code structure and tests, if the repo is not empty.
- Existing `.trellis/tasks/` and `.trellis/spec/` material relevant to the project.

Use repository inspection before asking the user questions. Ask only blocking questions that cannot be answered from local context.

### 2. Perform Read-only Analysis (Enhanced - Self-Review Loop)

Loop through the following steps until small model execution standards are met:

#### Round N Analysis

**2.1 Generate Analysis Output**

Load `references/analysis-output-template.md` and produce:

- Project goal summary.
- Requirements Traceability Matrix.
- Module dependency graph.
- Task split by capability.
- Recommended dependency-ordered MVP development sequence.
- Draft parent PRD.
- Draft child PRDs.

Use these statuses in the traceability matrix: `DONE`, `PARTIAL`, `MISSING`, `UNTESTED`, `UNCLEAR`.

**2.2 Self-Review**

Load `references/self-review-checklist.md` and check analysis output quality against the checklist item by item.

Use `references/self-review-report-template.md` to generate review report including:
- Overall score (5 dimensions)
- Checklist pass status
- Issue list (location, description, impact, improvement suggestion)
- Statistics
- Conclusion for this round

**2.3 Determine if Standards Met**

- ✅ All check items pass → proceed to Step 3 (Confirm Scope)
- ✅ 2 consecutive rounds with no new issues → auto-pass, proceed to Step 3
- ❌ Has failed check items → proceed to Step 2.4 (Targeted Improvements)
- ⚠️ Still has issues after 5 rounds → prompt user to choose:
  - Option A: Use stronger model to re-analyze
  - Option B: Manual review of current analysis
  - Option C: Accept current version (at own risk)

**2.4 Targeted Improvements**

Based on issue list in review report, make targeted improvements:
- Only modify parts marked as issues, do not re-analyze entire requirements document
- Keep passed parts unchanged
- After completing improvements, return to Step 2.1 for Round N+1 review

**Review Loop Principles**:
- Converge iteratively, do not redo everything
- Issue location must be precise (to specific REQ-xxx, Task ID, PRD section)
- Improvements must be targeted (fix issues, don't introduce new ones)

### 3. Confirm Scope

Present the analysis and ask for one confirmation before creating files:

```text
Confirm this task split and MVP boundary? If yes, I will create the Trellis parent task, child tasks, and PRDs without writing application code.
```

If the user changes scope, update the analysis first. Do not create tasks from stale assumptions.

### 4. Create Trellis Task Tree

After confirmation:

1. Create one parent task for the overall project.
2. Create child tasks with `--parent <parent-task-dir>`.
3. Write the parent `prd.md` using `references/parent-prd-template.md`.
4. Write each child `prd.md` using `references/child-prd-template.md`.
5. Preserve requirement IDs and dependencies exactly.
6. Do not start implementation.

Use:

```bash
python ./.trellis/scripts/task.py create "<parent title>" --slug <parent-slug>
python ./.trellis/scripts/task.py create "<child title>" --slug <child-slug> --parent "<parent-task-dir>"
```

### 5. Report Next Actions

Output:

- Task tree.
- Recommended execution order.
- Blocked tasks.
- Parallelizable tasks.
- First task to start and why.

## References

- `references/analysis-output-template.md` - read before producing the initial audit.
- `references/self-review-checklist.md` - read for self-review after each analysis round.
- `references/self-review-report-template.md` - read when generating review reports.
- `references/parent-prd-template.md` - read when drafting or writing the parent task PRD.
- `references/child-prd-template.md` - read when drafting or writing child task PRDs.
- `references/task-creation-checklist.md` - read before creating the task tree.
