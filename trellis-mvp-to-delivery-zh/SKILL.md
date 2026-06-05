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
- 任务粒度按执行模型能力分级：若执行阶段可能用能力有限的本地模型（如离线 qwen），把任务拆得更碎并标注复杂度。
- 交付任务 PRD 是给执行模型照着做的执行规格。规划阶段必须把所有 `<...>` 占位符替换为具体值（具体文件路径、可照抄的现有范例、有序实现步骤、可机器校验的验收断言、自检命令），禁止把推理判断（含 bug 修复走哪条分支）留给执行阶段。
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

### 2. 执行只读差距审计（增强版 - 自我评审循环）

循环执行以下步骤，直到满足小模型执行标准：

#### 第 N 轮审计

**2.1 生成差距审计输出**

读取 `references/gap-audit-template.md`，输出：

- Requirements Traceability Matrix。
- MVP 完成度摘要。
- 阻塞性问题。
- 按依赖排序的任务计划。
- 推荐优先级。
- 自动化测试要求。

只能使用这些状态：`DONE`、`PARTIAL`、`MISSING`、`UNTESTED`、`UNCLEAR`。

**2.2 自我评审**

读取 `references/self-review-checklist.md`，对照检查清单逐项检查审计输出质量。

使用 `references/self-review-report-template.md` 生成评审报告，包含：
- 整体评分（8个维度）
- 检查清单通过情况
- 发现的问题清单（位置、问题描述、影响、改进建议）
- MVP 兼容性检查
- 统计信息
- 本轮结论

**2.3 判断是否达标**

- ✅ 所有检查项通过 → 跳转到步骤3（确认交付计划）
- ✅ 连续2轮无新问题发现 → 自动通过，跳转到步骤3
- ❌ 有未通过检查项 → 执行步骤2.4（针对性改进）
- ⚠️ 超过5轮仍有问题 → 提示用户选择：
  - 选项A：使用更强模型重新审计
  - 选项B：人工介入审查当前审计
  - 选项C：接受当前版本（风险自负）

**2.4 针对性改进**

根据评审报告中的问题清单，进行针对性改进：
- 只修改标记为问题的部分，不重新审计整个 MVP
- 保持已通过部分不变
- 特别关注 MVP 兼容性（不破坏已有行为）
- 完成改进后，回到步骤2.1，进入第 N+1 轮评审

**评审循环原则**：
- 逐轮收敛，不全量重做
- 问题定位要精确（到具体的 REQ-xxx、Task ID、PRD 章节）
- 改进要针对性（修复问题，不引入新问题）
- 强调 MVP 兼容性（所有补缺任务不能破坏 MVP 行为）

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
- `references/self-review-checklist.md` - 每轮审计后进行自我评审时读取。
- `references/self-review-report-template.md` - 生成评审报告时读取。
- `references/delivery-task-prd-template.md` - 创建补缺任务 PRD 前读取。
- `references/test-coverage-matrix-template.md` - 规划或补齐测试覆盖时读取。
- `references/final-acceptance-template.md` - 最终交付验收时读取。
- `references/bug-classification-rules.md` - 验证发现缺陷时读取。
