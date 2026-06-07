# Debug Report

Copy this template into `<task-dir>/debug-report.md`. Keep that fixed file for the whole task and append one `## Session <n>` block per debugging incident. Update only the task-local file; do not edit the skill's `references/debug-report-template.md`.

## Session `<n>`

This session block is both "working memory" for the small model (prevent forgetting what's been tried) and handoff material when escalating to strong model.

### Failure Signal

- Reproduction command: `<command>`
- Original text (stack/assertion/exit code):

```
<paste failure original text>
```

- Stable reproduction: yes / no (if not, fix unstable reproduction first)

### Pinpointing Process

| Which trick used | Result (narrowed to where) |
| --- | --- |
| Read stack / Binary-comment / Add log | <file:line / variable actual value> |

### Hypothesis Record

| Round | Hypothesis (specific to variable/branch/contract) | Verification method | Conclusion (holds/false) |
| --- | --- | --- | --- |
| 1 | <hypothesis> | <how to verify> | <conclusion> |

Excluded items:

- <excluded hypothesis, avoid retrying>

### Fix

- Root cause: <verified root cause>
- Change location (one spot): <file:line>
- Re-run original failing command result: green / still red (rolled back)

### Defensive Regression

- Can this bug happen again from elsewhere: yes / no
- If yes: noted regression point in `check.jsonl` `<path>`, regression test: <test or "pending">

### Exit Status

- [ ] Green, return to TDD loop the failed step
- [ ] Rolled back, escalate (attach excluded items)
- [ ] Beyond 3 rounds, escalate to strong model/human
