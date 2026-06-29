---
name: trellis-zero-to-mvp-zh
description: |
  从完整需求文档创建 Trellis MVP 任务树。用于 Codex 收到产品说明、需求文档、PRD、从 0 到 MVP 的新项目需求、大型能力建设请求，或已经手工实现了一部分功能的项目时，先做只读分析，分配稳定 REQ/AC 编号，生成需求追踪矩阵和项目契约，识别已有实现证据，通过渐进式批次规划和子代理协作形成完整 MVP 父子任务树、PRD、设计/实现产物计划，并在用户确认后创建 Trellis 任务；不编写应用代码。
---

# Trellis 从 0 到 MVP

## 概览

将原始需求文档转化为 MVP 规模的 Trellis 交付计划。产出物是经用户确认的父任务、覆盖完整 MVP 范围的子任务、PRD 和必要规划产物，而不是应用代码。

把本技能当作规划编译器执行：

1. 源需求和本地代码/README/spec 是输入。
2. Full Requirement Matrix、MVP Coverage Matrix 和 Subtask Planning Ledger 是唯一中间表示。
3. Trellis task、`prd.md`、`design.md`、`implement.md`、JSONL 是输出。
4. Gate 是编译检查。Gate 未通过时停止并修复，不要继续下一阶段。
5. 小模型长程规划按 Stage State Packet 推进；每次跨阶段或恢复上下文时从矩阵、账本和真实目录重建状态，不依赖上一轮自然语言记忆。

## 核心不变量（分阶段标签）

> **小模型指引**：每个阶段只需关注本阶段标签下的不变量。进入下一阶段时再读对应的新规则。不要在 S0 试图记住全部 25 条规则。

### S0-S2 通用（发现与需求阶段）
- S0-S2: 不要编写业务代码。
- S0-S2: 在用户确认完整只读规划前，不要创建 Trellis task。
- S0-S2: 不要按文件拆任务。按可独立验收的业务能力或技术能力拆任务。
- S0-S2: 先完整抽取源需求，再规划 MVP。所有源需求功能点都必须进入 Full Requirement Matrix；若不进入当前 MVP，必须标记 `OUT_OF_SCOPE` 或 `BLOCKED` 并进入 Backlog。
- S0-S2: `REQ-xxx` 是源需求功能点的稳定身份，不是交付顺序编号；任务合并、拆分或重排只能改变 `Txx`。
- S0-S2: 必须分开维护 Full Requirement Matrix 和 MVP Coverage Matrix；禁止把 MVP 覆盖数量写成原始功能点总数。

### S2-S4 专用（契约与任务规划阶段）
- S2-S4: 规划任务前必须先选择 Project Contract Profile，再形成 Project Contract Lock 和 Contract Snapshot；后续父/子 PRD、`design.md`、`implement.md`、JSONL 只能采用其中的命名、路径、命令、API、包/模块、路由、表名、权限前缀和证据路径。
- S2-S4: 本地上下文优先级固定为：用户明确要求 > 源需求业务功能 > README/模块 README/AGENTS.md > `.trellis/spec/` > 现有代码结构 > 框架默认习惯 > 模型常识。
- S2-S4: 小模型或长程任务必须读取 `references/small-model-safety.md`，并在每个阶段输出 Stage State Packet；出现计数漂移、契约漂移或 Gate 与扫描不一致时立即 Drift Reset。
- S3-S4: Small Model Mode 下，一个子任务只覆盖一个主实体 CRUD、一个接口组、一个状态流转、一个前端页面或一个后端聚合查询；违反时继续拆分，除非用户明确点名允许合并。
- S3-S4: Small Model Mode 下单批最多创建 8 个可执行子任务，单批最多完整写入 5 个高质量子任务 PRD。分批是容量控制，不是范围裁剪。
- S3-S4: 分批规划必须维护 Subtask Planning Ledger。只完成 P0/P1 不等于完成规划；所有 MVP `TASK` 子任务都达到 `READY_TO_CONFIRM`、`BLOCKED` 或 `OUT_OF_SCOPE` 前，不得请求用户确认。

### 全阶段通用（S0-S10）
- 遵守 Trellis 规划产物边界：`prd.md` 只承载需求、约束、范围、依赖和验收；技术设计放 `design.md`；文件计划、实现步骤、自检命令、回滚点和评审门放 `implement.md`。只有本地工作流允许 PRD-only 且任务为低复杂度时，才能把精简执行附录留在 `prd.md`。
- 外部配置、第三方 key、地图/硬件/外部接口等不确定项必须归类为 `FIXED`、`BASELINE`、`BLOCKED` 或 `OUT_OF_SCOPE`。
- 对已有部分实现的项目，任务创建规则固定为：`DONE` -> 不建任务；`UNTESTED` -> 只建测试补齐任务；`PARTIAL` -> 只为缺失行为创建补缺任务；`MISSING` -> 创建新实现任务；`UNCLEAR` -> 阻塞问题或澄清任务。
- 小模型执行需要的窄路径仍必须在规划期定死；但优先写入 `design.md` / `implement.md`，不要用重型 PRD 破坏 Trellis artifact boundary。
- 当候选子任务超过单批上限、业务域超过 3 个、完整 PRD 草案超过 5 个，或用户要求多 agent 规划时，优先读取 `references/subagent-planning-template.md` 并唤起子代理；若当前平台不支持子代理，按同一 Agent Packet 串行模拟。
- `task.py create` 只负责创建任务目录和基础种子文件；规划产物矩阵或 PRD 声明需要的文件，创建任务后必须由本技能写入真实任务目录。
- 创建任务目录只能通过 `task.py create`。后续写文件必须使用 `task.py create` 输出的真实目录；不要按逻辑 Task ID 或 slug 自行拼路径。
- 每个任务的 PRD 只能写到真实任务目录根部的 `<task-dir>/prd.md`，且该目录必须包含 `task.json`。
- Artifact Gate 不能由模型手填。创建任务并写入产物后，必须运行 `scripts/trellis_zero_gate.py` 或等价机械扫描；最终 Gate 数值必须来自工具输出。

### S5-S6 专用（门控与确认阶段）
- S5-S6: Trellis 0.6+ 项目存在 `.trellis/workflow.md` 时，必须把它当作本地工作流契约；项目声明 `design.md`、`implement.md`、`implement.jsonl` 或 `check.jsonl` 时，不要按旧 PRD-only 工作流执行。
- S5-S6: Codex 项目必须读取 `.trellis/config.yaml` 的 `codex.dispatch_mode`：`inline` 模式下 JSONL 不作为规划就绪门槛，创建任务后可删除 seed JSONL 或标记 `NOT_NEEDED_WITH_REASON`；`sub-agent` 模式下必须填真实 `implement.jsonl` / `check.jsonl`，seed-only 不可通过。
- S6-S7: Artifact Gate 结果不是 `PASS` 时，不得汇报任务树可执行。

## Stop Gates

以下任一条件命中时，停止当前阶段，只输出 `FAIL` 报告、失败码和修复清单，不得继续创建任务、不得汇报任务树可执行：

- Project Contract Lock、Contract Snapshot 或证据路径缺失。
- 没有 Full Requirement Matrix、MVP Coverage Matrix 或 Subtask Planning Ledger。
- 任一源需求功能点没有覆盖状态，或覆盖统计与矩阵机械统计不一致。
- Subtask Planning Ledger 与 MVP Coverage Matrix 不一致。
- 存在 `UNASSIGNED_MVP_REQ`、`UNBATCHED_TASK`、`P0P1_ONLY_PLAN` 或 `DEFERRED_PRD_WITHOUT_PLAN`。
- 子任务候选违反 Small Model Mode 粒度规则，且没有用户显式确认合并。
- 用户确认前仍有 MVP `TASK` 子任务未达到 `READY_TO_CONFIRM`、`BLOCKED` 或 `OUT_OF_SCOPE`。
- PRD 声明需要 `design.md`、`implement.md`、`implement.jsonl` 或 `check.jsonl`，但真实任务目录缺失对应文件。
- 子任务 PRD 的“任务影响面矩阵”声明某影响面为“是”，但 `design.md` 或 `implement.md` 缺少对应章节。
- 在 sub-agent-dispatch 模式或规划产物矩阵声明 JSONL 为 `需要` 时，`implement.jsonl` 或 `check.jsonl` 包含 `_example` 种子行；Codex inline 模式下 seed JSONL 必须删除或按 `NOT_NEEDED_WITH_REASON` 解释，并使用 `--jsonl-mode inline` 运行 Gate。
- 产物包含 `{Entity}`、`{domain}`、`{entity}`、`<PageComponent>`、`<path>`、`TBD`、`待定`、`视情况`、`根据实际情况`、`YOUR_KEY`、`API_KEY_HERE`、`待用户提供`、`待配置` 或 `待申请`。
- Contract Snapshot forbidden tokens 在父/子 PRD、`design.md`、`implement.md` 或 JSONL 中命中。
- Gate 结果缺少机械扫描证据，或父 PRD 声明的 Gate 数值与机械扫描结果不一致。
- Artifact Gate 结果不是 `PASS`。

## 工作流

### 0. 读取流程契约（渐进式加载）

> **小模型指引**：不要一次性读完所有参考文件。Level 1 必须在开始前读完，Level 2 在进入对应阶段时再读。当前只需读 Level 1。

**Level 1 — 必读（S0 开始前通读，~10 分钟注意预算内可完成）**：
1. `references/small-model-safety.md` — 小模型安全规范（Stage State Packet、Context Budget、Evidence Discipline、Drift Reset）
2. `references/gate-definitions.md` — Gate 与失败码定义（通读，了解 45 种失败码的分类和含义）
3. 本节（0. 读取流程契约）和 **Stop Gates** 节

**Level 2 — 阶段进入时读取**：
| 进入阶段前 | 读取的参考文件 |
|---|---|
| S1 前 | `references/project-contract-profiles.md`（契约画像选择） |
| S2 前 | `references/analysis-output-template.md`（Contract Lock 部分 + Contract Snapshot 部分） |
| S3 前 | `references/analysis-output-template.md`（任务拆分部分 + Small Model Mode 粒度规则） |
| S4 前 | `references/subagent-planning-template.md`（仅在触发子代理条件时读） |
| S5 前 | `references/analysis-output-template.md`（Pre-Confirmation Gate 部分 + Artifact Gate 计划部分） |
| S7 前 | `references/task-creation-checklist.md` |
| S8 前 | `references/parent-prd-template.md`、`references/child-prd-template.md`、`references/planning-artifacts-template.md`、`references/design-surface-template.md` |

**Level 3 — 门控/修复时读取**：
| 场景 | 读取的参考文件 |
|---|---|
| 每轮自审后 | `references/self-review-checklist.md`（当前阶段对应部分即可） |
| 自审报告 | `references/self-review-report-template.md` |
| Gate 检查 | `scripts/trellis_planning_gate.py` — 在每阶段转换前运行机械扫描 |

后续每个阶段必须按状态机推进，不得跳过 Gate。每个阶段转换前运行 `scripts/trellis_planning_gate.py`（见各阶段的具体命令）。

### 1. 发现输入（S0_DISCOVER_CONTEXT）

定位并读取：

- 源需求文档。
- README、模块 README、AGENTS.md 或项目概览文件。
- 如果仓库不是空项目，读取现有代码结构和测试。
- 与项目相关的 `.trellis/tasks/` 和 `.trellis/spec/` 内容。
- Trellis 0.6+ 工作流元数据：`.trellis/workflow.md`、`.trellis/config.yaml`、`.trellis/.version`、`.trellis/.developer`、`.trellis/workspace/`。

先检查仓库再提问。只问无法从本地上下文判断的阻塞性问题。

**→ S0 Gate：** 确认输入路径和上下文清单明确后，运行：
```bash
python <skill-dir>/scripts/trellis_planning_gate.py --phase S1_REQUIREMENT_LEDGER --state-file .trellis/planning/planning-state.yaml
```
Gate 结果为 `PASS` 才能进入 S1。

### 2. 完整需求账本与项目契约

第一轮只读分析只能输出需求账本，不得创建任务，不得起草完整子任务 PRD。必须包含：

- Project Contract Lock 和 Contract Snapshot。
- Project Contract Profile 选择结果及证据；若默认 profile 不适配，必须使用 `custom` 并列出项目特定契约字段。
- Existing Implementation Baseline。
- 原始需求功能点清单与稳定 `REQ-xxx` / `AC-xxx`。
- Full Requirement Matrix。
- MVP Coverage Matrix。
- Backlog。
- Small Model Candidate Split 表。

**→ S1 Gate：** 完成需求账本后，运行：
```bash
python <skill-dir>/scripts/trellis_planning_gate.py --phase S2_CONTRACT_LOCK --state-file .trellis/planning/planning-state.yaml --matrix .trellis/planning/full-requirement-matrix.md --mvp-matrix .trellis/planning/mvp-coverage-matrix.md
```
Gate 结果为 `PASS` 且 `Requirement Ledger Gate = PASS` 才能进入 S2。

若源文档目录显示 PC、IOC、数据对接、小程序、报表等范围，但 Full Requirement Matrix 未覆盖这些范围，标记 `MATRIX_INCOMPLETE` 并继续抽取。

### 3. 渐进式主子任务规划

读取 `references/analysis-output-template.md`，形成完整规划输出：

- 任务合并/拆分记录。
- 完整平台范围与当前 MVP 边界差异。
- 模块依赖图。
- 按能力拆分的完整 MVP 子任务清单。
- Subtask Planning Ledger。
- Batch Completion Rollup。
- Small Model Mode 粒度检查。
- 规划产物矩阵。
- 父任务 PRD 草案。
- 子任务 PRD 草案。
- 中/高复杂度任务的 `design.md`、`implement.md`、`implement.jsonl`、`check.jsonl` 草案或明确不需要原因。
- 子任务“任务影响面矩阵”和对应设计面章节；涉及数据库、API、模块交互、外部系统、UI、权限、状态、校验、事务、测试等时，读取 `references/design-surface-template.md` 并补齐 `design.md` / `implement.md` 对应章节。

如果触发子代理条件，读取 `references/subagent-planning-template.md`。主代理负责分派、合并、冲突裁决和最终 Gate；子代理只做只读规划草案。

**→ S3 Gate：** 完成全部 MVP 候选任务拆分后，运行：
```bash
python <skill-dir>/scripts/trellis_planning_gate.py --phase S3_FULL_MVP_TASK_CANDIDATES --state-file .trellis/planning/planning-state.yaml --ledger .trellis/planning/subtask-ledger.yaml
```
Gate 结果为 `PASS` 才能进入 S4 批次规划。

### 4. 自我评审与 Gate 循环（S4_PROGRESSIVE_BATCH_PLANNING → S5_FULL_MVP_PLANNING_GATE）

每轮分析后：

1. 读取 `references/self-review-checklist.md`（当前批次对应部分即可，无需通读全文）。
2. 使用 `references/self-review-report-template.md` 输出评审报告。
3. 按 `references/gate-definitions.md` 执行 Requirement Ledger Gate、Contract Gate、Full MVP Planning Gate、Batch Completeness Gate 和 Pre-Confirmation Gate。
4. 对小模型或长程规划，按 `references/small-model-safety.md` 重建 Stage State Packet；若状态包与矩阵/账本不一致，先修复状态，不进入下一阶段。

**→ S4 Gate（批次完成时）：** 每批完成后运行：
```bash
python <skill-dir>/scripts/trellis_planning_gate.py --phase S4_PROGRESSIVE_BATCH_PLANNING --state-file .trellis/planning/planning-state.yaml --ledger .trellis/planning/subtask-ledger.yaml
```
输出 `BATCH_INCOMPLETE` 时继续规划下一批，不请求用户确认。

**→ S5 Gate（完整规划 Gate 时）：** 所有批次完成后运行：
```bash
python <skill-dir>/scripts/trellis_planning_gate.py --phase S5_FULL_MVP_PLANNING_GATE --state-file .trellis/planning/planning-state.yaml --ledger .trellis/planning/subtask-ledger.yaml --parent-prd .trellis/planning/parent-prd-draft.md
```
Gate 结果为 `PASS` 才能进入用户确认阶段。

判断：

- 所有检查项通过，且 Full MVP Planning Gate 与 Pre-Confirmation Gate 均为 `PASS` -> 进入用户确认。
- 检查项通过但仍有非终态 MVP 子任务 -> 输出 `BATCH_INCOMPLETE`，继续规划下一批，不请求用户确认。
- 任一 Gate 为 `FAIL` -> 输出失败码和修复清单，针对性改进后进入下一轮。
- 超过 5 轮仍有问题 -> 提示用户选择更强模型、人工审查或接受风险。

### 5. 用户确认完整规划

只有 Pre-Confirmation Gate 为 `PASS` 时，才能展示确认请求：

```text
请确认完整 MVP 任务树、全部批次规划、Backlog 边界、Blocked 项和首批创建范围。如果确认，我将创建 Trellis 父任务、全部已规划子任务及其所需 PRD/design/implement/JSONL 产物，不编写应用代码。
```

确认内容必须包含 Project Contract Lock 摘要、完整需求功能点数量、MVP Coverage 机械统计、Subtask Planning Ledger 汇总、Batch Completion Rollup、Backlog 摘要、Blocked 项、任务合并/裁剪高风险项和 Small Model Mode 分批策略。

如果用户调整范围，先更新矩阵、账本、批次和 Gate，不要基于过期假设创建任务。

### 6. 创建 Trellis 任务树与写入产物

用户确认后读取 `references/task-creation-checklist.md`，再执行：

1. 为整体项目创建父任务。
2. 记录 `task.py create` 输出的父任务真实目录；后续不要用逻辑 slug 拼路径。
3. 使用 `--parent <parent-task-dir>` 创建子任务；逐个记录每条命令输出的子任务真实目录，回填 Subtask Planning Ledger。
4. 写入任何产物前，确认目标目录存在 `task.json`。若没有，停止并修正映射。
5. 使用 `references/parent-prd-template.md` 写入父任务真实目录下的 `prd.md`。
6. 使用 `references/child-prd-template.md` 写入每个子任务真实目录下的 `prd.md`。
7. 按规划产物矩阵逐个写入所需 `design.md`、`implement.md`、`implement.jsonl`、`check.jsonl`。写入前必须先读取已有产物，禁止盲目覆盖。
8. 不要开始实现。

命令格式：

```bash
python ./.trellis/scripts/task.py create "<parent title>" --slug <parent-slug>
python ./.trellis/scripts/task.py create "<child title>" --slug <child-slug> --parent "<parent-task-dir>"
```

如果 `task.py create` 因 developer identity 未初始化而失败，停止并提示用户运行 `trellis init -u <name>`（加上项目平台参数，例如 `--codex`），或让用户提供明确 assignee。只有 Trellis CLI 不可用时，才把 `python ./.trellis/scripts/init_developer.py <name>` 作为旧版兜底方式。

### 7. Artifact Gate 与下一步

创建后运行：

```bash
python <skill-dir>/scripts/trellis_zero_gate.py \
  --tasks .trellis/tasks \
  --parent-task-json <parent-task-dir>/task.json \
  --parent-prd <parent-task-dir>/prd.md \
  --jsonl-mode <required|optional|inline>
```

`codex.dispatch_mode: inline` 时使用 `--jsonl-mode inline`；sub-agent-dispatch 模式或 JSONL 声明为需要时使用 `--jsonl-mode required`。如 Contract Snapshot 定义 forbidden tokens，追加 `--forbidden-token` 或 `--forbidden-regex`；如存在不能简化为 forbidden token 的契约冲突，追加 `--contract-mismatch-regex`。只有脚本或等价机械扫描返回 `result = PASS`，且 Development Recommendation Gate 为 `PASS` 时，才能输出：

- 任务树。
- 推荐执行顺序。
- 被阻塞任务。
- 可并行任务。
- Backlog / 二期范围。
- Artifact Gate 结果。
- 第一个建议开始的任务及原因。

若任一 Gate 未通过，输出：

```yaml
planning_status:
  development_ready: false
  failure_codes:
    - <code>
  next_action: <continue_planning | write_artifacts | fix_gate_failure | ask_user_confirmation>
```

不得建议开始开发。

## 落地阶段衔接

本技能止于创建任务树，不写代码。进入需求落地时，对每个子任务按依赖顺序使用执行期技能形成闭环：

1. `trellis-implement-tdd-zh` - 对子任务每条 AC 跑红到绿的 TDD 循环。
2. `trellis-debug-systematic-zh` - 测试或自检失败时系统定位修复。
3. `trellis-review-twostage-zh` - 完成前做规范符合和代码质量双阶段评审。

角色分层模型分配：规划用强模型，实现用小模型，评审 Stage 2 用强模型。

## 参考文件

- `references/workflow-state-machine.md` - 开始任务后先读取（Level 1），定义阶段状态和合法跳转。
- `references/gate-definitions.md` - 开始任务后先读取（Level 1），定义 Gate、失败码和通过条件。
- `references/small-model-safety.md` - 小模型/长程任务必须读取（Level 1），定义 Stage State Packet、上下文预算、证据纪律和 Drift Reset。
- `references/project-contract-profiles.md` - S1 进入前读取（Level 2），按项目类型选择契约字段，避免把 RuoYi/Java 假设套到 CLI、SDK、前端或其他项目。
- `references/analysis-output-template.md` - S2/S3/S5 前分段读取（Level 2），生成初始分析和渐进式规划输出。
- `references/subagent-planning-template.md` - 触发多 agent / 子代理批次规划时读取（Level 2）。
- `references/self-review-checklist.md` - 每轮分析后进行自我评审时读取（Level 3，只读当前阶段对应的部分）。
- `references/self-review-report-template.md` - 生成评审报告时读取（Level 3）。
- `references/planning-artifacts-template.md` - 为中/高复杂度任务起草 Trellis 0.6+ 的设计、实现和上下文清单产物时读取。
- `references/design-surface-template.md` - 当子任务涉及数据库、API、模块交互、外部系统、UI、权限、状态、校验、事务、测试等设计面时读取，提供 `design.md` 与 `implement.md` 必填章节模板。
- `references/parent-prd-template.md` - 起草或写入父任务 PRD 时读取。
- `references/child-prd-template.md` - 起草或写入子任务 PRD 时读取。
- `references/task-creation-checklist.md` - 创建任务树前读取。
- `scripts/trellis_zero_gate.py` - 创建任务并写入产物后运行（S9），生成不可手填的 Artifact Gate 机械扫描结果。
- `scripts/trellis_planning_gate.py` - **新增**：规划期阶段转换前运行（S0→S1→S2→S3→S4→S5），强制状态机合法转换、验证计数一致性和契约完整性，检测小模型漂移。
