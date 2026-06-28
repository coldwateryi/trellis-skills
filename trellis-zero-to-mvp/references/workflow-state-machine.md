# Trellis Zero to MVP Workflow State Machine

This file defines legal state transitions for `trellis-zero-to-mvp`. Do not treat "P0/P1 is planned" as complete MVP planning.

## States

| State | Goal | Allowed Actions | Exit Condition |
| --- | --- | --- | --- |
| `S0_DISCOVER_CONTEXT` | Find source requirements, local conventions, Trellis workflow, and existing implementation evidence | Read-only scan of docs, README, AGENTS, `.trellis/spec/`, `.trellis/tasks/`, code structure | Input paths and context inventory are clear |
| `S1_REQUIREMENT_LEDGER` | Extract all source requirements and assign `REQ/AC` IDs | Output source requirement list, Full Requirement Matrix, MVP Coverage Matrix, Backlog | Requirement Ledger Gate = PASS |
| `S2_CONTRACT_LOCK` | Lock local implementation contracts | Output Project Contract Lock, Contract Snapshot, forbidden tokens, conflict table | Contract Gate = PASS |
| `S3_FULL_MVP_TASK_CANDIDATES` | Form complete MVP child task candidates | Split all MVP `TASK` coverage by capability, add dependencies, complexity, priority, small-model granularity | Every MVP `TASK` requirement has a candidate Task ID |
| `S4_PROGRESSIVE_BATCH_PLANNING` | Complete all batch PRD/design/artifact plans | Use main agent or sub-agents to produce Subtask Planning Ledger, Batch Completion Rollup, PRD drafts, artifact matrix | Every MVP child task is `READY_TO_CONFIRM`, `BLOCKED`, or `OUT_OF_SCOPE` |
| `S5_FULL_MVP_PLANNING_GATE` | Mechanically check complete planning quality | Run Full MVP Planning Gate, Batch Completeness Gate, Pre-Confirmation Gate | All three Gates PASS |
| `S6_USER_CONFIRMATION` | Ask user to confirm the complete plan | Present full task tree, all batches, Backlog, Blocked items, and Gate results | User confirms or changes scope |
| `S7_TASK_CREATION` | Create Trellis parent/child tasks | Run `task.py create`, record real directories, backfill ledger | Task Creation Gate = PASS |
| `S8_ARTIFACT_WRITING` | Write PRDs and required planning artifacts | Write parent/child `prd.md`, `design.md`, `implement.md`, JSONL | Every declared artifact exists in the real directory |
| `S9_ARTIFACT_GATE` | Validate real task artifacts | Run placeholder, JSONL, contract, granularity, and missing-artifact checks | Artifact Gate = PASS |
| `S10_NEXT_IMPLEMENTATION_RECOMMENDATION` | Recommend first executable child task | Output task tree, execution order, parallel tasks, blocked tasks, first recommended task | Development Recommendation Gate = PASS |

## Hard Transition Rules

- Before `S0`, do not fill local contracts with model common sense.
- Before `S1`, do not draft full child PRDs.
- Before `S3`, do not produce the final task tree.
- Before `S5` PASS, do not ask the user to confirm.
- Before `S6` confirmation, do not run `task.py create`.
- Before `S9` PASS, do not claim the task tree is executable.
- Enter `S10` only after complete planning and Artifact Gate both PASS.

## Subtask Planning Ledger Status

| Status | Meaning | Terminal |
| --- | --- | --- |
| `CANDIDATE` | Candidate task found, but boundary/dependency/artifacts not frozen | No |
| `DRAFTED` | PRD/design draft exists but full planning Gate has not passed | No |
| `READY_TO_CONFIRM` | Boundary, REQ coverage, dependencies, acceptance, and artifact needs are frozen | Planning terminal |
| `USER_CONFIRMED` | User confirmed this task is in creation scope | No |
| `CREATED` | `task.py create` created a real directory and ledger is backfilled | No |
| `ARTIFACTS_WRITTEN` | All declared planning artifacts were written | No |
| `GATED_PASS` | Artifact Gate passed | Creation terminal |
| `BLOCKED` | Has explicit blocker, recovery condition, and owner | Terminal |
| `OUT_OF_SCOPE` | In Backlog, not created for current MVP | Terminal |

User confirmation condition:

```text
forall task in Subtask Planning Ledger:
  task.status in [READY_TO_CONFIRM, BLOCKED, OUT_OF_SCOPE]
```

Development recommendation condition:

```text
forall in-scope created task:
  task.status in [GATED_PASS, BLOCKED, OUT_OF_SCOPE]
```

## Batch Rules

- P0/P1 is priority, not planning completeness.
- B01/B02/B03 are planning batches, not scope cuts.
- Every MVP `TASK` child task must have a batch.
- If only B01 or P0/P1 is complete, output `BATCH_INCOMPLETE` and continue the next batch.
- Later batches may lack real directories before creation, but cannot lack Task ID, REQ coverage, dependencies, complexity, PRD draft, and artifact needs.
