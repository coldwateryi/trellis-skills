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
| C. PRD Quality | Pass / Fail | [summary] |
| D. Small Model Friendliness | Pass / Fail | [summary] |
| E. Risk Identification | Pass / Fail | [summary] |
| F. Artifact Gate Readiness | Pass / Fail | [placeholder, JSONL, contract, design surface, external config scan plan] |
| G. Progressive Planning and Gates | Pass / Fail | [Subtask Planning Ledger, batch completeness, confirmation threshold, development recommendation threshold] |

**Overall Conclusion**: Pass / Fail

---

## 2. Checklist Status

### 0. Project Contract and Workflow
- [x] 0.0 Project Contract Lock - pass
- [x] 0.1 Workflow discovery - pass
- [x] 0.2 Spec freshness - pass
- [x] 0.3 Planning artifacts - pass
- [x] 0.4 Existing implementation retrofit - pass
- [x] 0.5 State machine and Gates - pass

### A. Requirement Completeness
- [x] A1. Requirement identity - pass
- [x] A1.1 Source requirement coverage - pass
- [x] A2. Requirement clarity - pass
- [ ] A3. Boundary conditions - fail (see issue 1)
- [x] A4. Error handling - pass

### B. Task Split Quality
- [x] B1. Split principles - pass
- [ ] B2. Complexity assessment - fail (see issue 2)
- [x] B3. Dependencies - pass
- [x] B4. Priority - pass
- [x] B5. Progressive Planning Ledger - pass

### C. PRD Quality
- [ ] C1. Placeholder elimination - fail (see issues 3, 4)
- [x] C2. Reference implementation - pass
- [ ] C3. File Manifest / implement.md boundary - fail (see issue 5)
- [ ] C4. Implementation Steps / implement.md boundary - fail (see issue 6)
- [x] C5. Acceptance criteria - pass
- [x] C6. Self-check commands - pass
- [x] C7. Automated tests - pass

### D. Small Model Friendliness
- [ ] D1. Decision points pinned - fail (see issue 7)
- [x] D2. Copy-example feasibility - pass
- [x] D3. Forbidden list - pass
- [x] D4. Tool constraints - pass
- [x] D5. Context and design shift-left - pass
- [x] D6. Artifact Gate - pass
- [x] D7. Development Recommendation Threshold - pass

### E. Risk Checks
- [x] E1. Risk identification - pass
- [x] E2. Out of Scope clarity - pass

### F. Post-Creation Artifact Gate Readiness
- [x] Project Contract Check is defined
- [x] Small Model Grain Check is defined
- [x] Placeholder and JSONL seed scans are defined
- [x] External config scan is defined
- [x] `FAIL` blocking rule is defined
- [x] Design Surface Gate is defined

---

## 3. Issues

### Issue 1: [Category: A3 Boundary Conditions] [Severity: High]

**Location**: REQ-003

**Problem**:
- Empty input behavior is missing.
- Oversized input behavior is missing.
- Duplicate input error message is missing.

**Impact**:
- Small model may invent inconsistent behavior.
- Boundary behavior cannot be verified deterministically.

**Suggested Fix**:
Add exact boundary behavior, error code, and error message.

---

### Issue 2: [Category: B2 Complexity Assessment] [Severity: Medium]

**Location**: Task T03

**Problem**:
- Marked medium but includes callbacks, transaction consistency, and idempotency.

**Impact**:
- Small model may fail or hallucinate state handling.

**Suggested Fix**:
- Split into smaller tasks, or require `design.md` + `implement.md` + JSONL and pin every branch.

---

### Issue 3: [Category: C1 Placeholder Elimination] [Severity: High]

**Location**: Task T05 `implement.md`, ordered step 2

**Problem**:
- Contains unresolved placeholders such as `<ControllerClass>` or `<method>`.

**Impact**:
- Execution model cannot know exact file or method.

**Suggested Fix**:
- Replace placeholders with concrete paths, names, and method signatures.

---

### Issue 4: [Category: C1 Placeholder Elimination] [Severity: Medium]

**Location**: Task T07 child PRD, Technical Notes

**Problem**:
- References `<similar implementation>` instead of a concrete path.

**Impact**:
- Execution model cannot know which file to copy.

**Suggested Fix**:
- Replace with a concrete reference implementation path and replacement notes.

---

### Issue 5: [Category: C3 File Manifest / implement.md Boundary] [Severity: High]

**Location**: Task T04 `implement.md`, File Plan

**Problem**:
- File plan says "modify service layer files" without exact paths.

**Impact**:
- Execution model may edit wrong files.

**Suggested Fix**:
- List every file and exact modification location.

---

### Issue 6: [Category: C4 Implementation Steps / implement.md Boundary] [Severity: High]

**Location**: Task T06 `implement.md`, Ordered Steps

**Problem**:
- Step is an abstract goal such as "implement state machine logic".

**Impact**:
- Execution model must re-design behavior.

**Suggested Fix**:
- Break into exact enum/state definitions, transition rules, files, and verification commands.

---

### Issue 7: [Category: D1 Decision Points Pinned] [Severity: Medium]

**Location**: Task T08 `implement.md`

**Problem**:
- Leaves exception handling "based on business logic".

**Impact**:
- Error semantics may diverge from project conventions.

**Suggested Fix**:
- Pin exact exception class, message, status code, and branch.

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
- `forbidden_token_hits`: <n>
- `contract_mismatch_hits`: <n>
- `coverage_count_mismatch_hits`: <n>
- `high_complexity_missing_artifacts`: <n>
- `missing_declared_artifacts`: <n>
- `design_surface_prd_without_matrix`: <n>
- `design_surface_missing_hits`: <n>
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

- [ ] Pass: can enter user confirmation because Full MVP Planning Gate and Pre-Confirmation Gate are both PASS.
- [ ] Fail: needs Round N+1 improvement.
- [ ] Warning: checklist has no new issues but Gate still fails; do not request confirmation automatically. Continue planning next batch or block.

**Reason**: <summary>

**Next actions**:
1. Fix issues listed above.
2. Run self-review Round N+1.
3. If Round N+1 still has issues, keep improving.
4. If two consecutive rounds have no new issue but any Gate still fails, continue planning next batch or block; do not auto-pass.

---

## 6. Improvement Tracking

### Fixed in This Round (from Previous Round)

- Issue X (Round N-1): <problem>
  - Fix: <fix>
  - Verification: <check passed>

### New Issues This Round

- Issue 1-N (see above)

---

**Reviewer**: [model name + version]
**Next Review Plan**: immediately after improvements
