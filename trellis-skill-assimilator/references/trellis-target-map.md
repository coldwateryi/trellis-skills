# Trellis Target Map

| Capability type | Primary target | Allowed artifact |
| --- | --- | --- |
| Requirements traceability / RTM | `trellis-zero-to-mvp` / `trellis-mvp-to-delivery` | analysis/gap templates, checklist |
| Post-MVP audit | `trellis-mvp-to-delivery` | gap audit, delivery state, run log |
| Stage routing / automatic progress | `trellis-delivery-controller` | route policy, gates, model policy |
| TDD implementation | `trellis-implement-tdd` | TDD protocol, progress template |
| Systematic debugging | `trellis-debug-systematic` | debug protocol, debug report |
| Review gate | `trellis-review-twostage` | stage checklists, report template |
| Shift-left design | planning references | `design.md`, `implement.md`, JSONL context templates |
| Architecture archive | `.trellis/spec/` guidance | planning artifact templates, final acceptance |
| External capability assimilation | `trellis-skill-assimilator` | absorption card, update scan policy |
| Evaluation | future `evaluation/` | scenario, expected output, regression note |

## Disallowed Targets

- Do not put external project exposition directly into primary `SKILL.md` files.
- Do not put planning-stage judgment into execution-phase skills.
- Do not expand `mvp-to-delivery` with more stage-routing responsibility.
- Do not put license-risk content into reusable templates.

## Change Levels

| Level | Meaning | User confirmation |
| --- | --- | --- |
| L0 | Produce absorption card only | Not required |
| L1 | Add reference/checklist item | Recommended |
| L2 | Modify existing workflow or `SKILL.md` | Required |
| L3 | Change install scripts, default entrypoint, or state format | Required and must add verification scenario |
