---
name: trellis-mvp-to-delivery
description: Audit an existing MVP against a source requirements document and run a sustainable Trellis delivery loop. Use when Codex is asked to continue after an MVP, complete remaining requirements, perform a first full gap audit, maintain a Requirements Traceability Matrix, classify DONE/PARTIAL/MISSING/UNTESTED/UNCLEAR items, initialize or update .trellis/delivery-state.md, choose full/delta/early-exit audit scope, plan bounded gap-closing batches, require worktree + verifier gates, design automated test coverage, classify discovered bugs, or run final acceptance before delivery.
---

# Trellis MVP to Delivery

## Overview

Move an existing MVP toward complete delivery by returning to the source requirements, auditing evidence, maintaining a delivery state file, planning bounded gap-closing batches, and driving final acceptance. The first pass is always read-only and must produce a full requirements-vs-MVP gap matrix; later passes may use delta audit or early-exit when nothing relevant changed.

## Guardrails

- Do not "just continue development" after MVP. Audit requirements first.
- Do not mark a requirement `DONE` without implementation evidence and test evidence.
- Do not create delivery tasks until the user confirms the gap audit.
- Do not mix unrelated gaps into one task.
- Size tasks to the execution model's capability: if the execution phase may use a capability-limited local model (e.g. offline qwen), split finer and annotate complexity.
- A delivery task PRD is an execution spec the execution model copies from. During planning, replace every `<...>` placeholder with a concrete value (exact file paths, copyable existing examples, ordered implementation steps, machine-checkable acceptance assertions, self-check commands). Never leave reasoning — including which branch a bug fix takes — to the execution phase.
- For Trellis 0.6 beta projects, treat `.trellis/workflow.md` as the active local workflow contract when present. Preserve and extend `design.md`, `implement.md`, `implement.jsonl`, and `check.jsonl` artifacts if existing tasks use them.
- Do not put all testing into a final catch-all task. Each feature task must include its own basic tests.
- Create a final validation task only after functional gap tasks are planned.
- If a bug does not block the current requirement acceptance, classify it and create or propose a separate bug task.
- Treat this skill as the delivery controller, not the implementer. Implementation belongs to `trellis-implement-tdd`; debugging belongs to `trellis-debug-systematic`; completion review belongs to `trellis-review-twostage`.
- For L2/L3 gap-closing work, every implementation task must require an isolated worktree and verifier/review gate. Never let the implementer mark its own task complete.
- Keep `.trellis/delivery-state.md` and `.trellis/delivery-run-log.jsonl` current when running as a repeated delivery loop.
- Early-exit when there are no relevant changes since `last_audited_commit`; do not burn a full audit on a no-op run.

## Workflow

### 0. Load Delivery Loop State

Load `references/delivery-loop-policy.md`.

If `.trellis/delivery-state.md` exists, read it before auditing. If it is missing, this is the first run:

1. Load `references/delivery-loop-state-template.md`.
2. Plan to initialize `.trellis/delivery-state.md` after the full gap audit.
3. Default `loop_mode` to `L1`.
4. Treat the current commit as the MVP baseline unless the user provides a different baseline.

If `.trellis/delivery-run-log.jsonl` is missing, load `references/delivery-run-log-template.md` and plan to create it at the end of the run.

### 1. Decide Loop Mode and Audit Scope

Use `references/delivery-loop-policy.md` to choose:

- Loop mode: `L1` audit-only, `L2` assisted delivery, or `L3` controlled continuous loop.
- Audit scope: `full`, `delta`, or `early-exit`.

Rules:

- First run after MVP is always `L1 + full audit`.
- A full audit must compare source requirements against the MVP and output a complete Requirements Traceability Matrix.
- Delta audit is allowed only when delivery state exists and source requirements have not changed.
- Early-exit when no relevant requirement evidence, task status, code, or test files changed since `last_audited_commit`; append a run-log entry and stop.
- Stop and ask the user if `current_round` exceeds `max_rounds`, a requirement carried over too many rounds, a verifier failed twice, or any critical review issue exists.

### 2. Discover Evidence

Locate and read:

- Source requirements document.
- Existing MVP code and tests.
- Existing `.trellis/tasks/`, especially completed or active tasks.
- Existing requirement IDs, traceability matrices, and acceptance notes if present.
- Existing `.trellis/delivery-state.md` and `.trellis/delivery-run-log.jsonl` if present.
- Relevant `.trellis/spec/` indexes for affected packages.
- Trellis 0.6 beta workflow metadata when present: `.trellis/workflow.md`, `.trellis/config.yaml`, `.trellis/.version`, `.trellis/.developer`, and `.trellis/workspace/`.

Before planning gap-closing work, check whether `.trellis/spec/` and existing task artifacts are fresh enough to explain current behavior. If they are stale or too generic, add a spec-refresh/bootstrap or artifact-refresh task before implementation tasks.

Use local evidence before asking questions. Ask only blocking questions that cannot be resolved from the requirements or repository.

### 3. Perform Gap Audit (Enhanced - Self-Review Loop)

Loop through the following steps until small model execution standards are met:

#### Round N Audit

**3.1 Generate Gap Audit Output**

Load `references/gap-audit-template.md` and produce:

- Requirements Traceability Matrix.
- MVP completion summary.
- Blocking questions.
- Dependency-ordered task plan.
- Recommended priorities.
- Automated test requirements.
- For medium/high complexity gap-closing tasks, draft shift-left design, implementation-plan, and context-manifest artifacts using `references/planning-artifacts-template.md`: `design.md`, `implement.md`, `implement.jsonl`, and `check.jsonl` when the project workflow supports them.

Use only these statuses: `DONE`, `PARTIAL`, `MISSING`, `UNTESTED`, `UNCLEAR`.

On first run, the Requirements Traceability Matrix is the baseline for future delivery loop runs and must include every source requirement, even if no task is created yet.

**3.2 Self-Review**

Load `references/self-review-checklist.md` and check audit output quality against the checklist item by item.

Use `references/self-review-report-template.md` to generate review report including:
- Overall score (8 dimensions)
- Checklist pass status
- Issue list (location, description, impact, improvement suggestion)
- MVP compatibility check
- Statistics
- Conclusion for this round

**3.3 Determine if Standards Met**

- ✅ All check items pass → proceed to Step 4 (Update Delivery State)
- ✅ 2 consecutive rounds with no new issues → auto-pass, proceed to Step 4
- ❌ Has failed check items → proceed to Step 3.4 (Targeted Improvements)
- ⚠️ Still has issues after 5 rounds → prompt user to choose:
  - Option A: Use stronger model to re-audit
  - Option B: Manual review of current audit
  - Option C: Accept current version (at own risk)

**3.4 Targeted Improvements**

Based on issue list in review report, make targeted improvements:
- Only modify parts marked as issues, do not re-audit entire MVP
- Keep passed parts unchanged
- Pay special attention to MVP compatibility (don't break existing behavior)
- After completing improvements, return to Step 2.1 for Round N+1 review

**Review Loop Principles**:
- Converge iteratively, do not redo everything
- Issue location must be precise (to specific REQ-xxx, Task ID, PRD section)
- Improvements must be targeted (fix issues, don't introduce new ones)
- Emphasize MVP compatibility (all gap-closing tasks must not break MVP behavior)

### 4. Update Delivery State

Update or initialize `.trellis/delivery-state.md` from `references/delivery-loop-state-template.md`:

- Record `source_requirements`, `mvp_baseline_commit`, `last_audited_commit`, `loop_mode`, `current_round`, and `max_rounds`.
- Write the current status of every `REQ-*`.
- Preserve human decisions and blockers from prior runs.
- Increment carry-over count when a requirement remains open without progress.
- Mark requirements that must pause because carry-over count exceeded policy.
- Set `Next Loop Recommendation` to one of: `continue-next-batch`, `early-exit`, `pause-human-needed`, `run-final-acceptance`, or `rebaseline-required`.

### 5. Select Delivery Batch

Load `references/delivery-batch-template.md` and plan exactly one batch for this run.

Batch rules:

- L1 may recommend a batch but must not create tasks without confirmation.
- L2/L3 may create or update only the confirmed/current batch.
- Max gap tasks per run: 3.
- Max high-risk tasks per run: 1.
- Do not mix foundation contracts, business behavior, UI, tests, and final validation when their dependencies differ.
- Final acceptance is its own batch and only after P0/P1 gaps are DONE or explicitly deferred by a human.
- Any critical review issue, repeated verifier failure, or same REQ reopened twice stops the loop.

### 6. Confirm Delivery Plan

Ask for one confirmation before creating or modifying Trellis tasks:

```text
Confirm this gap audit, delivery state update, and selected batch? If yes, I will create or update Trellis tasks and PRDs for this batch without implementing features yet.
```

If the user changes priorities or scope, revise the matrix and task plan before creating tasks.

### 7. Create or Update Gap-closing Tasks

After confirmation:

1. Create or reuse a parent task for complete requirements and validation.
2. Create one child task per tightly related gap group.
3. Use `references/delivery-task-prd-template.md` for child PRDs.
4. Separate foundation contracts, business behavior, UI, tests, and final validation when they have different dependencies.
5. For medium/high complexity child tasks, write or draft `design.md`, `implement.md`, `implement.jsonl`, and `check.jsonl` when `.trellis/workflow.md` or existing tasks show those artifacts are expected. Do not overwrite existing artifacts without reading them first.
6. Add delivery loop controls to every PRD: worktree required, verifier required, implementation skill, debug skill, review skill, human gate, max fix attempts, rollback trigger.
7. Do not start coding.

### 8. Record Run Log

Load `references/delivery-run-log-template.md` and append one JSON object to `.trellis/delivery-run-log.jsonl`.

Record:

- run id, loop mode, round, audit scope, baseline commit, head commit
- requirements changed, open gaps, tasks created/updated/completed
- critical review issues, debug escalations, carry-over requirements
- estimated tokens, outcome, and next action

Do this for full audit, delta audit, task-creation, pause, final-acceptance-ready, and early-exit runs.

### 9. Plan Test Closure

Load `references/test-coverage-matrix-template.md` when asked to plan or fill test coverage. Map every `REQ-*` or `AC-*` to at least one unit, integration, e2e, smoke, regression, or manual verification entry.

### 10. Run Final Acceptance

Load `references/final-acceptance-template.md` when all functional tasks are complete. Do not add features during final acceptance unless a blocking bug prevents acceptance.

### 11. Classify Bugs

Load `references/bug-classification-rules.md` when validation discovers a bug. Decide whether to fix in the current task, create a separate bug task, or defer with a documented risk.

## Execution-phase Handoff (after gap tasks are created)

This skill audits, controls batches, and plans gap-closing tasks; it does not write application code. When moving into implementation, run each gap-closing child task through the execution-phase skills in dependency order, especially when the executor is a small model such as qwen3.6 35b:

1. **`trellis-implement-tdd`** - run RED-GREEN-REFACTOR per AC and protect the MVP compatibility contract with regression tests.
2. **`trellis-debug-systematic`** - when a test should be green but stays red, or a self-check fails, use the rigid debugging script.
3. **`trellis-review-twostage`** - before completion, run spec compliance (small model ok) plus code quality review (strong model recommended).

Role-layered model assignment: use a strong model for planning, a small model for mechanical implementation, and a strong model for review Stage 2 when available.

## References

- `references/delivery-loop-policy.md` - read before each repeated delivery run to choose loop mode, full/delta/early-exit audit scope, batch limits, and stop conditions.
- `references/delivery-loop-state-template.md` - read when initializing or updating `.trellis/delivery-state.md`.
- `references/delivery-batch-template.md` - read when selecting the one gap-closing batch for a run.
- `references/delivery-run-log-template.md` - read when appending `.trellis/delivery-run-log.jsonl`.
- `references/gap-audit-template.md` - read for the full or delta MVP gap audit.
- `references/self-review-checklist.md` - read for self-review after each audit round.
- `references/self-review-report-template.md` - read when generating review reports.
- `references/planning-artifacts-template.md` - read when drafting Trellis 0.6 beta design, implementation, and context manifest artifacts for medium/high complexity tasks.
- `references/delivery-task-prd-template.md` - read before creating gap-closing task PRDs.
- `references/test-coverage-matrix-template.md` - read when planning or adding test coverage.
- `references/final-acceptance-template.md` - read for final delivery acceptance.
- `references/bug-classification-rules.md` - read when validation finds defects.
