# Self-Review Report Template

Use this template to record each self-review round.

---

## Self-Review Report (Round N)

**Review Time**: YYYY-MM-DD HH:MM  
**Review Target**: [requirements document name]  
**Round**: N

---

## 1. Overall Score

| Dimension | Score | Notes |
| --- | --- | --- |
| 0. Project Contract and Workflow | Pass / Fail | [Project Contract Profile, Contract Lock, workflow, artifact requirements] |
| A. Requirement Completeness | Pass / Fail | [summary] |
| B. Task Split Quality | Pass / Fail | [summary] |
| C. PRD and Artifact Quality | Pass / Fail | [summary] |
| D. Small Model Friendliness | Pass / Fail | [summary] |
| E. Development Recommendation Threshold | Pass / Fail | [summary] |
| F. Artifact Gate Readiness | Pass / Fail | [placeholder, JSONL, contract, external config scan plan] |
| G. Progressive Planning and Gates | Pass / Fail | [Subtask Planning Ledger, batch completeness, confirmation threshold] |

**Overall Conclusion**: Pass / Fail

---

## 2. Checklist Status

### 0. Project Contract and Workflow
- [x] 0.0 Project Contract - pass
- [x] 0.1 Workflow discovery - pass
- [x] 0.2 Spec freshness - pass
- [x] 0.3 Planning artifacts - pass
- [x] 0.4 Existing implementation retrofit - pass
- [x] 0.5 State machine and Gates - pass

### A. Requirement Completeness
- [x] Requirement IDs and AC IDs - pass
- [x] Full Requirement Matrix and MVP Coverage Matrix - pass
- [x] Backlog and out-of-scope traceability - pass
- [ ] Boundary conditions - fail (see issue 1)
- [x] Error handling - pass

### B. Task Split Quality
- [x] Split principles - pass
- [ ] Complexity assessment - fail (see issue 2)
- [x] Dependencies - pass
- [x] Priority and batch assignment - pass
- [x] Subtask Planning Ledger - pass

### C. PRD and Artifact Quality
- [ ] Placeholder elimination - fail (see issue 3)
- [x] Reference implementation - pass
- [ ] File Manifest / implement.md boundary - fail (see issue 4)
- [ ] Implementation Steps / implement.md boundary - fail (see issue 5)
- [x] Acceptance criteria - pass
- [x] Self-check commands - pass
- [x] Automated tests - pass

### D. Small Model Friendliness
- [ ] Decision points pinned - fail (see issue 6)
- [x] Copy-example feasibility - pass
- [x] Forbidden list - pass
- [x] Tool constraints - pass
- [x] Context and design shift-left - pass
- [x] Artifact Gate - pass

### E. Development Recommendation Threshold
- [x] Pre-Confirmation Gate - pass
- [x] Artifact Gate readiness - pass
- [x] Development Recommendation Gate rule - pass

---

## 3. Issues

### Issue 1: [Category: A Boundary Conditions] [Severity: High]

**Location**: REQ-003

**Problem**:
- Empty input behavior is missing.
- Oversized input behavior is missing.
- Duplicate input error message is missing.

**Impact**:
- Execution model may invent behavior.
- Acceptance cannot be verified deterministically.

**Suggested Fix**:
Add exact boundary behavior, error code, and error message.

---

### Issue 2: [Category: B Complexity Assessment] [Severity: Medium]

**Location**: Task T03

**Problem**:
- Marked medium but includes callbacks, transactions, and idempotency.

**Impact**:
- Small model may fail or hallucinate state handling.

**Suggested Fix**:
Split into smaller tasks or require `design.md` + `implement.md` + JSONL and pin every branch.

---

### Issue 3: [Category: C Placeholder Elimination] [Severity: High]

**Location**: Task T05 `implement.md`, ordered step 2

**Problem**:
- Contains unresolved placeholders such as `<ControllerClass>` or `<method>`.

**Impact**:
- Execution model cannot know exact file or method.

**Suggested Fix**:
Replace placeholders with concrete paths, names, and method signatures.

---

### Issue 4: [Category: C File Manifest / implement.md Boundary] [Severity: High]

**Location**: Task T04 `implement.md`, File Plan

**Problem**:
- File plan says "modify service layer files" without exact paths.

**Impact**:
- Execution model may edit wrong files.

**Suggested Fix**:
List every file and exact modification location.

---

### Issue 5: [Category: C Implementation Steps / implement.md Boundary] [Severity: High]

**Location**: Task T06 `implement.md`, Ordered Steps

**Problem**:
- Step is an abstract goal such as "implement state machine logic".

**Impact**:
- Execution model must re-design the behavior.

**Suggested Fix**:
Break into exact enum/state definitions, transition rules, files, and verification commands.

---

### Issue 6: [Category: D Decision Points Pinned] [Severity: Medium]

**Location**: Task T08 `implement.md`

**Problem**:
- Leaves exception handling "based on business logic".

**Impact**:
- Error semantics may diverge from project conventions.

**Suggested Fix**:
Pin the exact exception class, message, status code, and branch.

---

## 4. Statistics

- Total checks: <n>
- Passed: <n>
- Failed: <n>
- N/A: <n>
- Pass rate: <percent>

Issue distribution:

- High: <n>
- Medium: <n>
- Low: <n>

**Expected Artifact Gate Output**:

- `scanned_tasks`: <n>
- `jsonl_mode`: <required/optional/inline>
- `placeholder_hits`: <n>
- `angle_placeholder_hits`: <n>
- `jsonl_seed_hits`: <n>
- `jsonl_seed_hits_raw`: <n>
- `forbidden_token_hits`: <n>
- `contract_mismatch_hits`: <n>
- `coverage_count_mismatch_hits`: <n>
- `high_complexity_missing_artifacts`: <n>
- `missing_declared_artifacts`: <n>
- `declared_gate_mismatch_hits`: <n>
- `external_config_hits`: <n>
- `mechanical_gate_evidence`: <script command or equivalent command output>
- `result`: PASS / FAIL

**Planning Gate Output**:

- `requirement_ledger_gate`: PASS / FAIL
- `contract_gate`: PASS / FAIL
- `full_mvp_planning_gate`: PASS / FAIL
- `batch_completeness_gate`: PASS / FAIL
- `pre_confirmation_gate`: PASS / FAIL
- `development_recommendation_gate`: PASS / FAIL
- `failure_codes`: []

---

## 5. Conclusion and Next Action

**This round meets standards**: Yes / No

If No:
- Fix issues listed above.
- Preserve passing sections.
- Rerun Gates.

If Yes:
- Proceed only to the next legal state in `workflow-state-machine.md`.
