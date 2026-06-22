# Ponytail Absorption Card

## Source

- Project: DietrichGebert/ponytail
- URL: https://github.com/DietrichGebert/ponytail
- Ref: `6da37bfa7d0282522c7785759f4d2f1544015354`
- License: MIT
- Analysis mode: initial-assimilation

## Source Analysis

Ponytail is an agent skill/ruleset that prevents over-engineered implementation. Its core pattern is a pre-code and post-green ladder:

1. Avoid building speculative work.
2. Prefer standard library.
3. Prefer native platform/framework capability.
4. Prefer already-installed dependencies over new dependencies.
5. Prefer direct expression over abstraction.
6. Only then write the minimum code that satisfies the task.

Its safety boundary is important: it does not simplify away trust-boundary validation, error handling that prevents data loss, security, accessibility, explicit requirements, hardware calibration knobs, or the smallest runnable check for non-trivial logic.

## Capability Extraction

| Capability ID | Source pattern | Trellis adaptation |
| --- | --- | --- |
| `CAP-EXEC-MINIMAL-IMPLEMENTATION` | Minimal implementation ladder before/after coding | Add a green-after complexity convergence gate to `trellis-implement-tdd-zh` |
| `CAP-REVIEW-OVERENGINEERING-CUTLIST` | Review for unnecessary complexity and deletion opportunities | Extend `trellis-review-twostage-zh` Stage 2 simplification/reuse checks |
| `CAP-EXEC-SAFE-SIMPLIFICATION-BOUNDARY` | Never cut validation/security/error handling/accessibility | Add explicit "cannot delete or weaken" boundary to implementation pass |
| `CAP-EXEC-INTENTIONAL-SHORTCUT-MARKER` | Mark known-ceiling shortcuts with upgrade path | Add `trellis-minimal:` comment convention for intentional simplifications |

## Trellis Current Gap

`trellis-implement-tdd-zh` already forces RED/GREEN and self-checks, but it did not have a named post-green convergence gate for removing unnecessary complexity introduced while making tests pass. The existing `trellis-review-twostage-zh` had simplification checks, but implementation did not require recording simplification decisions before review.

## Adaptation

- Primary target: `trellis-implement-tdd-zh`
- Secondary target: `trellis-review-twostage-zh`
- New artifact: `trellis-implement-tdd-zh/references/minimal-implementation-pass.md`
- Modified artifacts:
  - `trellis-implement-tdd-zh/SKILL.md`
  - `trellis-implement-tdd-zh/references/tdd-loop-protocol.md`
  - `trellis-implement-tdd-zh/references/tdd-progress-template.md`
  - `trellis-review-twostage-zh/references/review-stage2-checklist.md`

## Verification

- Scenario: `evaluation/scenarios/implement-tdd-minimal-pass.md`
- Structural validation: `python3 scripts/validate-skill-structure.py`
- Expected behavior: after AC tests are green, implementation must run a minimal implementation pass, delete unneeded abstraction/dependencies/files, keep safety checks, and record the result in `<task-dir>/tdd-progress.md`.

## Decision

- Recommendation: absorb
- Reason: aligns with Trellis small-model execution discipline by turning "avoid over-engineering" into a mechanical post-green gate with objective artifacts.
- Do not absorb:
  - Always-on mode switching and hooks.
  - Terse output style rules.
  - Ponytail branding or prose.
  - Direct wording from Ponytail skill files.
- Follow-up:
  - Consider an English equivalent after the Chinese pipeline stabilizes.
  - Add a future scenario runner that checks generated `tdd-progress.md` contains the minimal implementation section.
