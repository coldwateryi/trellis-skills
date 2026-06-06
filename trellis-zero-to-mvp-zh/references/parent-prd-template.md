# 父任务 PRD 模板

```markdown
# <项目标题>

## 目标

交付源需求文档描述的项目。父任务负责整体范围、需求 ID、依赖计划和最终验收定义；子任务负责实现可独立验收的能力。

## 源需求文档

- 路径: <需求文档路径>
- 版本: <版本或日期>
- 负责人: <业务或技术负责人>

## 需求 ID

| ID | 需求摘要 | 子任务 | 状态 |
| --- | --- | --- | --- |
| REQ-001 | <摘要> | <task slug> | PLANNED |

允许的状态：`PLANNED`、`IN_PROGRESS`、`DONE`、`PARTIAL`、`BLOCKED`、`VERIFIED`。

如果需求已经由现有代码满足，`子任务` 写 `none`，并在 Existing Baseline Summary 中引用证据。

## Existing Baseline Summary（已有基线摘要）

当开发早于 Trellis 规划时使用本节：

| 需求 ID | 已有能力 | 证据 | 剩余工作 |
| --- | --- | --- | --- |
| REQ-001 | <capability 或 "none"> | <code/test/spec paths> | <none/test gap/behavior gap> |

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
- [ ] 所有 MVP P0/P1 需求完成。
- [ ] 每个需求 ID 都有测试映射，或记录无法自动化验证的原因。
- [ ] lint、typecheck 和必要测试通过。
- [ ] 最终验收报告使用 PASS / FAIL / PARTIAL / NOT TESTED / BLOCKED。
- [ ] 行为变化时更新文档和运行说明。

## 范围外

- <MVP 明确排除项>

## 备注

- 严格依赖写在子任务的 `Dependencies` 部分。
- 已有能力可以在子任务中作为基线依赖引用。
- 父子任务链接用于组织范围，不替代依赖文档。
```
