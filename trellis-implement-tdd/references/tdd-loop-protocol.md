# TDD RED-GREEN Loop Protocol

Execute per acceptance criterion (AC). This file is a narrow-path script for the executor (which may be a qwen3.6 35b small model)—follow it, don't improvise.

## Single AC loop

### Step 1 · RED (write a failing test)

- Find the copyable test from `prd.md`「Reference Implementation/Test Example」, copy it, modify input and assertion for this AC.
- Test targets only **this AC's** observable result (return value / state change / error code / persisted result), don't be greedy.
- Assertion writes to concrete values, forbid weak assertions like "roughly", "non-empty is fine" (unless AC itself is non-empty validation).
- Test command taken from `prd.md`「Self-Check Commands」or「Automated Tests Required」, must be directly runnable.

### Step 2 · See red (confirm test actually fails)

- Run the test, **must see failure**.
- **Don't see failure = test didn't cover target behavior**: go back to step 1 to fix test, don't proceed.
- Failure message should point to "feature not implemented" (e.g. assertion mismatch / method doesn't exist), not "test written wrong" (e.g. import error / syntax error). If latter, fix test first.

### Step 3 · GREEN (write just-green minimal code)

- Landing point locked: where new code goes decided by `prd.md`「File Manifest」+ `design.md`「Orchestration-Computation Separation」. Orchestration layer changes orchestration, computation layer changes computation, don't mix.
- Decisions locked: naming / branching / schema / annotations per `prd.md`「Decision Table」, don't choose on your own.
- Only write "minimal code needed to make this test green", don't implement other ACs on the side, don't add unrequested abstractions.

### Step 4 · See green (confirm pass)

- Run the test again, see it pass.
- Still red and not obvious → trigger `trellis-debug-systematic`, fix, then return to this step and re-run.

### Step 5 · Self-check (confirm no regression)

- Run `prd.md`「Self-Check Commands」full set + project lint / type-check.
- Any item fails = this change broke something else → trigger `trellis-debug-systematic`.

### Step 6 · Record (stage, don't commit)

- Mark `AC-xxx` as done in progress table.
- Stage changes (e.g. `git add`), **don't `git commit`**.
- Move to next AC.

## Iron rules

- No failing test, no implementation code.
- One AC turns green at a time.
- Don't touch files outside「File Manifest」「Forbidden」; stop and report when needed.
- Don't delete existing tests to "make it green"; don't weaken assertions to "make it green".
- No commit / push / merge.

## Anti-patterns (stop and return to track when these appear)

- **Write implementation then add tests**: violates RED-first, delete untested code, start over from step 1.
- **Change multiple files in one go to green multiple ACs together**: lose pinpoint ability, break back to single AC.
- **Don't see red but proceed**: test isn't testing the real thing, fix test first.
- **Can't turn green so change test assertion to accommodate implementation**: unless confirmed test is wrong; otherwise implementation didn't satisfy AC, should change implementation or go to debug.
- **Refactor unrelated code on the side**: out of scope for this AC, note it in task remarks, leave for review/later, don't do it in green loop.
