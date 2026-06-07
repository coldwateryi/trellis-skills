# Stage 2 · Code Quality and Design Discipline Checklist

Review code itself against `.trellis/spec/guides/` and design discipline. **Should be executed by strong model**. Severity: critical (blocking) / major (should fix) / minor (record for later).

## Orchestration-Computation Separation (from CodeStable design discipline)

- [ ] Orchestration logic (main flow/control flow/branch orchestration) and computation logic (pure algorithms/pure functions/data transforms) not mixed in the same place.
- [ ] Pure computation not stuffed into orchestration layer causing inability to unit-test; logic that can be independently tested is indeed independently testable.
- [ ] New code lands in position consistent with `design.md` orchestration-computation layering.

## Structural Health (from CodeStable design discipline)

- [ ] Didn't keep piling into already-fat (over threshold) file, making it harder to separate responsibilities.
- [ ] Didn't create "kitchen-sink" style omnibus file/utility class.
- [ ] Directory attribution reasonable, didn't randomly toss new file into unrelated directory.

## Simplification and Reuse

- [ ] Didn't duplicate implementation of already-existing capability (should reuse reference implementation/existing tools).
- [ ] Didn't have unrequested over-abstraction / reserved extension points (YAGNI).
- [ ] No obviously removable duplicate code (DRY), and deduplication doesn't harm readability.

## Correctness (Not just happy path)

- [ ] Boundary conditions (empty/overlong/duplicate/illegal input) per `prd.md` behavior constraints actually handled, not just making normal-path test green. ⛔ Missing handling of declared boundary is critical
- [ ] Error paths return `prd.md` specified exact error code/message.
- [ ] Concurrency/sequencing assumptions (if applicable) hold, no obvious race conditions.
- [ ] Didn't break existing behavior (regression points see `check.jsonl`). ⛔ Breaking existing behavior is critical

## Spec Compliance (spec/guides)

- [ ] Naming / layering / module boundaries conform to `.trellis/spec/` relevant specs.
- [ ] Error semantics / logging / observability points conform to project conventions.
- [ ] Test style consistent with existing tests (assertion granularity, naming, organization).

## Architecture Impact (if involves new module/cross-module interface)

- [ ] New module exposed/dependency relationships clear, consistent with existing architecture.
- [ ] Suggested to add pointer in `.trellis/spec/<pkg>/ARCHITECTURE.md` (delivery wrap-up write-back).

> Reviewer only outputs issue list, doesn't directly change code. Critical must block.
