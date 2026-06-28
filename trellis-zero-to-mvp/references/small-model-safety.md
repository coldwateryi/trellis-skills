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
