# Model Role Policy

## Default Assignment

| Stage | Recommended executor | Reason |
| --- | --- | --- |
| Requirements analysis and task splitting | Strong model | Requires boundary, dependency, decomposition, and execution-spec judgment |
| Self-review checklist | Small or mid model | Mostly mechanical checking |
| TDD implementation | Small model | Follows red/green objective signals |
| First 3 systematic debug rounds | Small model | Uses fixed script and minimal repair |
| Complex debug takeover | Strong model | More than 3 rounds suggests root-cause judgment |
| Review Stage 1 | Small model | Mechanical PRD/spec compliance |
| Review Stage 2 | Strong model or human | Requires design quality, structural health, and correctness risk judgment |
| Final Acceptance | Strong model or human | Requires synthesis of requirements, evidence, and residual risk |

## Small-Model Prohibitions

- Do not expand scope.
- Do not edit outside the File Manifest.
- Do not write implementation before a failing test.
- Do not make tests green by deleting tests or weakening assertions.
- Do not self-complete Stage 2 code quality review.
- Do not mark requirements `DONE` without test evidence.

## Escalation Conditions

- Debugging exceeds 3 rounds.
- Review finds a critical issue.
- Requirements or architecture decisions cannot be fixed from file evidence.
- The same REQ has no progress for 2 rounds.
- Work requires judging cross-module architecture, data consistency, security, permissions, payment, or infrastructure risk.
