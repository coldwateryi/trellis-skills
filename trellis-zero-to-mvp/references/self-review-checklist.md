# Self-Review Checklist

Use this checklist to evaluate whether read-only planning is executable by small/local models such as qwen3.6 35b.

## Usage

1. After each read-only analysis round, check this list item by item.
2. All checks must pass or be explicitly marked `N/A`, and Full MVP Planning Gate plus Pre-Confirmation Gate must be `PASS`, before user confirmation.
3. Failed items become precise issues with targeted fixes.

---

## 0. Trellis 0.6+ Workflow Fit

### 0.0 Project Contract Lock
- [ ] User requirements, README/module README, AGENTS.md, `.trellis/spec/`, and existing code conventions were read.
- [ ] Project Contract Profile is selected with evidence and rejected-profile reasons.
- [ ] Project Contract Lock exists; applicable selected-profile fields have adopted values and evidence paths.
- [ ] Non-applicable fields are `not-applicable`; RuoYi/Java fields are not applied to CLI, SDK, frontend, Python service, or custom projects.
- [ ] If README/spec/code conflict, a `CONTRACT_CONFLICT` table is output.
- [ ] If `CONTRACT_CONFLICT` exists, confirmation is blocked and tasks are not created.
- [ ] Child task candidates follow Project Contract Lock for names, paths, APIs, commands, routes, data/state objects, and packages/modules.
- [ ] No task mixes two naming systems, path systems, API/command systems, or package/module structures.
- [ ] Contract Snapshot and forbidden tokens exist, with evidence for each forbidden token.
- [ ] Parent/child PRDs, `design.md`, `implement.md`, and JSONL were scanned for forbidden-token hits.

### 0.1 Workflow Discovery
- [ ] `.trellis/workflow.md` was read when present.
- [ ] `.trellis/config.yaml`, `.trellis/.version`, and `.trellis/.developer` were checked when present.
- [ ] Analysis states whether the project is legacy PRD-only or Trellis 0.6+ artifact workflow.
- [ ] `codex.dispatch_mode` was read; inline, sub-agent, and optional JSONL Gate modes are distinguished.
- [ ] Developer identity setup uses `trellis init -u <name>` first; `init_developer.py` is legacy fallback only.

### 0.2 Spec Freshness
- [ ] Relevant `.trellis/spec/` files are listed.
- [ ] Spec freshness is marked fresh/stale/missing/unknown.
- [ ] Stale or missing specs become a spec-refresh/bootstrap task or blocker.

### 0.3 Planning Artifacts
- [ ] Every task states required artifacts: `prd.md`, `design.md`, `implement.md`, `implement.jsonl`, `check.jsonl`.
- [ ] Planning artifact matrix exists and supports post-creation file existence checks.
- [ ] Medium/high complexity tasks include design and implementation artifacts or are split smaller.
- [ ] High complexity is not PRD-only; if no `design.md` and `implement.md` are generated, the task has been split to low/medium complexity.
- [ ] Stable specs, research notes, or external context that must be preloaded before implementation/checking are represented by JSONL context manifests.
- [ ] Detailed file plan, ordered steps, self-check commands, failure recovery, and review gates are in `implement.md`; low-complexity PRD-only exception has evidence.
- [ ] Every child task has a `Task Impact Matrix`.
- [ ] If any surface is `yes`, `design.md` contains the matching design section and `implement.md` contains the matching implementation-plan section.
- [ ] RuoYi/Vue CRUD or fullstack tasks do not mark common surfaces such as database, API, UI, permissions, query, validation, and tests all `no` without reason.

### 0.4 Existing Implementation Retrofit
- [ ] Existing Implementation Baseline exists for non-empty repos.
- [ ] Baseline entries include exact code evidence and test evidence, or explicitly state that test evidence is missing.
- [ ] Source requirements remain the source of truth; `.trellis/spec/` is not treated as the only requirements source.
- [ ] `DONE` requirements do not create implementation tasks.
- [ ] `UNTESTED` requirements create only test-coverage tasks.
- [ ] `PARTIAL` requirements create only gap-closing tasks for missing behavior.
- [ ] `MISSING` requirements create new implementation tasks.
- [ ] Every requirement row has a matching task action: `none`, `test-only`, `gap-task`, `new-task`, or `clarify`.
- [ ] Existing dependencies use `existing:<path-or-capability>`.
- [ ] Task split and PRD write-back paths use real `task.py create` directories, not logical IDs/slugs.

### 0.5 State Machine and Gates
- [ ] `workflow-state-machine.md` and `gate-definitions.md` were read.
- [ ] Current output names state S0-S10 and next state.
- [ ] Requirement Ledger Gate outputs PASS/FAIL, failure codes, and evidence.
- [ ] Contract Gate outputs PASS/FAIL, failure codes, and evidence.
- [ ] Full MVP Planning Gate outputs PASS/FAIL, failure codes, and evidence.
- [ ] Batch Completeness Gate outputs PASS/FAIL, failure codes, and evidence.
- [ ] Pre-Confirmation Gate outputs PASS/FAIL, failure codes, and evidence.
- [ ] If any Gate fails, there is no user confirmation request, no task creation, and no development recommendation.

---

## A. Requirement Completeness

### A1. Requirement Identity
- [ ] Every requirement has a unique `REQ-xxx` ID.
- [ ] Every acceptance criterion has a unique `AC-xxx` ID.
- [ ] IDs are continuous with no gaps unless gaps are explained.
- [ ] Every requirement-trace row has a clear status: `DONE`, `PARTIAL`, `MISSING`, `UNTESTED`, or `UNCLEAR`.
- [ ] `REQ-xxx` binds source requirement behavior and does not change meaning when tasks merge, split, or reorder.

### A1.1 Source Requirement Coverage
- [ ] All source-document verifiable points are listed.
- [ ] Every source point maps to a stable `REQ-xxx`.
- [ ] Full Requirement Matrix and MVP Coverage Matrix are output separately.
- [ ] Current MVP coverage counts are not reported as original source requirement counts.
- [ ] Parent PRD coverage summary comes from mechanical MVP Coverage Matrix counts, and `TASK+MERGED+BASELINE+OUT_OF_SCOPE+BLOCKED` equals Full Requirement Matrix rows.
- [ ] Full platform scope vs current MVP boundary is explicit.
- [ ] Every `REQ-xxx` has coverage status: `TASK`, `MERGED`, `BASELINE`, `OUT_OF_SCOPE`, or `BLOCKED`.
- [ ] `MERGED` requirements name target child task and covering AC.
- [ ] `BASELINE` requirements cite existing code/test evidence.
- [ ] `OUT_OF_SCOPE` requirements explain exclusion reason and are explicitly surfaced during user confirmation.
- [ ] All `OUT_OF_SCOPE` requirements enter Backlog with recommended stage and re-entry conditions.
- [ ] No source requirement disappears from traceability.

### A2. Requirement Clarity
- [ ] No vague expressions such as `TBD`, `as needed`, `depending on situation`, or `depends` remain.
- [ ] No incomplete lists such as "etc.", "such as", or "similar" remain unless fully bounded.
- [ ] Uncertain words such as "may", "perhaps", or "recommended" are eliminated or made concrete.

### A3. Boundary Conditions
- [ ] Empty input behavior is specified.
- [ ] Oversized input behavior is specified.
- [ ] Duplicate input/submission behavior is specified.
- [ ] Concurrency behavior is specified when applicable.
- [ ] Invalid format behavior is specified.

### A4. Error Handling
- [ ] Every failure scenario has a concrete error code.
- [ ] Every failure scenario has a concrete error message, not a generic "operation failed".
- [ ] Error response shape is specified.

---

## B. Task Split Quality

### B1. Split Principles
- [ ] Each child task is an independently verifiable business or technical capability.
- [ ] No file-based tasks such as "finish UserController.java".
- [ ] No time-based tasks such as "week 1 task".
- [ ] Each child task can be completed independently by a single developer/model run.
- [ ] Task merge/split record is complete and task-count changes have reasons.
- [ ] MVP task tree vs full platform scope is explicit.
- [ ] Small Model Mode: each task covers only one entity CRUD, one endpoint group, one state transition, one frontend page, or one backend aggregate query.
- [ ] Small Model Mode: no task combines multiple primary entities, multiple CRUD sets, CRUD + state machine + report, backend flow + mini-app page, map/GIS + multi-table aggregation + advanced analytics.
- [ ] The model did not exempt oversized tasks by claiming coupling; any retained merge has explicit user confirmation.
- [ ] Small Model Mode batch limits are respected; if exceeded, tasks are batched.
- [ ] Batch planning covers all MVP `TASK` children, not only P0/P1.
- [ ] `P0P1_ONLY_PLAN` does not exist.

### B2. Complexity Assessment
- [ ] Every task has complexity: low/medium/high.
- [ ] Complexity is assessed against small-model capability, not a human developer.
- [ ] High-complexity tasks are split into low/medium tasks or have steps pinned enough to require no reasoning.
- [ ] Low complexity has a direct example to copy or is standard CRUD/config.
- [ ] Medium complexity has limited business logic and explicit implementation steps.
- [ ] High complexity is split or has every decision branch pinned.

### B3. Dependencies
- [ ] Every task lists dependencies.
- [ ] No circular dependency exists.
- [ ] Tasks marked parallelizable truly have no dependency between them.
- [ ] Blocking P0 tasks are identified and ordered first.
- [ ] Baseline dependencies and Trellis task dependencies are separate.
- [ ] Existing code dependencies are not disguised as new Trellis child tasks.

### B4. Priority
- [ ] Every task has priority P0/P1/P2/P3.
- [ ] P0 blocks other modules or core correctness.
- [ ] P1 closes the core business loop.
- [ ] P2 covers experience, reports, notifications, or enhancements.
- [ ] P3 covers non-essential optimization.

### B5. Progressive Planning Ledger
- [ ] Subtask Planning Ledger is output.
- [ ] Every MVP Coverage Matrix `TASK` has a ledger row.
- [ ] Every ledger row has Task ID, REQ IDs, title, batch, dependencies, parallel group, complexity, PRD status, artifact needs, and next step.
- [ ] Batch Completion Rollup is output.
- [ ] Every MVP child task has a batch; `UNBATCHED_TASK` does not exist.
- [ ] Before user confirmation, all MVP child tasks are `READY_TO_CONFIRM`, `BLOCKED`, or `OUT_OF_SCOPE`.
- [ ] Later batches are not "to be planned"; their boundaries, REQ coverage, dependencies, complexity, and artifact needs are frozen.

---

## C. PRD Quality

### C1. Placeholder Elimination
- [ ] PRD contains no `<...>` placeholders.
- [ ] PRD/design/implement/JSONL contain no Contract Snapshot forbidden token.
- [ ] PRD contains no generic placeholders such as `{Entity}`, `{domain}`, `{entity}`, or `<PageComponent>`.
- [ ] PRD contains no abstract references such as "specific path" or "related file".
- [ ] PRD contains no `TBD`, "to be provided", "as needed", "depending on situation", or equivalent unresolved expressions.
- [ ] PRD/design/implement contain no `YOUR_KEY`, `API_KEY_HERE`, or unresolved external config.
- [ ] All external config is marked `FIXED`, `BASELINE`, `BLOCKED`, or `OUT_OF_SCOPE` with execution behavior.

### C1.1 Title and Body Consistency
- [ ] Each child task title, goal, file list, primary entity, table name, API route, and permission string belong to the same business domain.
- [ ] `design.md` and `implement.md` do not copy another task's page path, Service class, state machine, or business flow.
- [ ] If another task's entity/path is referenced, it is listed in dependencies or baseline with reason.
- [ ] A task's primary entity, route, or table name is not mixed with an unrelated task.
- [ ] Every child task has Project Contract Reference or equivalent contract reference.
- [ ] Child Project Contract Reference matches parent Project Contract Lock.
- [ ] Every child PRD `Task Impact Matrix` matches task type, semantic anchors, and file plan.
- [ ] If database/data model is involved, `design.md` has `Database Schema Design` and `implement.md` has `Database Migration Plan`.
- [ ] If API is involved, `design.md` has `API Contract Design` and `implement.md` has `API Implementation Plan`.
- [ ] If UI/project style is involved, `design.md` has `UI Design and Style Contract` and points to current project reference page/component style.
- [ ] If permission/data scope is involved, backend permission, frontend button permission, menu permission, and data scope rules are consistent.

### C2. Reference Implementation
- [ ] Concrete full paths are provided when a copyable example exists.
- [ ] If no example exists, it explicitly says "none, build from Technical Notes/design.md/implement.md".
- [ ] Replacement notes are concrete, such as "replace User with Order".
- [ ] It does not say vague things like "refer to related code" or "copy similar implementation".

### C3. File Manifest
- [ ] In Trellis 0.6+, file manifest lives in `implement.md`; PRD only states implementation plan location.
- [ ] If a low-complexity PRD-only task puts file list in PRD, there is evidence that local workflow permits it.
- [ ] Every file to edit is listed with a complete path.
- [ ] Every file has operation type, and modified files name exact locations.
- [ ] Data structure changes include complete field tables.

### C4. Implementation Steps
- [ ] In Trellis 0.6+, steps live in `implement.md`; PRD-only low-complexity tasks may use the compact appendix.
- [ ] Steps are ordered.
- [ ] Each step is a concrete action, not an abstract goal.
- [ ] Each step can be verified independently.
- [ ] Decisions that require reasoning are pinned in steps or design.

### C5. Acceptance Criteria
- [ ] Acceptance criteria are decidable assertions, not subjective statements.
- [ ] Normal path is covered.
- [ ] Failure path is covered.
- [ ] Boundary conditions are covered.

### C6. Self-Check Commands
- [ ] In Trellis 0.6+, self-check commands live in `implement.md`; PRD can keep acceptance-level summaries.
- [ ] Commands can be run directly.
- [ ] Commands are specific, not "run tests" or "verify feature".
- [ ] Expected result is stated.
- [ ] Commands do not require human judgment to determine pass/fail.

### C7. Automated Tests Required
- [ ] Test types are listed: unit/integration/e2e/etc.
- [ ] Every test point is concrete: method + input + expected output.
- [ ] It does not say abstract things like "add necessary tests" or "ensure enough coverage".

---

## D. Small Model Friendliness

### D1. Decision Points Pinned
- [ ] Annotation/framework choice is explicit.
- [ ] Branching choice is explicit.
- [ ] Naming/path/API/command/package/module choices are explicit.
- [ ] Table/schema/state/config structures are explicit, including field names, types, and constraints.
- [ ] Third-party keys, external interfaces, maps, hardware protocols, and other open items are fixed, blocked, or out of scope.

### D2. Copy-Example Feasibility
- [ ] If an example is referenced, it is highly similar to this task.
- [ ] Mapping from example to task is clear.
- [ ] If no example can be copied, from-scratch steps are detailed.

### D3. Forbidden List
- [ ] Forbidden actions are listed.
- [ ] File modification scope is clear.
- [ ] Dependency constraints are clear.

### D4. Tech Stack and Tool Constraints
- [ ] Frameworks/libraries are listed in Technical Notes.
- [ ] Build command is explicit.
- [ ] Test command is explicit.

### D5. Context and Design Shift-Left
- [ ] Context Manifest lists exact files the execution model must read before editing.
- [ ] Decision table pins naming, branches, schema, API, validation, and similar choices.
- [ ] Contract Snapshot defines API/interface/data/state behavior before coding.
- [ ] If `implement.jsonl` is used, entries list stable implementation-context files, not source files being edited or step actions.
- [ ] If `check.jsonl` is used, entries list stable verification-context files, not test commands.
- [ ] `implement.jsonl` / `check.jsonl` are not only `_example` seeds; if JSONL is unnecessary, reason is recorded.
- [ ] JSONL mode is one of `required/optional/inline` and matches `.trellis/config.yaml` and artifact matrix.
- [ ] If workflow requires `design.md` for complex tasks, `implement.md` is also prepared or not-needed reason is explicit.
- [ ] Artifacts marked required in PRD exist after task creation; declarations do not drift from filesystem.

### D6. Artifact Gate
- [ ] Post-creation Artifact Gate checks are planned.
- [ ] Artifact Gate includes placeholder scan, JSONL `_example` scan, Project Contract Check, Small Model Grain Check, high-complexity artifact check, and external config check.
- [ ] Artifact Gate uses `scripts/trellis_zero_gate.py` or equivalent mechanical scan as evidence, never model judgment.
- [ ] Artifact Gate includes generic `<...>` placeholder scan and parent PRD declared values vs mechanical scan consistency check.
- [ ] Artifact Gate `FAIL` blocks executable task-tree reporting until fixed or explicitly blocked.
- [ ] Artifact Gate `PENDING` is treated as `FAIL` for executable reporting.
- [ ] Artifact Gate output includes `jsonl_mode`, `forbidden_token_hits`, `contract_mismatch_hits`, `coverage_count_mismatch_hits`, `missing_declared_artifacts`, `angle_placeholder_hits`, `declared_gate_mismatch_hits`, and `external_config_hits`.
- [ ] Artifact Gate output includes `design_surface_prd_without_matrix` and `design_surface_missing_hits`, both with PASS condition 0.

### D7. Development Recommendation Threshold
- [ ] Development Recommendation Gate is defined and output.
- [ ] If Artifact Gate is not `PASS`, no "first recommended task" is output.
- [ ] If any unexplained non-terminal MVP child remains, output `development_ready: false`.
- [ ] If only this batch or P0/P1 is complete, output next planning action instead of development recommendation.

---

## E. Risk Checks

### E1. Risk Identification
- [ ] High-risk modules are marked with risk notes.
- [ ] Cross-team dependencies are explicit.
- [ ] Technical debt is recorded in Out of Scope.

### E2. Out of Scope Clarity
- [ ] Out of Scope lists concrete excluded functions.
- [ ] Out of Scope lists anything that cannot be pinned during planning.
- [ ] Out of Scope is not vague, such as "other features".

---

## F. TDD Readiness

### F1. AC Testability
- [ ] Every acceptance criterion can become an independently runnable failing test.
- [ ] Every AC expected observable result is concrete enough for assertions.
- [ ] Test commands are runnable and include expected results.
- [ ] Automated test requirements map to AC/REQ instead of vague "add tests".

### F2. Red-Green Feasibility
- [ ] There is a copyable test example path, or it explicitly says "none, write test from scratch".
- [ ] Boundary and error paths each have corresponding test points, not only happy path.

---

## G. Delivery Discipline Checks

### G1. Orchestration-Computation Separation
- [ ] Medium/high complexity task `design.md` marks orchestration and computation layers with landing files.
- [ ] Independently testable computation is not buried in orchestration layer.

### G2. Mount Points
- [ ] Mount point checklist is complete, usually 3-5 items by the "remove it and feature disappears" rule.
- [ ] Every mount point is a checkable wiring item: route/config/subscription/DI/entry.

### G3. Structure Health
- [ ] Threshold precheck was done for files/directories to edit.
- [ ] Threshold hits have a step 0 move-only micro-refactor with independent verification.

### G4. Execution-Phase Closure
- [ ] Medium/high complexity tasks wire in debugging script/process (`trellis-debug-systematic`) and review gate (`trellis-review-twostage`).
- [ ] Review Stage 2 is assigned to a stronger model in the role split.

---

## Pass Criteria

- All applicable checks pass or are marked `N/A` with reason.
- Full MVP Planning Gate = PASS.
- Pre-Confirmation Gate = PASS.
- `UNASSIGNED_MVP_REQ`, `UNBATCHED_TASK`, `P0P1_ONLY_PLAN`, and `DEFERRED_PRD_WITHOUT_PLAN` do not exist.

## Fail Handling

- Failed check -> mark as issue.
- Generate issue list: location, description, impact, suggested fix.
- Apply targeted improvements and enter the next review round.

## Convergence Conditions

- All checks pass and Full MVP Planning Gate / Pre-Confirmation Gate both PASS -> enter user confirmation.
- Two consecutive rounds with no new issue but Gate still FAIL -> do not auto-pass; continue planning or block.
- More than 5 rounds still failing -> ask the user to choose stronger model, manual intervention, or risk acceptance.
