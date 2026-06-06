# Test Coverage Matrix Template

Use this template when designing or filling automated tests for delivery closure.

## Test Coverage Matrix

| Requirement ID | Test Type | Test File | Test Case | Current Status | Gap | Manual Reason | Manual Steps |
| --- | --- | --- | --- | --- | --- | --- | --- |
| REQ-001 | unit |  |  | MISSING |  |  |  |

Allowed test types:

- `unit`
- `integration`
- `e2e`
- `smoke`
- `regression`
- `manual`

Coverage rules:

1. Every `REQ-*` and `AC-*` must map to at least one test or manual verification entry.
2. Prioritize core success paths, failure paths, boundary conditions, historical regression risk, and cross-module data flow.
3. Do not write meaningless tests for coverage numbers.
4. If automation is unsuitable, explain why and write clear manual verification steps.

## Execution Output

When tests are implemented, report:

- Tests added:
- Tests updated:
- Requirements covered:
- Requirements still untested:
- Commands run:
- Validation result:
