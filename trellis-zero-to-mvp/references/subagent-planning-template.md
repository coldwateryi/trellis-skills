# Batch Sub-Agent Planning Template

Use this when candidate child tasks exceed batch limits, business domains exceed 3, full PRD drafts exceed 5, or the user requests multi-agent planning. The main agent first completes Requirement Ledger Gate and Contract Gate, then dispatches read-only planning packets.

## Roles

| Role | Responsibility | Output |
| --- | --- | --- |
| `requirement-ledger-agent` | Independently review source requirement extraction completeness | Missing REQ/AC, matrix coverage gaps, Backlog omissions |
| `contract-audit-agent` | Review Project Contract Lock and Contract Snapshot | Conflicts, forbidden tokens, missing evidence paths |
| `batch-split-agent` | Split all MVP child tasks by Small Model Mode and assign batches | Task rows, B01/B02/..., dependency layers, parallel groups |
| `child-prd-agent` | Draft up to 5 high-quality child PRD drafts for one batch | PRD points, acceptance, contract reference, implementation-plan location |
| `artifact-planner-agent` | Plan design, implementation, and JSONL needs for medium/high tasks | `design.md` / `implement.md` / JSONL needs and reasons |
| `gate-check-agent` | Independently scan for Gate failures | Failure codes, evidence rows, fix actions |

## Main Agent Rules

- The main agent owns the single Subtask Planning Ledger. Sub-agents do not maintain final state.
- Sub-agent output is draft only; user confirmation, `task.py create`, real directory mapping, file writing, and Artifact Gate remain the main agent's responsibility.
- Do not average conflicting sub-agent outputs. Resolve by local context priority; if unresolved, mark `BLOCKED`.
- Do not ignore `gate-check-agent` failures; fix or block.
- If the platform has no sub-agent support, serially simulate the Agent Packets below and output `agent_mode: unavailable_fallback_serial`.

## Agent Packet Inputs

Give each sub-agent only the needed slice:

- Project Contract Lock and Contract Snapshot.
- Full Requirement Matrix rows relevant to this role or batch.
- MVP Coverage Matrix rows relevant to this role or batch.
- Relevant Existing Implementation Baseline evidence.
- Trellis workflow context.
- Allowed Task ID range, dependency boundaries, and forbidden adjacent domains.
- Output format and Gate names.

Do not leak expected answers, suspected bugs, or intended fixes to `gate-check-agent`. It should independently find issues.

## Generic Sub-Agent Prompt

```text
You are a Trellis MVP batch planning sub-agent. Do read-only planning only; do not create tasks, write files, or change REQ/AC numbering.

Inputs include Project Contract Lock, Contract Snapshot, requirement matrix slice, MVP coverage matrix slice, existing implementation baseline, Trellis workflow context, and this batch's Task ID range.

Your task:
1. Check that inputs follow Project Contract Lock.
2. Split tasks small enough for a capability-limited execution model.
3. For each task, output PRD draft points, complexity, dependencies, unlocks, and artifact needs.
4. Mark parallel groups and reasons tasks cannot run in parallel.
5. Identify conflicts that should block, move out of the batch, or return to the main agent for decision.

Output must include:
- agent_role
- batch_id
- task_rows
- prd_draft_notes
- planning_artifact_needs
- dependency_and_parallel_groups
- contract_risks
- blocking_questions
- gate_result: PASS/FAIL
- failure_codes

Forbidden:
- Create Trellis tasks
- Modify files
- Invent new names, paths, APIs, commands, packages/modules, routes, tables, or permission models
- Change REQ/AC meaning
- Pull requirements outside this batch into this batch
```

## Sub-Agent Output Table

| Task ID | REQ IDs | Title | Batch | Dependencies | Parallel Group | Complexity | PRD Draft Status | Artifact Needs | Risk | Failure Code |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T01 | REQ-001 | <title> | B01 | none | G01 | low/medium/high | draft/blocked | prd/design/implement/jsonl | <risk> | <none/code> |

## Merge Output

After merging, the main agent must update:

- Subtask Planning Ledger.
- Batch Completion Rollup.
- Planning artifact matrix.
- Gate output.
- Next batch action.
