# Trellis Requirements-to-Delivery Skills

This repository provides a set of Trellis workflow skills for Codex CLI, Claude Code, and other skill-capable CLI tools, covering the full lifecycle from raw requirements documents to complete delivery — **Analyze → Plan → Trace → Audit → Close Gaps → Accept**.

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

### ✨ New Feature: Self-Review Loop and Design Shift-left

**All skills now support a self-review loop and shift complex-task design, implementation steps, and stable context manifests into the planning phase, so output can meet execution requirements for small parameter models (e.g., qwen3.6 35b).**

**How It Works**:
1. 🔍 **Analyze** - Generate initial requirements traceability matrix, task split, and PRDs
2. ✅ **Self-Review** - Check against 45-60 item checklist
3. 🔧 **Targeted Improvements** - Fix only marked issues, not full redo
4. 🔄 **Iterative Convergence** - Repeat 2-3 rounds until all checks pass
5. ✅ **User Confirmation** - Create task tree only after meeting standards

**Key Benefits**:
- ✅ **Small Model Friendly** - Eliminates placeholders, provides concrete paths and steps
- ✅ **Design Shift-left** - Adds Context Manifest, Decision Table, `design.md`, `implement.md`, `implement.jsonl`, and `check.jsonl` for medium/high complexity tasks
- ✅ **Quality Assurance** - 45-60 precise checks, issues located to specific lines
- ✅ **Cost Effective** - ROI > 5:1 (planning costs +45k tokens, execution saves 200k tokens)
- ✅ **Proven Results** - Execution success rate improves 30%-50%

See: [Optimization Proposal](doc/OPTIMIZATION_PROPOSAL.md) and [Final Summary](doc/FINAL_SUMMARY.md)

## Trellis 0.6 Beta Compatibility

These skills remain compatible with the core Trellis task layout (`.trellis/tasks/`, `.trellis/spec/`, `task.py create --parent`) and now include 0.6 beta workflow support:

- If `.trellis/workflow.md` exists, treat it as the local workflow contract.
- If `.trellis/config.yaml`, `.trellis/.version`, `.trellis/.developer`, or `.trellis/workspace/` exist, include them in planning context.
- Check `.trellis/spec/` freshness before planning implementation-heavy tasks; plan spec refresh/bootstrap when specs are missing, generic, or stale.
- For medium/high complexity tasks, add `design.md`, `implement.md`, `implement.jsonl`, and `check.jsonl` in addition to `prd.md` when the project workflow expects them.
- Prefer `trellis init -u <name>` for first-time setup, with the project platform flag when needed; keep `init_developer.py` as a legacy fallback.

## Install From GitHub

The installer first checks whether the current directory contains `.trellis/`. If the current directory is an initialized Trellis project, it installs to that project's project-level skill directories by default. If the current directory is not a Trellis project, it asks for the target project directory. If the user-provided directory still does not contain `.trellis/`, the installer asks whether to install to global skill directories instead.

It then asks whether to install Chinese skills: yes installs `trellis-zero-to-mvp-zh`, `trellis-mvp-to-delivery-zh`, and the three execution-phase skills (`trellis-implement-tdd-zh`, `trellis-debug-systematic-zh`, `trellis-review-twostage-zh`); no installs only the English variants (5 skills total).

Default project-level install locations:

- `.agents/skills/`: Codex CLI / Trellis agent compatible directory
- `.claude/skills/`: Claude Code project-level skill discovery directory

Global fallback install locations:

- `$CODEX_HOME/skills`, or `~/.codex/skills` when `CODEX_HOME` is unset: Codex CLI global skill directory
- `~/.claude/skills`: Claude Code user-level skill directory

To install to only one platform directory, set `TRELLIS_SKILLS_AGENT_TARGETS=codex` or `TRELLIS_SKILLS_AGENT_TARGETS=claude`. When unset, the default is `both`.

If you run the script directly from this repository's `scripts/` directory, it first updates the parent `trellis-skills` directory from the GitHub `main` branch, then continues with the install flow above. The update uses fast-forward merge; if local changes exist or the branch cannot fast-forward, the script stops instead of overwriting local work.

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

The script primarily supports `bash` and `zsh`. If it is run with another incompatible shell such as `sh` or `dash`, it exits with a prompt to use `bash` or `zsh`. The script reads interactive answers from the current terminal, so target-directory and language prompts work even when the installer is run through `curl | bash` or `curl | zsh`.

During installation, the script prints step logs with a `[trellis-skills]` prefix. If something fails, keep the full installer output so the shell, working directory, target directory, source location, and failed step can be diagnosed.

Local script mode:

```bash
cd /path/to/trellis-skills/scripts
bash ./install-trellis-skills.sh
# or
zsh ./install-trellis-skills.sh

# Install only to the Claude Code project-level skill directory
TRELLIS_SKILLS_AGENT_TARGETS=claude bash ./install-trellis-skills.sh
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

# Install only to the Claude Code project-level skill directory
.\install-trellis-skills.ps1 -AgentTargets claude
```

## Claude Code Compatibility

Claude Code discovers project-level skills from `.claude/skills/<skill-name>/SKILL.md` and user-level skills from `~/.claude/skills/<skill-name>/SKILL.md`. The four skill directories already contain the required `SKILL.md` entry point and reference files; `agents/openai.yaml` is additional configuration for Codex/OpenAI-compatible runners and can be ignored by Claude Code.

For project-level installs, the installers write to both `.agents/skills/` and `.claude/skills/` by default, so the same Trellis project can be recognized by Codex CLI and Claude Code. The installers use global directories only when both the current directory and the user-provided directory are not Trellis projects and the user confirms the global fallback. If a team uses only one runner, limit the target with `TRELLIS_SKILLS_AGENT_TARGETS` or the PowerShell `-AgentTargets` parameter.

## Recommended Workflow

```
Requirements ──→ [Zero to MVP] ──→ MVP Task Tree ──→ Build the MVP
                                                          │
                                                          ▼
                              Requirements ──→ [MVP to Delivery] ──→ Gap Tasks ──→ Delivery & Acceptance
```

### Phase 1: Zero → MVP

When you have a complete requirements document (PRD / product brief / feature spec) and haven't started coding yet:

1. Place the requirements document in the project
2. Invoke `trellis-zero-to-mvp` (or the Chinese variant `trellis-zero-to-mvp-zh`)
3. The skill performs a **read-only analysis** and outputs:
   - Requirements Traceability Matrix
   - Module dependency graph
   - Capability-based task split
   - Dependency-ordered MVP development sequence
   - Draft parent and child PRDs
4. **After confirming the analysis**, the skill creates the Trellis task tree
5. Start coding in the recommended order

### Phase 2: MVP → Delivery

After the MVP is implemented, return to the source requirements document for complete delivery:

1. Invoke `trellis-mvp-to-delivery` (or the Chinese variant `trellis-mvp-to-delivery-zh`)
2. The skill performs a **gap audit**, checking the MVP against every requirement:
   - Requirements Traceability Matrix (with DONE / PARTIAL / MISSING / UNTESTED / UNCLEAR statuses)
   - MVP completion summary
   - Dependency-ordered gap-closing task plan
   - Automated test coverage requirements
3. **After confirming the audit**, the skill creates gap-closing Trellis tasks
4. Close gaps by priority, add tests, and run final acceptance

## Recommended Usage

### Scenario 1: New Project Kickoff

```
We're starting a new project. The requirements are in docs/requirements.md.

Use trellis-zero-to-mvp to turn this into an MVP task plan.
```

The skill starts with a read-only analysis — no code is written. Only after you confirm the task split and MVP boundary will it create the Trellis task tree.

**✨ Self-Review Loop**: The analysis process automatically performs 2-3 rounds of quality checks to ensure:
- ✅ All `<...>` placeholders replaced with concrete values
- ✅ File Manifest contains precise file paths
- ✅ Implementation Steps are executable concrete actions
- ✅ Complex tasks split to fit small model execution

### Scenario 2: MVP Ready for Full Delivery

```
The MVP is complete. Source requirements are in docs/requirements.md.

Use trellis-mvp-to-delivery to audit the MVP and plan full delivery.
```

The skill checks existing implementation and tests against the requirements document, identifies every gap, and creates gap-closing tasks.

**✨ Self-Review Loop**: The audit process automatically performs quality checks to ensure:
- ✅ Each DONE status has implementation evidence and test evidence
- ✅ Gap-closing task PRDs explicitly state not breaking MVP behavior
- ✅ Regression Tests cover MVP core flows
- ✅ Bug fix branch logic clearly pinned down

### Scenario 3: Partially Implemented Project Before MVP

```
Requirements are in docs/requirements.md. The project already has some manually implemented functionality, and trellis init was run midway.

Use trellis-zero-to-mvp to inspect existing code, .trellis/spec/, and the requirements document, then plan only the remaining MVP tasks.
```

The skill first produces an Existing Implementation Baseline, then handles requirement statuses as follows:

- `DONE`: creates no implementation task; uses evidence as an existing dependency.
- `UNTESTED`: creates only test coverage tasks.
- `PARTIAL`: creates only gap-closing tasks for missing behavior.
- `MISSING`: creates new implementation tasks.

### Scenario 4: Iterative Development

In practice, the two skills can be used in cycles:

1. Use `zero-to-mvp` to plan the first shippable version
2. Build the MVP
3. Use `mvp-to-delivery` to audit gaps and close them for full delivery
4. If new requirements arrive, return to step 1 and run `zero-to-mvp` again for the new scope

## Execution-Phase Skills Detailed Usage

After planning skills (`zero-to-mvp` / `mvp-to-delivery`) create the task tree, use the following **execution-phase skills** to implement each subtask in dependency order, forming a complete **Plan→Implement→Debug→Review** loop.

### Execution-Phase Skills Overview

| Skill | Trigger Timing | Core Value | Small-Model Adaptation |
| --- | --- | --- | --- |
| `trellis-implement-tdd` | Subtask enters implementation | Turn "implement requirement" into "make test green" mechanical loop, objective signal per step | ✅ Narrow path + objective signals, small model just chases "make assertion green" |
| `trellis-debug-systematic` | Test should be green but stays red, self-check fails | Rigid 4-step script (reproduce→pinpoint→verify→fix), prevents small model from changing everywhere | ✅ Iron rules: "one change at a time, must re-run after change, no guessing" |
| `trellis-review-twostage` | Implementation self-check all green | Spec compliance (small model) + code quality (strong model) two-stage gate, critical blocks | ✅ Role layering: Stage 1 small model, Stage 2 strong model |

### Typical Workflow: From Task to Done

Assume you've created a task tree with `trellis-zero-to-mvp` and now want to implement the first subtask:

#### 1️⃣ Start TDD Loop

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

#### 2️⃣ Debug When Red

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

#### 3️⃣ Review After Done

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

### Auto-Trigger Scenario Prompts

To avoid manually invoking execution-phase skills per subtask, use the following **auto-orchestration prompts** to let AI automatically drive the complete implement→debug→review loop:

#### English Auto-Orchestration Prompt

\`\`\`
Task tree created. Now automatically land all subtasks in dependency order, for each subtask:

1. Use trellis-implement-tdd for TDD implementation, AC-by-AC RED-GREEN loop
2. When test should be green but stays red or self-check fails, auto-switch to trellis-debug-systematic
3. After implementation self-check all green, auto-invoke trellis-review-twostage for two-stage review
4. After review passes, advance task status and continue to next subtask
5. After all subtasks complete, use trellis-mvp-to-delivery for final acceptance

Please execute the above flow automatically, stop to ask when hitting points requiring human decision.
\`\`\`

#### Small-Model Auto-Prompt (Role Layering)

If using qwen3.6 35b or similar small models, explicitly specify role layering in the prompt:

\`\`\`
Task tree created. Now I (qwen3.6 35b small model) handle implementation and mechanical checks, auto-prompt to switch to strong model when hitting judgment-requiring points.

For each subtask:
1. [Small model] Use trellis-implement-tdd for TDD implementation
2. [Small model] Use trellis-debug-systematic when red (prompt to escalate strong model beyond 3 rounds)
3. [Small model] trellis-review-twostage Stage 1 spec compliance check
4. [Prompt to switch strong model] trellis-review-twostage Stage 2 code quality review
5. [Small model] Advance task status after review passes

Please execute per above role assignment, prompt "switch to strong model to continue Stage 2 review" when reaching Stage 2 review.
\`\`\`

#### Single-Subtask Quick Trigger

If task tree already exists and you only want to execute the full loop for one specific subtask:

\`\`\`
For subtask .trellis/tasks/feature-user-auth/01-implement-login/ execute full implementation loop:

trellis-implement-tdd (TDD implementation) → trellis-debug-systematic (when red) → trellis-review-twostage (review) → advance status

Please execute automatically, report when blocked.
\`\`\`

#### Value of Automation

Benefits of using auto-trigger prompts:
- ✅ **Reduce manual invocation**: One prompt covers full flow, no need to manually invoke each skill
- ✅ **Standardize flow**: Guarantee every subtask goes through complete TDD→Debug→Review quality gate
- ✅ **Auto role switching**: Clear when to use small model, when to escalate strong model, cost optimal
- ✅ **Batch landing friendly**: With 10+ subtasks in task tree, auto mode significantly improves efficiency

> **Note**: In auto mode, AI still stops to ask when hitting points it cannot automatically decide (review finds critical issue, debugging beyond 3 rounds unresolved, needs to supplement PRD info, etc.), not fully unattended.

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
