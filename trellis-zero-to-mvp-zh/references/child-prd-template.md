# 子任务 PRD 模板

## 填写规则（规划阶段必读）

此 PRD 由规划模型填写，执行阶段可能由能力有限的本地模型照此实现。因此 PRD 必须确定需求、契约、边界、验收和依赖，但不要替代 Trellis 0.6+ 的 `design.md` / `implement.md`。

- 所有 `<...>` 占位符必须替换为具体值，禁止把占位符或“待定/视情况而定”留给执行阶段。
- 禁止保留 `{Entity}`、`{domain}`、`{entity}`、`<PageComponent>` 等泛化模板占位符。
- PRD 默认只承载需求、约束、范围、依赖和验收；技术设计写入 `design.md`，文件计划、有序步骤、自检命令、回滚点和评审门写入 `implement.md`。
- 只有低复杂度、项目本地工作流允许 PRD-only，且规划产物矩阵标为 `implement.md: 不需要` 时，才可在本 PRD 保留精简执行附录。
- 所有需要推理判断的部分（命名、路径、API/命令/路由、schema、状态分支、外部配置）必须在规划阶段定死；PRD 写行为契约，`design.md` / `implement.md` 写技术落点。
- 子任务必须引用父任务 Project Contract Lock；命名、路径、API、包/模块、路由、表名、权限标识不得自行发明。
- 子任务必须复制父任务 Contract Snapshot 中与本任务相关的 adopted_value 和 forbidden_tokens；PRD、`design.md`、`implement.md`、JSONL 不得命中 forbidden_tokens。
- Small Model Mode 下，一个子任务只允许覆盖一个主实体 CRUD、一个接口组、一个状态流转、一个前端页面或一个后端聚合查询；否则必须拆分。
- 每个子任务必须填写“任务影响面矩阵”。任一影响面为“是”时，`design.md` 必须包含对应设计章节，`implement.md` 必须包含对应落地计划章节；章节名来自 `design-surface-template.md`。
- 外部配置和第三方 key 必须写成固定配置名、已有基线证据、`BLOCKED` 或 `OUT_OF_SCOPE`；禁止 `YOUR_KEY`、`待用户提供` 等占位。
- 如果某点无法在规划阶段定死，把它列入 `范围外（Out of Scope）` 或拆成独立任务，不要留给执行模型自由发挥。
- `复杂度与规划产物` 必须和分析阶段的规划产物矩阵一致；凡写“需要”的产物，创建任务后都必须有对应文件。

## 模板

```markdown
# <任务标题>

## 需求 ID

- REQ-001
- AC-001

## 目标

实现或验证这个可独立验收的 MVP 能力。

## Project Contract Reference

从父任务 Project Contract Lock 复制本任务必须遵守的契约项。若本任务需要不同命名或路径，先更新父任务契约并说明原因。

| 契约项 | profile 字段 | 本任务采用值 | 父任务证据路径 |
| --- | --- | --- | --- |
| <契约项> | <profile field> | <具体路径/命名/API/命令/模块或 not-applicable> | <path> |

### Contract Snapshot Check

| 检查项 | 值 |
| --- | --- |
| 本任务必须采用的 adopted_value | <路径/命名/API/命令/模块/路由/表名/权限等> |
| 本任务 forbidden_tokens | <禁止出现的命名、路由、路径片段；无则写 none> |
| 扫描范围 | 本 PRD、design.md、implement.md、implement.jsonl、check.jsonl |
| 命中处理 | 命中即 Artifact Gate FAIL，先修正再执行 |

## 语义锚点

用于防止任务串线。下列字段必须全部替换为本任务具体值，并与 Project Contract Reference、验收标准、`design.md` / `implement.md` 一致。不适用字段写 `not-applicable`，不要凭空套用其他技术栈。

| 项 | 值 |
| --- | --- |
| Project Contract Profile | <selected profile> |
| 业务域/能力域 | <如 site / cli-task-create / workflow-template / auth-page> |
| 主对象/主实体/主接口 | <具体名称；不适用写 not-applicable> |
| 用户可见入口 | <页面路径 / CLI 命令 / API endpoint / SDK function / workflow section> |
| 数据或状态对象 | <表名 / schema / config key / state block / not-applicable> |
| 代码落点摘要 | <模块、包、workspace、template 或 not-applicable> |
| 权限/鉴权模型 | <permission prefix / guard / config / not-applicable> |
| 本任务不得引用的相邻业务域 | <除非列入依赖，否则禁止引用的相邻域> |

## Small Model 粒度检查

| 检查项 | 结果 |
| --- | --- |
| 本任务粒度 | <一个实体 CRUD / 一个接口组 / 一个状态流转 / 一个前端页面 / 一个后端聚合查询> |
| 主对象数量 | <n，Small Model Mode 下通常为 1> |
| 独立能力数量 | <n，Small Model Mode 下通常为 1> |
| 是否包含状态机/报表/地图/小程序等高复杂组合 | <是/否；是则说明为何未拆分> |
| 是否需要拆分 | <否/是；若包含禁止组合，必须写“是”，除非用户已明确确认合并并在依赖/风险中记录> |

## 缺口来源

- 本任务前的需求状态：<PARTIAL/MISSING/UNTESTED>
- 任务动作：<gap-task/new-task/test-only>
- 已有基线依赖：
  - <existing:path-or-capability，或 "none">
- Trellis task 依赖：
  - <task slug 或 "none">
- 范围规则：本任务不得重复实现 Existing Implementation Baseline 中已经列出的行为。

## 当前缺口

- 当前实现：<已有行为或无>
- 缺口：<缺失行为>
- 风险：<为什么重要>

## 复杂度与规划产物

- 复杂度：<低/中/高，按执行模型能力评估>
- 执行模型假设：<如 qwen3.6 35b 本地模型 / GPT-5.5 / Opus 4.8>
- 批次：<B01/B02/...>
- 可并行组：<G01/G02/...；若不可并行写 none>
- 规划账本状态：<必须与父任务 Subtask Planning Ledger 一致>
- 产物矩阵行：<复制分析阶段规划产物矩阵中本任务的一行，确保与真实文件一致>
- 必要产物：
  - `prd.md`：必须
  - `design.md`：<需要/不需要及原因>
  - `implement.md`：<需要/不需要及原因>
  - `implement.jsonl`：<需要/不需要及原因；jsonl_mode=required/optional/inline>
  - `check.jsonl`：<需要/不需要及原因；jsonl_mode=required/optional/inline>
- Trellis 0.6+ 产物边界：<文件计划、实现步骤、自检命令在 implement.md；或低复杂度 PRD-only 精简执行附录>
- Spec 新鲜度：<已读取哪些 `.trellis/spec/` 文件；如果过期，写明 spec 刷新任务>

## 任务影响面矩阵

本矩阵只声明影响面，不在 PRD 展开详细技术设计。任一行“是否涉及”为“是”时，必须在 `design.md` 和 `implement.md` 写入对应章节；若任务低复杂度且本地工作流允许 PRD-only，也必须把“否”的原因写清楚，不得省略矩阵。

| 影响面 | 是否涉及 | 设计位置 | 实现计划位置 | Gate |
| --- | --- | --- | --- | --- |
| 数据库/数据模型 | 是/否 | design.md#Database Schema Design | implement.md#Database Migration Plan | DATABASE_SCHEMA_MISSING |
| API 接口 | 是/否 | design.md#API Contract Design | implement.md#API Implementation Plan | API_CONTRACT_MISSING |
| 模块间交互 | 是/否 | design.md#Inter-Module Interaction Design | implement.md#Inter-Module Wiring Plan | INTER_MODULE_CONTRACT_MISSING |
| 外部系统接口 | 是/否 | design.md#External System Interface Design | implement.md#External Adapter Plan | EXTERNAL_INTERFACE_CONTRACT_MISSING |
| UI/项目风格 | 是/否 | design.md#UI Design and Style Contract | implement.md#UI Implementation Plan | UI_DESIGN_MISSING |
| 权限/数据权限 | 是/否 | design.md#Permission and Data Scope Design | implement.md#Permission Wiring Plan | PERMISSION_CONTRACT_MISSING |
| 字典/状态机 | 是/否 | design.md#Dictionary and State Design | implement.md#State Implementation Plan | STATE_TRANSITION_MISSING |
| 查询/导入导出 | 是/否 | design.md#Query and Import Export Design | implement.md#Query Export Plan | QUERY_CONTRACT_MISSING |
| 校验/错误语义 | 是/否 | design.md#Validation and Error Semantics | implement.md#Validation Implementation Plan | VALIDATION_CONTRACT_MISSING |
| 事务/并发/幂等 | 是/否 | design.md#Transaction Concurrency and Idempotency Design | implement.md#Transaction Implementation Plan | TRANSACTION_CONTRACT_MISSING |
| 异步任务/事件 | 是/否 | design.md#Async Job and Event Design | implement.md#Job Event Plan | ASYNC_JOB_CONTRACT_MISSING |
| 日志/审计 | 是/否 | design.md#Audit and Logging Design | implement.md#Audit Implementation Plan | AUDIT_LOG_CONTRACT_MISSING |
| 初始化/迁移 | 是/否 | design.md#Data Initialization and Migration Design | implement.md#Migration Plan | MIGRATION_COMPATIBILITY_MISSING |
| 测试策略 | 是/否 | design.md#Test Strategy Design | implement.md#Test Implementation Plan | TEST_STRATEGY_MISSING |
| 性能/容量 | 是/否 | design.md#Performance and Capacity Design | implement.md#Performance Verification Plan | PERFORMANCE_CONSTRAINT_MISSING |
| 安全/敏感数据 | 是/否 | design.md#Security and Sensitive Data Design | implement.md#Security Verification Plan | SECURITY_CONTRACT_MISSING |
| 配置/环境 | 是/否 | design.md#Configuration Design | implement.md#Configuration Plan | CONFIG_CONTRACT_MISSING |
| 框架约定 | 是/否 | design.md#Framework Convention Design | implement.md#Framework Implementation Plan | FRAMEWORK_CONVENTION_MISSING |
| 人工验收 | 是/否 | design.md#Manual Acceptance Design | implement.md#Manual Verification Plan | MANUAL_ACCEPTANCE_UNCLEAR |
| 文档/运维 | 是/否 | design.md#Documentation and Operations Handoff | implement.md#Docs Ops Plan | OPS_DOC_CONTRACT_MISSING |

## 上下文清单

执行模型编辑前必须读取：

| 类型 | 路径 | 用途 |
| --- | --- | --- |
| 现有范例 | <path> | <要照抄的模式> |
| 契约/spec | <path> | <API/schema/state 规则> |
| 测试范例 | <path> | <要照抄的测试风格> |

## 决策表

把所有原本需要执行阶段推理的决策定死：

| 决策点 | 选定方案 | 原因 | 影响文件或产物 |
| --- | --- | --- | --- |
| <命名/schema/状态分支/API/命令选择> | <确切选择> | <原因> | <prd/design/implement 或 paths> |

## 外部配置与未决项

所有外部配置必须已定死或排除，不能留占位。

`BLOCKED` 的外部配置不得写“先用占位符/执行期替换/待用户提供”。若实现依赖该配置，本任务必须改为 `BLOCKED` 或把相关能力列入范围外；可执行任务只能实现不依赖该配置的降级能力。

| 配置/外部依赖 | 状态 | 规划期处理 | 执行期行为 |
| --- | --- | --- | --- |
| <如地图 key / 第三方接口 / 硬件协议> | FIXED/BASELINE/BLOCKED/OUT_OF_SCOPE | <配置名、证据或排除原因> | <失败/缺失时的确切行为> |

## 参考实现

执行时优先照抄以下现有范例，仅按本任务替换实体/字段/命名：

- 业务/接口范例：<现有可照抄的文件路径；无则写"无，按 design.md / implement.md 从零实现">
- 数据/状态/配置范例：<现有 schema / mapper / template / config / workflow 文件路径或 none>
- UI/CLI/SDK 范例：<现有页面、组件、命令、SDK API 或模板路径或 none>
- 替换说明：<把范例里的 Xxx 替换为本任务的 Yyy；详细文件替换在 implement.md>

## 实现计划定位

Trellis 0.6+ 默认把详细文件计划写入 `implement.md`。本节只声明执行计划放在哪里，避免 PRD 和 `implement.md` 互相冲突。

| 项 | 值 |
| --- | --- |
| 文件计划位置 | `implement.md` / 本 PRD 精简执行附录 |
| 有序步骤位置 | `implement.md` / 本 PRD 精简执行附录 |
| 自检命令位置 | `implement.md` / 本 PRD 精简执行附录 |
| 允许 PRD-only 的证据 | <低复杂度 + 本地工作流允许 + 产物矩阵 implement.md 不需要；否则写 not-applicable> |

### PRD-only 精简执行附录（仅低复杂度适用）

非 PRD-only 任务删除本小节并在 `implement.md` 中完整填写文件计划、步骤和命令。

| 操作 | 文件路径 | 说明 |
| --- | --- | --- |
| 新建/修改 | <path> | <这个文件干什么；非 PRD-only 时不要在此处填写> |

1. <仅 PRD-only 时填写具体动作；否则写"见 implement.md">

```bash
<仅 PRD-only 时填写自检命令；否则写"见 implement.md">
```

## 挂载点

让本能力真正“接上线”的登记点（判据：“删了它，本能力在用户/系统视角就消失”，一般 3-5 条）。执行阶段逐项接线、评审阶段逐项核对，防止“写了实现没接线”：

| 挂载点 | 类型 | 位置 | 接线动作 |
| --- | --- | --- | --- |
| <名称> | 路由注册/配置项/事件订阅/DI 绑定/菜单入口/CLI 注册/SDK export | <path> | <注册或绑定的确切动作> |

## 行为约束

- <必须实现的行为，写成可判定的断言>
- <边界条件：输入为空/超长/重复时的确切行为>
- <错误处理：失败时返回的确切错误码/消息>
- <兼容性要求：不能破坏的已有行为>

## 验收标准

写成可机器校验或可逐条勾选的断言，避免“正确实现”这类主观表述：

- [ ] REQ-001 在本任务范围内完整实现。
- [ ] <构建/编译命令> 成功通过。
- [ ] <具体调用，如某接口/命令/页面操作某入参> 返回 <确切预期>。
- [ ] <失败路径，如重复/非法输入> 返回 <确切错误码与消息>。
- [ ] 不破坏已有 MVP 行为。
- [ ] 必要测试通过。

## 自动化测试要求

### Unit Tests

- <测试点：被测方法 + 输入 + 期望输出>

### Integration Tests

- <测试点>

### Regression Tests

- <测试点>

### E2E / Smoke Tests

- <测试点>

## 依赖

- Trellis task 依赖:
  - <task slug or none>
- 已有基线依赖:
  - <existing:path-or-capability or none>
- 原因:
  - <依赖原因>

## 解锁项

- <完成后解锁的任务>

## 范围外

- <明确排除项>
- <任何无法在规划阶段定死、不应交给执行模型自由发挥的点>

## 禁止事项

给执行模型的负面约束，防止它擅自发挥：

- 不要新建已有的基类/工具类，必须复用参考实现指向的现有实现。
- 不要改动 `implement.md` 文件计划之外的文件；PRD-only 低复杂度任务不得改动精简执行附录之外的文件。
- 不要引入未在 `design.md` / `implement.md` 列出的新依赖或新框架。
- 不要改变 Project Contract Reference 中的命名、路径、API、命令、包/模块、路由、表名或权限模型。
- 不要使用 Contract Snapshot 中列出的 forbidden_tokens。
- 不要在本任务中顺手实现相邻业务域；相邻业务必须列入依赖或另建任务。
- 不要保留 `YOUR_KEY`、`API_KEY_HERE`、`TBD`、`待定`、`视情况` 等占位。
- <其他项目特定红线>

## 技术备注

- 相关文件：
- 现有模式：
- 相关规范：
- 风险：
```
