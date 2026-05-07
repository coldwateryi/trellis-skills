---
name: trellis-mvp-to-delivery-zh
description: |
  根据源需求文档审计已有 MVP，并规划 Trellis 完整交付。用于 Codex 被要求在 MVP 后继续、补齐剩余需求、执行差距审计、创建 Requirements Traceability Matrix、分类 DONE/PARTIAL/MISSING/UNTESTED/UNCLEAR 条目、规划补缺 Trellis 任务、设计自动化测试覆盖、分类发现的 bug，或在交付前执行最终验收的场景。
---

# Trellis 从 MVP 到完整交付

## 概览

通过回到源需求文档、审计证据、创建补缺任务和规划最终验收，将已有 MVP 推进到完整交付。第一轮始终是只读审计。

## 约束

- MVP 之后不要直接“继续开发”，必须先做需求审计。
- 没有实现证据和测试证据时，不要把需求标记为 `DONE`。
- 在用户确认差距审计前，不要创建交付任务。
- 不要把无关缺口混进同一个任务。
- 不要把所有测试都推到最终兜底任务。每个功能任务必须包含自己的基础测试。
- 最终验证任务只能在功能补缺任务规划完成后创建。
- 如果 bug 不阻塞当前需求验收，先分类，再创建或建议独立 bug task。

## 工作流

### 1. 发现证据

定位并读取：

- 源需求文档。
- 已有 MVP 代码和测试。
- 现有 `.trellis/tasks/`，尤其是已完成或进行中的任务。
- 已有需求 ID、追踪矩阵和验收备注。
- 受影响 package 的相关 `.trellis/spec/` 索引。

先使用本地证据再提问。只问无法从需求文档或仓库判断的阻塞性问题。

### 2. 执行只读差距审计

读取 `references/gap-audit-template.md`，输出：

- Requirements Traceability Matrix。
- MVP 完成度摘要。
- 阻塞性问题。
- 按依赖排序的任务计划。
- 推荐优先级。
- 自动化测试要求。

只能使用这些状态：`DONE`、`PARTIAL`、`MISSING`、`UNTESTED`、`UNCLEAR`。

### 3. 确认交付计划

在创建或修改 Trellis task 前请求一次确认：

```text
请确认这个差距审计和交付任务计划。如果确认，我将创建 Trellis tasks 和 PRD，但暂不实现功能。
```

如果用户调整优先级或范围，先更新矩阵和任务计划，再创建任务。

### 4. 创建补缺任务

用户确认后：

1. 创建或复用一个完整需求和验证的父任务。
2. 为每组高度相关的缺口创建一个子任务。
3. 使用 `references/delivery-task-prd-template.md` 写入子任务 PRD。
4. 如果基础契约、业务行为、UI、测试和最终验证的依赖不同，就分开任务。
5. 不要开始编码。

### 5. 规划测试闭环

当用户要求规划或补齐测试覆盖时，读取 `references/test-coverage-matrix-template.md`。将每个 `REQ-*` 或 `AC-*` 映射到至少一个 unit、integration、e2e、smoke、regression 或 manual verification 条目。

### 6. 执行最终验收

所有功能任务完成后，读取 `references/final-acceptance-template.md`。最终验收阶段不要新增功能，除非阻塞性 bug 导致无法验收。

### 7. 分类 Bug

验证发现 bug 时，读取 `references/bug-classification-rules.md`。判断是在当前任务修复、创建独立 bug task，还是记录风险后延期。

## 参考文件

- `references/gap-audit-template.md` - 第一次只读 MVP 审计时读取。
- `references/delivery-task-prd-template.md` - 创建补缺任务 PRD 前读取。
- `references/test-coverage-matrix-template.md` - 规划或补齐测试覆盖时读取。
- `references/final-acceptance-template.md` - 最终交付验收时读取。
- `references/bug-classification-rules.md` - 验证发现缺陷时读取。
