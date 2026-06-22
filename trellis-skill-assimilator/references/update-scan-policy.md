# Update Scan Policy

## Input

- Source URL.
- Current ref.
- Last analyzed ref.
- Previous absorption card or absorbed capability list.

## Scan Scope

Analyze only changes since `last_analyzed_ref` in:

- README / docs.
- `SKILL.md`.
- references.
- scripts.
- license.
- release notes or changelog.

## Delta Output

| Change | Impact | Action |
| --- | --- | --- |
| New skill | May introduce capability | Generate candidate capability |
| Workflow change | May affect absorbed capability | Mark for review |
| License change | May change safety boundary | Mark needs-human-review |
| New script | May inspire automation | Analyze purpose only; do not move |
| Removed capability | May signal design rollback | Evaluate whether Trellis should adjust |

## Decision

- `no-op`: No change worth absorbing.
- `watch`: Interesting change, but not suitable for Trellis now.
- `absorb-candidate`: Worth absorbing, but needs confirmation and verification scenario.
- `risk-review`: License, safety, or architecture risk requires human judgment.

## Update Record

Each update-scan outputs:

- `last_analyzed_ref`.
- `current_ref`.
- Changed files summary.
- New/changed/rejected capabilities.
- Recommended next scan trigger.
