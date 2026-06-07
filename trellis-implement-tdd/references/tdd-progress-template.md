# TDD Progress Table Template

Copy this template to `<task-dir>/tdd-progress.md`. Update that task-local file throughout execution; do not edit the skill's `references/tdd-progress-template.md`.

After loading the task, extract each AC from `prd.md` into one row. Write back status throughout, ensuring "only one AC in progress at a time".

## Progress Table

| AC ID | Expected Observable Result | Test File | Test Command | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| AC-001 | <input X → return Y> | <test path> | <command> | red / green / done | <e.g. triggered debugging> |
| AC-002 | <failure path → error code Z> | <test path> | <command> | pending | |

Status values:

- `pending` —— Not started yet
- `red` —— Wrote failing test and saw red, now writing implementation
- `green` —— Test passed, now running self-check
- `done` —— Self-check all green, no regression, staged

## Wrap-up checklist

- [ ] All ACs status is `done`.
- [ ] No AC stuck at `red` / `green`.
- [ ] `prd.md` self-check command full set last run all green.
- [ ] `design.md` mount point checklist item by item wired (if any).
- [ ] Not committed; changes staged, awaiting `trellis-review-twostage`.
