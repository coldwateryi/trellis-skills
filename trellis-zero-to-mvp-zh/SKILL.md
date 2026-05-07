---
name: trellis-zero-to-mvp-zh
description: |
  从完整需求文档创建 Trellis MVP 任务树。用于 Codex 收到产品说明、需求文档、PRD、从 0 到 MVP 的新项目需求或大型能力建设请求时，先做只读分析，分配稳定 REQ/AC 编号，生成需求追踪矩阵，将范围拆成 Trellis 父任务和子任务，起草 PRD，并在编码前规划按依赖排序的 MVP 交付路径。
---

# Trellis 从 0 到 MVP

## 概览

将原始需求文档转化为 MVP 规模的 Trellis 交付计划。产出物是经用户确认的父任务和可独立验收的子任务，而不是应用代码。

## 约束

- 不要编写业务代码。
- 在用户确认只读分析前，不要创建 Trellis task。
- 不要按文件拆任务。按可独立验收的业务能力或技术能力拆任务。
- 在任务规划前先分配稳定需求编号：`REQ-001`、`REQ-002`、`AC-001`。
- 每个子任务必须包含需求 ID、验收标准、测试要求、依赖、解锁项、范围外内容和技术备注。
- Trellis 的父子任务关系只表达任务结构。严格依赖必须写入每个子任务的 `prd.md`。
- 如果 `task.py create` 因 developer identity 未初始化而失败，停止并提示用户运行 `python ./.trellis/scripts/init_developer.py <name>`，或让用户提供明确的 assignee。

## 工作流

### 1. 发现输入

定位并读取：

- 源需求文档。
- README 或项目概览文件。
- 如果仓库不是空项目，读取现有代码结构和测试。
- 与项目相关的 `.trellis/tasks/` 和 `.trellis/spec/` 内容。

先检查仓库再提问。只问无法从本地上下文判断的阻塞性问题。

### 2. 执行只读分析

读取 `references/analysis-output-template.md`，输出：

- 项目目标摘要。
- Requirements Traceability Matrix。
- 模块依赖图。
- 按能力拆分的任务清单。
- 按依赖排序的 MVP 推荐开发顺序。
- 父任务 PRD 草案。
- 子任务 PRD 草案。

需求追踪矩阵只能使用这些状态：`DONE`、`PARTIAL`、`MISSING`、`UNTESTED`、`UNCLEAR`。

### 3. 确认范围

展示分析结果，并在创建文件前请求一次确认：

```text
请确认这个任务拆分和 MVP 边界。如果确认，我将创建 Trellis 父任务、子任务和 PRD，不编写应用代码。
```

如果用户调整范围，先更新分析结果。不要基于过期假设创建任务。

### 4. 创建 Trellis 任务树

用户确认后：

1. 为整体项目创建一个父任务。
2. 使用 `--parent <parent-task-dir>` 创建子任务。
3. 使用 `references/parent-prd-template.md` 写入父任务 `prd.md`。
4. 使用 `references/child-prd-template.md` 写入每个子任务 `prd.md`。
5. 精确保留需求 ID 和依赖关系。
6. 不要开始实现。

使用：

```bash
python ./.trellis/scripts/task.py create "<parent title>" --slug <parent-slug>
python ./.trellis/scripts/task.py create "<child title>" --slug <child-slug> --parent "<parent-task-dir>"
```

### 5. 汇报下一步

输出：

- 任务树。
- 推荐执行顺序。
- 被阻塞任务。
- 可并行任务。
- 第一个建议开始的任务及原因。

## 参考文件

- `references/analysis-output-template.md` - 生成初始分析前读取。
- `references/parent-prd-template.md` - 起草或写入父任务 PRD 时读取。
- `references/child-prd-template.md` - 起草或写入子任务 PRD 时读取。
- `references/task-creation-checklist.md` - 创建任务树前读取。
