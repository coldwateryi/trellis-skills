# Gate Definitions

本文件是 `trellis-zero-to-mvp-zh` 的 Gate 单一事实来源。其他模板可以引用这些 Gate，不要重复定义互相冲突的通过条件。

## 失败码

| 失败码 | 含义 | 处理 |
| --- | --- | --- |
| `MATRIX_INCOMPLETE` | Full Requirement Matrix 未覆盖源需求全部可验收功能点 | 继续抽取需求 |
| `CONTRACT_CONFLICT` | README/spec/现有代码契约冲突未裁决 | 阻塞并请用户确认采用方案 |
| `CONTRACT_SNAPSHOT_MISSING` | 缺少 Contract Snapshot 或 forbidden_tokens | 补齐契约快照 |
| `UNASSIGNED_MVP_REQ` | MVP `TASK` 需求没有目标子任务 | 补齐任务映射 |
| `UNBATCHED_TASK` | 子任务没有批次 | 分配 B01/B02/... |
| `P0P1_ONLY_PLAN` | 只规划 P0/P1，但 MVP 仍有未完成规划的 `TASK` | 继续规划后续批次 |
| `DEFERRED_PRD_WITHOUT_PLAN` | 后续批次没有 PRD 草案或产物需求 | 补齐规划草案 |
| `SMALL_MODEL_GRAIN_FAIL` | 子任务违反 Small Model Mode 粒度 | 拆分任务或阻塞用户确认合并 |
| `ARTIFACT_MATRIX_INCOMPLETE` | 规划产物矩阵缺任务或缺原因 | 补齐矩阵 |
| `DESIGN_SURFACE_MISSING` | 子任务声明涉及某设计面，但缺少对应 `design.md` 或 `implement.md` 章节 | 补齐设计面章节或修正影响面矩阵 |
| `DATABASE_SCHEMA_MISSING` | 涉及数据库/数据模型但缺表结构设计或迁移计划 | 补齐 Database Schema Design 与 Database Migration Plan |
| `API_CONTRACT_MISSING` | 涉及 API 但缺请求/响应/错误/权限契约或实现计划 | 补齐 API Contract Design 与 API Implementation Plan |
| `INTER_MODULE_CONTRACT_MISSING` | 涉及模块间交互但缺调用边界、事务边界或失败策略 | 补齐 Inter-Module Interaction Design 与 Wiring Plan |
| `EXTERNAL_INTERFACE_CONTRACT_MISSING` | 涉及外部系统但缺协议、认证、配置、超时、降级或 mock 策略 | 补齐 External System Interface Design 与 Adapter Plan |
| `UI_DESIGN_MISSING` | 涉及页面/UI 但缺项目风格、页面结构、表格/表单/状态设计 | 补齐 UI Design and Style Contract 与 UI Implementation Plan |
| `UI_STYLE_CONTRACT_MISMATCH` | UI 设计与 Project Contract Lock 或当前项目风格不一致 | 按参考页面和设计系统修正 |
| `PERMISSION_CONTRACT_MISSING` | 涉及权限/数据权限但缺后端权限、前端按钮权限、菜单或数据范围规则 | 补齐 Permission and Data Scope Design |
| `DATA_SCOPE_RULE_MISSING` | 涉及数据范围但缺部门/角色/租户过滤规则 | 补齐数据范围规则 |
| `DICT_CONTRACT_MISSING` | 涉及字典/枚举但缺字典类型和值 | 补齐 Dictionary and State Design |
| `STATE_TRANSITION_MISSING` | 涉及状态流转但缺允许转换、角色、前置条件和非法行为 | 补齐状态机设计 |
| `QUERY_CONTRACT_MISSING` | 涉及查询列表但缺查询字段、匹配方式、排序或分页规则 | 补齐 Query and Import Export Design |
| `EXPORT_IMPORT_CONTRACT_MISSING` | 涉及导入/导出但缺字段、权限、模板或错误处理 | 补齐导入导出设计 |
| `VALIDATION_CONTRACT_MISSING` | 涉及表单/接口入参但缺前后端校验和业务校验 | 补齐 Validation and Error Semantics |
| `ERROR_SEMANTICS_MISSING` | 缺具体错误消息、错误码或失败响应结构 | 补齐错误语义 |
| `TRANSACTION_CONTRACT_MISSING` | 涉及多写入/状态流转/批量处理但缺事务边界 | 补齐事务设计 |
| `IDEMPOTENCY_CONTRACT_MISSING` | 涉及回调/同步/重复提交但缺幂等策略 | 补齐幂等设计 |
| `ASYNC_JOB_CONTRACT_MISSING` | 涉及定时任务/异步任务但缺触发、锁、失败处理 | 补齐 Async Job and Event Design |
| `EVENT_CONTRACT_MISSING` | 涉及事件/消息但缺 topic/payload/consumer/失败策略 | 补齐事件设计 |
| `AUDIT_LOG_CONTRACT_MISSING` | 涉及管理操作或外部调用但缺日志/审计设计 | 补齐 Audit and Logging Design |
| `SENSITIVE_LOGGING_RISK` | 日志可能记录敏感信息但缺脱敏策略 | 补齐脱敏规则 |
| `DATA_INIT_CONTRACT_MISSING` | 涉及菜单/字典/配置初始化但缺初始化设计 | 补齐 Data Initialization and Migration Design |
| `MIGRATION_COMPATIBILITY_MISSING` | 涉及表字段/数据迁移但缺兼容已有数据或回滚策略 | 补齐迁移兼容设计 |
| `TEST_STRATEGY_MISSING` | 缺测试策略设计 | 补齐 Test Strategy Design |
| `AC_TEST_MAPPING_MISSING` | AC 未映射到具体测试或人工验收 | 补齐 AC -> 测试映射 |
| `PERFORMANCE_CONSTRAINT_MISSING` | 涉及报表/导入/聚合/大列表但缺性能容量约束 | 补齐 Performance and Capacity Design |
| `SECURITY_CONTRACT_MISSING` | 涉及安全入口但缺安全约束 | 补齐 Security and Sensitive Data Design |
| `SENSITIVE_DATA_POLICY_MISSING` | 涉及敏感数据但缺展示、导出、日志脱敏策略 | 补齐敏感数据策略 |
| `CONFIG_CONTRACT_MISSING` | 涉及配置项但缺配置名、默认值、缺失行为、环境差异 | 补齐 Configuration Design |
| `FRAMEWORK_CONVENTION_MISSING` | 涉及框架生成/目录/基类/注解但缺项目框架约定 | 补齐 Framework Convention Design |
| `MANUAL_ACCEPTANCE_UNCLEAR` | 需要人工验收但缺前置条件、步骤、通过标准和证据 | 补齐 Manual Acceptance Design |
| `OPS_DOC_CONTRACT_MISSING` | 涉及配置、部署、定时、外部系统但缺文档/运维交接 | 补齐 Documentation and Operations Handoff |
| `MISSING_DECLARED_ARTIFACT` | 声明需要的产物未写入真实目录 | 写入产物或修正声明 |
| `PLACEHOLDER_HIT` | 产物中有模板占位或未决表达 | 替换成具体值 |
| `JSONL_SEED_HIT` | JSONL 仍包含 `_example` 种子行 | 填真实上下文或删除并说明不需要 |
| `JSONL_MODE_MISMATCH` | JSONL 模式与 `.trellis/config.yaml` 或规划产物矩阵不一致 | 修正 `required/optional/inline` 模式后重跑 Gate |
| `CONTRACT_TOKEN_HIT` | forbidden token 命中 | 按 Contract Snapshot 修正 |
| `COVERAGE_COUNT_MISMATCH` | 覆盖统计与矩阵机械统计不一致 | 重新统计并修正父 PRD |
| `MECHANICAL_GATE_MISSING` | Gate 结果没有命令/脚本输出证据，或由模型手填 | 运行机械扫描并用真实结果覆盖 |
| `DECLARED_GATE_MISMATCH` | 父 PRD 声明的 Gate 数值与机械扫描结果不一致 | 以机械扫描为准修正产物和 PRD |
| `STATE_DRIFT` | Stage State Packet 与矩阵、账本或真实目录不一致 | Drift Reset，重建状态后继续 |
| `DEVELOPMENT_NOT_READY` | 不满足开发建议门槛 | 不建议开发，输出下一步 |

## Gate 输出格式

每个 Gate 输出统一使用：

```yaml
gate:
  name: <Gate Name>
  result: PASS | FAIL
  failure_codes:
    - <code>
  evidence:
    - <file/table/row>
  next_action: <具体修复或下一批规划动作>
```

Gate 的 `evidence` 不能只写自然语言判断。数量类、文件存在性、占位符、JSONL 种子、forbidden token 和 Artifact Gate 必须引用命令输出、脚本输出、矩阵行或真实文件路径。缺少机械证据时 Gate 自动为 `FAIL`，失败码为 `MECHANICAL_GATE_MISSING`。

## Requirement Ledger Gate

输入：

- 源需求文档。
- 原始需求功能点清单。
- Full Requirement Matrix。
- MVP Coverage Matrix。
- Backlog。

PASS 条件：

- 每个源需求功能点都有稳定 `REQ-xxx`。
- 每个验收点都有稳定 `AC-xxx`。
- Full Requirement Matrix 覆盖源需求全部可验收功能点。
- MVP Coverage Matrix 每行状态属于 `TASK`、`MERGED`、`BASELINE`、`OUT_OF_SCOPE`、`BLOCKED`。
- `TASK + MERGED + BASELINE + OUT_OF_SCOPE + BLOCKED` 机械统计等于 Full Requirement Matrix 行数。
- 所有 `OUT_OF_SCOPE` 进入 Backlog。

FAIL 时不得起草完整子任务 PRD。

## Contract Gate

输入：

- Project Contract Lock。
- Contract Snapshot。
- README、AGENTS、`.trellis/spec/`、现有代码证据。

PASS 条件：

- 已选择 Project Contract Profile，并说明选择证据与拒绝其他 profile 的原因。
- Contract Lock 使用所选 profile 的字段；每个适用字段都有 adopted value 和证据路径。
- 不适用字段显式写 `not-applicable`，没有把 Java/RuoYi 字段套到 CLI、SDK、前端、Python 服务或自定义项目。
- forbidden_tokens 来自冲突来源、旧任务错误命名、框架默认误判或与 README/spec 不一致的候选值。
- 无未裁决 `CONTRACT_CONFLICT`。

FAIL 时不得创建任务。

## Full MVP Planning Gate

输入：

- Full Requirement Matrix。
- MVP Coverage Matrix。
- Subtask Planning Ledger。
- Batch Completion Rollup。
- 规划产物矩阵。
- 父/子 PRD 草案。

PASS 条件：

- 每个 MVP `TASK` 覆盖项都有目标 Task ID。
- 每个 `MERGED` 覆盖项写明目标子任务和覆盖 AC。
- 每个 Task ID 有标题、REQ 覆盖、依赖、优先级、批次、可并行组、复杂度、Small Model 粒度、验收标准、PRD 草案和产物需求。
- 每个 Task ID 有任务影响面矩阵；任一影响面为“是”时，规划产物矩阵必须要求 `design.md` 与 `implement.md`，并列出对应章节。
- 所有 MVP 子任务状态为 `READY_TO_CONFIRM`、`BLOCKED` 或 `OUT_OF_SCOPE`。
- 不存在 `UNASSIGNED_MVP_REQ`、`UNBATCHED_TASK`、`P0P1_ONLY_PLAN`、`DEFERRED_PRD_WITHOUT_PLAN`。
- 规划产物矩阵覆盖 Subtask Planning Ledger 中所有当前 MVP `TASK` 子任务。
- Stage State Packet 中的 `total_mvp_tasks`、`ready_to_confirm`、`blocked`、`out_of_scope`、`non_terminal` 与 Subtask Planning Ledger 机械统计一致。

FAIL 时继续规划下一批，不请求用户确认。

## Batch Completeness Gate

输入：

- Subtask Planning Ledger。
- Batch Completion Rollup。

PASS 条件：

- 每个 MVP `TASK` 子任务有批次。
- 每个批次列出 Task ID、目标、依赖层级、可并行组、状态、剩余非终态任务和下一步。
- 单批不超过 Small Model Mode 上限。
- 后续批次不是“待规划”；至少有冻结的任务边界、REQ 覆盖、依赖、复杂度和产物需求。

FAIL 时输出 `BATCH_INCOMPLETE`。

## Design Surface Gate

输入：

- 子任务 PRD 的“任务影响面矩阵”。
- `design.md`。
- `implement.md`。
- `references/design-surface-template.md`。

PASS 条件：

- 每个子任务 PRD 都包含“任务影响面矩阵”。
- 任一影响面 `是否涉及 = 是` 时，`design.md` 存在且包含矩阵中声明的设计章节。
- 任一影响面 `是否涉及 = 是` 时，`implement.md` 存在且包含矩阵中声明的实现计划章节。
- 影响面矩阵声明的 Gate 失败码与 `design-surface-template.md` 映射一致。
- 若任务是 `java-ruoyi-crud` CRUD/fullstack/frontend/backend 任务，数据库、API、UI、权限、查询、校验、测试等常见影响面不得无理由全部标为“否”。

第一版机械 Gate 只要求“声明为是 -> 章节存在”。如模型把明显涉及的影响面错误标为“否”，自我评审必须输出风险，后续可由关键词推断增强。

## Pre-Confirmation Gate

输入：

- Requirement Ledger Gate 结果。
- Contract Gate 结果。
- Full MVP Planning Gate 结果。
- Batch Completeness Gate 结果。

PASS 条件：

- 上述 Gate 均为 `PASS`。
- 用户确认内容可覆盖完整 MVP 任务树、全部批次、Backlog、Blocked 项和首批创建范围。

FAIL 时不得输出确认请求。

## Task Creation Gate

输入：

- 用户确认记录。
- `task.py create` 输出。
- Subtask Planning Ledger。

PASS 条件：

- 用户已确认完整规划。
- 父任务和全部确认范围内子任务均通过 `task.py create` 创建。
- 每个真实目录包含 `task.json`。
- 逻辑 Task ID -> 真实任务目录映射已回填账本。
- 未创建无 `task.json` 的旁路目录承载 PRD。

FAIL 时不得写入产物。

## Artifact Gate

输入：

- 真实任务目录。
- 父/子 `prd.md`。
- `design.md`、`implement.md`、`implement.jsonl`、`check.jsonl`。
- 规划产物矩阵。
- Contract Snapshot。
- `scripts/trellis_zero_gate.py` 输出，或等价机械扫描命令输出。

推荐命令：

```bash
python <skill-dir>/scripts/trellis_zero_gate.py \
  --tasks .trellis/tasks \
  --parent-task-json <parent-task-dir>/task.json \
  --parent-prd <parent-task-dir>/prd.md \
  --jsonl-mode <required|optional|inline>
```

如 Contract Snapshot 定义 forbidden tokens，追加 `--forbidden-token '<token>'` 或 `--forbidden-regex '<regex>'`。若存在不能简化为 forbidden token 的项目契约冲突，追加 `--contract-mismatch-regex '<regex>'`。

PASS 条件：

- `scanned_tasks` 等于本批父/子任务数。
- `placeholder_hits = 0`。
- `angle_placeholder_hits = 0`。
- `jsonl_seed_hits = 0`。仅 `jsonl_mode=required` 时 seed-only 阻断；`optional` / `inline` 必须输出 raw seed examples 并在规划产物矩阵说明删除或不需要原因。
- `forbidden_token_hits = 0`。
- `contract_mismatch_hits = 0`。
- `coverage_count_mismatch_hits = 0`。
- `high_complexity_missing_artifacts = 0`。
- `missing_declared_artifacts = 0`。
- `design_surface_prd_without_matrix = 0`。
- `design_surface_missing_hits = 0`。
- `declared_gate_mismatch_hits = 0`。
- `external_config_hits = 0`。
- 机械扫描输出 `result = PASS`。

FAIL 或 PENDING 时不得汇报任务树可执行。

## Development Recommendation Gate

输入：

- Subtask Planning Ledger。
- Artifact Gate 结果。
- 阻塞任务列表。

PASS 条件：

- Artifact Gate 为 `PASS`。
- 所有已创建且属于当前 MVP 的子任务为 `GATED_PASS`、`BLOCKED` 或 `OUT_OF_SCOPE`。
- 没有未解释的非终态任务。
- 可推荐任务的依赖已满足或依赖为 existing baseline。

FAIL 时输出 `development_ready: false`，不得建议开始开发。
