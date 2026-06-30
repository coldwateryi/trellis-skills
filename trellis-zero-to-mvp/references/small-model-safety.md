# Small Model Long-Run Safety

Use this when local/small or medium parameter models perform long Trellis planning. The goal is to reduce hallucination, state drift, and self-certified PASS results.

## Goal

Break long reasoning into recoverable short phases. The model drafts from current phase inputs; counts, file existence, placeholder hits, JSONL seeds, contract hits, and Gate results must come from mechanical scans or explicit table statistics.

## Stage State Packet

Before entering a new phase, recovering context, calling a sub-agent, or writing task directories, output and verify:

```yaml
stage_state:
  state: S0_DISCOVER_CONTEXT | S1_REQUIREMENT_LEDGER | S2_CONTRACT_LOCK | S3_FULL_MVP_TASK_CANDIDATES | S4_PROGRESSIVE_BATCH_PLANNING | S5_FULL_MVP_PLANNING_GATE | S6_USER_CONFIRMATION | S7_TASK_CREATION | S8_ARTIFACT_WRITING | S9_ARTIFACT_GATE | S10_NEXT_IMPLEMENTATION_RECOMMENDATION
  source_docs:
    - <path>
  contract_snapshot: <present/missing/path>
  full_requirement_count: <number or unknown>
  mvp_coverage_counts:
    TASK: <n>
    MERGED: <n>
    BASELINE: <n>
    OUT_OF_SCOPE: <n>
    BLOCKED: <n>
  subtask_ledger:
    total_mvp_tasks: <n>
    ready_to_confirm: <n>
    blocked: <n>
    out_of_scope: <n>
    non_terminal: <n>
  current_batch: <Bxx or none>
  next_legal_action: <one action>
  stop_gate_failures:
    - <none or failure codes>
```

Rules:

- `unknown` is allowed only during discovery; before Gates it must be replaced with mechanical statistics.
- `next_legal_action` must be exactly one action, preventing the model from creating tasks, writing artifacts, and recommending development at the same time.
- If `stop_gate_failures` is non-empty, do not continue to the next phase.

## Context Budget

- Do not load the entire source document, parent PRD, all child PRDs, and old task outputs into a small model at once.
- Each sub-agent or serial simulation step receives only relevant REQ rows, Contract Snapshot, dependency boundaries, and output format.
- After each batch, the main agent rereads state from Subtask Planning Ledger rather than relying on previous natural-language memory.
- More than 5 child PRDs or 3 business domains require Agent Packets; if sub-agents are unavailable, run packets serially and mark `agent_mode: unavailable_fallback_serial`.

### Context Budget Table (Per-Model Capacity)

The following table applies to Qwen3.6 35B (128K context window). Adjust per phase according to project complexity.

| Phase | Budget | Contains | Strategy |
|:---|:---|:---|:---|
| S0 Discovery | ≤20K tokens | README + key code structure + `.trellis/` metadata | Read only directory trees and file headers; do not read full source files |
| S1 Requirements | ≤15K tokens | Source requirements doc + Full Requirement Matrix template | Read requirements once, output matrix, then write intermediate results to file immediately |
| S2 Contract Lock | ≤8K tokens | README + spec key lines + Contract Lock template | Read only contract-relevant sections; skip unrelated modules |
| S3 Task Candidates | ≤10K tokens | MVP Coverage Matrix + Small Model granularity rules | Consider one business domain at a time |
| S4 Batch Planning | ≤10K tokens/batch | Batch Task ID range + Contract Snapshot + PRD template | Write to `.trellis/planning/` filesystem after each batch |
| S5 Gate | ≤5K tokens | Matrices + ledger + Gate definitions | Check only, do not generate new content |
| S6 User Confirmation | ≤4K tokens | Summary + Gate results | Show final data only, no reasoning |
| S7 Task Creation | ≤6K tokens | Ledger + task.py commands | Create one task at a time, no parallel |
| S8 Artifact Writing | ≤8K tokens/task | Corresponding template + Contract Snapshot | Write one task's PRD/design/implement at a time |
| S9 Artifact Gate | ≤4K tokens | trellis_zero_gate.py output | Read script output only, do not hand-fill Gate values |
| Self-Review (any round) | ≤6K tokens | Current-phase checklist items | Read only current-phase section (≤10 items) |
| Single Drift Reset | ≤6K tokens | Matrices + ledger + real directories | Rebuild state from files only, no memory |

### Phase Capacity Warning

When any threshold below is reached, stop the current phase, write intermediate artifacts to `.trellis/planning/`, then proceed to the next phase:

- Current phase context consumption > 80% of budget
- More than 8 task candidates identified but batch planning not started
- More than 5 PRD drafts per batch but not yet written to files
- More than 10,000 tokens generated continuously without a Gate check

## Evidence Discipline

The following conclusions require evidence paths or command output summaries:

- Requirement counts and coverage counts.
- Child task counts, batch counts, and each batch's remaining non-terminal count.
- Whether `design.md` / `implement.md` are required and whether they exist.
- Whether JSONL still contains `_example`.
- Whether placeholder and forbidden-token hits are zero.
- Whether Artifact Gate is PASS.

Forbidden:

- Using "checked", "looks consistent", or "should be fine" as Gate evidence.
- Hand-filling `jsonl_seed_hits = 0` or `result = PASS` without mechanical scanning.
- Recommending development while any failure exists.

## Mechanical Artifact Gate

After task creation and artifact writing, run:

```bash
python <skill-dir>/scripts/trellis_zero_gate.py \
  --tasks .trellis/tasks \
  --parent-task-json <parent-task-dir>/task.json \
  --parent-prd <parent-task-dir>/prd.md \
  --jsonl-mode <required|optional|inline>
```

Add Contract Snapshot checks as needed:

```bash
  --forbidden-token '<token>'
  --forbidden-regex '<regex>'
  --contract-mismatch-regex '<regex>'
```

If script `result` is not `PASS`, output failure codes and a fix list; do not claim the task tree is executable.

## Drift Reset

Immediately rebuild Stage State Packet and return to the nearest legal state when:

- The model starts using names, paths, APIs, routes, commands, tables, or package/module names absent from Contract Snapshot.
- Requirement count, TASK count, or child task count changes without merge/split records.
- The model asks for user confirmation after planning only P0/P1.
- Parent PRD Gate results differ from mechanical scan results.
- A child PRD declares design/implementation artifacts but the real directory lacks them.

During reset, read only factual sources: source requirements, Contract Snapshot, Full Requirement Matrix, MVP Coverage Matrix, Subtask Planning Ledger, real task directories, and mechanical Gate output.

## Per-Phase Atomic Checklists (≤10 items each)

At the end of each phase, check the corresponding list. Record results in Stage State Packet's `stop_gate_failures`.

### S0 Discovery Phase
- [ ] Source requirements document located, path confirmed
- [ ] README/module README/AGENTS read (if present)
- [ ] `.trellis/workflow.md`, `.trellis/config.yaml`, `.trellis/.version` checked
- [ ] Existing code/test structure scanned (non-empty repos)
- [ ] No child task PRDs drafted yet
- [ ] Level 1 reference files read
- [ ] `trellis_planning_gate.py --phase S1_REQUIREMENT_LEDGER` run with PASS result

### S1 Requirement Ledger Phase
- [ ] Every source requirement has REQ-xxx
- [ ] Full Requirement Matrix row count = source requirement count
- [ ] MVP Coverage Matrix five-class sum = Full Requirement Matrix row count
- [ ] All OUT_OF_SCOPE requirements entered Backlog
- [ ] Contract Profile selected with evidence
- [ ] No Trellis tasks created
- [ ] No full child PRDs drafted yet
- [ ] `trellis_planning_gate.py --phase S2_CONTRACT_LOCK` run with PASS result

### S2 Contract Lock Phase
- [ ] Contract Lock output with adopted values and evidence for all applicable fields
- [ ] Contract Snapshot output with forbidden_tokens
- [ ] Non-applicable fields written as `not-applicable`
- [ ] No unresolved `CONTRACT_CONFLICT` (if present, confirmation is blocked)
- [ ] Task splitting and PRD drafting not yet started
- [ ] Contract Gate = PASS

### S3 Task Candidate Phase
- [ ] All MVP `TASK` requirements have target Task IDs
- [ ] Each Task ID has complete fields (title, dependency, priority, complexity)
- [ ] Small Model Mode: one task = one entity CRUD / one endpoint group / one state transition / one page / one aggregate query
- [ ] High-complexity tasks split into low/medium (or designated design.md + implement.md)
- [ ] Model did not self-exempt oversized tasks using "strongly coupled" or "same flow" as excuse
- [ ] Subtask Planning Ledger output
- [ ] `trellis_planning_gate.py --phase S3_FULL_MVP_TASK_CANDIDATES` run with PASS result

### S4 Batch Planning Phase
- [ ] Batch ≤8 executable tasks, ≤5 full PRDs
- [ ] PRD drafts frozen to READY_TO_CONFIRM
- [ ] No P0P1_ONLY_PLAN (P2/P3 tasks also planned)
- [ ] Later batches not "to be planned"; have frozen task boundaries, REQ coverage, dependencies, complexity, and artifact needs
- [ ] Child PRDs include Task Impact Matrix
- [ ] `trellis_planning_gate.py --phase S4_PROGRESSIVE_BATCH_PLANNING` run after each batch

### S5 Gating Phase
- [ ] Full MVP Planning Gate = PASS
- [ ] Batch Completeness Gate = PASS
- [ ] Pre-Confirmation Gate = PASS
- [ ] All MVP TASK tasks status ∈ {READY_TO_CONFIRM, BLOCKED, OUT_OF_SCOPE}
- [ ] No UNASSIGNED_MVP_REQ, UNBATCHED_TASK, P0P1_ONLY_PLAN, DEFERRED_PRD_WITHOUT_PLAN
- [ ] No placeholders in parent/child PRD drafts
- [ ] `trellis_planning_gate.py --phase S5_FULL_MVP_PLANNING_GATE` run with PASS result

### Monotonic Convergence Protection

**If 2 consecutive self-review rounds find the exact same unfixed issues:**
1. Output `STALLED_CONVERGENCE`
2. Stop the current path
3. Recommend user switch to stronger model or manual intervention
4. Record all attempted fix rounds (round number and approach tried for each issue)
