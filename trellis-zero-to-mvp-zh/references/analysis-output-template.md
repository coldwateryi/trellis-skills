# 从 0 到 MVP 分析输出模板

> **小模型指引**：此模板覆盖了 S1-S10 的所有输出格式。不要试图一次填完。下方标记了每个章节适用的阶段：
> - `[S1]` 需求账本阶段填写
> - `[S2]` 合约锁定阶段填写
> - `[S3]` 任务候选阶段填写
> - `[S4]` 批次规划阶段填写
> - `[S5]` 门控阶段填写
> - `[S6]` 用户确认阶段填写
> - `[S7]` 任务创建阶段填写
> - `[S8]` 产物写入阶段填写
> - `[S9]` Artifact Gate 阶段填写
> - `[ALL]` 全阶段引用
>
> **关键规则**：每个节中的 `___` 标记必须填具体数字，禁止留空。

## [S0] 项目目标摘要

用 5-10 条说明需求文档最终要求交付什么。

## [S2] Project Contract Profile（项目契约画像）

> **S2 阶段：** 在需求账本（S1）完成后进入。此时已了解项目全貌，可以锁定契约。

先读取 `project-contract-profiles.md`，基于仓库证据选择 profile。不要把 RuoYi/Java CRUD 字段套到 CLI、SDK、前端、Python 服务或自定义框架项目。

```yaml
project_contract_profile:
  selected: <java-ruoyi-crud|typescript-cli-framework|frontend-spa|python-service|custom>
  secondary_profiles:
    - <profile or none>
  evidence:
    - <path:reason>
  rejected_profiles:
    - profile: <name>
      reason: <why not applicable>
```

## [S2] Project Contract Lock（项目契约锁定）

先从用户要求、README、模块 README、AGENTS.md、`.trellis/spec/` 和现有代码中锁定项目实现契约。后续任务产物必须遵守此表，不得由模型自行换命名体系。

| 契约项 | profile 字段 | adopted_value | evidence_path | forbidden_tokens | 备注 |
| --- | --- | --- | --- | --- | --- |
| <契约项> | <profile field> | <具体值或 not-applicable> | <path> | <tokens or none> | <说明> |

示例字段（按所选 profile 取用，不适用时不要填）：

- `java-ruoyi-crud`：后端模块、Java 实体命名、表名前缀、Controller 包/路由、Service/Mapper/XML、前端 API/Views、权限前缀、SQL 组织。
- `typescript-cli-framework`：workspace 包管理、package 布局、CLI 入口和命令、SDK public API、模板源路径、生成目标路径、workflow 状态块、平台配置器、脚本模板、测试/构建命令。
- `frontend-spa`：路由定义、页面组件、共享组件、API client、状态管理、设计系统、权限守卫、测试/构建命令。
- `python-service`：package 布局、app/CLI 入口、router/command、service module、schema/model、配置策略、测试/lint/typecheck 命令。

### Contract Snapshot 与 Forbidden Tokens

把 Project Contract Lock 转成后续产物可机械扫描的契约快照。`forbidden_tokens` 必须来自冲突来源、旧任务错误命名、框架默认误判或与 README/spec 不一致的候选值。

| profile 字段 | adopted_value（必须采用） | forbidden_tokens（禁止出现） | 证据路径 | 备注 |
| --- | --- | --- | --- | --- |
| <field> | <具体路径/命令/API/命名> | <冲突 token 或 none> | <path> | <说明> |

规则：父/子 PRD、`design.md`、`implement.md`、JSONL 命中 forbidden token 时，Artifact Gate 必须 FAIL。

### CONTRACT_CONFLICT（如有）

| 冲突项 | 来源 A | 来源 B | 推荐采用 | 风险 | 是否阻塞 |
| --- | --- | --- | --- | --- | --- |
| <命名/路径/表前缀> | <path/value> | <path/value> | <value> | <risk> | <yes/no> |

冲突阻塞时，不要创建任务；先让用户确认采用哪个契约。

## [S1] Existing Implementation Baseline（已有实现基线）

当仓库已经包含手工实现功能，或 Trellis/spec 是在开发开始后才初始化时，使用本节。

| 已有能力 | 证据类型 | 代码证据 | 测试证据 | 覆盖的需求 ID | 基线依赖名 | 备注 |
| --- | --- | --- | --- | --- | --- | --- |
| <capability> | code/test/spec/task | <精确路径> | <精确路径或 "none"> | REQ-001 | existing:<capability-or-file> | <复用约束> |

规则：

- 源需求文档是需求真相来源；现有代码和 `.trellis/spec/` 是证据，不替代需求。
- 如果需求已是 `DONE`，不要为该范围创建实现任务。
- 如果需求是 `UNTESTED`，除非实现证据薄弱，否则只创建测试补齐任务。
- 如果需求是 `PARTIAL`，只为缺失行为创建补缺任务。
- 如果需求是 `MISSING`，创建新实现任务。

## [S0] Trellis 工作流上下文

| 项目 | 值 | 备注 |
| --- | --- | --- |
| Trellis 版本/来源 | <来自 `.trellis/.version` 或 "unknown"> | <0.6+/legacy 信号> |
| 工作流契约 | <`.trellis/workflow.md` 路径或 "not present"> | <发现的产物要求> |
| 配置 | <`.trellis/config.yaml` 路径或 "not present"> | <相关选项> |
| Codex dispatch_mode | <inline/sub-agent/unknown/not-codex> | <JSONL Gate 模式：inline/required/optional> |
| Developer identity | <来自 `.trellis/.developer` 或 "not initialized"> | <缺失时要做什么> |
| Spec 新鲜度 | <fresh/stale/missing/unknown> | <已读 spec 文件或需要的刷新任务> |

## [ALL] 执行模型画像

| 项目 | 值 |
| --- | --- |
| 预期执行模型 | <如 qwen3.6 35b 本地模型 / GPT-5.5 / Opus 4.8> |
| 规划深度 | <standard / small-model-safe / high-risk> |
| 任务粒度规则 | <此画像下任务必须拆到多小> |
| Small Model Mode | <启用/不启用；触发原因> |
| 单批创建上限 | <如最多 8 个可执行子任务、最多 5 个完整 PRD> |
| 分批规划要求 | <若候选任务超过上限，写明全部 B01/B02/... 批次；不得只写 P0/P1> |

## [ALL] Stage State Packet

> **必填字段**：`___` 标记必须填具体数字。`unknown` 只允许在 S0 发现阶段出现。

小模型、长程复杂任务、候选子任务超过 8 个或恢复上下文后必须先填写本节。字段来自矩阵、账本和真实目录；未知值只能出现在发现阶段。

```yaml
stage_state:
  state: <S0_DISCOVER_CONTEXT...S10_NEXT_IMPLEMENTATION_RECOMMENDATION>
  source_docs:
    - <path>
  contract_snapshot: <present/missing/path>
  full_requirement_count: <number or unknown>
  mvp_coverage_counts:
    TASK: <n>
    MERGED: <n>
    BASELINE: <n>
    OUT_OF_SCOPE: <n>
    BLOCKED: <n>
  subtask_ledger:
    total_mvp_tasks: <n>
    ready_to_confirm: <n>
    blocked: <n>
    out_of_scope: <n>
    non_terminal: <n>
  current_batch: <Bxx or none>
  next_legal_action: <one action>
  stop_gate_failures:
    - <none or failure codes>
```

规则：

- `next_legal_action` 只能有一个。
- `stop_gate_failures` 非空时，不得请求用户确认、创建任务或建议开发。
- Stage State Packet 与 Full Requirement Matrix、MVP Coverage Matrix、Subtask Planning Ledger 或真实目录不一致时，输出 `STATE_DRIFT` 并 Drift Reset。

## [S1] 原始需求功能点清单

从源需求文档抽取所有可验收功能点。`REQ-xxx` 是源需求功能点的稳定身份，后续任务合并、拆分、重排不得改变其语义。

| 原始编号/章节 | 功能点 | 稳定需求 ID | 需求摘要 | 备注 |
| --- | --- | --- | --- | --- |
| <章节/页码/标题> | <原始功能点> | REQ-001 | <一句话摘要> | <必要上下文> |

## [S1] Full Requirement Matrix（完整源需求矩阵）

本表只表达源需求真相，不做 MVP 裁剪。源需求中每个可验收功能点都必须有一行。

| ID | 源章节/功能点 | 需求摘要 | 实现状态 | 相关代码 | 现有测试 | 缺口 |
| --- | --- | --- | --- | --- | --- | --- |
| REQ-001 | <章节/功能点> | <摘要> | MISSING | <path or none> | <path or none> | <gap> |

允许的状态：

- `DONE`：已完整实现且有测试。
- `PARTIAL`：部分实现。
- `MISSING`：未实现。
- `UNTESTED`：已实现但缺少足够测试。
- `UNCLEAR`：需求不够清楚，无法实现。

## [S1] MVP Coverage Matrix（当前 MVP 覆盖矩阵）

> **机械统计约束**：`TASK` + `MERGED` + `BASELINE` + `OUT_OF_SCOPE` + `BLOCKED` = ___ = Full Requirement Matrix 行数

本表表达当前 MVP 对完整需求的处理方式。禁止把 MVP 覆盖数量写成原始功能点总数。

本表生成后必须做机械统计：`TASK`、`MERGED`、`BASELINE`、`OUT_OF_SCOPE`、`BLOCKED` 五类数量之和必须等于 Full Requirement Matrix 行数。统计值必须被父 PRD 复用，不得重新手写估算。

| ID | 需求摘要 | 覆盖状态 | 任务动作 | 建议任务/基线/范围外说明 | 覆盖 AC | MVP/Backlog 说明 |
| --- | --- | --- | --- | --- | --- | --- |
| REQ-001 | <摘要> | TASK | new-task | T01 | AC-001 | MVP |

覆盖状态：

- `TASK`：创建独立子任务覆盖。
- `MERGED`：并入其他子任务，必须写明目标任务和覆盖 AC。
- `BASELINE`：由现有实现覆盖，必须写明基线证据。
- `OUT_OF_SCOPE`：不属于当前 MVP，必须写明原因并在用户确认时提示。
- `BLOCKED`：存在阻塞问题，必须写明问题和下一步。

任务动作：

- `none`：需求已是 `DONE`，只作为基线证据。
- `test-only`：需求是 `UNTESTED`，只创建测试补齐任务，不重做实现。
- `gap-task`：需求是 `PARTIAL`，只实现缺失行为。
- `new-task`：需求是 `MISSING`，创建新实现任务。
- `clarify`：需求是 `UNCLEAR`，实现前先提出阻塞问题或创建澄清任务。

## [S1-S2] 完整平台范围与 MVP 边界

| 范围块 | 完整平台要求 | 当前 MVP 处理 | 差异/风险 |
| --- | --- | --- | --- |
| <PC/IOC/数据对接/小程序/报表等> | <源需求范围> | <TASK/MERGED/OUT_OF_SCOPE> | <风险> |

## [S3] 任务合并/拆分记录

当源需求功能点和 Trellis 子任务不是一对一关系时必须填写。没有被单独建任务的功能点必须能在此表中找到去向。

| 需求 ID | 源功能点 | 处理方式 | 目标子任务/基线/范围外 | 覆盖 AC | 原因 | 风险 |
| --- | --- | --- | --- | --- | --- | --- |
| REQ-001 | <功能点> | MERGED | T03 | AC-003-01 | <为何合并> | <遗漏/耦合风险> |

处理方式只能使用：`SPLIT`、`MERGED`、`BASELINE`、`OUT_OF_SCOPE`、`BLOCKED`。

## Backlog / 二期范围

所有 `OUT_OF_SCOPE` 需求都必须进入本表，不能从需求追踪中消失。

| 需求 ID | 源功能点 | 排除原因 | 推荐阶段 | 恢复进入范围的前置条件 | 依赖的 MVP 任务 |
| --- | --- | --- | --- | --- | --- |
| REQ-999 | <功能点> | <原因> | MVP+1/V2/BLOCKED | <条件> | <task ids> |

## 模块依赖图

| 模块 | 职责 | 依赖模块 | 被哪些模块依赖 | 风险 |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## [S3] 任务拆分

Small Model Mode 规则：

0. 模型不得自行用"强耦合""同一流程""拆分会增加依赖"为理由保留超大任务；只有用户显式确认合并的任务可例外，并必须在风险列写明。

1. 一个子任务最多包含一个主实体的一套 CRUD、一个接口组、一个状态流转、一个前端页面或一个后端聚合查询。
2. 候选任务同时包含两个以上主实体、两套独立 CRUD、CRUD+状态机+报表、后端流程+小程序页面、地图/GIS+多表聚合+高级分析时，必须拆分。
3. 单批最多创建 8 个可执行子任务，单批最多完整写入 5 个高质量 PRD；超出时先排完整批次索引。P0/P1 只是优先级，不是完整规划完成条件。
4. 高复杂度任务必须拆成低/中复杂度，或要求 `design.md` + `implement.md` + JSONL 上下文。

| Task ID | 标题 | 目标 | 类型 | 需求 ID | 来源状态 | 依赖 | 基线依赖 | 优先级 | 复杂度 | Small Model 粒度 | 规划产物 | 是否可并行 | 验收标准 | 可能涉及区域 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T0 |  |  | docs | REQ-001 | MISSING | none | none | P0 | 低 | 一个实体 CRUD / 一个接口 / 一个状态流转 / 一个页面 / 一个聚合查询 | prd.md | no |  |  |

允许的任务类型：`backend`、`frontend`、`fullstack`、`cli`、`sdk`、`template`、`workflow`、`script`、`docs`、`test`、`infra`。

复杂度（按执行模型能力评估，决定拆分粒度和 PRD 详细度）：

- `低`：标准 CRUD、配置、有现成范例可照抄。弱模型可独立完成。
- `中`：含少量业务校验或跨表逻辑，需要明确实现步骤。弱模型在详细 PRD 下可完成。
- `高`：复杂事务、并发、跨模块一致性、需要大量隐性领域知识。弱模型难以独立完成，应进一步拆碎到"低/中"，或在 PRD 里把每步定死到无需推理。

优先级规则：

- `P0`：阻塞其他模块或核心正确性。
- `P1`：核心业务闭环。
- `P2`：体验、报表、通知、增强能力。
- `P3`：非必要优化。

排序规则：

1. 数据结构、API 契约和配置优先。
2. 阻塞其他模块的任务优先于依赖它们的任务。
3. 高风险和未知多的任务提前验证。
4. UI 打磨、文档和体验增强靠后。
5. 不要把互相依赖的任务标记为可并行。

Small Model Mode 规则：

0. 模型不得自行用“强耦合”“同一流程”“拆分会增加依赖”为理由保留超大任务；只有用户显式确认合并的任务可例外，并必须在风险列写明。

1. 一个子任务最多包含一个主实体的一套 CRUD、一个接口组、一个状态流转、一个前端页面或一个后端聚合查询。
2. 候选任务同时包含两个以上主实体、两套独立 CRUD、CRUD+状态机+报表、后端流程+小程序页面、地图/GIS+多表聚合+高级分析时，必须拆分。
3. 单批最多创建 8 个可执行子任务，单批最多完整写入 5 个高质量 PRD；超出时先排完整批次索引。P0/P1 只是优先级，不是完整规划完成条件。
4. 高复杂度任务必须拆成低/中复杂度，或要求 `design.md` + `implement.md` + JSONL 上下文。

已有部分实现规则：

1. 不要为 `DONE` 需求创建子任务。
2. 只有测试缺失时，才为 `UNTESTED` 需求创建 `test` 任务。
3. 为 `PARTIAL` 需求创建补缺子任务；目标必须命名缺失行为，而不是已实现行为。
4. 任务依赖已有能力时，在 `基线依赖` 中写明，例如 `existing:src/auth/session.ts`。
5. 不要把已有基线依赖伪装成新的 Trellis task。

## [S4] Subtask Planning Ledger（子任务规划账本）

本表是渐进式完成所有 MVP 子任务规划的唯一状态源。每个 MVP Coverage Matrix 中覆盖状态为 `TASK` 的子任务都必须有一行；分批规划时不得只保留当前批次。

| Task ID | 需求 ID | 标题 | 优先级 | 批次 | 依赖 | 可并行组 | 负责 Agent | 规划状态 | PRD 状态 | design/implement 状态 | Artifact Gate | 真实目录 | 下一步 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T01 | REQ-001 | <标题> | P0 | B01 | none | G01 | main/agent-a | CANDIDATE/DRAFTED/READY_TO_CONFIRM/USER_CONFIRMED/CREATED/ARTIFACTS_WRITTEN/GATED_PASS/BLOCKED/OUT_OF_SCOPE | missing/draft/ready/written | not-needed/draft/ready/written | PENDING/PASS/FAIL/N/A | <task.py 输出目录或 pending> | <继续动作> |

状态规则：

- `CANDIDATE`：已识别候选任务，但边界、依赖或产物未冻结。
- `DRAFTED`：已有草案，但未通过 Full MVP Planning Gate。
- `READY_TO_CONFIRM`：任务边界、REQ 覆盖、依赖、验收、PRD 草案和产物需求均已冻结，可进入用户确认。
- `USER_CONFIRMED`：用户已确认该任务属于当前创建范围。
- `CREATED`：已通过 `task.py create` 创建真实目录并回填账本。
- `ARTIFACTS_WRITTEN`：已写入所有声明需要的规划产物。
- `GATED_PASS`：Artifact Gate 通过。
- `BLOCKED`：有明确阻塞原因、责任方和恢复条件。
- `OUT_OF_SCOPE`：已进入 Backlog，当前 MVP 不创建。

进入用户确认前，所有 MVP `TASK` 子任务必须是 `READY_TO_CONFIRM`、`BLOCKED` 或 `OUT_OF_SCOPE`。存在 `CANDIDATE` 或 `DRAFTED` 时，输出 `BATCH_INCOMPLETE`，继续规划下一批。

## [S4] Batch Completion Rollup（批次完成汇总）

| 批次 | 包含 Task ID | 目标 | 状态 | READY_TO_CONFIRM | BLOCKED | OUT_OF_SCOPE | 剩余非终态 | 下一批动作 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B01 | T01,T02,T03 | P0 基础能力 | planned/in-progress/ready/blocked | <n> | <n> | <n> | <n> | <继续规划 B02 或 none> |

完成判定：

- `all_mvp_task_count` 必须等于 Subtask Planning Ledger 中当前 MVP `TASK` 子任务数。
- `ready_or_terminal_count = READY_TO_CONFIRM + BLOCKED + OUT_OF_SCOPE`。
- 只有 `ready_or_terminal_count == all_mvp_task_count` 时，才能输出 `ALL_SUBTASK_PLANNING_COMPLETE`。
- 否则输出 `BATCH_INCOMPLETE`，并列出下一批 Task ID、未完成原因和主代理下一步动作。

## [S4] Agent 分派计划（如触发）

当候选子任务超过单批上限、业务域超过 3 个、完整 PRD 草案超过 5 个，或用户要求多 agent 规划时，按 `subagent-planning-template.md` 输出：

| Agent | 输入范围 | 输出范围 | 状态 | 失败码 |
| --- | --- | --- | --- | --- |
| requirement-ledger-agent | <REQ 范围> | <矩阵复核> | planned/running/done/blocked | <none/code> |
| batch-split-agent | <MVP TASK 范围> | <批次拆分> | planned/running/done/blocked | <none/code> |
| gate-check-agent | <全部草案> | <Gate FAIL/PASS> | planned/running/done/blocked | <none/code> |

## [S5] 规划产物矩阵

创建 Trellis 任务前必须填写。本矩阵是创建后核验文件存在性的依据；`task.py create` 不会自动补齐 `design.md` 或 `implement.md`。

| Task ID | 真实目录 | 标题 | 复杂度 | prd.md | design.md | implement.md | implement.jsonl | check.jsonl | jsonl_mode | 写入状态 | 校验结果 | 原因 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T01 | <task.py create 输出目录> | <标题> | <低/中/高> | 需要 | <需要/不需要> | <需要/不需要> | <需要/不需要> | <需要/不需要> | required/optional/inline | WRITTEN/NOT_NEEDED_WITH_REASON/BLOCKED | PASS/FAIL/PENDING | <按工作流、复杂度、执行模型能力说明> |

规则：

- 每个子任务必须有 `prd.md`。
- 高复杂度任务不得是 PRD-only；要么拆成低/中复杂度任务，要么要求 `design.md` + `implement.md`。
- 如果项目工作流或既有任务目录包含 `implement.jsonl` / `check.jsonl`，矩阵必须说明 JSONL 模式：`required`（sub-agent 或确需预加载稳定上下文）、`optional`（可删除或说明不需要）、`inline`（Codex inline，不作为规划就绪门槛）。不能只保留 `_example` 种子。
- 创建完成后，矩阵中标为"需要"的文件必须真实存在于 `task.py create` 返回的任务目录。
- `写入状态` 为 `WRITTEN` 时必须能在真实目录找到文件；`NOT_NEEDED_WITH_REASON` 必须写明为什么不需要；`BLOCKED` 必须阻止汇报可执行。

## [S5] MVP 推荐开发顺序

本节只能在 Full MVP Planning Gate 通过后输出。顺序必须覆盖全部当前 MVP `TASK` 子任务；若只覆盖已创建批次，标题必须改为“本批执行顺序”，并禁止建议开始开发。

1. `<task-id>`：`<原因>`
2. `<task-id>`：`<原因>`

## [S5] Artifact Gate 计划

任务创建后必须运行并汇报：

| 检查项 | 命中时处理 |
| --- | --- |
| `_example` JSONL | 填真实上下文、删除并说明不需要，或阻塞 |
| `{Entity}` / `<path>` / `TBD` / `待定` / `视情况` | 修正为具体值 |
| `YOUR_KEY` / `API_KEY_HERE` / 未决外部配置 | 标为 `FIXED`、`BASELINE`、`BLOCKED` 或 `OUT_OF_SCOPE` |
| 契约不一致或 forbidden token 命中 | 按 Contract Snapshot 修正，禁止用模型自创命名覆盖 README/spec |
| 高复杂度缺 `design.md` / `implement.md` | 补齐或拆小 |
| PRD/design/implement 语义锚点不一致 | 停止并修正 |
| 任务影响面声明为“是”但缺设计/实现章节 | 补齐对应 `design.md` / `implement.md` 章节或修正影响面矩阵 |

推荐机械命令：

```bash
python <skill-dir>/scripts/trellis_zero_gate.py \
  --tasks .trellis/tasks \
  --parent-task-json <parent-task-dir>/task.json \
  --parent-prd <parent-task-dir>/prd.md \
  --jsonl-mode <required|optional|inline>
```

如有 Contract Snapshot forbidden tokens，追加 `--forbidden-token` 或 `--forbidden-regex`。不得在未运行机械扫描时手填 PASS。

## [S9] Artifact Gate 输出字段

创建任务后必须输出以下字段，`result` 只能是 `PASS` 或 `FAIL`，不能用 `PENDING` 汇报可执行：

| 字段 | 含义 | PASS 条件 |
| --- | --- | --- |
| scanned_tasks | 扫描的新任务数量 | 等于本批父/子任务数 |
| placeholder_hits | 模板占位/未决表达命中 | 0 |
| angle_placeholder_hits | 通用 `<...>` 占位命中 | 0 |
| jsonl_seed_hits | `_example` JSONL 命中 | 0 |
| forbidden_token_hits | Contract Snapshot 禁止词命中 | 0 |
| contract_mismatch_hits | 与 Project Contract Lock 不一致 | 0 |
| coverage_count_mismatch_hits | 覆盖统计与矩阵不一致 | 0 |
| high_complexity_missing_artifacts | 中/高复杂任务缺设计/实现产物 | 0 |
| missing_declared_artifacts | PRD/矩阵声明需要但文件缺失 | 0 |
| design_surface_prd_without_matrix | 子任务 PRD 缺任务影响面矩阵 | 0 |
| design_surface_missing_hits | 任务影响面矩阵声明涉及但缺少对应设计/实现章节 | 0 |
| declared_gate_mismatch_hits | 父 PRD 声明 Gate 与机械扫描不一致 | 0 |
| external_config_hits | 未决外部配置或占位 key | 0 |
| result | 总结果 | 全部为 0 时 PASS |

## [S6] Pre-Confirmation Gate

输出确认请求前必须填写。任一项不通过时，不得请求用户确认，只能继续规划或修复。

| 检查项 | 结果 | 证据/下一步 |
| --- | --- | --- |
| Requirement Ledger Gate | PASS/FAIL | <证据> |
| Contract Gate | PASS/FAIL | <证据> |
| Full MVP Planning Gate | PASS/FAIL | <证据> |
| Batch Completeness Gate | PASS/FAIL | <证据> |
| UNASSIGNED_MVP_REQ | 0/<n> | <REQ IDs> |
| UNBATCHED_TASK | 0/<n> | <Task IDs> |
| P0P1_ONLY_PLAN | false/true | <说明> |
| DEFERRED_PRD_WITHOUT_PLAN | 0/<n> | <Task IDs> |
| ALL_SUBTASK_PLANNING_COMPLETE | PASS/FAIL | <说明> |

失败时输出：

```yaml
planning_status:
  full_mvp_planning_gate: FAIL
  development_ready: false
  failure_codes:
    - <code>
  next_action: <继续规划的批次或修复动作>
```

## 父任务 PRD 草案

使用 `parent-prd-template.md` 起草父任务 PRD。

## 子任务 PRD 草案

为每个子任务使用 `child-prd-template.md` 起草 PRD。

对每个中/高复杂度子任务，同时使用 `planning-artifacts-template.md` 起草必要的 Trellis 0.6+ 规划产物。

## 确认请求

只有 Pre-Confirmation Gate 为 `PASS` 时，最后输出：

```text
请确认完整 MVP 任务树、全部批次规划、Backlog 边界、Blocked 项和首批创建范围。如果确认，我将创建 Trellis 父任务、全部已规划子任务及其所需 PRD/design/implement/JSONL 产物，不编写应用代码。
```
