---
name: trellis-implement-tdd
description: |
  Implement a Trellis subtask using strict TDD (RED→GREEN→REFACTOR), turning acceptance criteria into code one by one. Used when Codex / Claude Code drives a small-parameter model like qwen3.6 35b—transforms "understand and implement requirements" into a mechanical "make this failing test green" loop with objective signals at every step.
---

# Trellis TDD Implementation (RED-GREEN-REFACTOR)

## Overview

Implement a planned Trellis subtask by going through its `prd.md` acceptance criteria (AC) one by one using TDD: write a failing test and see red, write minimal code and see green, run self-checks to confirm no regression, record progress, move to the next AC.

This skill is **invoked by the orchestration session (main session, typically a strong model)** to drive **the implementation executor (which may be a small model like qwen3.6 35b)**. The flow is "held" by this skill; the executor only performs mechanically verifiable steps without needing to judge "am I done?"—**test turns green = done**.

Input: A subtask directory with `status` in-progress and dependencies satisfied (contains `prd.md`, may contain `design.md`, `implement.md`, `implement.jsonl`, `check.jsonl`). Output: Code changes passing tests + progress written back to `<task-dir>/tdd-progress.md`, **without executing git commit** (Trellis implementation executors forbid commit/push/merge).

## Constraints

- **Do not write implementation code before a failing test.** The first step for every AC is always writing a test that fails.
- **Only handle one AC at a time.** Don't start the next AC until the current one turns green.
- **Do not judge "what the requirement is".** Requirements are locked down by `prd.md` acceptance criteria, decision table, and contracts; executor's job is to make the corresponding test green.
- **Landing point is locked.** Where new code goes is decided by `prd.md` file manifest + `design.md` orchestration-computation layering; don't decide on your own.
- **Do not touch files outside file manifest / forbidden list.** When you need to touch other files, stop and report—don't spread modifications autonomously.
- **Do not execute `git commit` / `git push` / `git merge`.** After completing an AC, only stage/record.
- **RED/GREEN signals are the only completion criteria.** Test doesn't show red means test didn't capture the behavior—stop and fix the test, don't write implementation to "make it green".
- When test should be green but stays red, or self-check command fails, **switch to `trellis-debug-systematic`**—don't trial-and-error in this loop.
- If `prd.md` lacks executable test definitions or self-check commands (violates planning-phase quality gate), stop and report—ask to supplement planning artifacts first, don't force through.

## Workflow

### 1. Load task context (must-read before editing)

Read in order, loading only "must-read-before-editing" stable context to control small-model context occupancy:

1. Subtask `prd.md`: focus on `Acceptance Criteria`, `Automated Tests Required`, `Reference Implementation`, `File Manifest`, `Decision Table`, `Behavior Constraints`, `Self-Check Commands`, `Forbidden`.
2. If `implement.jsonl` exists: pre-load each stable context item listed (spec / contract / research).
3. If `design.md` exists: read `Orchestration-Computation Separation` and `Mount Point Checklist` sections to confirm each new code's landing point.
4. If `.trellis/spec/<relevant-layer>` exists: read specs directly related to this task.

Before editing code, copy `references/tdd-progress-template.md` to `<task-dir>/tdd-progress.md`. This task-local file is the writable progress record; the template under the skill directory stays read-only.

Extract each `AC-xxx` from `prd.md` into a **TODO test list**, write to `<task-dir>/tdd-progress.md`.

### 2. Run RED-GREEN loop for each AC

For each AC in order, execute the loop from `references/tdd-loop-protocol.md`:

```
1. RED  ── Copy prd.md「Reference Implementation/Test Example」, write a test for AC-xxx asserting its expected observable result
2. See red ── Run the test, must see failure (objective evidence). No failure → test didn't cover behavior, go back to step 1 to fix test
3. GREEN ── Write "just enough to turn it green" minimal code; landing point per file manifest+orchestration layering, decisions per decision table, no free improvisation
4. See green ── Run the test again, see it pass (objective signal)
5. Self-check ── Run prd.md「Self-Check Commands」full set, confirm no breakage of already-green ACs (no regression)
6. Record ── Mark AC-xxx as done in `<task-dir>/tdd-progress.md`, stage changes (no commit)
7. Next AC
```

Any step fails and not obvious → trigger `trellis-debug-systematic`, fix, then return to the failed step and re-run.

### 3. Wrap-up self-check

After all ACs turn green:

1. Run all `prd.md` self-check commands + project lint / type-check, all green.
2. Check `design.md` `Mount Point Checklist` item by item to confirm wiring (route registration / config item / event subscription / DI binding, etc.), preventing "wrote implementation but didn't wire it".
3. `<task-dir>/tdd-progress.md` shows all ACs as done, no remaining red lights.

### 4. Handoff to review

After implementation self-check all green, **do not mark task complete on your own**. Hand off to `trellis-review-twostage` for two-stage review; mark task complete only after review passes, via orchestration session.

## Small-model adaptation highlights

- **Decisions left-shifted**: Naming / branching / schema / landing points decided by strong model in planning phase, executor just mechanically copies.
- **Objective signal-driven**: Each step's completion determined by test red/green / command exit code, not letting small model subjectively judge.
- **Narrow context**: Only face one AC + one test at a time, naturally slicing context to minimum.
- **Role-layered model assignment**: This skill drives implementation executor configured with small model (e.g. qwen3.6 35b); debugging beyond 3 rounds, review Stage 2 escalate to strong model (see `trellis-review-twostage`).

## Reference files

- `references/tdd-loop-protocol.md` —— Detailed RED-GREEN loop per AC, iron rules and anti-patterns, read before starting implementation.
- `references/tdd-progress-template.md` —— Read-only template for `<task-dir>/tdd-progress.md`; update the task-local file throughout execution.
