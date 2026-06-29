# Small Model Long-Run Safety

用于本地小/中参数模型执行长程 Trellis 规划时降低幻觉、漂移和自证通过。

## 目标

把长程推理拆成可复原的短阶段。模型只负责根据当前阶段输入生成草案；所有计数、文件存在性、占位符、JSONL 种子、契约命中和 Gate 结果必须由机械扫描或明确表格统计产生。

## Stage State Packet

每次进入新阶段、恢复上下文、调用子代理、写入任务目录前，都先输出并复核本状态包：

```yaml
stage_state:
  state: S0_DISCOVER_CONTEXT | S1_REQUIREMENT_LEDGER | S2_CONTRACT_LOCK | S3_FULL_MVP_TASK_CANDIDATES | S4_PROGRESSIVE_BATCH_PLANNING | S5_FULL_MVP_PLANNING_GATE | S6_USER_CONFIRMATION | S7_TASK_CREATION | S8_ARTIFACT_WRITING | S9_ARTIFACT_GATE | S10_NEXT_IMPLEMENTATION_RECOMMENDATION
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

- `unknown` 只能出现在发现阶段；进入 Gate 前必须替换为机械统计值。
- `next_legal_action` 只能有一个，避免模型同时创建任务、写产物和建议开发。
- 若 `stop_gate_failures` 非空，不得继续下一阶段。

## Context Budget

- 不要把完整源文档、完整父 PRD、所有子 PRD 和旧任务结果一次性塞给小模型。
- 每个子代理或串行模拟步骤只给相关 REQ 行、Contract Snapshot、依赖边界和输出格式。
- 每规划完一批，主代理从 Subtask Planning Ledger 重新读取状态，不依赖上一轮自然语言记忆。
- 超过 5 个子任务 PRD 或 3 个业务域时，拆成多个 Agent Packet；平台不支持子代理时，按 packet 串行模拟并标记 `agent_mode: unavailable_fallback_serial`。

### 上下文预算表（按模型能力分配）

以下表格以 Qwen3.6 35B（128K 上下文窗口）为基准。分配到每个阶段/操作的上下文量视项目复杂度调整。

| 阶段 | 上下文预算 | 包含内容 | 策略 |
|:---|:---|:---|:---|
| S0 发现 | ≤20K tokens | README + 关键代码结构 + `.trellis/` 元数据 | 只读目录树和头部注释，不要直接读完整源文件 |
| S1 需求账本 | ≤15K tokens | 源需求文档 + Full Requirement Matrix 模板 | 一次读完源需求，输出矩阵后立即将中间结果写入文件 |
| S2 合约锁定 | ≤8K tokens | README + spec 关键行 + Contract Lock 模板 | 不要读取无关模块，只关注命名/路径/API 等契约字段 |
| S3 任务候选 | ≤10K tokens | MVP Coverage Matrix + Small Model 粒度规则 | 一次只考虑一个业务域的任务拆分 |
| S4 批次规划 | ≤10K tokens/批 | 本批 Task ID 范围 + Contract Snapshot + PRD 模板 | 每批完成后立即写入 .trellis/planning/ 文件系统 |
| S5 Gate | ≤5K tokens | 矩阵 + 账本 + Gate 定义 | 只检查，不生成新内容 |
| S6 用户确认 | ≤4K tokens | 汇总摘要 + Gate 结果 | 只用最终数据展示，不推理 |
| S7 任务创建 | ≤6K tokens | 账本 + task.py 命令 | 一次创建一个 task，不要并行创建 |
| S8 产物写入 | ≤8K tokens/任务 | 对应模板 + Contract Snapshot | 一次写一个任务的 PRD/design/implement |
| S9 Artifact Gate | ≤4K tokens | trellis_zero_gate.py 输出 | 只解读脚本输出，不手填 Gate 值 |
| 自审检查（任一轮） | ≤6K tokens | 本阶段对应检查清单条目 | 只读本阶段相关的检查项（≤10 条） |
| 一次 Drift Reset | ≤6K tokens | 矩阵 + 账本 + 真实目录 | 只从文件重建状态，不依赖记忆 |

### 阶段满载警告

达到以下任一阈值时，必须停在本阶段、将中间产物写入 `.trellis/planning/` 目录，再进入下一阶段：

- 当前阶段上下文消耗 > 80% 预算
- 子任务候选超过 8 个但未开始批次规划
- 单批 PRD 草案超过 5 个但未提交文件
- 已连续生成 >10000 tokens 未执行 Gate 检查

## Evidence Discipline

任何以下结论都必须带证据路径或命令输出摘要：

- 需求数量和覆盖状态数量。
- 子任务数量、批次数量、每批剩余非终态数量。
- `design.md` / `implement.md` 是否需要、是否存在。
- JSONL 是否仍含 `_example`。
- 占位符和 forbidden token 是否为 0。
- Artifact Gate 是否 PASS。

禁止：

- 用“已检查”“看起来一致”“应当没有问题”作为 Gate 证据。
- 在未运行机械扫描时手填 `jsonl_seed_hits = 0` 或 `result = PASS`。
- 在失败项存在时建议开始开发。

## Mechanical Artifact Gate

创建任务并写入产物后，运行：

```bash
python <skill-dir>/scripts/trellis_zero_gate.py \
  --tasks .trellis/tasks \
  --parent-task-json <parent-task-dir>/task.json \
  --parent-prd <parent-task-dir>/prd.md
```

如有 Contract Snapshot forbidden tokens，追加：

```bash
  --forbidden-token '<token>'
```

或：

```bash
  --forbidden-regex '<regex>'
```

脚本 `result` 不是 `PASS` 时，必须输出失败码和修复清单，不能汇报任务树可执行。

## Drift Reset

出现以下任一情况时，立即重建 Stage State Packet，并回到最近的合法状态：

- 模型开始引用未在 Contract Snapshot 中出现的实体名、包路径、路由或表名。
- 需求总数、TASK 数、子任务数与上一阶段不一致且没有合并/拆分记录。
- 只规划 P0/P1 后开始请求用户确认。
- 父 PRD 的 Gate 结果与机械扫描结果不一致。
- 子任务 PRD 声明需要设计/实现产物，但真实目录不存在。

重建时只读取事实来源：源需求、Contract Snapshot、Full Requirement Matrix、MVP Coverage Matrix、Subtask Planning Ledger、真实任务目录和机械 Gate 输出。

## 阶段原子检查清单（每阶段 ≤10 条）

小模型在每个阶段完成时，必须逐条检查本阶段对应的清单。检查结果记入 Stage State Packet 的 `stop_gate_failures`。

### S0 发现阶段检查

- [ ] 已找到源需求文档，确认路径
- [ ] 已读取 README/模块 README/AGENTS（如存在）
- [ ] 已检查 `.trellis/workflow.md`、`.trellis/config.yaml`、`.trellis/.version`
- [ ] 已定位现有代码/测试结构（非空项目时）
- [ ] 尚未起草任何子任务 PRD
- [ ] Level 1 参考文件已读取
- [ ] 已运行 `trellis_planning_gate.py --phase S1_REQUIREMENT_LEDGER` 且结果为 PASS

### S1 需求账本阶段检查

- [ ] 每个源需求功能点都有 REQ-xxx
- [ ] Full Requirement Matrix 行数 = 源需求功能点数
- [ ] MVP Coverage Matrix 五类之和 = Full Requirement Matrix 行数（机械统计）
- [ ] 所有 OUT_OF_SCOPE 需求已进入 Backlog 表
- [ ] Contract Profile 已选择并有证据
- [ ] 未创建任何 Trellis task
- [ ] 未起草任何完整子任务 PRD
- [ ] 已运行 `trellis_planning_gate.py --phase S2_CONTRACT_LOCK` 且结果为 PASS

### S2 合约锁定阶段检查

- [ ] Contract Lock 已输出，所有适用字段有 adopted_value 和 evidence_path
- [ ] Contract Snapshot 已输出，包含 forbidden_tokens
- [ ] 不适用字段写 `not-applicable`，没有把 Java/RuoYi 字段套到非 Java 项目
- [ ] 无未裁决 `CONTRACT_CONFLICT`（如有已阻塞用户确认）
- [ ] 尚未开始任务拆分和 PRD 起草
- [ ] Contract Gate = PASS

### S3 任务候选阶段检查

- [ ] 全部 MVP `TASK` 需求都有目标 Task ID
- [ ] 每个 Task ID 有完整字段（标题、依赖、优先级、复杂度）
- [ ] Small Model Mode 下，一个子任务只覆盖一个主实体 CRUD / 一个接口组 / 一个状态流转 / 一个页面 / 一个聚合查询
- [ ] 高复杂度任务已被拆分为中/低复杂度（或指定了 design.md + implement.md）
- [ ] 模型没有用"强耦合""同一流程"为理由自行豁免超大任务
- [ ] 已输出 Subtask Planning Ledger（所有 TASK 任务都有行）
- [ ] 已运行 `trellis_planning_gate.py --phase S3_FULL_MVP_TASK_CANDIDATES` 且结果为 PASS

### S4 批次规划阶段检查

- [ ] 单批 ≤8 个可执行子任务，≤5 个完整 PRD
- [ ] 每批的 PRD 草案已冻结（READY_TO_CONFIRM）
- [ ] 不存在的 `P0P1_ONLY_PLAN`（P2/P3 任务也已规划）
- [ ] 后续批次不是"待规划"；已有冻结的任务边界、REQ 覆盖、依赖、复杂度和产物需求
- [ ] 子任务 PRD 包含"任务影响面矩阵"
- [ ] 每批完成后运行 `trellis_planning_gate.py --phase S4_PROGRESSIVE_BATCH_PLANNING`

### S5 门控阶段检查

- [ ] Full MVP Planning Gate = PASS
- [ ] Batch Completeness Gate = PASS
- [ ] Pre-Confirmation Gate = PASS
- [ ] 所有 MVP TASK 子任务状态 ∈ {READY_TO_CONFIRM, BLOCKED, OUT_OF_SCOPE}
- [ ] 不存在 UNASSIGNED_MVP_REQ、UNBATCHED_TASK、P0P1_ONLY_PLAN、DEFERRED_PRD_WITHOUT_PLAN
- [ ] 无占位符在父/子 PRD 草案中
- [ ] 已运行 `trellis_planning_gate.py --phase S5_FULL_MVP_PLANNING_GATE` 且结果为 PASS

### 单调收敛保护

**如果连续 2 轮自我评审发现完全相同的问题且未修复：**
1. 输出 `STALLED_CONVERGENCE`
2. 停止当前路径
3. 建议用户换强模型或人工介入
4. 记录已在哪些轮次尝试修复（列出轮次号和尝试的方案）
