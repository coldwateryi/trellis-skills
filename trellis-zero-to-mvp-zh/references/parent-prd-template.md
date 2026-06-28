# 父任务 PRD 模板

```markdown
# <项目标题>

## 目标

交付源需求文档描述的项目。父任务负责整体范围、需求 ID、依赖计划和最终验收定义；子任务负责实现可独立验收的能力。

## 源需求文档

- 路径: <需求文档路径>
- 版本: <版本或日期>
- 负责人: <业务或技术负责人>

## Project Contract Lock

本节锁定项目本地实现契约。所有子任务 PRD、`design.md`、`implement.md` 必须遵守；如需改变，先更新本节和相关 README/spec。

| 项 | 值 |
| --- | --- |
| Project Contract Profile | <java-ruoyi-crud/typescript-cli-framework/frontend-spa/python-service/custom> |
| Profile 选择证据 | <README/spec/code paths> |

| 契约项 | profile 字段 | adopted_value | 证据路径 | forbidden_tokens |
| --- | --- | --- | --- | --- |
| <契约项> | <profile field> | <具体路径/命名/API/命令/模块或 not-applicable> | <path> | <tokens or none> |

## 完整平台范围与当前 MVP 边界

| 范围块 | 完整平台要求 | 当前 MVP 处理 | 差异/风险 |
| --- | --- | --- | --- |
| <PC/IOC/数据对接/小程序/报表等> | <源需求范围> | <TASK/MERGED/OUT_OF_SCOPE/BLOCKED> | <风险> |

## 需求 ID

| ID | 需求摘要 | 覆盖状态 | 子任务/基线/范围外说明 | 覆盖 AC | 实现状态 |
| --- | --- | --- | --- | --- | --- |
| REQ-001 | <摘要> | TASK | <task slug> | AC-001 | PLANNED |

允许的覆盖状态：`TASK`、`MERGED`、`BASELINE`、`OUT_OF_SCOPE`、`BLOCKED`。
允许的实现状态：`PLANNED`、`IN_PROGRESS`、`DONE`、`PARTIAL`、`BLOCKED`、`VERIFIED`。

如果需求已经由现有代码满足，`子任务` 写 `none`，并在 Existing Baseline Summary 中引用证据。
如果需求被合并，`子任务/基线/范围外说明` 写目标子任务，并在"任务合并/拆分记录"中说明原因和覆盖 AC。

## 需求覆盖汇总

| 类别 | 数量 | 说明 |
| --- | --- | --- |
| 原始功能点总数 | <n> | 源需求文档抽取的可验收功能点数量 |
| 当前 MVP 覆盖 | <n> | `TASK` + `MERGED` + `BASELINE` |
| 独立子任务覆盖 | <n> | `TASK` |
| 合并覆盖 | <n> | `MERGED` |
| 已有基线覆盖 | <n> | `BASELINE` |
| 当前范围外 | <n> | `OUT_OF_SCOPE` |
| 阻塞 | <n> | `BLOCKED` |

## 任务合并/拆分记录

| 需求 ID | 源功能点 | 处理方式 | 目标子任务/基线/范围外 | 覆盖 AC | 原因 | 风险 |
| --- | --- | --- | --- | --- | --- | --- |
| REQ-001 | <功能点> | MERGED | <task slug> | AC-001 | <合并原因> | <遗漏/耦合风险> |

## Backlog / 二期范围

所有 `OUT_OF_SCOPE` 需求必须列入本表，不能从需求追踪中消失。

| 需求 ID | 源功能点 | 排除原因 | 推荐阶段 | 恢复进入范围的前置条件 | 依赖的 MVP 任务 |
| --- | --- | --- | --- | --- | --- |
| REQ-999 | <功能点> | <原因> | MVP+1/V2/BLOCKED | <条件> | <task ids> |

## Existing Baseline Summary（已有基线摘要）

当开发早于 Trellis 规划时使用本节：

| 需求 ID | 已有能力 | 证据 | 剩余工作 |
| --- | --- | --- | --- |
| REQ-001 | <capability 或 "none"> | <code/test/spec paths> | <none/test gap/behavior gap> |

## 子任务规划进度

本表必须覆盖所有当前 MVP `TASK` 子任务。存在非终态时，父任务不得声明所有子任务规划完成。

| Task ID | 需求 ID | 批次 | 可并行组 | 规划状态 | 真实目录 | Gate | 阻塞/下一步 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T01 | REQ-001 | B01 | G01 | READY_TO_CONFIRM/GATED_PASS/BLOCKED/OUT_OF_SCOPE | <task.py 输出目录或 pending> | PASS/FAIL/N/A | <说明> |

## 批次完成汇总

| 批次 | 包含 Task ID | 目标 | 状态 | 剩余非终态 | 下一步 |
| --- | --- | --- | --- | --- | --- |
| B01 | T01,T02 | <目标> | planned/ready/gated/blocked | <n> | <说明> |

## 任务依赖图

```text
T0 需求追踪
  -> T1 基础能力
    -> T2 核心能力
      -> T3 业务闭环
  -> T-final 验证
```

## 交付策略

1. 完成需求追踪和技术计划。
2. 实现基础能力和契约。
3. 实现 MVP 核心业务闭环。
4. 只有依赖完成后才添加次级能力。
5. 最后完成验证和验收报告。

## 完成定义

- [ ] 每个需求 ID 都有状态。
- [ ] 所有当前 MVP `TASK` 子任务已完成、阻塞或明确移出范围；不能只要求 P0/P1。
- [ ] 每个需求 ID 都有测试映射，或记录无法自动化验证的原因。
- [ ] lint、typecheck 和必要测试通过。
- [ ] 最终验收报告使用 PASS / FAIL / PARTIAL / NOT TESTED / BLOCKED。
- [ ] 行为变化时更新文档和运行说明。

## 范围外

- <MVP 明确排除项>

## Artifact Gate

创建任务后必须通过本节检查，`FAIL` 时不得声明任务树可执行。检查结果必须来自 `scripts/trellis_zero_gate.py` 或等价机械扫描，不得由模型手填。

```bash
python <skill-dir>/scripts/trellis_zero_gate.py \
  --tasks .trellis/tasks \
  --parent-task-json <parent-task-dir>/task.json \
  --parent-prd <parent-task-dir>/prd.md \
  --jsonl-mode <required|optional|inline>
```

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| scanned_tasks | <n> | <扫描任务数> |
| jsonl_mode | <required/optional/inline> | <来自 Codex dispatch_mode 或规划产物矩阵> |
| placeholder_hits | <0/n> | `{Entity}`、`<path>`、`TBD`、`待定` 等 |
| angle_placeholder_hits | <0/n> | 通用 `<...>` 占位 |
| jsonl_seed_hits | <0/n> | `_example` JSONL |
| contract_mismatch_hits | <0/n> | 与 Project Contract Lock 不一致 |
| forbidden_token_hits | <0/n> | Contract Snapshot 禁止词 |
| coverage_count_mismatch_hits | <0/n> | 需求覆盖统计不一致 |
| high_complexity_missing_artifacts | <0/n> | 高复杂度缺 `design.md` / `implement.md` |
| missing_declared_artifacts | <0/n> | 声明需要但真实目录缺失 |
| design_surface_prd_without_matrix | <0/n> | 子任务 PRD 缺任务影响面矩阵 |
| design_surface_missing_hits | <0/n> | 任务影响面矩阵声明涉及但缺少对应设计/实现章节 |
| declared_gate_mismatch_hits | <0/n> | 父 PRD 声明值与机械扫描不一致 |
| external_config_hits | <0/n> | `YOUR_KEY`、未决 key/外部配置 |
| result | PASS/FAIL | <FAIL 时列修复动作或阻塞原因> |

## 备注

- 严格依赖写在子任务的 `Dependencies` 部分。
- 已有能力可以在子任务中作为基线依赖引用。
- 父子任务链接用于组织范围，不替代依赖文档。
- 子任务的命名、路径、API、命令、包/模块、路由、表名和权限模型必须与 Project Contract Lock 一致。
```
