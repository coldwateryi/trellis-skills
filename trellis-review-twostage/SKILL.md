---
name: trellis-review-twostage
description: |
  Before marking a Trellis subtask complete after self-check all green, conduct two-stage code review: mechanically check spec compliance (against PRD acceptance criteria/decision table/forbidden/file manifest/mount points), then code quality review (against .trellis/spec/guides engineering standards and design discipline). Used in Codex / Claude Code team collaboration scenarios, especially when implementation is by a small-parameter model like qwen3.6 35b—small models reviewing their own code is unreliable, Stage 2 should escalate to strong model; critical issues block completion.
---

# Trellis Two-Stage Review

## Overview

Quality gate before marking subtask complete, after implementation self-check all green. Split into two independent review stages:

- **Stage 1 Spec Compliance**: Mechanically check against `prd.md`, can be done by small model + checklist.
- **Stage 2 Code Quality**: Check against engineering standards and design discipline, **should be done by strong model** (small model reviewing its own output is unreliable).

Any stage finding **critical** issue blocks completion, send back to `trellis-implement-tdd` for fix; after fix, review again.

Trigger: `trellis-implement-tdd` wrap-up self-check all green, handoff to review.

Write every review pass to the fixed task-local file `<task-dir>/review-report.md`. Create it from `references/review-report-template.md` on the first review pass, then append a new review-round block for each re-review. Do not edit the template under the skill directory.

## Constraints

- **Review based on diff + `prd.md`**, not re-reading entire requirements document.
- **Stage 1 and Stage 2 separate, don't merge**—merging causes "did it follow spec" and "is code good" to mask each other.
- **Stage 2 use strong model** (role-layered model assignment). If only small model available, Stage 2 at least strictly walk `references/review-stage2-checklist.md` item by item, and flag "not reviewed by strong model" risk in report.
- **Severity grading**: critical (blocking) / major (should fix) / minor (can record for later). Only critical blocks completion.
- Reviewer **doesn't directly change code**: output issue list to send back to implementation skill for fix, keeping "write" and "review" separate.

## Workflow

### 1. Prepare

- Get this task's diff (relative to task start point).
- Read `prd.md`: `Acceptance Criteria`, `Decision Table`, `Forbidden`, `File Manifest`, `Behavior Constraints`; if `design.md` exists read `Mount Point Checklist`, `Orchestration-Computation Separation`.
- If `check.jsonl` exists: pre-load the regression/risk context listed.

### 2. Stage 1 · Spec Compliance (Mechanical check, small model ok)

Walk `references/review-stage1-checklist.md` item by item, check if implementation **did as planned**:

- Each `AC-xxx` has corresponding test and is green?
- Changed files all within「File Manifest」? Any file outside manifest changed?
- Any violation of「Forbidden」(create already-existing base class, introduce unlisted dependency, etc.)?
- Choices in「Decision Table」followed (annotation / naming / schema / branching)?
- 「Mount Point Checklist」wired item by item (route / config / subscription / DI)?
- Any non-compliance → record as issue. AC without test, changed forbidden file, mount point missing wire = **critical**.

### 3. Stage 2 · Code Quality (Strong model)

Walk `references/review-stage2-checklist.md` item by item, review **code itself** against `.trellis/spec/guides/` and design discipline:

- **Orchestration-Computation Separation**: Orchestration logic and computation logic mixed in one place? Pure computation stuffed into orchestration layer making it hard to test?
- **Structural Health**: Keep piling into an already-fat file? Create "kitchen-sink that holds everything"?
- **Simplification/Reuse**: Duplicate implementation of existing capability? Unrequested over-abstraction (YAGNI violation)?
- **Correctness**: Boundary / error paths actually handled (not just making happy-path test green)?
- **Spec Compliance**: Naming / layering / error semantics conform to `.trellis/spec/`?
- Record by severity; introducing correctness defect or breaking existing behavior = **critical**.

### 4. Issue report and verdict

Use `references/review-report-template.md` to produce/update `<task-dir>/review-report.md`:

- Has **critical** → block, send back to `trellis-implement-tdd`, only fix flagged items, after fix return to step 1 for re-review.
- Only major/minor → can pass; major suggest fix this round, minor note to task remarks/later.
- All pass → hand back to orchestration session to advance task status (`task.py` advance / enter finish).

## Small-model adaptation highlights

- **Write-review separation + model layering**: Implementation uses small model, Stage 2 review uses strong model—this is key to trusting small-model output.
- **Stage 1 mechanization**: Spec compliance is mechanical item-by-item checking against PRD, small model can handle it, use it to filter out low-level deviations first.
- **Critical blocking**: Turn "quality meets bar" into objective gate, not subjective feeling of letting pass.
- For teams: Two-stage review + severity grading makes PRs reviewable, gives objective acceptance criteria for others'/small-model output.

## Reference files

- `references/review-stage1-checklist.md` —— Spec compliance mechanical check list, read in Stage 1.
- `references/review-stage2-checklist.md` —— Code quality and design discipline list (includes orchestration-computation separation/structural health), read in Stage 2.
- `references/review-report-template.md` —— Read-only template for `<task-dir>/review-report.md`; append/update the task-local file when producing review results.
