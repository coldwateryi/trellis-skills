# Trellis 0.6+ Planning Artifacts Template

Use this template for medium/high complexity child tasks, or whenever `.trellis/workflow.md` or nearby tasks show that the project expects `design.md`, `implement.md`, `implement.jsonl`, or `check.jsonl`.

These artifacts shift reasoning left. A capability-limited execution model should follow a narrow path instead of redesigning during implementation.

## Complexity Gate

| Complexity | Required Artifacts |
| --- | --- |
| low | `prd.md` is enough only when there is a direct reference implementation and executable checks. |
| medium | Add `design.md` and `implement.md`; add JSONL context manifests when stable specs or research context must be preloaded. |
| high | Split the task first. If it cannot be split, add `design.md`, `implement.md`, `implement.jsonl`, and `check.jsonl`, with every decision pinned and stable context preloaded. |

## General Rules

- `design.md` and `implement.md` inherit parent Project Contract Lock; names, paths, APIs, commands, packages/modules, routes, tables, and permission models must match PRD.
- In Small Model Mode, split complex tasks first; if keeping medium/high complexity, pin design and steps so the execution model does not re-reason.
- External config and third-party keys must be `FIXED`, `BASELINE`, `BLOCKED`, or `OUT_OF_SCOPE`; no `YOUR_KEY`, `API_KEY_HERE`, or "to be provided".
- Do not mix two naming/path systems in one artifact.
- `design.md` and `implement.md` must copy relevant Contract Snapshot values; forbidden-token hits make Artifact Gate FAIL.
- Detailed file plan, ordered steps, self-check commands, failure recovery, and review gate live in `implement.md` by default.
- JSONL mode must be explicit in the artifact matrix: `required`, `optional`, or `inline`.

## `design.md`

```markdown
# Design: <Task Title>

## Project Contract Reference

| Contract Item | This Task Uses | Parent Evidence Path |
| --- | --- | --- |
| <item> | <specific path/name/API/command/module or not-applicable> | <path> |

## Requirement Coverage

| Requirement ID | Design Element | Notes |
| --- | --- | --- |
| REQ-001 | <component/contract/flow> | <how this design satisfies it> |

## Context Manifest

| Kind | Path | Why It Matters | Read Before Editing |
| --- | --- | --- | --- |
| Existing example | <path> | <pattern to copy> | yes |
| Contract | <path> | <API/schema/state contract> | yes |
| Test | <path> | <expected test style> | yes |

## Decisions

| Decision | Selected Option | Rejected Options | Reason | Affected Files |
| --- | --- | --- | --- | --- |
| <naming/branch/schema/API choice> | <exact choice> | <options not used> | <reason> | <paths> |

## External Config and Open Items

| Config / External Dependency | Status | Planning Handling | Execution Behavior |
| --- | --- | --- | --- |
| <map key / external API / hardware protocol> | FIXED/BASELINE/BLOCKED/OUT_OF_SCOPE | <config name, evidence, or exclusion reason> | <exact behavior> |

## Contracts

### API / Interface

- Endpoint/function/class:
- Inputs:
- Outputs:
- Error cases:

### Data / State

| Field/State | Type | Allowed Values | Default | Validation |
| --- | --- | --- | --- | --- |
| <name> | <type> | <values> | <default> | <rules> |

## Orchestration-Computation Separation

| Layer | Elements Touched In This Task | Landing Point |
| --- | --- | --- |
| Orchestration Layer | <main flow/control/branch/workflow> | <path> |
| Computation Layer | <pure logic/data transform> | <path> |

## Mount Point Checklist

Rule: if this line disappears, the feature disappears from the user/system point of view.

| Mount Point | Type | Location | Exact Wiring Action |
| --- | --- | --- | --- |
| <name> | route/config/event/DI/menu/CLI/SDK export | <path> | <exact action> |

## Non-goals

- <explicitly excluded behavior>
```

## `implement.md`

```markdown
# Implementation Plan: <Task Title>

## Project Contract Reference

| Contract Item | Profile Field | This Task Uses | Parent Evidence Path |
| --- | --- | --- | --- |
| <item> | <profile field> | <specific path/name/API/command/module or not-applicable> | <path> |

## File Plan

| Step | File | Action | Exact Location | Verification |
| --- | --- | --- | --- | --- |
| 1 | <path> | <new/modify> | <method/section> | <command or assertion> |

## Structure Health Precheck

The planner decides this before execution; the execution model does not decide whether to refactor.

| Target File/Directory | Current Lines/Files | Threshold | Needs Micro-refactor | Micro-refactor Plan (move only, no behavior change) |
| --- | --- | --- | --- | --- |
| <path> | <n> | file 400 lines / directory 15 files | yes/no | <move what -> where -> how to verify unchanged> |

If threshold is hit, put a step 0 "move only, no behavior change" micro-refactor before the main work and verify it independently.

## Ordered Steps

0. <if structure precheck hits: move-only micro-refactor; otherwise skip>
1. <copy or create exact file/section>
2. <make exact replacement or edit>
3. <add exact validation or branch>
4. <run exact check>

## Patch Boundaries

- Allowed files:
- Forbidden files:
- Forbidden dependencies:
- Forbidden contract changes: names, paths, APIs, commands, packages/modules, routes, tables, and permissions must match PRD.
- Forbidden placeholders: `YOUR_KEY`, `API_KEY_HERE`, `TBD`, `depends`, `as needed`.

## Rollback / Recovery

- If check `<command>` fails with `<symptom>`, inspect `<file>` and fix `<specific issue>`.
```

## `implement.jsonl`

Each line is one stable context item to preload before implementation. Use this for specs, research notes, API docs, design references, or stable context. Do not list source files being edited, and do not encode steps here.

Delete `_example` seed rows after task creation. If JSONL is not needed, delete the file or mark `NOT_NEEDED_WITH_REASON` in the artifact matrix.

JSONL modes:

- `required`: sub-agent dispatch or stable context preload is required; seed-only must FAIL.
- `optional`: PRD/design/implement already constrain context; JSONL may be deleted or explained as not needed. Seed-only does not block Artifact Gate but must be explained.
- `inline`: Codex `dispatch_mode: inline`; JSONL is not a planning-readiness gate. Gate uses `--jsonl-mode inline`.

```jsonl
{"file":"<path-to-stable-spec-or-doc>","reason":"<why implementation needs this context>"}
{"file":"<path-to-stable-reference>","reason":"<decision, API, schema, or domain rule it anchors>"}
```

## `check.jsonl`

Each line is stable context to preload before checking/verification. Commands and expected results go in `implement.md` or PRD, not JSONL.

```jsonl
{"file":"<path-to-acceptance-spec-or-test-plan>","reason":"<why verification needs this context>"}
{"file":"<path-to-regression-or-risk-note>","reason":"<behavior or risk it protects>"}
```
