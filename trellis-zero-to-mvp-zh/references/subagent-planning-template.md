# 批次化子代理规划模板

当候选子任务超过单批上限、业务域超过 3 个、完整 PRD 草案超过 5 个，或用户要求多 agent 规划时使用。主代理先完成 Requirement Ledger Gate 和 Contract Gate，再分派只读规划包。

## 角色

| 角色 | 职责 | 输出 |
| --- | --- | --- |
| `requirement-ledger-agent` | 独立复核源需求抽取完整性 | 缺失 REQ/AC、矩阵覆盖问题、Backlog 漏项 |
| `contract-audit-agent` | 复核 Project Contract Lock 与 Contract Snapshot | 冲突项、forbidden_tokens、证据路径缺失 |
| `batch-split-agent` | 按 Small Model Mode 拆分全部 MVP 子任务并分配批次 | Task rows、B01/B02/...、依赖层级、可并行组 |
| `child-prd-agent` | 为一个批次起草最多 5 个高质量子任务 PRD 草案 | PRD 草案要点、验收、契约引用、实现计划定位 |
| `design-surface-agent` | 判断每个子任务涉及的设计面并规划必填章节 | 任务影响面矩阵、design/implement 必填章节、缺失风险 |
| `artifact-planner-agent` | 为中/高复杂任务补设计、实现、JSONL 计划 | `design.md` / `implement.md` / JSONL 需求和原因 |
| `gate-check-agent` | 独立做 Gate 失败扫描 | 失败码、证据行、修复动作 |

## 主代理规则

- 主代理负责唯一 Subtask Planning Ledger，不允许子代理各自维护最终状态。
- 子代理输出只是草案；用户确认、`task.py create`、真实目录映射、文件写入和 Artifact Gate 由主代理负责。
- 子代理冲突不得平均折中；按本地上下文优先级裁决，无法裁决则标记 `BLOCKED`。
- `gate-check-agent` 的失败项不得静默忽略，必须修复或阻塞。
- 若当前平台没有子代理能力，主代理按下列 Agent Packet 顺序串行模拟，并输出 `agent_mode: unavailable_fallback_serial`。

## Agent Packet 输入

每个子代理只接收任务所需切片：

- Project Contract Lock 与 Contract Snapshot。
- 与本批或本角色相关的 Full Requirement Matrix 行。
- 与本批或本角色相关的 MVP Coverage Matrix 行。
- Existing Implementation Baseline 中相关证据。
- Trellis 工作流上下文。
- 本批允许规划的 Task ID 范围、依赖边界、禁止越界的业务域。
- 输出格式要求和 Gate 名称。

不要把预期答案、主代理怀疑的错误或修复方案泄漏给 gate-check-agent。它应独立发现问题。

## 通用子代理提示词

```text
你是 Trellis MVP 批次规划子代理。只做只读规划，不创建 task，不写文件，不改 REQ/AC 编号。

输入包括 Project Contract Lock、Contract Snapshot、需求矩阵切片、MVP 覆盖矩阵切片、已有实现基线、Trellis 工作流上下文和本批 Task ID 范围。

你的任务：
1. 检查输入是否遵守 Project Contract Lock。
2. 按 Small Model Mode 把任务拆到可由能力有限执行模型独立完成。
3. 为每个任务输出 PRD 草案要点、复杂度、依赖、解锁项、规划产物需求。
4. 判断每个任务的设计面影响，输出“任务影响面矩阵”，并列出 `design.md` / `implement.md` 必填章节。
5. 标记本批内部可并行组和不能并行的原因。
6. 找出应阻塞、应移出本批或必须回到主代理裁决的冲突。

输出必须包含：
- agent_role
- batch_id
- task_rows
- prd_draft_notes
- design_surface_matrix
- planning_artifact_needs
- dependency_and_parallel_groups
- contract_risks
- blocking_questions
- gate_result: PASS/FAIL
- failure_codes

禁止：
- 创建 Trellis task
- 修改文件
- 发明新的命名、路径、API、命令、包/模块、路由、表名或权限模型
- 改变 REQ/AC 语义
- 把本批之外的需求顺手纳入本批
```

## 子代理输出表

| Task ID | REQ IDs | 标题 | 批次 | 依赖 | 可并行组 | 复杂度 | PRD 草案状态 | 产物需求 | 风险 | 失败码 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T01 | REQ-001 | <标题> | B01 | none | G01 | 低/中/高 | draft/blocked | prd/design/implement/jsonl | <风险> | <none/code> |

## 合并输出

主代理合并后必须更新：

- Subtask Planning Ledger。
- Batch Completion Rollup。
- 规划产物矩阵。
- Gate 输出。
- 下一批动作。
