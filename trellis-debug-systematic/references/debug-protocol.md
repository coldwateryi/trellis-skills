# Systematic Debugging Script Details

Narrow-path debugging script for executor (which may be a qwen3.6 35b small model). Follow it, no skipping steps, no guessing.

## Three-trick pinpointing (by cost low to high, stop when hit)

| Trick | How to do it | Applicable when |
| --- | --- | --- |
| Read stack | Look directly at file and line pointed to by error stack/failed assertion | Has clear stack/assertion location |
| Binary-comment | Binary-comment or short-circuit suspicious code segment, see if failure disappears | Large range, no clear stack |
| Add one log line | Print actual value of key variable in narrowed range, compare with expected | Suspect data/state is wrong |

> All three tricks exhausted still can't pinpoint → escalate, don't start changing randomly.

## Single-hypothesis writing

- Must be specific to **variable / branch / contract**: `I believe root cause is user.role is null in X branch`, not "permission logic has issues".
- **Verify truth first** then fix: check that variable's actual value / check contract definition / run a smaller probe.
- Only hold one hypothesis at a time. Proven false then note into "excluded", switch to next one.

## Minimal fix boundary

- Only change the **one spot** of verified root cause.
- After changing **immediately re-run original failing command**—this is the only verification method.
- Still red → **rollback this change** then try another hypothesis. Never keep stacking changes on top of an invalid change.
- Don't refactor, change signatures, change unrelated files under the name of debugging.

## Defensive regression

After fixing green must answer one sentence: "Can this bug happen again from other entry points?"

- Yes → append one regression point line to the task's `check.jsonl`, and try to add a regression test covering that entry.
- No → record "locally sealed".

## Anti-patterns (stop when these appear)

- **Shotgun modification**: change several spots at once to see which works—lose causality, go back to one at a time.
- **Claim fixed without re-run**: no re-run of original failing command = no verification.
- **Change code carrying unverified hypothesis**: verify hypothesis truth first.
- **Change test assertion to accommodate implementation**: unless confirmed test itself is wrong, otherwise implementation didn't satisfy AC.
- **Keep stacking on wrong change**: rollback first.
- **Beyond 3 rounds still trying**: stop escalate, attach excluded items.
