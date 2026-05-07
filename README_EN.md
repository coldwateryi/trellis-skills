# Trellis Requirements-to-Delivery Skills

This repository provides a set of Trellis workflow skills for [Codex CLI](https://github.com/anthropics/codex), covering the full lifecycle from raw requirements documents to complete delivery — **Analyze → Plan → Trace → Audit → Close Gaps → Accept**.

## Skill Overview

| Skill | Language | Purpose |
| --- | --- | --- |
| `trellis-zero-to-mvp` | EN | Zero to MVP: turn a requirements document into an MVP task tree |
| `trellis-mvp-to-delivery` | EN | MVP to Delivery: gap audit, gap-closing plan, final acceptance |
| `trellis-zero-to-mvp-zh` | ZH | Same as above (Chinese) |
| `trellis-mvp-to-delivery-zh` | ZH | Same as above (Chinese) |

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

### Scenario 2: MVP Ready for Full Delivery

```
The MVP is complete. Source requirements are in docs/requirements.md.

Use trellis-mvp-to-delivery to audit the MVP and plan full delivery.
```

The skill checks existing implementation and tests against the requirements document, identifies every gap, and creates gap-closing tasks.

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
