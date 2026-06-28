# Trellis Zero to MVP 工作流状态机

本文件定义主流程的合法状态转换。执行 `trellis-zero-to-mvp-zh` 时必须按状态机推进，不得用“已完成 P0/P1”替代完整规划完成。

## 状态表

| 状态 | 目标 | 允许动作 | 退出条件 |
| --- | --- | --- | --- |
| `S0_DISCOVER_CONTEXT` | 找到源需求、本地约定、Trellis 工作流和已有实现证据 | 只读扫描文档、README、AGENTS、`.trellis/spec/`、`.trellis/tasks/`、代码结构 | 输入路径和上下文清单明确 |
| `S1_REQUIREMENT_LEDGER` | 完整抽取源需求并分配 `REQ/AC` | 输出原始需求功能点清单、Full Requirement Matrix、MVP Coverage Matrix、Backlog | Requirement Ledger Gate = PASS |
| `S2_CONTRACT_LOCK` | 锁定本地实现契约 | 输出 Project Contract Lock、Contract Snapshot、forbidden_tokens、冲突表 | Contract Gate = PASS |
| `S3_FULL_MVP_TASK_CANDIDATES` | 形成完整 MVP 子任务候选 | 按能力拆分所有 MVP `TASK`，标依赖、复杂度、优先级、Small Model 粒度 | 所有 MVP `TASK` 需求都有候选 Task ID |
| `S4_PROGRESSIVE_BATCH_PLANNING` | 渐进式补齐全部批次的 PRD/设计/产物计划 | 使用主代理或子代理逐批生成 Subtask Planning Ledger、Batch Completion Rollup、PRD 草案、规划产物矩阵 | 所有 MVP 子任务达到 `READY_TO_CONFIRM`、`BLOCKED` 或 `OUT_OF_SCOPE` |
| `S5_FULL_MVP_PLANNING_GATE` | 机械检查完整规划质量 | 执行 Full MVP Planning Gate、Batch Completeness Gate、Pre-Confirmation Gate | 三个 Gate 均 PASS |
| `S6_USER_CONFIRMATION` | 请求用户确认完整规划 | 展示完整任务树、全部批次、Backlog、Blocked 项和 Gate 结果 | 用户确认或调整范围 |
| `S7_TASK_CREATION` | 创建 Trellis 父子任务 | 运行 `task.py create`，记录真实目录，回填账本 | Task Creation Gate = PASS |
| `S8_ARTIFACT_WRITING` | 写入 PRD 和必要规划产物 | 写父/子 `prd.md`、`design.md`、`implement.md`、JSONL | 所有声明需要的产物真实存在 |
| `S9_ARTIFACT_GATE` | 校验真实任务目录产物 | 运行占位符、JSONL、契约、粒度、缺失产物检查 | Artifact Gate = PASS |
| `S10_NEXT_IMPLEMENTATION_RECOMMENDATION` | 推荐首个可执行子任务 | 输出任务树、执行顺序、并行任务、阻塞任务、首个建议任务 | Development Recommendation Gate = PASS |

## 强制跳转规则

- `S0` 前不得使用模型常识填补本地契约。
- `S1` 前不得起草完整子任务 PRD。
- `S3` 前不得生成最终任务树。
- `S5` 未 PASS 前不得请求用户确认。
- `S6` 未确认前不得运行 `task.py create`。
- `S9` 未 PASS 前不得汇报任务树可执行。
- `S10` 只有在完整规划和 Artifact Gate 均 PASS 后才能建议开发第一个子任务。

## Subtask Planning Ledger 状态

| 状态 | 含义 | 是否终态 |
| --- | --- | --- |
| `CANDIDATE` | 已识别候选任务，但边界、依赖或产物未冻结 | 否 |
| `DRAFTED` | 已有 PRD/设计草案，但未通过完整规划 Gate | 否 |
| `READY_TO_CONFIRM` | 任务边界、REQ 覆盖、依赖、验收、产物需求均已冻结，可请求用户确认 | 规划阶段终态 |
| `USER_CONFIRMED` | 用户已确认该任务属于当前创建范围 | 否 |
| `CREATED` | 已通过 `task.py create` 创建真实目录并回填账本 | 否 |
| `ARTIFACTS_WRITTEN` | 已写入所有声明需要的规划产物 | 否 |
| `GATED_PASS` | Artifact Gate 通过 | 创建后终态 |
| `BLOCKED` | 有明确阻塞原因、恢复条件和责任方 | 终态 |
| `OUT_OF_SCOPE` | 已进入 Backlog，当前 MVP 不创建 | 终态 |

规划阶段进入用户确认的条件：

```text
forall task in Subtask Planning Ledger:
  task.status in [READY_TO_CONFIRM, BLOCKED, OUT_OF_SCOPE]
```

创建后建议开发的条件：

```text
forall in-scope created task:
  task.status in [GATED_PASS, BLOCKED, OUT_OF_SCOPE]
```

## 批次规则

- P0/P1 是优先级，不是完整规划完成状态。
- B01/B02/B03 是规划批次，不是范围裁剪。
- 每个 MVP `TASK` 子任务必须有批次。
- 若只完成 B01 或 P0/P1，输出 `BATCH_INCOMPLETE` 并继续规划下一批。
- 后续批次可以暂不创建真实目录，但不能没有 Task ID、REQ 覆盖、依赖、复杂度、PRD 草案和产物需求。
