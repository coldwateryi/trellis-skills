# Capability Taxonomy

## Naming

Use `CAP-<DOMAIN>-<ACTION>`, for example:

- `CAP-REQ-TRACEABILITY`
- `CAP-PLAN-SELF-REVIEW`
- `CAP-EXEC-TDD-LOOP`
- `CAP-DEBUG-SYSTEMATIC`
- `CAP-REVIEW-TWOSTAGE`
- `CAP-CONTEXT-FRESH-GATE`
- `CAP-CODE-SIMPLIFY-PASS`
- `CAP-STATE-RUN-LOG`
- `CAP-ARCH-DECISION-ARCHIVE`
- `CAP-SKILL-UPDATE-SCAN`

## Domains

| Domain | Meaning | Trellis stage |
| --- | --- | --- |
| REQ | Requirements traceability, ACs, RTM | planning / audit |
| PLAN | Task splitting, shift-left design, self-review loop | zero-to-mvp / mvp-to-delivery |
| EXEC | Implementation discipline, TDD, file boundaries | implement-tdd |
| DEBUG | Reproduce, pinpoint, hypothesize, minimal fix | debug-systematic |
| REVIEW | Spec compliance, code quality, review gates | review-twostage |
| CONTEXT | Fresh context and context-rot prevention | controller / shared policy |
| STATE | State files, run log, delta audit | delivery-controller / mvp-to-delivery |
| ARCH | Architecture archive, decision record, structural health | planning artifacts / spec |
| SKILL | Skill absorption, update scan, governance | skill-assimilator |

## Selection Rules

- Assign one primary domain per capability.
- Split cross-stage capabilities into multiple capability IDs.
- Capability names describe behavior, not source project names.
- Source projects are recorded only in the absorption card.
