# Scenario: TDD Minimal Implementation Pass

## Purpose

Verify that `trellis-implement-tdd-zh` applies the Ponytail-inspired Trellis minimal implementation pass after tests are green, without weakening safety or validation.

## Input Task Shape

A Trellis child task has:

- `prd.md` with `AC-001`: use the browser's native date input for a booking form date field.
- File Manifest:
  - modify `src/components/BookingForm.tsx`
  - modify `src/components/BookingForm.test.tsx`
- Forbidden:
  - do not add dependencies
  - do not introduce a custom date picker component
- Self-check:
  - `npm test -- BookingForm.test.tsx`
  - `npm run typecheck`

## Bad Output Pattern

The implementation:

- Adds a new date picker dependency.
- Creates `DatePickerWrapper.tsx`.
- Adds a custom parser for ISO dates.
- Adds styling for a calendar popup.
- Passes the test but leaves the extra abstraction in place.

## Expected Trellis Behavior

After GREEN:

1. Read `references/minimal-implementation-pass.md`.
2. Replace the custom wrapper with native `<input type="date">`.
3. Remove the new dependency and wrapper file from the intended diff.
4. Keep the test that verifies the date value is submitted.
5. Keep validation required by `prd.md`; do not delete error handling.
6. Record in `<task-dir>/tdd-progress.md`:
   - deleted custom wrapper/dependency
   - reused native browser input
   - retained validation/test
   - no `trellis-minimal:` comment needed unless there is a known ceiling

## Pass Criteria

- `trellis-implement-tdd-zh/SKILL.md` references `minimal-implementation-pass.md`.
- `tdd-loop-protocol.md` includes a post-green convergence step.
- `tdd-progress-template.md` has a "最小实现收敛" section.
- `review-stage2-checklist.md` checks standard library/platform/dependency reuse and progress-record evidence.
- `scripts/validate-skill-structure.py` passes.
