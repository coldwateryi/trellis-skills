# Self-Review Checklist (MVP to Delivery Phase)

This checklist evaluates whether MVP gap audit output meets the requirements for execution by small parameter models (e.g., qwen3.6 35b).

## Usage

1. After completing each round of gap audit, check against this list item by item
2. All check items must pass (or be marked "N/A") before proceeding to user confirmation
3. If any items fail, mark specific issues and perform targeted improvements

---

## A. Requirements Traceability Matrix Quality Check

### A1. Status Determination Accuracy
- [ ] Every requirement has clear status (DONE/PARTIAL/MISSING/UNTESTED/UNCLEAR)
- [ ] DONE requirements have implementation and test evidence
- [ ] UNTESTED requirements have implementation evidence and clear test gaps
- [ ] PARTIAL requirements explain what's done and what's missing
- [ ] MISSING requirements truly lack implementation evidence
- [ ] UNCLEAR requirements provide blocking issues or ambiguity explanations

### A2. Evidence Completeness
- [ ] Related code lists specific file paths (not "related implementation")
- [ ] Existing tests list specific test class and method names
- [ ] Gap descriptions are specific (not "partially unimplemented")
- [ ] Each DONE requirement has corresponding code and test references

### A3. Gap Identification Completeness
- [ ] Feature implementation gaps identified
- [ ] Test coverage gaps identified
- [ ] Boundary condition handling gaps identified
- [ ] Error handling gaps identified

---

## B. MVP Completion Assessment Check

### B1. Statistics Accuracy
- [ ] Completed requirements count accurate
- [ ] Partially completed requirements count accurate
- [ ] Unimplemented requirements count accurate
- [ ] Implemented but untested requirements count accurate
- [ ] Unclear requirements count accurate
- [ ] Percentage calculations correct

### B2. Completion Judgment
- [ ] MVP completion judgment based on evidence, not subjective estimate
- [ ] Critical feature gaps clearly identified
- [ ] Test coverage deficiencies clearly identified

---

## C. Gap-Closing Task Split Quality Check

### C1. Split Principles
- [ ] One task closes one group of tightly related gaps
- [ ] Foundation contracts and UI display separated (unless inseparable)
- [ ] Feature implementation and final validation separated
- [ ] Each feature task includes its own basic tests
- [ ] No tasks split by file

### C2. Complexity Assessment
- [ ] Every task annotated with complexity (low/medium/high)
- [ ] Complexity based on small model capability
- [ ] High complexity tasks split or have detailed steps

### C3. Dependencies
- [ ] Dependencies clearly listed
- [ ] No circular dependencies
- [ ] Test tasks depend on their tested feature tasks
- [ ] Final validation task depends on all feature tasks

### C4. Priority
- [ ] Every task assigned priority (P0/P1/P2/P3)
- [ ] Blocking gaps have high priority
- [ ] Test gap tasks have reasonable priority

---

## D. Delivery Task PRD Quality Check (Critical!)

### D1. Placeholder Elimination
- [ ] No `<...>` placeholders in PRD
- [ ] No abstract terms like "specific path", "related files"
- [ ] No reasoning gaps like "as needed"

### D2. Current Gap Description
- [ ] Current status clear (DONE/PARTIAL/MISSING/UNTESTED/UNCLEAR)
- [ ] Evidence section lists specific code and test paths
- [ ] Gap section specifically states what's missing
- [ ] Risk section explains why it's important

### D3. Reference Implementation
- [ ] If similar implementation exists in MVP, points to specific file path
- [ ] If no similar implementation, states "None, implement from scratch"
- [ ] Replacement instructions specific
- [ ] Not vague like "refer to MVP related code"

### D4. File Manifest
- [ ] Lists all files, precise to full path
- [ ] Each file annotated with operation type
- [ ] Modify operations specify exact location
- [ ] If data structure changes, includes complete field table

### D5. Implementation Steps
- [ ] Steps are ordered
- [ ] Each step is concrete action, not abstract goal
- [ ] Each step independently verifiable
- [ ] Bug fix branch choices pinned down
- [ ] Reasoning decisions pinned down

### D6. Implementation Scope
- [ ] Behavior constraints as decidable assertions
- [ ] Boundary condition exact behavior specified
- [ ] Error handling exact behavior specified
- [ ] Compatibility requirements specified (don't break MVP behavior)

### D7. Acceptance Criteria
- [ ] Criteria are decidable assertions
- [ ] Includes requirement ID reaching expected status
- [ ] Includes normal path acceptance
- [ ] Includes exception path acceptance
- [ ] Includes boundary condition acceptance
- [ ] Includes not breaking MVP behavior acceptance

### D8. Self-Check Commands
- [ ] Provides directly executable commands
- [ ] Commands are specific
- [ ] Commands include expected result
- [ ] No human judgment required

### D9. Automated Tests Required
- [ ] Lists required test types
- [ ] Each test point specific
- [ ] Regression Tests cover MVP existing behavior
- [ ] Not abstract like "add necessary tests"

---

## E. Small Model Execution Friendliness Check

### E1. Decision Points Pinned
- [ ] All annotation choices specified
- [ ] All branch choices specified (including bug fix branches)
- [ ] All naming rules specified
- [ ] All table structure changes specified

### E2. MVP Reuse Guidance Clear
- [ ] Which MVP code to reuse is clear
- [ ] Which MVP code to extend is clear (extend what)
- [ ] Which MVP code to modify is clear (where, how)
- [ ] Constraints on not breaking MVP behavior are clear

### E3. Forbidden List
- [ ] Lists what not to do
- [ ] Specifies MVP behaviors that cannot be broken
- [ ] Specifies file modification scope
- [ ] Specifies dependency constraints

### E4. Tech Stack and Tool Constraints
- [ ] Frameworks/libraries listed
- [ ] Build commands specified
- [ ] Test commands specified (including regression tests)

---

## F. Test Coverage Planning Check

### F1. Test Mapping Completeness
- [ ] Each requirement (REQ-xxx) maps to at least one test
- [ ] Each acceptance criterion (AC-xxx) maps to at least one test
- [ ] Test type distribution reasonable (unit/integration/e2e/smoke/regression)

### F2. Regression Test Requirements
- [ ] MVP existing behaviors have regression test coverage
- [ ] Regression tests specific (test what, expect what)
- [ ] Not abstract like "ensure not breaking existing features"

---

## G. Bug Classification and Handling Check

### G1. Bug Classification Accuracy
- [ ] Each discovered bug has clear classification
- [ ] Classification based on whether it blocks current requirement acceptance
- [ ] Blocking bugs planned for current task fix
- [ ] Non-blocking bugs documented as risk or separate task created

### G2. Bug Fix Planning
- [ ] Blocking bug fix steps specified
- [ ] Bug fix branch logic pinned down
- [ ] Bug fix verification methods specified
- [ ] Non-blocking bug risks documented

---

## H. Risk Point Check

### H1. Risk Identification
- [ ] High-risk modules annotated
- [ ] MVP change compatibility risks identified
- [ ] Test coverage deficiency risks identified
- [ ] Technical debt recorded in Out of Scope

### H2. Out of Scope Clarity
- [ ] Lists explicitly excluded features
- [ ] Lists points that cannot be pinned (if any)
- [ ] Not vague like "other features"
- [ ] Deferred non-blocking bugs recorded in Out of Scope

---

## Convergence Conditions

- All check items pass → proceed to user confirmation
- 2 consecutive rounds with no new issues → auto-pass
- Still have issues after 5 rounds → prompt user choice
