# Delivery Loop Routing

## Responsibility Boundary

The controller decides whether to enter full audit, delta audit, early-exit, batch planning, or final acceptance. `trellis-mvp-to-delivery` executes the chosen stage: it produces the gap matrix, updates delivery state/run log, plans batches, creates or updates gap tasks, and runs final acceptance.

If the user invokes `trellis-mvp-to-delivery` directly, that skill may use its local `references/delivery-loop-policy.md` for standalone routing. If the user invokes the controller, the controller's routing decision takes precedence.

## Loop Modes

| Mode | Name | Controller condition | Allowed actions |
| --- | --- | --- | --- |
| L1 | audit-only | First post-MVP audit, or user asks for read-only audit | full/delta audit, state/log update, batch recommendation |
| L2 | assisted delivery | User confirms the gap matrix and current batch | create/update current batch gap tasks, require verifier/review gate |
| L3 | controlled continuous loop | User explicitly authorizes automatic progress to safety gates | run by L2 rules, pause at safety gates |

When `.trellis/delivery-state.md` is missing, route to `L1 + full audit`.

## Audit Scope

### Full Audit

Use full audit when:

- `.trellis/delivery-state.md` is missing.
- Source requirements changed.
- `mvp_baseline_commit` or `last_audited_commit` is missing.
- Final acceptance failed and the full requirements matrix must be realigned.
- The user asks to rebaseline.

### Delta Audit

Use delta audit when:

- `.trellis/delivery-state.md` exists.
- Source requirements did not change.
- Related code, tests, or Trellis tasks changed since `last_audited_commit`.
- Open gaps have stable `REQ-*` IDs and task links.

### Early Exit

Use early-exit when:

- Source requirements did not change.
- No related code, test, or task files changed since `last_audited_commit`.
- Blockers, human decisions, and current batch are unchanged.

Early-exit may only append a run log entry. It must not rerun full audit or create tasks.

## Batch Routing

- L1 recommends a batch only; it does not create tasks.
- L2/L3 handles only one confirmed/current batch per run.
- Maximum gap tasks per run: 3.
- Maximum high-risk tasks per run: 1.
- Final acceptance must be its own batch.

## Stop Conditions

The controller must output `pause-human-needed` when:

- The same `REQ-*` has no progress for 2 consecutive rounds.
- Verifier fails twice.
- Review reports a critical issue.
- Debugging exceeds 3 rounds and still fails.
- Work requires editing outside the File Manifest.
- Requirements, schema, auth, payment, security, or infrastructure decisions are unclear.
- Full audit conflicts with delivery state on requirement status.
