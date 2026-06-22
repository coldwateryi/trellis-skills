---
name: trellis-delivery-controller
description: |
  Trellis requirements-to-delivery entrypoint and workflow controller. Use when the user wants to invoke one Trellis skill that detects the current stage and routes work across requirements analysis, MVP task planning, post-MVP gap audit, delivery loop, TDD implementation, systematic debugging, two-stage review, and final acceptance. Coordinates trellis-zero-to-mvp, trellis-mvp-to-delivery, trellis-implement-tdd, trellis-debug-systematic, and trellis-review-twostage while enforcing safety gates.
---

# Trellis Delivery Controller

## Overview

Treat the Trellis skills as a layered delivery pipeline instead of requiring the user to remember every stage-specific skill. This controller detects project state, chooses the next stage, sets safety gates, and routes execution to the dedicated stage skill.

This skill does not replace stage-specific skills:

- Requirements to MVP task tree: use `trellis-zero-to-mvp`.
- Post-MVP gap audit and gap planning: use `trellis-mvp-to-delivery`.
- Subtask implementation: use `trellis-implement-tdd`.
- Failure root cause and repair: use `trellis-debug-systematic`.
- Completion review: use `trellis-review-twostage`.

## Guardrails

- Do not write application code directly; implementation belongs to execution-phase skills.
- Do not skip confirmation gates: first read-only analysis, first full gap audit, scope expansion, edits outside the File Manifest, or missing strong-model review must pause.
- Do not let implementers mark their own task complete; completion requires self-checks and review gates.
- Do not repeat full audit when `.trellis/delivery-state.md` exists and requirements have not changed; prefer delta audit or early-exit.
- Do not assimilate third-party skill capabilities in the controller; external capability intake belongs to `trellis-skill-assimilator`.

## Workflow

### 1. Discover Project State

Read `references/route-policy.md`, then inspect:

- Whether a source requirements document exists.
- Whether `.trellis/` exists.
- Whether `.trellis/tasks/`, `.trellis/spec/`, and `.trellis/workflow.md` exist.
- Whether `.trellis/delivery-state.md` and `.trellis/delivery-run-log.jsonl` exist.
- Whether a specific subtask directory was provided.
- Whether there is a recent failing test, self-check failure, or review report.

### 2. Choose Stage

Use `references/route-policy.md` to output exactly one next stage:

- `zero-to-mvp-readonly`
- `zero-to-mvp-create-tasks`
- `mvp-to-delivery-full-audit`
- `mvp-to-delivery-delta-audit`
- `delivery-batch-planning`
- `implement-tdd`
- `debug-systematic`
- `review-twostage-stage1`
- `review-twostage-stage2`
- `final-acceptance`
- `early-exit`
- `pause-human-needed`

Explain the evidence, required context files, skill to invoke, and safety gate.

When the next stage belongs to the delivery loop, read `references/delivery-loop-routing.md` to choose loop mode and audit scope. Pass that routing decision to `trellis-mvp-to-delivery`.

### 3. Route Execution

Read `references/stage-transition-gates.md` and advance only to the next safety gate:

- After read-only planning analysis, wait for user confirmation before task creation.
- After first full audit, wait for user confirmation of the gap matrix and first gap batch.
- For subtask work, route through `trellis-implement-tdd -> trellis-debug-systematic -> trellis-review-twostage`.
- Stage 2 review requires a strong model or human review; if the current model is not suitable, output an evidence pack and pause.

### 4. Check State Updates

When a stage involves the delivery loop, `trellis-mvp-to-delivery` maintains:

- `.trellis/delivery-state.md`
- `.trellis/delivery-run-log.jsonl`
- Requirements Gap Matrix
- Current batch and next action recommendation

The controller only checks whether these artifacts exist, are fresh, and allow the next stage.

### 5. Report

Each run outputs:

- Current stage.
- Next Trellis skill to invoke.
- Context to read.
- Automatic progress boundary.
- Required pause gates.
- If paused, the blocker and required user or strong-model input.

## References

- `references/route-policy.md` - Read to detect project state and next stage.
- `references/delivery-loop-routing.md` - Read to choose post-MVP full/delta/early-exit behavior, loop mode, and batch boundaries.
- `references/stage-transition-gates.md` - Read to decide stage transitions and stop conditions.
- `references/model-role-policy.md` - Read to decide small-model, strong-model, and human-review responsibilities.
