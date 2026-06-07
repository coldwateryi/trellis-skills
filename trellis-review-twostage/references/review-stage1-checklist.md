# Stage 1 · Spec Compliance Checklist

Mechanically check "did implementation do as `prd.md` planned". Can be executed item by item by small model. Marked ⛔ non-compliance is **critical** (blocking).

## Acceptance Criteria Coverage

- [ ] Each `AC-xxx` has corresponding test. ⛔ Missing is critical
- [ ] All AC corresponding tests currently green. ⛔ Red is critical
- [ ] Didn't use "delete test/weaken assertion" to make it green. ⛔ If yes then critical

## File Manifest Compliance

- [ ] Every changed file is within「File Manifest」. ⛔ Changed file outside manifest is critical (unless reported and approved)
- [ ] 「File Manifest」marked "new" is actually new, marked "modify" changed at specified location.

## Forbidden Compliance

- [ ] Didn't create「Forbidden」named already-existing base class/utility class (should reuse reference implementation). ⛔ critical
- [ ] Didn't introduce dependencies/frameworks not listed in Technical Notes. ⛔ critical
- [ ] Didn't touch other red lines named in Forbidden.

## Decision Table Compliance

- [ ] Annotations / naming / schema / branching etc. all per「Decision Table」selected options, no self-re-selection.

## Mount Point Wiring (if design.md has mount point checklist)

- [ ] Mount points wired item by item: route registration / config item / event subscription / DI binding / menu entry etc. ⛔ Missing wire is critical (feature equals not launched)

## Scope Compliance

- [ ] Didn't implement features named in「Out of Scope」.
- [ ] Didn't go beyond to implement other ACs / other tasks' content.

> Any ⛔ hit → Stage 1 judges critical, can skip entering Stage 2, directly send back for fix.
