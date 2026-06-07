# Trellis 0.6 Beta Planning Artifacts Template

Use this template for medium/high complexity gap-closing tasks, or whenever `.trellis/workflow.md` or nearby tasks show that the project expects `design.md`, `implement.md`, `implement.jsonl`, or `check.jsonl`.

These artifacts shift reasoning left. They should preserve MVP behavior while making the gap-closing change narrow enough for a capability-limited execution model.

## Complexity Gate

| Complexity | Required Artifacts |
| --- | --- |
| low | `prd.md` is enough if the task has a direct MVP example to copy and executable checks. |
| medium | Add `design.md` and `implement.md`; add JSONL context manifests if stable specs, research context, or regression notes must be preloaded. |
| high | Split the task first. If it cannot be split, add `design.md`, `implement.md`, `implement.jsonl`, and `check.jsonl`, with every decision pinned down and stable implementation/check context preloaded. |

## `design.md`

```markdown
# Design: <task title>

## Requirement Coverage

| Requirement ID | Current Status | Design Element | Expected Status After Task |
| --- | --- | --- | --- |
| REQ-001 | PARTIAL | <component/contract/flow> | DONE |

## MVP Compatibility Contract

| Existing Behavior | Evidence | Must Preserve? | Regression Check |
| --- | --- | --- | --- |
| <behavior> | <path/test> | yes | <command/test> |

## Context Manifest

| Kind | Path | Why It Matters | Read Before Editing |
| --- | --- | --- | --- |
| MVP code | <path> | <behavior to preserve or extend> | yes |
| Existing test | <path> | <regression style> | yes |
| Spec | <path> | <contract source> | yes |

## Decisions

| Decision | Selected Option | Rejected Options | Reason | Affected Files |
| --- | --- | --- | --- | --- |
| <bug branch/schema/API choice> | <exact choice> | <options not used> | <reason> | <paths> |

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

Separate this gap-closing change into orchestration vs computation, and point each part to its landing point in the File Manifest. The execution phase follows this placement plan instead of choosing files on its own.

| Layer | Elements Touched In This Task | Landing Point (File Manifest Path) |
| --- | --- | --- |
| Orchestration Layer (main flow / control flow / branch orchestration / workflow) | <orchestration elements> | <path> |
| Computation Layer (pure algorithms / pure functions / data transforms) | <independently testable logic> | <path> |

- The orchestration layer should only coordinate; independently testable logic belongs in the computation layer.
- During gap-closing work, prefer extending the existing orchestration layer instead of creating a parallel implementation.

## Mount Point Checklist

Use this rule: "if this line disappears, the feature disappears from the user/system point of view." Usually 3-5 rows. The execution phase wires these points one by one; review checks them one by one, so implementation does not stop at "code exists but is not launched".

| Mount Point | Type | Location | Exact Wiring Action |
| --- | --- | --- | --- |
| <name> | route registration / config entry / event subscription / DI binding / menu entry | <path> | <exact registration or binding action> |

## Non-goals

- <explicitly excluded behavior>
```

## `implement.md`

```markdown
# Implementation Plan: <task title>

## File Plan

| Step | File | Action | Exact Location | Verification |
| --- | --- | --- | --- | --- |
| 1 | <path> | <new/modify> | <method/section> | <command or assertion> |

## Ordered Steps

1. <copy or create exact file/section>
2. <make exact replacement or edit>
3. <add exact validation or bug-fix branch>
4. <run exact check>

## Patch Boundaries

- Allowed files:
- Forbidden files:
- Existing MVP behavior that must not change:
- Forbidden dependencies:

## Rollback / Recovery

- If check `<command>` fails with `<symptom>`, inspect `<file>` and fix `<specific issue>`.
```

## `implement.jsonl`

Each line is one stable context item to preload before implementation. Use this for specs, research notes, API docs, design references, migration notes, or other stable context that is not likely to change during the task. Do not list source files being edited, and do not encode step actions here.

```jsonl
{"file":"<path-to-stable-spec-or-doc>","reason":"<why this context is needed before implementation>"}
{"file":"<path-to-stable-reference>","reason":"<decision, API, schema, migration, or domain rule it anchors>"}
```

## `check.jsonl`

Each line is one stable context item to preload before checking/verification. Put commands and expected results in `implement.md` or `prd.md`, not in this JSONL manifest.

```jsonl
{"file":"<path-to-acceptance-spec-or-test-plan>","reason":"<why this context is needed before verification>"}
{"file":"<path-to-regression-or-risk-note>","reason":"<MVP behavior or risk it protects>"}
```
