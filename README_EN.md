# Trellis Requirements-to-Delivery Skills

This repository provides a set of Trellis workflow skills for [Codex CLI](https://github.com/anthropics/codex), covering the full lifecycle from raw requirements documents to complete delivery — **Analyze → Plan → Trace → Audit → Close Gaps → Accept**.

## Skill Overview

| Skill | Language | Purpose |
| --- | --- | --- |
| `trellis-zero-to-mvp` | EN | Zero to MVP: turn a requirements document into an MVP task tree |
| `trellis-mvp-to-delivery` | EN | MVP to Delivery: gap audit, gap-closing plan, final acceptance |
| `trellis-zero-to-mvp-zh` | ZH | Same as above (Chinese) |
| `trellis-mvp-to-delivery-zh` | ZH | Same as above (Chinese) |

### ✨ New Feature: Self-Review Loop

**All skills now support self-review loop mechanism to ensure planning phase output meets execution requirements for small parameter models (e.g., qwen3.6 35b).**

**How It Works**:
1. 🔍 **Analyze** - Generate initial requirements traceability matrix, task split, and PRDs
2. ✅ **Self-Review** - Check against 45-60 item checklist
3. 🔧 **Targeted Improvements** - Fix only marked issues, not full redo
4. 🔄 **Iterative Convergence** - Repeat 2-3 rounds until all checks pass
5. ✅ **User Confirmation** - Create task tree only after meeting standards

**Key Benefits**:
- ✅ **Small Model Friendly** - Eliminates placeholders, provides concrete paths and steps
- ✅ **Quality Assurance** - 45-60 precise checks, issues located to specific lines
- ✅ **Cost Effective** - ROI > 5:1 (planning costs +45k tokens, execution saves 200k tokens)
- ✅ **Proven Results** - Execution success rate improves 30%-50%

See: [Optimization Proposal](OPTIMIZATION_PROPOSAL.md) and [Final Summary](FINAL_SUMMARY.md)

### ✨ New Feature: Self-Review Loop

**All skills now support self-review loop mechanism to ensure planning phase output meets execution requirements for small parameter models (e.g., qwen3.6 35b).**

**How It Works**:
1. 🔍 **Analyze** - Generate initial requirements traceability matrix, task split, and PRDs
2. ✅ **Self-Review** - Check against 45-60 item checklist
3. 🔧 **Targeted Improvements** - Fix only marked issues, not full redo
4. 🔄 **Iterative Convergence** - Repeat 2-3 rounds until all checks pass
5. ✅ **User Confirmation** - Create task tree only after meeting standards

**Key Benefits**:
- ✅ **Small Model Friendly** - Eliminates placeholders, provides concrete paths and steps
- ✅ **Quality Assurance** - 45-60 precise checks, issues located to specific lines
- ✅ **Cost Effective** - ROI > 5:1 (planning costs +45k tokens, execution saves 200k tokens)
- ✅ **Proven Results** - Execution success rate improves 30%-50%

See: [Optimization Proposal](OPTIMIZATION_PROPOSAL.md) and [Final Summary](FINAL_SUMMARY.md)

## Recommended Workflow

```
Requirements ──→ [Zero to MVP] ──→ MVP Task Tree ──→ Build the MVP
                                                          │
                                                          ▼
                              Requirements ──→ [MVP to Delivery] ──→ Gap Tasks ──→ Delivery & Acceptance
```

### Phase 1: Zero → MVP

When you have a complete requirements document (PRD / product brief / feature spec) and haven't started coding yet:

1. Place the requirements document in the project
2. Invoke `trellis-zero-to-mvp` (or the Chinese variant `trellis-zero-to-mvp-zh`)
3. The skill performs a **read-only analysis** and outputs:
   - Requirements Traceability Matrix
   - Module dependency graph
   - Capability-based task split
   - Dependency-ordered MVP development sequence
   - Draft parent and child PRDs
4. **After confirming the analysis**, the skill creates the Trellis task tree
5. Start coding in the recommended order

### Phase 2: MVP → Delivery

After the MVP is implemented, return to the source requirements document for complete delivery:

1. Invoke `trellis-mvp-to-delivery` (or the Chinese variant `trellis-mvp-to-delivery-zh`)
2. The skill performs a **gap audit**, checking the MVP against every requirement:
   - Requirements Traceability Matrix (with DONE / PARTIAL / MISSING / UNTESTED / UNCLEAR statuses)
   - MVP completion summary
   - Dependency-ordered gap-closing task plan
   - Automated test coverage requirements
3. **After confirming the audit**, the skill creates gap-closing Trellis tasks
4. Close gaps by priority, add tests, and run final acceptance

## Recommended Usage

### Scenario 1: New Project Kickoff

```
We're starting a new project. The requirements are in docs/requirements.md.

Use trellis-zero-to-mvp to turn this into an MVP task plan.
```

The skill starts with a read-only analysis — no code is written. Only after you confirm the task split and MVP boundary will it create the Trellis task tree.

**✨ Self-Review Loop**: The analysis process automatically performs 2-3 rounds of quality checks to ensure:
- ✅ All `<...>` placeholders replaced with concrete values
- ✅ File Manifest contains precise file paths
- ✅ Implementation Steps are executable concrete actions
- ✅ Complex tasks split to fit small model execution

### Scenario 2: MVP Ready for Full Delivery

```
The MVP is complete. Source requirements are in docs/requirements.md.

Use trellis-mvp-to-delivery to audit the MVP and plan full delivery.
```

The skill checks existing implementation and tests against the requirements document, identifies every gap, and creates gap-closing tasks.

**✨ Self-Review Loop**: The audit process automatically performs quality checks to ensure:
- ✅ Each DONE status has implementation evidence and test evidence
- ✅ Gap-closing task PRDs explicitly state not breaking MVP behavior
- ✅ Regression Tests cover MVP core flows
- ✅ Bug fix branch logic clearly pinned down

### Scenario 3: Iterative Development

In practice, the two skills can be used in cycles:

1. Use `zero-to-mvp` to plan the first shippable version
2. Build the MVP
3. Use `mvp-to-delivery` to audit gaps and close them for full delivery
4. If new requirements arrive, return to step 1 and run `zero-to-mvp` again for the new scope

## Requirement Statuses

Both skills use a unified set of requirement statuses:

| Status | Meaning |
| --- | --- |
| `DONE` | Fully implemented and tested |
| `PARTIAL` | Partially implemented |
| `MISSING` | Not yet implemented |
| `UNTESTED` | Implemented but lacking adequate tests |
| `UNCLEAR` | Requirement is not clear enough to implement |

## Directory Structure

```
skills/
├── trellis-zero-to-mvp/          # Zero → MVP (English)
│   ├── SKILL.md                  # Skill definition & workflow
│   ├── agents/
│   │   └── openai.yaml           # Codex agent config
│   └── references/
│       ├── analysis-output-template.md   # Read-only analysis template
│       ├── parent-prd-template.md        # Parent task PRD template
│       ├── child-prd-template.md         # Child task PRD template
│       └── task-creation-checklist.md    # Task creation checklist
├── trellis-mvp-to-delivery/      # MVP → Delivery (English)
│   ├── SKILL.md
│   ├── agents/
│   │   └── openai.yaml
│   └── references/
│       ├── gap-audit-template.md         # Gap audit template
│       ├── delivery-task-prd-template.md # Gap-closing task PRD template
│       ├── test-coverage-matrix-template.md  # Test coverage matrix template
│       ├── final-acceptance-template.md      # Final acceptance template
│       └── bug-classification-rules.md       # Bug classification rules
├── trellis-zero-to-mvp-zh/       # Zero → MVP (Chinese)
│   └── (same structure as above)
├── trellis-mvp-to-delivery-zh/   # MVP → Delivery (Chinese)
│   └── (same structure as above)
├── README.md                     # Chinese README
└── README_EN.md                  # English README (this file)
```

## Prerequisites

- [Codex CLI](https://github.com/anthropics/codex) installed
- Trellis initialized in the project (`.trellis/` directory exists)
- Run `python ./.trellis/scripts/init_developer.py <name>` before first use to set the developer identity

## Key Principles

- **Analyze first, act later** — Every skill starts with a read-only pass. No tasks are created and no code is written until you confirm.
- **Split by capability, not by file** — Each child task maps to an independently verifiable business or technical capability.
- **Stable IDs** — Requirement IDs (REQ-xxx) and acceptance criteria IDs (AC-xxx) are assigned during analysis and remain fixed thereafter.
- **Explicit dependencies** — Parent/child task relationships express structure only. True execution dependencies are written into each child task's PRD.
