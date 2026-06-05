---
name: trellis-mvp-to-delivery
description: Audit an existing MVP against a source requirements document and plan final Trellis delivery. Use when Codex is asked to continue after an MVP, complete remaining requirements, perform a gap audit, create Requirements Traceability Matrix entries, classify DONE/PARTIAL/MISSING/UNTESTED/UNCLEAR items, plan gap-closing Trellis tasks, design automated test coverage, classify discovered bugs, or run final acceptance before delivery.
---

# Trellis MVP to Delivery

## Overview

Move an existing MVP toward complete delivery by returning to the source requirements, auditing evidence, creating gap-closing tasks, and planning final acceptance. The first pass is always read-only.

## Guardrails

- Do not "just continue development" after MVP. Audit requirements first.
- Do not mark a requirement `DONE` without implementation evidence and test evidence.
- Do not create delivery tasks until the user confirms the gap audit.
- Do not mix unrelated gaps into one task.
- Size tasks to the execution model's capability: if the execution phase may use a capability-limited local model (e.g. offline qwen), split finer and annotate complexity.
- A delivery task PRD is an execution spec the execution model copies from. During planning, replace every `<...>` placeholder with a concrete value (exact file paths, copyable existing examples, ordered implementation steps, machine-checkable acceptance assertions, self-check commands). Never leave reasoning — including which branch a bug fix takes — to the execution phase.
- Do not put all testing into a final catch-all task. Each feature task must include its own basic tests.
- Create a final validation task only after functional gap tasks are planned.
- If a bug does not block the current requirement acceptance, classify it and create or propose a separate bug task.

## Workflow

### 1. Discover Evidence

Locate and read:

- Source requirements document.
- Existing MVP code and tests.
- Existing `.trellis/tasks/`, especially completed or active tasks.
- Existing requirement IDs, traceability matrices, and acceptance notes if present.
- Relevant `.trellis/spec/` indexes for affected packages.

Use local evidence before asking questions. Ask only blocking questions that cannot be resolved from the requirements or repository.

### 2. Perform Read-only Gap Audit (Enhanced - Self-Review Loop)

Loop through the following steps until small model execution standards are met:

#### Round N Audit

**2.1 Generate Gap Audit Output**

Load `references/gap-audit-template.md` and produce:

- Requirements Traceability Matrix.
- MVP completion summary.
- Blocking questions.
- Dependency-ordered task plan.
- Recommended priorities.
- Automated test requirements.

Use only these statuses: `DONE`, `PARTIAL`, `MISSING`, `UNTESTED`, `UNCLEAR`.

**2.2 Self-Review**

Load `references/self-review-checklist.md` and check audit output quality against the checklist item by item.

Use `references/self-review-report-template.md` to generate review report including:
- Overall score (8 dimensions)
- Checklist pass status
- Issue list (location, description, impact, improvement suggestion)
- MVP compatibility check
- Statistics
- Conclusion for this round

**2.3 Determine if Standards Met**

- ✅ All check items pass → proceed to Step 3 (Confirm Delivery Plan)
- ✅ 2 consecutive rounds with no new issues → auto-pass, proceed to Step 3
- ❌ Has failed check items → proceed to Step 2.4 (Targeted Improvements)
- ⚠️ Still has issues after 5 rounds → prompt user to choose:
  - Option A: Use stronger model to re-audit
  - Option B: Manual review of current audit
  - Option C: Accept current version (at own risk)

**2.4 Targeted Improvements**

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

### 3. Confirm Delivery Plan

Ask for one confirmation before creating or modifying Trellis tasks:

```text
Confirm this gap audit and delivery task plan? If yes, I will create Trellis tasks and PRDs without implementing features yet.
```

If the user changes priorities or scope, revise the matrix and task plan before creating tasks.

### 4. Create Gap-closing Tasks

After confirmation:

1. Create or reuse a parent task for complete requirements and validation.
2. Create one child task per tightly related gap group.
3. Use `references/delivery-task-prd-template.md` for child PRDs.
4. Separate foundation contracts, business behavior, UI, tests, and final validation when they have different dependencies.
5. Do not start coding.

### 5. Plan Test Closure

Load `references/test-coverage-matrix-template.md` when asked to plan or fill test coverage. Map every `REQ-*` or `AC-*` to at least one unit, integration, e2e, smoke, regression, or manual verification entry.

### 6. Run Final Acceptance

Load `references/final-acceptance-template.md` when all functional tasks are complete. Do not add features during final acceptance unless a blocking bug prevents acceptance.

### 7. Classify Bugs

Load `references/bug-classification-rules.md` when validation discovers a bug. Decide whether to fix in the current task, create a separate bug task, or defer with a documented risk.

## References

- `references/gap-audit-template.md` - read for the first read-only MVP audit.
- `references/self-review-checklist.md` - read for self-review after each audit round.
- `references/self-review-report-template.md` - read when generating review reports.
- `references/delivery-task-prd-template.md` - read before creating gap-closing task PRDs.
- `references/test-coverage-matrix-template.md` - read when planning or adding test coverage.
- `references/final-acceptance-template.md` - read for final delivery acceptance.
- `references/bug-classification-rules.md` - read when validation finds defects.
