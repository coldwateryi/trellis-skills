# Self-Review Checklist

Use this checklist to evaluate whether read-only planning is executable by small/local models such as qwen3.6 35b.

## Usage

1. After each read-only analysis round, check this list item by item.
2. All applicable checks must pass, and Full MVP Planning Gate plus Pre-Confirmation Gate must be `PASS`, before user confirmation.
3. Failed items become precise issues with targeted fixes.

## 0. Trellis 0.6+ Workflow Fit

### 0.0 Project Contract
- [ ] User requirements, README/module README, AGENTS.md, `.trellis/spec/`, and code conventions were read.
- [ ] Project Contract Profile is selected with evidence and rejected-profile reasons.
- [ ] Project Contract Lock exists; applicable profile fields have adopted values and evidence paths.
- [ ] Non-applicable fields are `not-applicable`; RuoYi/Java fields are not applied to unrelated projects.
- [ ] `CONTRACT_CONFLICT` blocks confirmation until resolved.
- [ ] Child candidates follow Project Contract Lock.
- [ ] No task mixes two naming/path/API/command systems.
- [ ] Contract Snapshot and forbidden tokens exist, with evidence.
- [ ] Draft PRD/design/implement/JSONL are clean of forbidden tokens.

### 0.1 Workflow Discovery
- [ ] `.trellis/workflow.md` was read when present.
- [ ] `.trellis/config.yaml`, `.trellis/.version`, `.trellis/.developer` were checked when present.
- [ ] Analysis states legacy PRD-only vs Trellis 0.6+ artifact workflow.
- [ ] `codex.dispatch_mode` was read; inline/sub-agent/optional JSONL Gate mode is distinguished.
- [ ] Developer identity setup uses `trellis init -u <name>` first; `init_developer.py` is legacy fallback only.

### 0.2 Spec Freshness
- [ ] Relevant `.trellis/spec/` files are listed.
- [ ] Spec freshness is fresh/stale/missing/unknown.
- [ ] Stale or missing specs become spec-refresh/bootstrap task or blocker.

### 0.3 Planning Artifacts
- [ ] Every task states required artifacts: `prd.md`, `design.md`, `implement.md`, `implement.jsonl`, `check.jsonl`.
- [ ] Planning artifact matrix exists and supports post-creation file existence checks.
- [ ] Medium/high complexity tasks include design and implementation artifacts or are split smaller.
- [ ] High complexity is not PRD-only.
- [ ] Stable-context preload needs JSONL context manifests.
- [ ] Detailed file plan, ordered steps, self-check commands, failure recovery, and review gates are in `implement.md`; low-complexity PRD-only exception has evidence.

### 0.4 Existing Implementation Retrofit
- [ ] Existing Implementation Baseline exists for non-empty repos.
- [ ] Baseline entries include exact code and test evidence, or explicitly state missing tests.
- [ ] Source requirements remain source of truth.
- [ ] `DONE` requirements do not create implementation tasks.
- [ ] `UNTESTED` requirements create only test coverage tasks.
- [ ] `PARTIAL` requirements create only gap-closing tasks.
- [ ] `MISSING` requirements create new implementation tasks.
- [ ] Requirement rows have matching actions: `none`, `test-only`, `gap-task`, `new-task`, `clarify`.
- [ ] Existing dependencies use `existing:<path-or-capability>`.
- [ ] Task paths use real `task.py create` directories, not logical IDs/slugs.

### 0.5 State Machine and Gates
- [ ] `workflow-state-machine.md` and `gate-definitions.md` were read.
- [ ] Current output names state S0-S10 and next state.
- [ ] Requirement Ledger Gate, Contract Gate, Full MVP Planning Gate, Batch Completeness Gate, and Pre-Confirmation Gate have PASS/FAIL, failure codes, and evidence.
- [ ] If any Gate fails, there is no user confirmation request, no task creation, and no development recommendation.

## A. Requirement Completeness

- [ ] Every source requirement has unique stable REQ-xxx.
- [ ] Every acceptance criterion has AC-xxx.
- [ ] Full Requirement Matrix and MVP Coverage Matrix are separate.
- [ ] MVP coverage counts are not reported as source requirement count.
- [ ] Parent PRD coverage summary comes from mechanical MVP Coverage Matrix counts.
- [ ] Every `REQ-xxx` has coverage status: TASK/MERGED/BASELINE/OUT_OF_SCOPE/BLOCKED.
- [ ] `MERGED`, `BASELINE`, and `OUT_OF_SCOPE` rows have target/evidence/reason.
- [ ] All `OUT_OF_SCOPE` rows are in Backlog.
- [ ] No source requirement disappears from traceability.
- [ ] Requirements avoid vague terms: TBD, as needed, depends, etc.
- [ ] Boundary conditions, error cases, and response/error structures are concrete.

## B. Task Split Quality

- [ ] Each child task is an independently verifiable capability.
- [ ] No file-based or time-based task split.
- [ ] Task merge/split record is complete.
- [ ] Full platform scope vs MVP boundary is explicit.
- [ ] Small Model Mode: one entity CRUD / endpoint group / state transition / page / aggregate query per task.
- [ ] No overlarge task is kept merely because it is "coupled" unless user explicitly approved.
- [ ] Batch limits are respected; all MVP `TASK` children are planned, not just P0/P1.
- [ ] Every task has complexity, dependencies, priority, batch, and parallel group.
- [ ] No circular dependencies; baseline dependencies are separate from Trellis tasks.
- [ ] Subtask Planning Ledger and Batch Completion Rollup exist and all rows are terminal before confirmation.

## C. PRD and Artifact Quality

- [ ] PRD/design/implement/JSONL contain no unresolved placeholders or forbidden tokens.
- [ ] Child PRD Project Contract Reference matches parent Contract Lock.
- [ ] Child PRD semantic anchors match `design.md` and `implement.md`.
- [ ] Reference implementation paths are concrete or explicitly none.
- [ ] File Manifest lives in `implement.md` for Trellis 0.6+; PRD only points to implementation plan location unless PRD-only low complexity is justified.
- [ ] Implementation steps live in `implement.md` or PRD-only compact appendix.
- [ ] Self-check commands live in `implement.md`; PRD may keep acceptance-level command summary.
- [ ] Acceptance criteria are decidable and include normal, failure, and boundary paths.
- [ ] Automated test requirements are concrete.

## D. Small Model Friendliness

- [ ] All naming/path/API/command/package decisions are pinned.
- [ ] Table/schema/state/config structures are pinned.
- [ ] External config, third-party keys, maps, hardware, and protocols are fixed, baseline, blocked, or out of scope.
- [ ] Example-to-task mapping is clear.
- [ ] Forbidden list constrains files, dependencies, and contract changes.
- [ ] Build/test/lint commands are concrete.
- [ ] Context Manifest lists exact files to read before editing.
- [ ] `implement.jsonl` and `check.jsonl` contain stable context, not steps or edited source files.
- [ ] JSONL mode is `required`, `optional`, or `inline` and matches config/artifact matrix.
- [ ] Artifact Gate uses `scripts/trellis_zero_gate.py` or equivalent mechanical scan, never hand-filled.
- [ ] Artifact Gate output includes `jsonl_mode`, `forbidden_token_hits`, `contract_mismatch_hits`, `coverage_count_mismatch_hits`, `missing_declared_artifacts`, `angle_placeholder_hits`, `declared_gate_mismatch_hits`, and `external_config_hits`.

## E. Development Recommendation Threshold

- [ ] No development recommendation until Pre-Confirmation Gate, Task Creation Gate, Artifact Gate, and Development Recommendation Gate pass.
- [ ] Any `FAIL` or `PENDING` Gate blocks executable-claim output.
- [ ] Recommended first task has satisfied dependencies or only existing baselines.

## Pass Criteria

- All applicable checks pass or are marked `N/A` with reason.
- Full MVP Planning Gate and Pre-Confirmation Gate are `PASS`.
- If tasks were created, Artifact Gate and Development Recommendation Gate are `PASS`.
