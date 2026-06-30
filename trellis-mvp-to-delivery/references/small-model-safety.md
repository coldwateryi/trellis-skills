# Small Model Long-Run Safety (MVP to Delivery)

Use this when local/small or medium parameter models run multi-round MVP delivery audits. The goal is to reduce hallucination, state drift, and self-certified PASS results.

## Stage State Packet

Before entering a new phase, recovering context, calling a sub-agent, or writing `delivery-state.md`, output and verify:

```yaml
stage_state:
  state: S0_LOAD_STATE | S1_DETERMINE_LOOP | S2_DISCOVER_EVIDENCE | S3_GAP_AUDIT | S4_UPDATE_STATE | S5_PICK_BATCH | S6_CONFIRM | S7_CREATE_TASKS | S8_RUN_LOG | S9_PLAN_TESTS | S10_FINAL_ACCEPTANCE
  loop_mode: L1 | L2 | L3
  audit_scope: full | delta | early-exit
  current_round: <n>
  max_rounds: <n>
  open_gaps: <n>
  tasks_created: <n>
  tasks_completed: <n>
  carry_over: <n>
  critical_review_issues: <n>
  next_legal_action: <one action>
  stop_conditions:
    - <none or condition>
```

Rules:
- `next_legal_action` must be exactly one action.
- If `stop_conditions` is non-empty, stop the loop.

## Context Budget Table

| Phase | Budget | Strategy |
|:---|:---|:---|
| S0 Load State | ≤4K tokens | Read `.trellis/delivery-state.md` + `delivery-loop-policy.md` |
| S1 Determine Loop | ≤4K tokens | Determine full/delta/early-exit only; do not read code |
| S2 Discover Evidence | ≤12K tokens | Read source requirements + key code structure + `.trellis/tasks/` |
| S3 Gap Audit | ≤15K tokens | Output RTM + self-review; write to file immediately after |
| S4 Update State | ≤4K tokens | Write `delivery-state.md` |
| S5 Pick Batch | ≤4K tokens | Read `delivery-batch-template.md` |
| S6 Confirm | ≤4K tokens | Show summary only |
| S7 Create Tasks | ≤6K tokens | One task at a time |
| S8 Run Log | ≤2K tokens | Append one JSON line |
| S9 Plan Tests | ≤8K tokens | Read `test-coverage-matrix-template.md` |
| S10 Acceptance | ≤8K tokens | Read `final-acceptance-template.md` |

### Phase Capacity Warning

- S3 audit exceeds 8 requirements without writing intermediate results → write to file before continuing
- More than 5 open gaps after a single round without batch selection → freeze the batch first
- 2 consecutive self-review rounds with the same unfixed issues → `STALLED_CONVERGENCE`, stop

## Evidence Discipline

The following conclusions require evidence paths or command output summaries:
- Status determination for each requirement in the traceability matrix
- Code and test evidence for DONE requirements
- MVP completion percentage
- Dependencies and blocking reasons

Forbidden:
- Using "checked", "looks consistent", or "should be fine" as evidence
- Inventing completion percentages without local evidence
- Continuing while a critical review issue exists

## Drift Reset

Immediately rebuild Stage State Packet when:
- Requirement status changes without modification
- Carry-over count differs from the previous round
- Loop_mode changes without user confirmation
- Task creation count is inconsistent with batch rules

During reset, read only: `delivery-state.md`, `delivery-run-log.jsonl`, source requirements, and existing task directories.

## Per-Phase Atomic Checklists

### S0 Load State
- [ ] `.trellis/delivery-state.md` read (if exists) or planned for initialization
- [ ] `delivery-loop-policy.md` read
- [ ] Level 1 reference files read

### S1 Determine Loop Mode
- [ ] loop_mode determined (L1/L2/L3)
- [ ] audit_scope determined (full/delta/early-exit)
- [ ] First run is always L1 + full audit

### S2 Discover Evidence
- [ ] Source requirements document located
- [ ] Completed tasks in `.trellis/tasks/` read
- [ ] Existing `.trellis/delivery-state.md` and `.trellis/delivery-run-log.jsonl` read (if present)

### S3 Gap Audit (Critical)
- [ ] Every requirement in RTM has a clear status (DONE/PARTIAL/MISSING/UNTESTED/UNCLEAR)
- [ ] DONE requirements have code and test evidence
- [ ] Coverage percentage derived from mechanical statistics
- [ ] All open gaps have precise descriptions
- [ ] Cumulative carry-over count recorded
- [ ] No unresolved placeholders

### S4 Update State
- [ ] `delivery-state.md` written/updated
- [ ] `current_round` incremented
- [ ] `Next Loop Recommendation` set

### S5 Pick Batch
- [ ] At most 3 gap tasks per round
- [ ] At most 1 high-risk task per round
- [ ] No unconfirmed tasks created

## Monotonic Convergence Protection

If the audit loop finds the exact same unfixed issues for 2 consecutive rounds:
1. Output `STALLED_CONVERGENCE`
2. Stop the current path
3. Recommend the user switch to a stronger model or manual intervention
4. Record which rounds attempted fixes and what was tried