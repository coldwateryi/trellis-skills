# Early Core Layering Refactor

## Intent

Use the 2026-05-07 early Trellis skills as the architectural core and layer later capabilities around it instead of continuing to expand the original planning skills.

The early core had two clear responsibilities:

- `trellis-zero-to-mvp-*`: convert requirements into an MVP Trellis task tree.
- `trellis-mvp-to-delivery-*`: audit an MVP against requirements and plan gap-closing tasks.

Later additions remain valuable, but they should be layered:

- Controller: route stages and safety gates.
- Execution skills: TDD, systematic debugging, two-stage review.
- Shared policies: model roles, evidence, stage transitions.
- Assimilation governance: evaluate external GitHub skill projects before absorbing ideas.

## Current First Step

This branch adds `trellis-delivery-controller-zh` / `trellis-delivery-controller` as dedicated orchestration layers. It preserves existing user paths while making the intended layering explicit.

## Follow-Up Refactor Targets

1. Move delivery loop route decisions out of `trellis-mvp-to-delivery-zh` into controller references. Initial controller routing lives in `trellis-delivery-controller-zh/references/delivery-loop-routing.md` and `trellis-delivery-controller/references/delivery-loop-routing.md`.
2. Keep `trellis-mvp-to-delivery-zh` focused on gap audit, batch planning, state updates, and final acceptance. It still supports standalone route selection through its local `delivery-loop-policy.md`.
3. Extract repeated model-role and stop-condition rules from planning skills into shared policy references.
4. Add `trellis-skill-assimilator-zh` / `trellis-skill-assimilator` for external GitHub skill project analysis and update scans. Initial governance skills now exist with source analysis, capability taxonomy, target mapping, license policy, and update-scan policy.
5. Add evaluation scenarios before removing any existing behavior.

## Non-Goals

- Do not revert to the early version.
- Do not remove execution-phase skills.
- Do not drop delivery state or run-log support.
- Do not change install scripts until the new skill list stabilizes.
