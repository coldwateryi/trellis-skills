---
name: trellis-skill-assimilator
description: |
  Extract reusable engineering capabilities from external GitHub skill projects and produce safe Trellis absorption plans. Use when the user provides a GitHub repository URL, skill project URL, open-source agent skill collection, or asks to compare or update projects such as superpowers, gsd, CodeStable, loop-engineering, ponytail, or similar. Analyze README/SKILL.md/references/scripts/license and produce source analysis, capability extraction, absorption card, Trellis target mapping, risk judgment, update-scan delta report, and verification scenario recommendations. Do not copy third-party skill text directly; absorb capability patterns, workflow structure, and verifiable design only.
---

# Trellis Skill Assimilator

## Overview

Convert useful patterns from external GitHub skill projects into governed Trellis capabilities. The goal is not to copy a skill. The goal is to answer:

- What engineering problem does the project solve?
- Which Trellis capabilities are missing or weak?
- Which capabilities should be absorbed, watched, or rejected?
- Which Trellis stage, reference, or gate should receive the capability?
- How will we verify that the absorption improves output quality?

## Guardrails

- Do not copy large passages from third-party skills.
- Absorb by capability, not by project name.
- Do not absorb a capability without a Trellis target.
- Do not merge a capability without a verification scenario.
- When license is unclear, strong copyleft, commercially restricted, or untrusted, only summarize ideas; do not move text, scripts, or templates.
- Do not directly modify Trellis core skills; first produce an absorption plan and verification recommendation, then wait for user confirmation.
- Do not put absorption governance into `trellis-zero-to-mvp`, `trellis-mvp-to-delivery`, or `trellis-delivery-controller`.

## Modes

### Initial Assimilation

Use for first-time analysis of an external GitHub skill project.

1. Read `references/source-analysis-template.md`.
2. Analyze repository README, skill directories, `SKILL.md`, references, scripts, docs, and license.
3. Read `references/capability-taxonomy.md` and classify findings as capabilities.
4. Read `references/trellis-target-map.md` and map capabilities to Trellis targets.
5. Read `references/license-safety-policy.md` and decide the absorption boundary.
6. Use `references/absorption-card-template.md` to output the absorption card.

### Update Scan

Use when a previously analyzed project changes.

1. Read the existing absorption card or user-provided `last_analyzed_ref`.
2. Compare current ref against `last_analyzed_ref` for README, `SKILL.md`, references, scripts, docs, and license changes.
3. Read `references/update-scan-policy.md` and analyze only new capabilities, changed capabilities, risk changes, or updates to already absorbed capabilities.
4. Output a delta absorption report.

## Output

Every run must output:

- Source Analysis.
- Capability Extraction.
- Absorption Card.
- Trellis Target Map.
- License and Safety Notes.
- Evaluation Requirements.
- Recommendation: `absorb`, `watch`, `reject`, or `needs-human-review`.

If recommending absorption, also provide:

- Trellis files to add or modify.
- Purpose of each change.
- New verification scenario.
- Rollback condition.
- Whether strong-model or human review is required.

## References

- `references/source-analysis-template.md` - Read when analyzing external repository structure and capability.
- `references/absorption-card-template.md` - Read when producing an absorption card.
- `references/capability-taxonomy.md` - Read when classifying and naming capabilities.
- `references/trellis-target-map.md` - Read when mapping to Trellis targets.
- `references/license-safety-policy.md` - Read when deciding license and content movement boundaries.
- `references/update-scan-policy.md` - Read when scanning an already analyzed project for changes.
