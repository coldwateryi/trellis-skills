# 任务创建检查清单

用户确认只读分析后使用此清单。

## 创建任务前

- [ ] 已知源需求文档路径。
- [ ] 如存在 `.trellis/workflow.md`，已读取；如存在 `.trellis/config.yaml`、`.trellis/.version`、`.trellis/.developer`，已检查。
- [ ] 已读取 `.trellis/config.yaml` 中的 `codex.dispatch_mode`；`inline` 使用 `jsonl_mode=inline`，sub-agent 或 JSONL 必需场景使用 `jsonl_mode=required`。
- [ ] 相关 `.trellis/spec/` 文件足够新，或已规划在实现任务前执行 spec 刷新/bootstrap 任务。
- [ ] 已选择 Project Contract Profile，并说明选择证据和拒绝其他 profile 的原因。
- [ ] 已输出 Project Contract Lock，且所选 profile 的适用字段都有 adopted value 和证据路径；不适用字段写 `not-applicable`。
- [ ] 没有把 RuoYi/Java 字段套到 CLI、SDK、前端、Python 服务或自定义框架项目。
- [ ] 如存在 `CONTRACT_CONFLICT`，已让用户确认采用方案；未确认前没有创建任务。
- [ ] 已输出 Contract Snapshot 与 forbidden_tokens；每个子任务候选都已对照 forbidden_tokens 扫描，命中项已修正。
- [ ] 所有子任务候选都遵守 Project Contract Lock；没有混用两套命名体系、表名前缀、路由或包路径。
- [ ] 如果仓库已经有手工实现，Existing Implementation Baseline（已有实现基线）已完整。
- [ ] `DONE` 需求没有实现子任务。
- [ ] `UNTESTED` 需求只创建测试覆盖任务。
- [ ] `PARTIAL` 需求只为缺失行为创建补缺任务。
- [ ] 需求 ID 稳定。
- [ ] `REQ-xxx` 绑定源需求功能点，不因任务合并、拆分、重排而改变语义。
- [ ] 原始需求功能点清单完整，且每个功能点都有 `REQ-xxx`。
- [ ] Full Requirement Matrix 和 MVP Coverage Matrix 已分开；没有把 MVP 覆盖数量写成原始功能点总数。
- [ ] 完整平台范围和当前 MVP 边界差异已说明。
- [ ] 每个 `REQ-xxx` 都有覆盖状态：`TASK`、`MERGED`、`BASELINE`、`OUT_OF_SCOPE` 或 `BLOCKED`。
- [ ] 每个 `MERGED` 需求都写明目标子任务和覆盖 AC。
- [ ] 每个 `BASELINE` 需求都写明已有实现证据。
- [ ] 每个 `OUT_OF_SCOPE` 需求都写明排除原因，并将在确认范围时提示用户。
- [ ] 所有 `OUT_OF_SCOPE` 需求已进入 Backlog 表，写明推荐阶段、恢复条件和依赖的 MVP 任务。
- [ ] 任务合并/拆分记录完整，任务数量变化有明确理由。
- [ ] MVP 边界明确。
- [ ] 已生成 Subtask Planning Ledger，且每个 MVP Coverage Matrix 中 `TASK` 状态的子任务都有账本行。
- [ ] 已生成 Batch Completion Rollup，明确 B01/B02/... 的 Task ID、依赖层级、可并行组和本批目标。
- [ ] 所有 MVP 子任务均为 `READY_TO_CONFIRM`、`BLOCKED` 或 `OUT_OF_SCOPE`；不存在只规划 P0/P1 的情况。
- [ ] 不存在 `UNASSIGNED_MVP_REQ`、`UNBATCHED_TASK`、`P0P1_ONLY_PLAN` 或 `DEFERRED_PRD_WITHOUT_PLAN`。
- [ ] 用户已确认完整 MVP 任务树、全部批次规划、Backlog 边界、Blocked 项和首批创建范围。
- [ ] 每个子任务都有验收标准。
- [ ] 每个子任务都有测试要求。
- [ ] 依赖关系明确。
- [ ] Trellis task 依赖和已有基线依赖已分开表达。
- [ ] 已区分规划期逻辑标识（如 `T01`、`REQ-001`、`<child-slug>`）和 Trellis 真实任务目录（`task.py create` 输出的 `.trellis/tasks/<MM-DD-slug>/`）。
- [ ] 每个子任务已标注复杂度（低/中/高），高复杂度任务已拆碎或在 PRD 里把每步定死。
- [ ] Small Model Mode 下，每个子任务只覆盖一个实体 CRUD、一个接口组、一个状态流转、一个前端页面或一个后端聚合查询。
- [ ] Small Model Mode 下，没有子任务同时包含两个以上主实体、两套 CRUD、CRUD+状态机+报表、后端流程+小程序页面、地图/GIS+多表聚合+高级分析。
- [ ] Small Model Mode 下，没有用“强耦合”“同一流程”“拆分会增加依赖”为理由自行豁免超大任务；如保留合并，已有用户明确确认记录。
- [ ] Small Model Mode 下，单批最多创建 8 个可执行子任务，单批最多完整写入 5 个高质量 PRD；超出时已排完整批次，不只排 P0/P1。
- [ ] 如果使用小模型规划且预计子任务超过 15 个，已采用分批规划，而不是一次性生成全部完整 PRD；非首批 MVP 任务也有标题、REQ 覆盖、依赖、复杂度、产物需求和预计批次。
- [ ] 若运行环境支持子代理，已按 Agent Packet 分派批次或业务域；若不支持，已标记 `agent_mode: unavailable_fallback_serial`。
- [ ] 每个子任务 PRD 的所有 `<...>` 占位符已替换为具体值，无"待定/视情况而定"。
- [ ] 每个子任务 PRD 没有 `{Entity}`、`{domain}`、`{entity}`、`<PageComponent>`、`TBD` 等模板残留。
- [ ] 每个子任务 PRD 没有 `YOUR_KEY`、`API_KEY_HERE`、`待用户提供` 等未决配置；外部配置已定为 `FIXED`、`BASELINE`、`BLOCKED` 或 `OUT_OF_SCOPE`。
- [ ] 每个子任务的标题、业务域、主实体、表名、路由、文件清单一致；引用其他任务内容时已列出依赖或基线原因。
- [ ] 每个子任务都有 Project Contract Reference 或等价契约引用，并与父任务 Project Contract Lock 一致。
- [ ] 每个子任务 PRD 含参考实现路径、行为约束、验收标准、依赖、Project Contract Reference 和实现计划定位。
- [ ] 每个子任务 PRD 含“任务影响面矩阵”，且影响面判断与任务类型、语义锚点、文件计划一致。
- [ ] 影响面矩阵中任一项为“是”时，已准备对应 `design.md` 章节和 `implement.md` 落地计划章节。
- [ ] Trellis 0.6+ 项目中，详细文件清单、有序实现步骤、自检命令已写入 `implement.md`；只有低复杂度 PRD-only 且本地工作流允许时，才放在 PRD 精简执行附录。
- [ ] 已生成规划产物矩阵，逐个子任务列出 `prd.md`、`design.md`、`implement.md`、`implement.jsonl`、`check.jsonl` 是否需要以及原因。
- [ ] 中/高复杂度子任务已按项目工作流和风险，包含或明确要求 `design.md`、`implement.md`、`implement.jsonl`、`check.jsonl`。
- [ ] 高复杂度任务没有 PRD-only；如仍为高复杂度，必须要求 `design.md` + `implement.md`，否则已继续拆小并更新复杂度。
- [ ] 如果工作流要求中/高复杂度任务有 `design.md`，已同时准备 `implement.md`，或明确说明不需要。
- [ ] `implement.jsonl` / `check.jsonl` 如果存在，不只保留 `_example` 种子行；`jsonl_mode=optional/inline` 时已删除 seed 或在规划产物矩阵标记 `NOT_NEEDED_WITH_REASON`。
- [ ] 涉及数据库、API、UI、权限、字典、状态、校验、事务、外部接口或测试策略的任务，不得缺失对应 design surface 章节。
- [ ] 验收标准写成可机器校验或可逐条勾选的断言。
- [ ] 父 PRD 的覆盖汇总数量由 MVP Coverage Matrix 机械统计得出，没有手写估算。
- [ ] 小模型或长程复杂任务已按 `small-model-safety.md` 输出 Stage State Packet；状态包计数与矩阵/账本一致。

## 命令

```bash
python ./.trellis/scripts/task.py create "<parent title>" --slug <parent-slug>
python ./.trellis/scripts/task.py create "<child title>" --slug <child-slug> --parent "<parent-task-dir>"
```

执行命令时必须记录每条 `task.py create` 的 stdout 返回路径，并把它作为写入产物的唯一可信路径。不要根据 slug、日期或 Task ID 自行拼接目录。

如果 `task.py create` 报告未设置 developer，停止并要求用户先初始化 Trellis：

```bash
trellis init -u <name>
```

如果项目使用特定平台参数，一并加上，例如 `--codex`。

只有 Trellis CLI 不可用时，才使用旧版兜底方式：

```bash
python ./.trellis/scripts/init_developer.py <name>
```

或要求用户提供可用于 `--assignee` 的 assignee。

## 创建任务后

- [ ] 每个已创建任务目录都包含 `task.json`。
- [ ] 已用 `task.py create` 输出的真实目录回填 Subtask Planning Ledger。
- [ ] 写入父任务真实目录下的 `prd.md`。
- [ ] 写入每个子任务真实目录下的 `prd.md`。
- [ ] 写入前后都没有把完整 PRD 放进 `.trellis/tasks/<logical-task-id>/`、`.trellis/tasks/tXX-*/` 等无 `task.json` 的旁路目录。
- [ ] 没有创建或使用 `<task-dir>/prd/` 子目录作为 PRD 容器；PRD 文件路径必须是 `<task-dir>/prd.md`。
- [ ] 按规划产物矩阵写入所有标记为"需要"的 `design.md`、`implement.md`、`implement.jsonl` 和 `check.jsonl`，且这些产物位于同一个真实任务目录。
- [ ] 不存在 `prd.md` 写明某产物"需要"，但真实目录缺失该文件的任务。
- [ ] 不存在高复杂度 PRD-only 任务；若没有额外产物，必须已拆小并在父任务合并/拆分记录中说明。
- [ ] `python ./.trellis/scripts/task.py list` 能显示父任务和全部子任务，父子关系正确。
- [ ] 新写入的父/子任务 `prd.md` 不再保留 `TBD`、`<...>`、"待定"或"视情况而定"。
- [ ] 运行占位符扫描，结果为空：

```bash
rg -n '\{Entity\}|\{domain\}|\{entity\}|<PageComponent>|<任务标题>|<path>|TBD|待定|视情况|根据实际情况' .trellis/tasks/*/*.md
```

- [ ] 运行通用尖括号占位扫描，结果为空或每项都有明确非占位解释：

```bash
rg -n '<[A-Za-z0-9_.:/ -]+>' .trellis/tasks/*/*.{md,jsonl}
```

- [ ] 运行 JSONL 种子扫描；若命中，新任务的 JSONL 已填入真实上下文或说明无需 JSONL：

```bash
rg -n '"_example"' .trellis/tasks/*/*.jsonl
```

- [ ] 运行 Contract forbidden token 扫描；把 `<forbidden-token-regex>` 替换为 Contract Snapshot 生成的禁止词正则，结果必须为空：

```bash
rg -n '<forbidden-token-regex>' .trellis/tasks/*/*.{md,jsonl}
```

- [ ] 抽查每个 `design.md` / `implement.md`，标题、语义锚点、文件计划、路由/API/命令/表名/状态对象与对应 `prd.md` 一致，没有串用其他任务内容。
- [ ] 运行 Project Contract Check：命名、路径、API、命令、包/模块、路由、表名和权限模型均与父任务 Project Contract Lock 一致。
- [ ] 运行 Design Surface Check：PRD 影响面矩阵声明为“是”的设计面，在 `design.md` 和 `implement.md` 中均有对应章节。
- [ ] 运行 Small Model Grain Check：新任务仍满足一个实体/接口/状态流转/页面/聚合查询；不满足则拆分或阻塞。
- [ ] 运行外部配置扫描，结果为空或已标 `FIXED`、`BASELINE`、`BLOCKED`、`OUT_OF_SCOPE`：

```bash
rg -n 'YOUR_KEY|API_KEY_HERE|待用户提供|待配置|待申请' .trellis/tasks/*/*.{md,jsonl}
```

- [ ] 输出 Artifact Gate 结果：`scanned_tasks`、`placeholder_hits`、`jsonl_seed_hits`、`forbidden_token_hits`、`contract_mismatch_hits`、`coverage_count_mismatch_hits`、`high_complexity_missing_artifacts`、`missing_declared_artifacts`、`design_surface_prd_without_matrix`、`design_surface_missing_hits`、`external_config_hits`、`result: PASS/FAIL`。
- [ ] 运行确定性 Gate 脚本，并以脚本 JSON 作为 Artifact Gate 单一证据来源：

```bash
python <skill-dir>/scripts/trellis_zero_gate.py \
  --tasks .trellis/tasks \
  --parent-task-json <parent-task-dir>/task.json \
  --parent-prd <parent-task-dir>/prd.md \
  --jsonl-mode <required|optional|inline>
```

- [ ] 如 Contract Snapshot 定义 forbidden tokens，已追加 `--forbidden-token` 或 `--forbidden-regex`。
- [ ] 输出 Artifact Gate 结果：`scanned_tasks`、`placeholder_hits`、`angle_placeholder_hits`、`jsonl_seed_hits`、`forbidden_token_hits`、`contract_mismatch_hits`、`coverage_count_mismatch_hits`、`high_complexity_missing_artifacts`、`missing_declared_artifacts`、`design_surface_prd_without_matrix`、`design_surface_missing_hits`、`declared_gate_mismatch_hits`、`external_config_hits`、`result: PASS/FAIL`。
- [ ] 父 PRD 中已声明的 Gate 数值与脚本输出一致；不一致时以脚本结果为准，失败码为 `DECLARED_GATE_MISMATCH`。
- [ ] Artifact Gate 为 `FAIL` 或 `PENDING` 时，没有汇报任务树可执行；已修正或明确阻塞。
- [ ] 本批已创建任务的状态已更新为 `CREATED`、`ARTIFACTS_WRITTEN`、`GATED_PASS` 或 `BLOCKED`。
- [ ] 若仍存在未创建、未写入或未 Gate 通过的 MVP 子任务，最终汇报使用 `BATCH_INCOMPLETE`，不得建议开始开发。
- [ ] 只有 Development Recommendation Gate 为 `PASS` 时，才输出第一个建议开始的任务。
- [ ] 输出任务树。
- [ ] 输出按依赖排序的执行计划。
- [ ] 输出被阻塞任务列表。
- [ ] 输出可并行任务列表。
- [ ] 不要开始实现。
