# Trellis Requirements-to-Delivery Skills

This repository provides a set of Trellis workflow skills for Codex CLI, Claude Code, and other skill-capable CLI tools, covering the full lifecycle from raw requirements documents to complete delivery — **Analyze → Plan → Trace → Audit → Close Gaps → Accept**.

## Quick Start

Run the installer from a Trellis project root, then choose Chinese or English skills:

```bash
curl -fsSL https://raw.githubusercontent.com/coldwateryi/trellis-skills/main/scripts/install-trellis-skills.sh | bash
```

If you do not have an MVP yet, start from the requirements document:

```text
The requirements are in docs/requirements.md.
Use trellis-zero-to-mvp for read-only analysis and output an MVP task plan. Do not write code yet.
```

If the MVP is already complete, enter the full delivery loop:

```text
The MVP is complete. Use trellis-mvp-to-delivery in L1 mode for the first full audit, output the complete Requirements Gap Matrix, and initialize .trellis/delivery-state.md.
```

## Skill Overview

| Skill | Language | Purpose |
| --- | --- | --- |
| `trellis-zero-to-mvp` | EN | Planning: turn a requirements document into an MVP task tree |
| `trellis-mvp-to-delivery` | EN | Planning: gap audit, gap-closing plan, final acceptance |
| `trellis-zero-to-mvp-zh` | ZH | Same as above (Chinese) |
| `trellis-mvp-to-delivery-zh` | ZH | Same as above (Chinese) |
| `trellis-implement-tdd` | EN | Execution: strict RED-GREEN-REFACTOR per AC (small-model friendly) |
| `trellis-debug-systematic` | EN | Execution: rigid 4-step debugging — reproduce→pinpoint→verify→fix |
| `trellis-review-twostage` | EN | Execution: spec compliance (small model) + code quality (strong model) gate |
| `trellis-implement-tdd-zh` | ZH | Same as above (Chinese) |
| `trellis-debug-systematic-zh` | ZH | Same as above (Chinese) |
| `trellis-review-twostage-zh` | ZH | Same as above (Chinese) |

## Progressive Usage Path

Treat this repository as a delivery pipeline, not as a set of unrelated prompts:

```text
Source requirements
  └─ trellis-zero-to-mvp: read-only analysis → MVP task tree
       └─ trellis-implement-tdd / debug-systematic / review-twostage: build the MVP
            └─ trellis-mvp-to-delivery: L1 full audit → L2 gap batches → delta audit → final acceptance
```

### Which skill should I use?

| Current state | Skill to use | Output for this round |
| --- | --- | --- |
| You only have requirements and no Trellis task tree yet | `trellis-zero-to-mvp` | Requirements Traceability Matrix, MVP boundary, parent/child task PRDs |
| You have an MVP and need to compare it with full requirements | `trellis-mvp-to-delivery` | Complete Requirements Gap Matrix, delivery state, first batch recommendation |
| You have a Trellis subtask and need to write code | `trellis-implement-tdd` | AC-by-AC red/green implementation and tests |
| A test should be green but stays red, or self-check fails | `trellis-debug-systematic` | Stable reproduction, single hypothesis, minimal fix |
| A subtask is self-check green and needs a gate | `trellis-review-twostage` | Stage 1 spec compliance + Stage 2 code quality review |

### Path A: Start from complete requirements

Use this for new projects, rewrite projects, or any project that has requirements but not yet a Trellis task tree.

```text
The requirements are in docs/requirements.md.

Use trellis-zero-to-mvp for read-only analysis:
- Assign stable REQ IDs to every source requirement
- Output a Requirements Traceability Matrix
- Define the MVP boundary and explicitly excluded scope
- Split Trellis parent and child tasks in dependency order
- Do not write code; wait for my confirmation before creating the task tree
```

`trellis-zero-to-mvp` runs a self-review loop during planning. It checks placeholders, file paths, implementation steps, acceptance assertions, and whether complex work is split small enough for execution models. After you confirm the analysis, ask it to create the Trellis task tree.

If the project already has manually implemented functionality, use this version:

```text
Requirements are in docs/requirements.md. The project already has some manually implemented functionality, and trellis init was run midway.

Use trellis-zero-to-mvp to inspect existing code, .trellis/spec/, and the requirements document, then plan only the remaining MVP tasks.
Mark implemented requirements with evidence as DONE; implemented requirements without tests as UNTESTED; create follow-up tasks only for PARTIAL and MISSING items.
```

### Path B: MVP is complete, enter the sustainable Delivery Loop

Use this once the MVP exists and you need to move from "usable" to "fully delivered". `trellis-mvp-to-delivery` is no longer just a one-shot audit. It is the outer delivery state machine: first compare the full requirements against the MVP, then advance bounded batches.

#### Round 1: L1 full audit

The first run must still compare the MVP against the real requirements and output a complete gap matrix. It initializes `.trellis/delivery-state.md` and `.trellis/delivery-run-log.jsonl` as persistent memory for later loops.

```text
The MVP is complete. Use trellis-mvp-to-delivery in L1 mode for the first full audit:
- Compare docs/requirements.md against the current MVP
- Output the complete Requirements Gap Matrix, covering every source requirement
- Mark DONE / PARTIAL / MISSING / UNTESTED / UNCLEAR
- Initialize .trellis/delivery-state.md
- Initialize .trellis/delivery-run-log.jsonl
- Recommend the first gap batch only; do not create implementation tasks
```

#### Round 2-N: L2 batch progress

After you confirm the gap matrix, advance one batch per round. The default batch limit is 3 gap tasks and at most 1 high-risk task; code-changing tasks must require worktree, verifier, and the `trellis-review-twostage` gate.

```text
Use trellis-mvp-to-delivery in L2 mode to advance the current delivery batch:
- Read .trellis/delivery-state.md
- Process only current_batch
- Require worktree + verifier + trellis-review-twostage for every code-changing task
- Do not implement functionality directly; only create or update Trellis tasks and PRDs for this batch
- Update .trellis/delivery-state.md
- Append .trellis/delivery-run-log.jsonl
```

#### Later audits: delta audit or early exit

Once delivery state exists and source requirements have not changed, later runs should not repeat full audit. They should inspect only code, tests, and Trellis task changes related to open gaps since `last_audited_commit`; if nothing relevant changed, they should early-exit.

```text
Use trellis-mvp-to-delivery to run a delta audit:
- Read last_audited_commit from .trellis/delivery-state.md
- Inspect code, tests, and task changes related to open gaps from last_audited_commit to HEAD
- Update only affected REQ entries in the Requirements Gap Matrix
- If there are no relevant changes, early-exit and only append .trellis/delivery-run-log.jsonl
```

#### Closing round: final acceptance

After all P0/P1 gaps are done or explicitly deferred by a human, run final acceptance. Final acceptance must not add features; it only classifies blocking bugs.

```text
All P0/P1 gap tasks are complete or explicitly deferred.

Use trellis-mvp-to-delivery for final acceptance:
- Read final-acceptance-template.md
- Verify every in-scope REQ in the Requirements Gap Matrix
- Summarize automated test, regression test, and manual acceptance evidence
- Do not add functionality; only classify blocking bugs
```

Most projects should converge in 3-6 outer loops: first full audit → P0/foundation batch → P1/core behavior batch → regression/final acceptance. Pause for human confirmation if the loop exceeds 6 rounds, the same REQ has no progress for 2 rounds, a verifier fails twice, or review reports critical.

## Execution-Phase Skills Detailed Usage

After planning skills (`zero-to-mvp` / `mvp-to-delivery`) create the task tree, use the following **execution-phase skills** to implement each subtask in dependency order, forming a complete **Plan→Implement→Debug→Review** loop.

### Execution-Phase Skills Overview

| Skill | Trigger Timing | Core Value | Small-Model Adaptation |
| --- | --- | --- | --- |
| `trellis-implement-tdd` | Subtask enters implementation | Turn "implement requirement" into "make test green" mechanical loop, objective signal per step | Narrow path + objective signals; small model only chases "make assertion green" |
| `trellis-debug-systematic` | Test should be green but stays red, self-check fails | Rigid 4-step script (reproduce→pinpoint→verify→fix), prevents small model from changing everywhere | Iron rules: one change at a time, re-run after every change, no guessing |
| `trellis-review-twostage` | Implementation self-check all green | Spec compliance (small model) + code quality (strong model) two-stage gate, critical blocks | Role layering: Stage 1 small model, Stage 2 strong model |

### Typical Workflow: From Task to Done

Assume you've created a task tree with `trellis-zero-to-mvp` and now want to implement the first subtask:

#### 1. Start TDD Loop

```
Now implement subtask .trellis/tasks/feature-user-auth/01-implement-login/

Please use trellis-implement-tdd for TDD landing.
```

**What the skill does**:
- Reads subtask `prd.md` (acceptance criteria, file manifest, decision table, self-check commands)
- If `design.md` exists, reads orchestration-computation separation, mount point checklist
- For each acceptance criterion (AC-001, AC-002...), executes RED-GREEN loop:
  1. **RED**: Write a failing test (copy test example from `prd.md` reference implementation)
  2. **See red**: Run test, must see failure (no failure = test didn't cover behavior, go back to fix test)
  3. **GREEN**: Write minimal code to turn it green, landing point per file manifest + design layering
  4. **See green**: Run test again, see it pass
  5. **Self-check**: Run all `prd.md` self-check commands, confirm no regression
  6. **Record**: Mark AC as done, stage changes (no commit), move to next AC

**Key constraints**:
- No failing test, no implementation code
- Only handle one AC at a time
- Don't touch files outside file manifest / forbidden list
- Don't execute `git commit` (Trellis implementation executors forbid commit)

#### 2. Debug When Red

If an AC's test should be green but stays red, or self-check command fails:

```
AC-003's test should be green but stays red, error message is "AssertionError: Expected 200, got 401"

Please use trellis-debug-systematic to pinpoint and fix.
```

**What the skill does**:
1. **Pin failure signal**: Paste error original text, confirm stable reproduction
2. **Pinpoint** (three tricks by cost low to high):
   - Read stack: Look directly at file and line from error stack
   - Binary-comment: Binary-comment suspicious code segment, see if failure disappears
   - Add one log line: Print key variable actual value, compare with expected
3. **Single hypothesis**: Write one-sentence hypothesis (specific to variable/branch), verify truth before fixing
4. **Minimal fix**: Only change the verified root cause spot, re-run original failing command immediately
5. **Defensive regression**: Ask "Can this bug happen again from elsewhere?" → If yes, add regression test

**Iron rules**:
- One change at a time
- Must re-run original failing command after change
- No guessing (pinpointing uses only three tricks)
- Beyond 3 rounds still red → Stop, escalate to strong model

#### 3. Review After Done

After all ACs turn green and self-check all green:

```
Subtask implementation self-check all green, now hand off to review.

Please use trellis-review-twostage to review this change.
```

**What the skill does**:

**Stage 1 · Spec Compliance** (small model ok, mechanical check):
- Each AC has corresponding test and is green? ⛔ Missing/red = critical
- Changed files all within file manifest? ⛔ Changed file outside = critical
- No violation of forbidden (create already-existing base class, introduce unlisted dependency)? ⛔ critical
- Decision table choices followed (annotation / naming / schema / branching)?
- Mount point checklist wired item by item (route / config / subscription / DI)? ⛔ Missing wire = critical

**Stage 2 · Code Quality** (strong model execution):
- Orchestration-computation separation: Mixed in one place?
- Structural health: Keep piling into already-fat file?
- Simplification/reuse: Duplicate implementation of existing capability? Over-abstraction (YAGNI)?
- Correctness: Boundary / error paths actually handled (not just happy path)? ⛔ Missing = critical
- Spec compliance: Naming / layering / error semantics conform to `.trellis/spec/`?

**Verdict**:
- Has **critical** → Block, send back to `trellis-implement-tdd`, only fix flagged items, re-review after fix
- Only major/minor → Pass (major suggest fix this round, minor note to remarks)
- All pass → Hand back to orchestration session to advance task status

### Role-Layered Model Assignment (Small-Model Friendly)

| Phase | Recommended Model | Reason |
| --- | --- | --- |
| Planning (zero-to-mvp / mvp-to-delivery) | Strong model (Opus 4.8 / GPT-5.5) | Needs judgment: split, boundaries, design decisions |
| Implementation (trellis-implement-tdd) | Small model (qwen3.6 35b) | Mechanical execution: make test green per PRD |
| Debugging (trellis-debug-systematic) | Small model → beyond 3 rounds escalate strong | Early mechanical pinpointing; complex root cause escalate |
| Review Stage 1 | Small model | Mechanical check spec compliance |
| Review Stage 2 | Strong model | Needs judgment: design discipline, code quality |

**Why small models can handle implementation/debugging/review Stage 1**:
- Judgment already left-shifted to planning phase (naming/branching/schema/landing/refactor all decided by strong model)
- Execution phase only faces narrow-path mechanical tasks like "make assertion green", "change one at a time", "check list item by item"
- Each step has objective signal (test red/green, command exit code), doesn't rely on small model's subjective judgment

### As-Automatic-As-Possible Mode

"As automatic as possible" means the AI advances to the next safety gate, not that it skips confirmation gates unattended. Use it when the task tree is large and you want to avoid manually naming each skill.

The AI should continue automatically by default for:

- Reading requirements, code, tests, `.trellis/`, and related specs.
- Selecting the next dependency-ready subtask or delivery batch.
- Running `trellis-implement-tdd` → `trellis-debug-systematic` → `trellis-review-twostage` for implementation tasks.
- Debugging self-check failures, with a maximum of 3 hypothesis/fix rounds per task.
- Advancing to the next ready task or next delta audit after review passes.
- Appending `.trellis/delivery-run-log.jsonl` and updating `.trellis/delivery-state.md`.

The AI must stop and ask at these safety gates:

- After first read-only analysis, before creating or modifying the Trellis task tree.
- After the first `mvp-to-delivery` L1 full audit, before confirming the gap matrix and first gap batch.
- When a task needs files outside the File Manifest, or requirement/schema/auth/payment/security/infrastructure decisions are unclear.
- When a verifier fails twice, debugging exceeds 3 rounds, or review reports critical.
- When a small model reaches `trellis-review-twostage` Stage 2, or design-quality judgment requires a strong model.
- Before any destructive git operation, commit, push, tag, or release unless the user explicitly authorized it in the current request.
- When the outer delivery loop exceeds 6 rounds, or the same `REQ-*` has no progress for 2 rounds.

#### Example A: Requirements to MVP, Mostly Automatic

```text
Please run the Trellis requirements landing flow as automatically as possible, advancing to the next safety gate.

Goal:
- Requirements are in docs/requirements.md
- Create the MVP task tree first
- Then land all MVP subtasks in dependency order
- After the MVP is complete, run trellis-mvp-to-delivery L1 full audit

Execution rules:
1. Use trellis-zero-to-mvp for read-only analysis first, outputting Requirements Traceability Matrix, MVP boundary, task split, and draft PRDs.
2. Stop before creating or modifying the Trellis task tree, and wait for my confirmation.
3. After I confirm, automatically select the next ready subtask in dependency order.
4. For each subtask, use trellis-implement-tdd for AC-by-AC red/green loops.
5. When a test should be green but stays red or self-check fails, automatically use trellis-debug-systematic; stop if still failing after 3 rounds.
6. After subtask self-check is green, automatically use trellis-review-twostage; stop when Stage 2 needs a strong model.
7. After review passes, advance task status and continue to the next subtask.
8. After all MVP subtasks are done, use trellis-mvp-to-delivery for L1 full audit, output the complete Requirements Gap Matrix, and initialize .trellis/delivery-state.md plus .trellis/delivery-run-log.jsonl.

Except for the safety gates above, do not ask me at every step.
```

#### Example B: Existing MVP, Mostly Automatic Delivery Loop

```text
The MVP is complete. Please run the trellis-mvp-to-delivery delivery loop as automatically as possible, advancing to the next safety gate.

Goal:
- Compare docs/requirements.md against the current MVP
- Complete the first L1 full audit
- Close P0/P1 gaps by batch
- Run delta audit after each batch
- Run final acceptance when conditions are met

Execution rules:
1. If .trellis/delivery-state.md does not exist, run L1 full audit first, output the complete Requirements Gap Matrix, and initialize delivery state/run log.
2. After L1 audit, stop and wait for my confirmation on the gap matrix, deferred items, and first gap batch.
3. After I confirm, enter L2 batch progress; process only current_batch per round, max 3 gap tasks, max 1 high-risk task.
4. Code-changing tasks must use an isolated worktree and require verifier + trellis-review-twostage.
5. For each task in the batch, automatically run trellis-implement-tdd → trellis-debug-systematic → trellis-review-twostage.
6. After the batch is complete, automatically run delta audit and update Requirements Gap Matrix, .trellis/delivery-state.md, and .trellis/delivery-run-log.jsonl.
7. If there are no relevant changes, early-exit and only append run log.
8. When all P0/P1 gaps are DONE or explicitly deferred by me, run final acceptance. Final acceptance must not add functionality; only classify blocking bugs.

Stop on critical review, two verifier failures, the same REQ having no progress for two rounds, a needed change outside File Manifest, or outer loop > 6 rounds.
```

#### Example C: Existing Task Tree, One Subtask Only

```text
For subtask .trellis/tasks/feature-user-auth/01-implement-login/, run the as-automatic-as-possible loop:

trellis-implement-tdd (TDD implementation) → trellis-debug-systematic (when red) → trellis-review-twostage (review) → advance status.

Only handle this subtask. Stop on critical review, debugging beyond 3 rounds, required changes outside File Manifest, or Stage 2 judgment needing a strong model.
```

#### Small-Model Auto-Prompt

```text
Task tree created. I am using qwen3.6 35b as the small model for implementation and mechanical checks; prompt me to switch to a strong model when a judgment-heavy step appears.

For each subtask:
1. [Small model] Use trellis-implement-tdd for TDD implementation
2. [Small model] Use trellis-debug-systematic when red; prompt to escalate beyond 3 rounds
3. [Small model] Run trellis-review-twostage Stage 1 spec compliance check
4. [Prompt to switch strong model] Run trellis-review-twostage Stage 2 code quality review
5. [Small model] Advance task status after review passes

Execute per this role assignment, and prompt "switch to strong model to continue Stage 2 review" when reaching Stage 2.
```

Value of this mode:

- **Reduce manual invocation**: One prompt covers planning, implementation, debugging, review, and next-round audit.
- **Standardize flow**: Every subtask passes through the TDD→debug→review quality gate.
- **Recoverable state**: `.trellis/delivery-state.md` and `.trellis/delivery-run-log.jsonl` support later delta audit.
- **Clear boundaries**: Automation stays inside confirmed scope and stops for high-risk judgment or destructive operations.

### Integration with Planning Skills

Both planning skills' SKILL.md include a "Landing Phase Integration" section, prompting to use execution-phase skills after creating task tree. Typical flow:

1. **`trellis-zero-to-mvp`** outputs task tree + execution plan sorted by dependency
2. For the first executable subtask (dependencies satisfied):
   - Invoke **`trellis-implement-tdd`** for AC-by-AC RED-GREEN loop
   - Trigger **`trellis-debug-systematic`** when hitting red light
   - Trigger **`trellis-review-twostage`** after self-check all green
3. Review passes → Advance task status → Next subtask
4. All subtasks done → **`trellis-mvp-to-delivery`** final acceptance + architecture spec write-back

## Requirement Statuses

Both skills use a unified set of requirement statuses:

| Status | Meaning |
| --- | --- |
| `DONE` | Fully implemented and tested |
| `PARTIAL` | Partially implemented |
| `MISSING` | Not yet implemented |
| `UNTESTED` | Implemented but lacking adequate tests |
| `UNCLEAR` | Requirement is not clear enough to implement |

## Installation and Compatibility

The installer first checks whether the current directory contains `.trellis/`. If the current directory is an initialized Trellis project, it installs to that project's project-level skill directories by default. If the current directory is not a Trellis project, it asks for the target project directory. If the user-provided directory still does not contain `.trellis/`, the installer asks whether to install to global skill directories instead.

It then asks whether to install Chinese skills: yes installs `trellis-zero-to-mvp-zh`, `trellis-mvp-to-delivery-zh`, and the three execution-phase skills (`trellis-implement-tdd-zh`, `trellis-debug-systematic-zh`, `trellis-review-twostage-zh`); no installs only the English variants (5 skills total).

Default project-level install locations:

- `.agents/skills/`: Codex CLI / Trellis agent compatible directory
- `.claude/skills/`: Claude Code project-level skill discovery directory

Global fallback install locations:

- `$CODEX_HOME/skills`, or `~/.codex/skills` when `CODEX_HOME` is unset: Codex CLI global skill directory
- `~/.claude/skills`: Claude Code user-level skill directory

To install to only one platform directory, set `TRELLIS_SKILLS_AGENT_TARGETS=codex` or `TRELLIS_SKILLS_AGENT_TARGETS=claude`. When unset, the default is `both`.

### macOS / Linux / Git Bash

```bash
curl -fsSL https://raw.githubusercontent.com/coldwateryi/trellis-skills/main/scripts/install-trellis-skills.sh | bash
```

Install only to the Codex / Trellis agent directory:

```bash
curl -fsSL https://raw.githubusercontent.com/coldwateryi/trellis-skills/main/scripts/install-trellis-skills.sh | TRELLIS_SKILLS_AGENT_TARGETS=codex bash
```

Install only to the Claude Code directory:

```bash
curl -fsSL https://raw.githubusercontent.com/coldwateryi/trellis-skills/main/scripts/install-trellis-skills.sh | TRELLIS_SKILLS_AGENT_TARGETS=claude bash
```

macOS default zsh also works:

```bash
curl -fsSL https://raw.githubusercontent.com/coldwateryi/trellis-skills/main/scripts/install-trellis-skills.sh | zsh
```

Local script mode:

```bash
cd /path/to/trellis-skills/scripts
bash ./install-trellis-skills.sh
# or
zsh ./install-trellis-skills.sh
```

### PowerShell

```powershell
irm https://raw.githubusercontent.com/coldwateryi/trellis-skills/main/scripts/install-trellis-skills.ps1 | iex
```

Install only to the Claude Code directory:

```powershell
$env:TRELLIS_SKILLS_AGENT_TARGETS = "claude"
irm https://raw.githubusercontent.com/coldwateryi/trellis-skills/main/scripts/install-trellis-skills.ps1 | iex
```

Local script mode:

```powershell
cd C:\path\to\trellis-skills\scripts
.\install-trellis-skills.ps1
.\install-trellis-skills.ps1 -AgentTargets claude
```

The script primarily supports `bash` and `zsh`. If it is run with another incompatible shell such as `sh` or `dash`, it exits with a prompt to use `bash` or `zsh`. The script reads interactive answers from the current terminal, so target-directory and language prompts work even when the installer is run through `curl | bash` or `curl | zsh`.

If you run the script directly from this repository's `scripts/` directory, it first updates the parent `trellis-skills` directory from the GitHub `main` branch, then continues with the install flow above. The update uses fast-forward merge; if local changes exist or the branch cannot fast-forward, the script stops instead of overwriting local work.

Claude Code discovers project-level skills from `.claude/skills/<skill-name>/SKILL.md` and user-level skills from `~/.claude/skills/<skill-name>/SKILL.md`. `agents/openai.yaml` is additional configuration for Codex/OpenAI-compatible runners and can be ignored by Claude Code.

## Advanced Mechanisms

### Self-Review Loop and Design Shift-left

All skills support a self-review loop and shift complex-task design, implementation steps, and stable context manifests into the planning phase, so output can meet execution requirements for small parameter models such as qwen3.6 35b.

How it works:

1. **Analyze**: generate the first requirements traceability matrix, task split, and PRDs
2. **Self-review**: check against a 45-60 item checklist
3. **Targeted improvement**: fix only marked issues, not a full redo
4. **Converge**: repeat 2-3 rounds until checks pass
5. **User confirmation**: create the task tree only after the output meets standards

Key benefits:

- Small-model friendly: removes placeholders and provides concrete paths and steps
- Design shift-left: adds Context Manifest, Decision Table, `design.md`, `implement.md`, `implement.jsonl`, and `check.jsonl` for medium/high complexity tasks
- Quality assurance: precise checks with issues located to specific lines
- Cost control: ROI > 5:1 (planning costs +45k tokens, execution saves 200k tokens)

See [Optimization Proposal](doc/OPTIMIZATION_PROPOSAL.md) and [Final Summary](doc/FINAL_SUMMARY.md).

### Trellis 0.6 Beta Compatibility

These skills remain compatible with the core Trellis task layout (`.trellis/tasks/`, `.trellis/spec/`, `task.py create --parent`) and include 0.6 beta workflow support:

- If `.trellis/workflow.md` exists, treat it as the local workflow contract.
- If `.trellis/config.yaml`, `.trellis/.version`, `.trellis/.developer`, or `.trellis/workspace/` exist, include them in planning context.
- Check `.trellis/spec/` freshness before planning implementation-heavy tasks; plan spec refresh/bootstrap when specs are missing, generic, or stale.
- For medium/high complexity tasks, add `design.md`, `implement.md`, `implement.jsonl`, and `check.jsonl` in addition to `prd.md` when the project workflow expects them.
- Prefer `trellis init -u <name>` for first-time setup, with the project platform flag when needed; keep `init_developer.py` as a legacy fallback.

## Directory Structure

```
trellis-skills/
├── trellis-zero-to-mvp/          # Planning: Zero → MVP (English)
│   ├── SKILL.md                  # Skill definition & workflow
│   ├── agents/
│   │   └── openai.yaml           # OpenAI-compatible runner config
│   └── references/
│       ├── analysis-output-template.md   # Read-only analysis template
│       ├── parent-prd-template.md        # Parent task PRD template
│       ├── child-prd-template.md         # Child task PRD template
│       ├── planning-artifacts-template.md # 0.6 beta design/implementation/context manifest template
│       ├── self-review-checklist.md      # Self-review checklist
│       ├── self-review-report-template.md # Self-review report template
│       └── task-creation-checklist.md    # Task creation checklist
├── trellis-mvp-to-delivery/      # Planning: MVP → Delivery (English)
│   ├── SKILL.md
│   ├── agents/
│   │   └── openai.yaml
│   └── references/
│       ├── gap-audit-template.md         # Gap audit template
│       ├── delivery-loop-policy.md       # Sustainable delivery loop policy
│       ├── delivery-loop-state-template.md # .trellis/delivery-state.md template
│       ├── delivery-batch-template.md    # Single-run gap batch template
│       ├── delivery-run-log-template.md  # .trellis/delivery-run-log.jsonl template
│       ├── delivery-task-prd-template.md # Gap-closing task PRD template
│       ├── planning-artifacts-template.md # 0.6 beta design/implementation/context manifest template
│       ├── test-coverage-matrix-template.md  # Test coverage matrix template
│       ├── final-acceptance-template.md      # Final acceptance template
│       ├── bug-classification-rules.md       # Bug classification rules
│       ├── self-review-checklist.md      # Self-review checklist
│       └── self-review-report-template.md # Self-review report template
├── trellis-zero-to-mvp-zh/       # Planning: Zero → MVP (Chinese)
│   └── (same structure as trellis-zero-to-mvp)
├── trellis-mvp-to-delivery-zh/   # Planning: MVP → Delivery (Chinese)
│   └── (same structure as trellis-mvp-to-delivery)
├── trellis-implement-tdd/        # Execution: TDD Implementation (English)
│   ├── SKILL.md
│   ├── agents/
│   │   └── openai.yaml
│   └── references/
│       ├── tdd-loop-protocol.md      # RED-GREEN loop protocol
│       └── tdd-progress-template.md  # Progress table template
├── trellis-debug-systematic/     # Execution: Systematic Debugging (English)
│   ├── SKILL.md
│   ├── agents/
│   │   └── openai.yaml
│   └── references/
│       ├── debug-protocol.md         # 4-step debugging script
│       └── debug-report-template.md  # Debugging record template
├── trellis-review-twostage/      # Execution: Two-Stage Review (English)
│   ├── SKILL.md
│   ├── agents/
│   │   └── openai.yaml
│   └── references/
│       ├── review-stage1-checklist.md # Stage 1 spec compliance checklist
│       ├── review-stage2-checklist.md # Stage 2 code quality checklist
│       └── review-report-template.md  # Review report template
├── trellis-implement-tdd-zh/     # Execution: TDD Implementation (Chinese)
│   └── (same structure as trellis-implement-tdd)
├── trellis-debug-systematic-zh/  # Execution: Systematic Debugging (Chinese)
│   └── (same structure as trellis-debug-systematic)
├── trellis-review-twostage-zh/   # Execution: Two-Stage Review (Chinese)
│   └── (same structure as trellis-review-twostage)
├── doc/                          # Design documents
│   ├── FRAMEWORK_COMPARISON_REPORT.md       # 5-framework deep comparison
│   ├── REQUIREMENT_LANDING_ENHANCEMENT.md   # Requirement landing enhancement design
│   ├── OPTIMIZATION_PROPOSAL.md             # Optimization proposal
│   └── FINAL_SUMMARY.md                     # Implementation summary
├── scripts/                      # Install skills from the GitHub main branch
│   ├── install-trellis-skills.sh
│   └── install-trellis-skills.ps1
├── README.md                     # Chinese README
└── README_EN.md                  # English README (this file)
```

## Prerequisites

- Codex CLI, Claude Code, or another skill-capable CLI tool installed
- Trellis initialized in the project (`.trellis/` directory exists)
- Prefer `trellis init -u <name>` before first use to set the developer identity, adding the project platform flag when needed (for example `--codex`)
- If the Trellis CLI is unavailable, use the legacy fallback: `python ./.trellis/scripts/init_developer.py <name>`

## Key Principles

- **Analyze first, act later** — Every skill starts with a read-only pass. No tasks are created and no code is written until you confirm.
- **Split by capability, not by file** — Each child task maps to an independently verifiable business or technical capability.
- **Stable IDs** — Requirement IDs (REQ-xxx) and acceptance criteria IDs (AC-xxx) are assigned during analysis and remain fixed thereafter.
- **Explicit dependencies** — Parent/child task relationships express structure only. True execution dependencies are written into each child task's PRD.

## Acknowledgements

This project's design references ideas and practices from the following open-source projects:

- [obra/superpowers](https://github.com/obra/superpowers)
- [open-gsd/gsd-core](https://github.com/open-gsd/gsd-core)
- [liuzhengdongfortest/CodeStable](https://github.com/liuzhengdongfortest/CodeStable)

Thanks to these projects for influencing the skill organization, requirement-to-delivery workflow, and engineering quality constraints used here.
