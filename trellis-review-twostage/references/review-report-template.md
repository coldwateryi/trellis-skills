# Review Report

Copy this template into `<task-dir>/review-report.md`. Keep that fixed file for the whole task and append one `## Review Round <n>` block per full review or re-review. Update only the task-local file; do not edit the skill's `references/review-report-template.md`.

## Review Round `<n>`

### Review Subject

- Task: `<task directory>`
- Diff range: `<start..current>`
- Stage 2 review model: `<strong model name / if small model flag "not reviewed by strong model" risk>`

### Stage 1 · Spec Compliance

| Check Item | Result | Severity | Location | Notes |
| --- | --- | --- | --- | --- |
| AC test coverage | pass/non-compliant | - / critical | <file:line> | |
| File manifest compliance | | | | |
| Forbidden compliance | | | | |
| Decision table compliance | | | | |
| Mount point wiring | | | | |

### Stage 2 · Code Quality

| Check Item | Result | Severity | Location | Improvement Suggestion |
| --- | --- | --- | --- | --- |
| Orchestration-computation separation | | critical/major/minor | <file:line> | |
| Structural health | | | | |
| Simplification and reuse | | | | |
| Correctness (boundary/error/regression) | | | | |
| Spec compliance (spec) | | | | |

### Issue Summary (by severity)

- **Critical (blocking)**:
  - <location + issue + how to fix>
- **Major (should fix)**:
  - <...>
- **Minor (record for later)**:
  - <...>

### Verdict

- [ ] Has critical → send back to `trellis-implement-tdd`, only fix flagged items, after fix re-review
- [ ] Only major/minor → pass; major suggest fix this round, minor note to task remarks
- [ ] All pass → hand back to orchestration session to advance task status (`task.py` advance / enter finish)
