# Self-Review Checklist

This checklist evaluates whether read-only analysis output meets the requirements for execution by small parameter models (e.g., qwen3.6 35b).

## Usage

1. After completing each round of read-only analysis, check against this list item by item
2. All check items must pass (or be marked "N/A") before proceeding to user confirmation
3. If any items fail, mark specific issues and perform targeted improvements

---

## 0. Trellis 0.6 Beta Workflow Fit Check

### 0.1 Workflow Discovery
- [ ] `.trellis/workflow.md` was read when present
- [ ] `.trellis/config.yaml`, `.trellis/.version`, and `.trellis/.developer` were checked when present
- [ ] The analysis states whether the project uses legacy PRD-only tasks or Trellis 0.6 beta planning artifacts
- [ ] Developer identity setup uses `trellis init -u <name>` as the primary instruction, with `init_developer.py` only as legacy fallback

### 0.2 Spec Freshness
- [ ] Relevant `.trellis/spec/` files are listed
- [ ] Spec freshness is marked fresh/stale/missing/unknown
- [ ] Stale or missing specs become a spec-refresh/bootstrap task or blocking note

### 0.3 Planning Artifact Gate
- [ ] Every task states required artifacts (`prd.md`, `design.md`, `implement.md`, `implement.jsonl`, `check.jsonl`)
- [ ] Medium/high complexity tasks include design and implementation artifacts or are split smaller
- [ ] JSONL context manifests are required when stable specs, research notes, or external context must be preloaded before implementation/checking

### 0.4 Partial Implementation Retrofit
- [ ] If the repository is not empty, Existing Implementation Baseline is present
- [ ] Baseline entries list exact code evidence and test evidence, or explicitly state test evidence is missing
- [ ] Source requirements remain the source of truth; `.trellis/spec/` is not treated as the only requirement source
- [ ] `DONE` requirements do not create implementation tasks
- [ ] `UNTESTED` requirements create test-only tasks, not duplicated implementation tasks
- [ ] `PARTIAL` requirements create gap-closing tasks scoped only to missing behavior
- [ ] `MISSING` requirements create new implementation tasks
- [ ] Every traceability row has a Task Action matching its Current Status (`none`, `test-only`, `gap-task`, `new-task`, or `clarify`)
- [ ] Existing capabilities used as dependencies are listed as baseline dependencies such as `existing:<path-or-capability>`

---

## A. Requirements Completeness Check

### A1. Requirement Identification
- [ ] Every requirement has a unique REQ-xxx ID
- [ ] Every acceptance criterion has a unique AC-xxx ID
- [ ] ID numbering is sequential with no gaps
- [ ] Every requirement has clear status (DONE/PARTIAL/MISSING/UNTESTED/UNCLEAR)

### A2. Requirement Description Clarity
- [ ] No vague terms like "TBD", "as needed", "depending on situation"
- [ ] No incomplete enumerations like "etc.", "such as"
- [ ] All uncertain words eliminated or clarified

### A3. Boundary Conditions
- [ ] Behavior for empty input is specified
- [ ] Behavior for oversized input is specified
- [ ] Behavior for duplicate input is specified
- [ ] Behavior for concurrent scenarios (if applicable) is specified
- [ ] Behavior for invalid format input is specified

### A4. Error Handling
- [ ] Every failure scenario defines specific error code
- [ ] Every failure scenario defines specific error message
- [ ] Error response data structure is specified

---

## B. Task Split Quality Check

### B1. Split Principles
- [ ] Each subtask corresponds to independently verifiable capability
- [ ] No tasks split by file
- [ ] No tasks split by time
- [ ] Each subtask can be completed independently

### B2. Complexity Assessment
- [ ] Every task annotated with complexity (low/medium/high)
- [ ] Complexity based on small model capability
- [ ] High complexity tasks split or have very detailed steps
- [ ] Low: has example to copy or standard CRUD
- [ ] Medium: has business logic, PRD has clear steps
- [ ] High: split or every step pinned down

### B3. Dependencies
- [ ] Dependencies clearly listed
- [ ] No circular dependencies
- [ ] "Parallelizable" tasks truly have no dependencies
- [ ] Blocking tasks (P0) identified and prioritized
- [ ] Baseline dependencies are separated from Trellis task dependencies
- [ ] Existing code dependencies are not represented as new Trellis child tasks

### B4. Priority
- [ ] Every task assigned priority (P0/P1/P2/P3)
- [ ] P0: blocks other modules or core correctness
- [ ] P1: core business loop
- [ ] P2: experience, reports, notifications, enhancements
- [ ] P3: non-essential optimization

---

## C. PRD Quality Check (Critical!)

### C1. Placeholder Elimination
- [ ] No `<...>` placeholders in PRD
- [ ] No abstract terms like "specific path", "related files"
- [ ] No reasoning gaps like "as needed"

### C2. Reference Implementation
- [ ] If example exists, points to specific file with full path
- [ ] If no example, states "None, implement from scratch"
- [ ] Replacement instructions specific
- [ ] Not vague like "refer to related code"

### C3. File Manifest
- [ ] Lists all files, precise to full path
- [ ] Each file annotated with operation type
- [ ] Modify operations specify exact location
- [ ] If data structure involved, includes complete field table

### C4. Implementation Steps
- [ ] Steps are ordered
- [ ] Each step is concrete action, not abstract goal
- [ ] Each step independently verifiable
- [ ] Reasoning decisions pinned down

### C5. Acceptance Criteria
- [ ] Criteria are decidable assertions
- [ ] Includes normal path acceptance
- [ ] Includes exception path acceptance
- [ ] Includes boundary condition acceptance

### C6. Self-Check Commands
- [ ] Provides directly executable commands
- [ ] Commands are specific
- [ ] Commands include expected result
- [ ] No human judgment required

### C7. Automated Tests Required
- [ ] Lists required test types
- [ ] Each test point specific
- [ ] Not abstract like "add necessary tests"

---

## D. Small Model Execution Friendliness Check

### D1. Decision Points Pinned
- [ ] All annotation choices specified
- [ ] All branch choices specified
- [ ] All naming rules specified
- [ ] All table structure specified

### D2. Copy-Example Feasibility
- [ ] If pointing to example, highly similar to task
- [ ] Mapping from example to task is clear
- [ ] If cannot copy, from-scratch steps very detailed

### D3. Forbidden List
- [ ] Lists what not to do
- [ ] Specifies file modification scope
- [ ] Specifies dependency constraints

### D4. Tech Stack and Tool Constraints
- [ ] Frameworks/libraries listed
- [ ] Build commands specified
- [ ] Test commands specified

### D5. Context and Design Shift-left
- [ ] Context Manifest lists exact files the execution model must read before editing
- [ ] Decision Table pins naming, branch, schema, API, and validation choices
- [ ] Contract snapshots define API/interface/data/state behavior before coding
- [ ] `implement.jsonl` entries list stable implementation context files, not source files or step actions, when used
- [ ] `check.jsonl` entries list stable verification context files, not test commands, when used

---

## E. Risk Point Check

### E1. Risk Identification
- [ ] High-risk modules annotated
- [ ] Cross-team dependencies specified
- [ ] Technical debt recorded in Out of Scope

### E2. Out of Scope Clarity
- [ ] Lists explicitly excluded features
- [ ] Lists points that cannot be pinned (if any)
- [ ] Not vague like "other features"

---

## Pass Criteria

- All applicable check items are marked ✅
- Non-applicable items are marked `N/A` with a reason

## Failure Handling

- Failed check items become explicit issues
- Generate an issue list (location, description, impact, improvement suggestion)
- Apply targeted improvements and continue to the next review round

## Convergence Conditions

- All check items pass → proceed to user confirmation
- 2 consecutive rounds with no new issues → auto-pass
- Still have issues after 5 rounds → prompt user choice
