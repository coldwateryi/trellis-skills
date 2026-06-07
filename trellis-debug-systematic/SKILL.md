---
name: trellis-debug-systematic
description: |
  When a test should be green but stays red, or a self-check command fails during Trellis subtask implementation/verification, use this non-deviable rigid script for systematic root-cause pinpointing and minimal fix. Used when Codex / Claude Code drives a small-parameter model like qwen3.6 35b—small models quickly spiral out of control when debugging freely; this skill uses "one change at a time, must re-run after change, no guessing" iron rules to lock it on a narrow path with defensive regression checks.
---

# Trellis Systematic Debugging (Rigid Script)

## Overview

Take over a failing test or self-check command, fix it in 4 fixed steps: pin failure signal → pinpoint → single-hypothesis verification → minimal fix + regression. This skill exists to **prevent (especially small models) from changing things everywhere and making it worse while debugging**—so it's a **numbered script + iron rules**, not suggestions.

Trigger: A test in `trellis-implement-tdd`'s RED-GREEN loop should be green but stays red, or `prd.md` self-check command fails, and the cause is not obvious.

Record the debugging trail in the fixed task-local file `<task-dir>/debug-report.md`. Create it from `references/debug-report-template.md` on the first debugging incident, then append a new session block for each later incident. Do not edit the template under the skill directory.

## Constraints (Iron Rules)

- **One change at a time**. After changing, immediately re-run that failing command, then decide next step.
- **Must re-run original failing command after change**. No re-run = no verification.
- **No guessing**. Pinpointing uses only "read stack / binary-comment / add one log line" three tricks to narrow the range, not imagination-based code changes.
- **Don't touch files outside file manifest / forbidden list**. When suspecting root cause is out of scope, stop and report—don't autonomously spread modifications.
- **Rollback if fix didn't work**. One modification re-run still fails, rollback this change first before trying another hypothesis—don't stack on top of a wrong change.
- **No commit / push / merge**.
- Beyond 3 rounds of "hypothesis→fix→re-run" still not green → stop, escalate to strong model or report to human, don't infinitely burn tokens.

## Workflow

### 1. Pin failure signal (no action without reproduction)

- Paste the **original text** of the failure: error stack / failed assertion / command non-zero exit code and output.
- Confirm stable reproduction: note down reproduction command (taken from `prd.md` self-check commands or test commands).
- Can't reproduce then fix "unstable reproduction" first, don't blindly fix against transient phenomena.
- Write the reproduction command, original failure text, and stability result into `<task-dir>/debug-report.md`.

### 2. Pinpoint (only three tricks, narrow to specific line)

By cost low to high, stop when hit:

1. **Read stack**: File and line pointed to by error stack/assertion, look directly at that spot.
2. **Binary-comment**: Binary-comment or short-circuit suspicious code segment, see if failure disappears, narrow range.
3. **Add one log line**: Print actual value of key variable in narrowed range, compare with expected value.

Output: Narrow range to "specific file + specific line/variable", not vague "something is wrong somewhere".

### 3. Single hypothesis (verify truth first, then talk about fix)

- Write one-sentence hypothesis: `I believe root cause is X (specific to variable/branch/contract)`.
- First **verify hypothesis truth** with minimal means (check variable actual value / check contract definition / run a smaller probe), confirm before fixing.
- Hypothesis proven false → go back to step 2 for another spot, don't carry wrong hypothesis to make changes.

### 4. Minimal fix + regression

- Only change **that one spot** targeting verified root cause.
- Re-run original failing command → green then continue; still red then rollback this change, go back to step 3 for another hypothesis.
- After green, run `prd.md` self-check command full set, confirm no new red (no regression).
- **Defensive wrap-up**: Answer one sentence "Can this bug happen again from other entry points?"
  - Yes → append one regression point line to `check.jsonl` (`{"file":"<regression test or risk point>","reason":"<behavior it protects>"}`), and consider adding a regression test.
  - No → note "locally sealed" in debugging record.

### 5. Exit

- **Green**: return to `trellis-implement-tdd` the failed step and continue.
- **Rolled back and can't come up with valid hypothesis**: record excluded hypotheses, escalate.
- **Beyond 3 rounds still red**: stop, escalate to strong model / human, attach failure signal, tried hypotheses, excluded items.

## Small-model adaptation highlights

- Debugging is where small models most easily lose control—this skill uses **numbered steps + one at a time + must re-run after change** to turn it into a mechanical process.
- "No guessing, verify hypothesis first" prevents small model from randomly changing "looks related" code all over.
- Clear exit and escalation conditions prevent small model from getting stuck in debugging repeatedly burning tokens.
- Role layering: Debugging defaults to small model execution; beyond 3 rounds escalate to strong model.

## Reference files

- `references/debug-protocol.md` —— 4-step script's criteria details, three-trick pinpointing and anti-patterns, read before starting debug.
- `references/debug-report-template.md` —— Read-only template for `<task-dir>/debug-report.md`; append/update the task-local file throughout debugging.
