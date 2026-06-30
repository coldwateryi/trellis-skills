---
name: trellis-zero-to-mvp
description: |
  Create a Trellis MVP task tree from a full requirements document. Use when Codex receives a product brief, requirements document, PRD, zero-to-MVP request, large capability-building request, or partially implemented project and must do read-only analysis, assign stable REQ/AC IDs, build full requirement and MVP coverage matrices, lock project contracts, identify existing implementation evidence, use progressive batch and sub-agent planning to form a complete MVP parent/child task tree, draft PRD/design/implementation artifacts, and create Trellis tasks only after user confirmation; do not write application code.
---

# Trellis Zero to MVP

## Overview

Turn a raw requirements document into an MVP-sized Trellis delivery plan. The output is a user-confirmed parent task, child tasks covering the complete MVP scope, PRDs, and any required planning artifacts. It is not application code.

Treat this skill as a planning compiler:

1. Source requirements plus local README/spec/code are inputs.
2. Full Requirement Matrix, MVP Coverage Matrix, and Subtask Planning Ledger are the only intermediate representation.
3. Trellis task, `prd.md`, `design.md`, `implement.md`, and JSONL files are outputs.
4. Gates are compile checks. If a gate fails, stop and fix before moving forward.
5. For small/local models and long planning runs, advance through Stage State Packets; after every phase boundary or context recovery, rebuild state from matrices, ledgers, and real directories instead of relying on natural-language memory.

## Core Invariants (Phase-Tagged)

> **Small model note:** Focus only on invariants tagged for your current phase. Read new rules when entering the next phase. Do not attempt to remember all 25 rules at S0.

### S0-S2 Common (Discovery & Requirements)
- S0-S2: Do not write business code.
- S0-S2: Do not create Trellis tasks until the user confirms the complete read-only plan.
- S0-S2: Do not split tasks by files. Split by independently verifiable business or technical capability.
- S0-S2: Extract complete source requirements before planning the MVP. Every source requirement must enter the Full Requirement Matrix; if it is not in the current MVP, mark it `OUT_OF_SCOPE` or `BLOCKED` and put it in Backlog.
- S0-S2: `REQ-xxx` is the stable identity of a source requirement, not delivery order. Task merge/split/reorder can only change `Txx`.
- S0-S2: Maintain Full Requirement Matrix and MVP Coverage Matrix separately; never report MVP coverage count as the original source requirement count.

### S2-S4 Dedicated (Contract & Task Planning)
- S2-S4: Before task planning, choose a Project Contract Profile, then form Project Contract Lock and Contract Snapshot. Later parent/child PRDs, `design.md`, `implement.md`, and JSONL may only use names, paths, commands, APIs, packages/modules, routes, tables, permission prefixes, and evidence paths from that contract.
- S2-S4: Local context priority is fixed: explicit user request > source requirement behavior > README/module README/AGENTS.md > `.trellis/spec/` > existing code structure > framework defaults > model common sense.
- S2-S4: Small/local models or long tasks must read `references/small-model-safety.md` and output Stage State Packet at each phase. If counts, contracts, or gate results drift from scans, do Drift Reset immediately.
- S3-S4: In Small Model Mode, one child task covers only one primary entity CRUD, one endpoint group, one state transition, one front-end page, or one backend aggregate query. Split further unless the user explicitly permits a merge.
- S3-S4: In Small Model Mode, create at most 8 executable child tasks per batch and fully draft at most 5 high-quality child PRDs per batch. Batching controls capacity; it is not scope trimming.
- S3-S4: Batch planning must maintain Subtask Planning Ledger. Completing only P0/P1 is not complete planning. Do not ask the user to confirm until every MVP `TASK` child task is `READY_TO_CONFIRM`, `BLOCKED`, or `OUT_OF_SCOPE`.

### All Phases (S0-S10)
- Respect Trellis planning artifact boundaries: `prd.md` contains requirements, constraints, scope, dependencies, and acceptance; technical design goes in `design.md`; file plan, implementation steps, self-check commands, rollback points, and review gates go in `implement.md`. Only when the local workflow permits PRD-only and the task is low complexity may a compact execution appendix remain in `prd.md`.
- External configuration, third-party keys, maps, hardware, and external interfaces must be classified as `FIXED`, `BASELINE`, `BLOCKED`, or `OUT_OF_SCOPE`.
- For partially implemented projects, task creation rules are fixed: `DONE` -> no task; `UNTESTED` -> test-only task; `PARTIAL` -> gap-closing task for missing behavior only; `MISSING` -> new implementation task; `UNCLEAR` -> blocking question or clarification task.
- Small-model execution still needs narrow paths fixed during planning, but put them primarily in `design.md` / `implement.md` rather than overloading PRD.
- When candidate child tasks exceed batch limits, business domains exceed 3, full PRD drafts exceed 5, or the user requests multi-agent planning, read `references/subagent-planning-template.md` and prefer sub-agents. If the platform has no sub-agent support, serially simulate the same Agent Packets.
- `task.py create` only creates task directories and seed files. Any artifacts declared in matrices or PRDs must be written by this skill into the real task directories after creation.
- Create task directories only through `task.py create`. Afterward, write files only to the real directory returned by `task.py create`; do not build paths from logical Task IDs or slugs.
- Each task PRD goes only to `<task-dir>/prd.md`, and that directory must contain `task.json`.
- Artifact Gate must not be hand-filled by the model. After task creation and artifact writing, run `scripts/trellis_zero_gate.py` or an equivalent mechanical scan. Final Gate counts must come from tool output.

### S5-S6 Dedicated (Gating & Confirmation)
- S5-S6: If a Trellis 0.6+ project has `.trellis/workflow.md`, treat it as the local workflow contract. If the project declares `design.md`, `implement.md`, `implement.jsonl`, or `check.jsonl`, do not use an old PRD-only workflow.
- S5-S6: Codex projects must read `.trellis/config.yaml` `codex.dispatch_mode`: in `inline` mode JSONL is not a planning-readiness gate, and seed JSONL may be deleted or marked `NOT_NEEDED_WITH_REASON`; in sub-agent mode, fill real `implement.jsonl` / `check.jsonl`; seed-only cannot pass.
- S6-S7: Artifact Gate result must be `PASS` before reporting the task tree as executable.

## Stop Gates

If any condition below is true, stop the current phase and output a `FAIL` report, failure codes, and fix list. Do not continue task creation or claim the task tree is executable.

- Project Contract Lock, Contract Snapshot, or evidence paths are missing.
- Full Requirement Matrix, MVP Coverage Matrix, or Subtask Planning Ledger is missing.
- Any source requirement lacks coverage status, or coverage statistics differ from mechanical matrix statistics.
- Subtask Planning Ledger and MVP Coverage Matrix disagree.
- `UNASSIGNED_MVP_REQ`, `UNBATCHED_TASK`, `P0P1_ONLY_PLAN`, or `DEFERRED_PRD_WITHOUT_PLAN` exists.
- A child task violates Small Model Mode granularity without explicit user confirmation.
- Before user confirmation, any MVP `TASK` child task is not `READY_TO_CONFIRM`, `BLOCKED`, or `OUT_OF_SCOPE`.
- PRD declares `design.md`, `implement.md`, `implement.jsonl`, or `check.jsonl` as required, but the real task directory lacks that file.
- A child PRD `Task Impact Matrix` declares a surface as involved, but `design.md` or `implement.md` lacks the corresponding section.
- In sub-agent dispatch mode or when the artifact matrix declares JSONL required, `implement.jsonl` or `check.jsonl` contains `_example`; in Codex inline mode, seed JSONL must be deleted or explained as `NOT_NEEDED_WITH_REASON`, and Gate must run with `--jsonl-mode inline`.
- Artifacts contain `{Entity}`, `{domain}`, `{entity}`, `<PageComponent>`, `<path>`, `TBD`, `depends`, `as needed`, `YOUR_KEY`, `API_KEY_HERE`, `to be provided`, `pending config`, or equivalent unresolved placeholders.
- Contract Snapshot forbidden tokens appear in parent/child PRD, `design.md`, `implement.md`, or JSONL.
- Gate result lacks mechanical scan evidence, or parent PRD declared Gate counts differ from mechanical scan results.
- Artifact Gate result is not `PASS`.

## Workflow

### 0. Read Workflow Contracts (Graduated Loading)

> **Small model note:** Do not read all reference files at once. Level 1 must be read before starting. Level 2 is read when entering the corresponding phase. For now, only Level 1 is needed.

**Level 1 — Required (read before S0, ~10 min attention budget):**
1. `references/small-model-safety.md` — small model safety (Stage State Packet, Context Budget, Evidence Discipline, Drift Reset)
2. `references/gate-definitions.md` — Gate and failure code definitions (overview, understand the 45 failure codes)
3. This section (0. Read Workflow Contracts) and the **Stop Gates** section

**Level 2 — Read when entering each phase:**
| Before entering phase | Reference files to read |
|---|---|
| Before S1 | `references/project-contract-profiles.md` (contract profile selection) |
| Before S2 | `references/analysis-output-template.md` (Contract Lock + Contract Snapshot sections) |
| Before S3 | `references/analysis-output-template.md` (task splitting + Small Model Mode granularity rules) |
| Before S4 | `references/subagent-planning-template.md` (only if sub-agent triggers apply) |
| Before S5 | `references/analysis-output-template.md` (Pre-Confirmation Gate + Artifact Gate plan) |
| Before S7 | `references/task-creation-checklist.md` |
| Before S8 | `references/parent-prd-template.md`, `references/child-prd-template.md`, `references/planning-artifacts-template.md`, `references/design-surface-template.md` |

**Level 3 — Read for gating/fixing:**
| Scenario | Reference files to read |
|---|---|
| After each self-review round | `references/self-review-checklist.md` (current-phase section only) |
| Self-review report | `references/self-review-report-template.md` |
| Gate checks | `scripts/trellis_planning_gate.py` — run mechanical scan before each phase transition |

Every later phase must advance through the state machine and cannot skip Gates. Before each phase transition, run `scripts/trellis_planning_gate.py` (see specific commands in each phase section).

### 1. Discover Inputs (S0_DISCOVER_CONTEXT)

Locate and read:

- The source requirements document.
- README, module README, AGENTS.md, or project overview files.
- Existing code structure and tests if the repo is not empty.
- Relevant `.trellis/tasks/` and `.trellis/spec/` material.
- Trellis 0.6+ metadata: `.trellis/workflow.md`, `.trellis/config.yaml`, `.trellis/.version`, `.trellis/.developer`, `.trellis/workspace/`.

Inspect the repository before asking questions. Ask only blocking questions that cannot be answered from local context.

**→ S0 Gate:** After confirming input paths and context inventory, run:
```bash
python <skill-dir>/scripts/trellis_planning_gate.py --phase S1_REQUIREMENT_LEDGER --state-file .trellis/planning/planning-state.yaml
```
Only proceed to S1 if Gate result is `PASS`.

### 2. Complete Requirement Ledger and Project Contract

The first read-only pass may only output the requirement ledger. Do not create tasks or draft full child PRDs yet. It must include:

- Project Contract Profile selection with evidence; if no default profile fits, use `custom` and list project-specific contract fields.
- Project Contract Lock and Contract Snapshot.
- Existing Implementation Baseline.
- Source requirement list with stable `REQ-xxx` / `AC-xxx`.
- Full Requirement Matrix.
- MVP Coverage Matrix.
- Backlog.
- Small Model Candidate Split table.

If the source docs mention broad scopes such as PC, IOC, data integrations, mobile applets, reports, or external systems but the Full Requirement Matrix does not cover them, mark `MATRIX_INCOMPLETE` and keep extracting.

**→ S1 Gate:** After completing the requirement ledger, run:
```bash
python <skill-dir>/scripts/trellis_planning_gate.py --phase S2_CONTRACT_LOCK --state-file .trellis/planning/planning-state.yaml --matrix .trellis/planning/full-requirement-matrix.md --mvp-matrix .trellis/planning/mvp-coverage-matrix.md
```
Only proceed to S2 if Gate result is `PASS` and Requirement Ledger Gate is `PASS`.

### 3. Progressive Parent/Child Task Planning

Read `references/analysis-output-template.md` and produce the complete planning output:

- Task merge/split records.
- Full platform scope vs current MVP boundary.
- Module dependency graph.
- Complete capability-based MVP child task list.
- Subtask Planning Ledger.
- Batch Completion Rollup.
- Small Model Mode granularity check.
- Planning artifact matrix.
- Parent PRD draft.
- Child PRD drafts.
- Draft `design.md`, `implement.md`, `implement.jsonl`, and `check.jsonl` for medium/high complexity tasks, or explicit not-needed reasons.
- Child task `Task Impact Matrix` rows and matching design surface sections. When a task touches database, API, inter-module interaction, external systems, UI, permissions, state, validation, transactions, tests, or similar surfaces, read `references/design-surface-template.md` and fill the required `design.md` / `implement.md` sections.

If sub-agent triggers apply, read `references/subagent-planning-template.md`. The main agent owns dispatch, merge, conflict resolution, and final Gate. Sub-agents only produce read-only planning drafts.

**→ S3 Gate:** After completing all MVP task candidates, run:
```bash
python <skill-dir>/scripts/trellis_planning_gate.py --phase S3_FULL_MVP_TASK_CANDIDATES --state-file .trellis/planning/planning-state.yaml --ledger .trellis/planning/subtask-ledger.yaml
```
Only proceed to S4 if Gate result is `PASS`.

### 4. Self-Review and Gate Loop (S4_PROGRESSIVE_BATCH_PLANNING → S5_FULL_MVP_PLANNING_GATE)

After each analysis round:

1. Read `references/self-review-checklist.md` (current batch section only, not the full document).
2. Use `references/self-review-report-template.md` for the review report.
3. Execute Requirement Ledger Gate, Contract Gate, Full MVP Planning Gate, Batch Completeness Gate, and Pre-Confirmation Gate from `references/gate-definitions.md`.
4. For small/local models or long plans, rebuild Stage State Packet from `references/small-model-safety.md`; if it disagrees with matrices or ledgers, fix state before moving forward.

**→ S4 Gate (batch complete):** After each batch, run:
```bash
python <skill-dir>/scripts/trellis_planning_gate.py --phase S4_PROGRESSIVE_BATCH_PLANNING --state-file .trellis/planning/planning-state.yaml --ledger .trellis/planning/subtask-ledger.yaml
```
If output is `BATCH_INCOMPLETE`, continue planning the next batch; do not ask for user confirmation.

**→ S5 Gate (full planning gate):** After all batches complete, run:
```bash
python <skill-dir>/scripts/trellis_planning_gate.py --phase S5_FULL_MVP_PLANNING_GATE --state-file .trellis/planning/planning-state.yaml --ledger .trellis/planning/subtask-ledger.yaml --parent-prd .trellis/planning/parent-prd-draft.md
```
Only proceed to user confirmation if Gate result is `PASS`.

Decision:

- All checks pass and Full MVP Planning Gate plus Pre-Confirmation Gate are `PASS` -> ask for user confirmation.
- Checks pass but any MVP child task remains non-terminal -> output `BATCH_INCOMPLETE` and continue planning the next batch; do not ask for confirmation.
- Any Gate fails -> output failure codes and fixes, then improve and rerun.
- More than 5 rounds still failing -> ask the user to choose stronger model, manual review, or risk acceptance.

### 5. User Confirmation of Complete Plan

Only when Pre-Confirmation Gate is `PASS`, ask:

```text
Please confirm the complete MVP task tree, all batch plans, Backlog boundary, Blocked items, and first creation scope. If confirmed, I will create the Trellis parent task, all planned child tasks, and their required PRD/design/implement/JSONL artifacts without writing application code.
```

The confirmation summary must include Project Contract Lock, source requirement count, MVP Coverage mechanical statistics, Subtask Planning Ledger summary, Batch Completion Rollup, Backlog, Blocked items, high-risk merges/trims, and Small Model Mode batch strategy.

If the user changes scope, update matrices, ledgers, batches, and Gates before creating tasks.

### 6. Create Trellis Task Tree and Write Artifacts

After user confirmation, read `references/task-creation-checklist.md`, then:

1. Create one parent task for the overall project.
2. Record the real parent task directory from `task.py create`.
3. Create child tasks with `--parent <parent-task-dir>`; record each real directory and backfill Subtask Planning Ledger.
4. Before writing any artifact, verify the target directory contains `task.json`.
5. Write parent `<task-dir>/prd.md` using `references/parent-prd-template.md`.
6. Write each child `<task-dir>/prd.md` using `references/child-prd-template.md`.
7. Write required `design.md`, `implement.md`, `implement.jsonl`, and `check.jsonl` from the planning artifact matrix. Read existing artifacts before overwriting.
8. Do not start implementation.

Commands:

```bash
python ./.trellis/scripts/task.py create "<parent title>" --slug <parent-slug>
python ./.trellis/scripts/task.py create "<child title>" --slug <child-slug> --parent "<parent-task-dir>"
```

If `task.py create` fails because developer identity is uninitialized, stop and tell the user to run `trellis init -u <name>` with project platform flags such as `--codex`, or provide an explicit assignee. Use `python ./.trellis/scripts/init_developer.py <name>` only as a legacy fallback when Trellis CLI is unavailable.

### 7. Artifact Gate and Next Step

After task creation and artifact writing, run:

```bash
python <skill-dir>/scripts/trellis_zero_gate.py \
  --tasks .trellis/tasks \
  --parent-task-json <parent-task-dir>/task.json \
  --parent-prd <parent-task-dir>/prd.md \
  --jsonl-mode <required|optional|inline>
```

Use `--jsonl-mode inline` when `codex.dispatch_mode: inline`; use `--jsonl-mode required` for sub-agent dispatch or JSONL-required tasks. If Contract Snapshot defines forbidden tokens, add `--forbidden-token` or `--forbidden-regex`; if contract conflicts cannot be simplified to forbidden tokens, add `--contract-mismatch-regex`.

Only when the mechanical scan returns `result = PASS` and Development Recommendation Gate is `PASS`, output:

- Task tree.
- Recommended execution order.
- Blocked tasks.
- Parallelizable tasks.
- Backlog / later scope.
- Artifact Gate result.
- First recommended task to start and why.

If any Gate fails, output:

```yaml
planning_status:
  development_ready: false
  failure_codes:
    - <code>
  next_action: <continue_planning | write_artifacts | fix_gate_failure | ask_user_confirmation>
```

Do not recommend starting development.

## Delivery Phase Handoff

This skill stops after creating the task tree and planning artifacts. For implementation, use execution-phase skills by dependency order:

1. `trellis-implement-tdd` - implement each child AC with red/green TDD loops.
2. `trellis-debug-systematic` - isolate and fix failing checks.
3. `trellis-review-twostage` - run spec compliance and code-quality review before completion.

Recommended role split: strong model for planning, small model for implementation, strong model for Review Stage 2.

## References

- `references/workflow-state-machine.md` - read at startup (Level 1); defines planning states and legal transitions.
- `references/gate-definitions.md` - read at startup (Level 1); defines Gates, failure codes, and pass conditions.
- `references/small-model-safety.md` - read at startup (Level 1); defines Stage State Packet, context budget, evidence discipline, and Drift Reset.
- `references/project-contract-profiles.md` - read before S1 (Level 2); select project contract fields and avoid applying RuoYi/Java assumptions to CLI, SDK, frontend, or other projects.
- `references/analysis-output-template.md` - read before S2/S3/S5 (Level 2); generate initial analysis and progressive planning output.
- `references/subagent-planning-template.md` - read when multi-agent or batch planning is triggered (Level 2).
- `references/self-review-checklist.md` - read for self-review after each analysis round (Level 3, current-phase section only).
- `references/self-review-report-template.md` - read when generating review reports (Level 3).
- `references/planning-artifacts-template.md` - read when drafting Trellis 0.6+ design, implementation, and context manifest artifacts.
- `references/design-surface-template.md` - read when a child task touches database, API, inter-module interaction, external systems, UI, permissions, state, validation, transactions, tests, or similar design surfaces.
- `references/parent-prd-template.md` - read when drafting or writing the parent task PRD.
- `references/child-prd-template.md` - read when drafting or writing child task PRDs.
- `references/task-creation-checklist.md` - read before creating the task tree.
- `scripts/trellis_zero_gate.py` - run after task creation and artifact writing (S9); produces non-handwritten Artifact Gate counts.
- `scripts/trellis_planning_gate.py` - **new**: run before each planning phase transition (S0→S1→S2→S3→S4→S5); enforces legal state machine transitions, validates count consistency and contract completeness, detects small-model drift.
