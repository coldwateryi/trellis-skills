# Bug Classification Rules

Use these rules when validation discovers a bug during MVP-to-delivery work.

## Classification

```markdown
## Bug Classification

- Bug:
- Affected Requirement IDs:
- Blocks current task: yes/no
- Recommended action:
  - fix in current task
  - create bug task
  - defer with documented risk

## Proposed Bug Task

- Title:
- Slug:
- Priority:
- Dependencies:
- Acceptance criteria:
- Tests required:
```

## Decision Rules

1. If the bug prevents the current requirement IDs from meeting acceptance criteria, fix it in the current task.
2. If the bug is unrelated to the current task but affects final delivery, create a separate bug task.
3. If the bug reflects a historical behavior change or product ambiguity, document the risk and ask for confirmation.
4. Do not hide unrelated bug fixes inside the current feature task.
5. Every bug fix must include a regression test or a documented reason why automation is unsuitable.
