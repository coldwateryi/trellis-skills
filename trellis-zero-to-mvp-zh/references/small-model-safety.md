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
