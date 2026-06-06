# Trellis 0.6 Beta Planning Artifacts Template

Use this template for medium/high complexity child tasks, or whenever `.trellis/workflow.md` or nearby tasks show that the project expects `design.md`, `implement.md`, `implement.jsonl`, or `check.jsonl`.

These artifacts shift reasoning left. They should let a capability-limited execution model follow a narrow path instead of redesigning during implementation.

## Complexity Gate

| Complexity | Required Artifacts |
| --- | --- |
| low | `prd.md` is enough if the task has a direct reference implementation and executable checks. |
| medium | Add `design.md` and `implement.md`; add JSONL context manifests if stable specs or research context must be preloaded. |
| high | Split the task first. If it cannot be split, add `design.md`, `implement.md`, `implement.jsonl`, and `check.jsonl`, with every decision pinned down and stable context preloaded. |

## `design.md`

```markdown
# Design: <task title>

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
3. <add exact validation or branch>
4. <run exact check>

## Patch Boundaries

- Allowed files:
- Forbidden files:
- Forbidden dependencies:

## Rollback / Recovery

- If check `<command>` fails with `<symptom>`, inspect `<file>` and fix `<specific issue>`.
```

## `implement.jsonl`

Each line is one stable context item to preload before implementation. Use this for specs, research notes, API docs, design references, or other stable context that is not likely to change during the task. Do not list source files being edited, and do not encode step actions here.

```jsonl
{"file":"<path-to-stable-spec-or-doc>","reason":"<why this context is needed before implementation>"}
{"file":"<path-to-stable-reference>","reason":"<decision, API, schema, or domain rule it anchors>"}
```

## `check.jsonl`

Each line is one stable context item to preload before checking/verification. Put commands and expected results in `implement.md` or `prd.md`, not in this JSONL manifest.

```jsonl
{"file":"<path-to-acceptance-spec-or-test-plan>","reason":"<why this context is needed before verification>"}
{"file":"<path-to-regression-or-risk-note>","reason":"<behavior or risk it protects>"}
```
