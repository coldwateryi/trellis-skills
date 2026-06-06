# Trellis Requirements-to-Delivery Skills

This repository provides a set of Trellis workflow skills for Codex CLI, Claude Code, and other skill-capable CLI tools, covering the full lifecycle from raw requirements documents to complete delivery — **Analyze → Plan → Trace → Audit → Close Gaps → Accept**.

## Skill Overview

| Skill | Language | Purpose |
| --- | --- | --- |
| `trellis-zero-to-mvp` | EN | Zero to MVP: turn a requirements document into an MVP task tree |
| `trellis-mvp-to-delivery` | EN | MVP to Delivery: gap audit, gap-closing plan, final acceptance |
| `trellis-zero-to-mvp-zh` | ZH | Same as above (Chinese) |
| `trellis-mvp-to-delivery-zh` | ZH | Same as above (Chinese) |

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

It then asks whether to install Chinese skills: yes installs only `trellis-zero-to-mvp-zh` and `trellis-mvp-to-delivery-zh`; no installs only the English variants.

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
skills/
├── trellis-zero-to-mvp/          # Zero → MVP (English)
│   ├── SKILL.md                  # Skill definition & workflow
│   ├── agents/
│   │   └── openai.yaml           # OpenAI-compatible runner config
│   └── references/
│       ├── analysis-output-template.md   # Read-only analysis template
│       ├── parent-prd-template.md        # Parent task PRD template
│       ├── child-prd-template.md         # Child task PRD template
│       ├── planning-artifacts-template.md # 0.6 beta design/implementation/context manifest template
│       └── task-creation-checklist.md    # Task creation checklist
├── trellis-mvp-to-delivery/      # MVP → Delivery (English)
│   ├── SKILL.md
│   ├── agents/
│   │   └── openai.yaml
│   └── references/
│       ├── gap-audit-template.md         # Gap audit template
│       ├── delivery-task-prd-template.md # Gap-closing task PRD template
│       ├── planning-artifacts-template.md # 0.6 beta design/implementation/context manifest template
│       ├── test-coverage-matrix-template.md  # Test coverage matrix template
│       ├── final-acceptance-template.md      # Final acceptance template
│       └── bug-classification-rules.md       # Bug classification rules
├── trellis-zero-to-mvp-zh/       # Zero → MVP (Chinese)
│   └── (same structure as above)
├── trellis-mvp-to-delivery-zh/   # MVP → Delivery (Chinese)
│   └── (same structure as above)
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
