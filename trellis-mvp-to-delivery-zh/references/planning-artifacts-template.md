# Trellis 0.6 Beta 规划产物模板

用于中/高复杂度补缺任务，或当 `.trellis/workflow.md`、邻近任务显示项目期望 `design.md`、`implement.md`、`implement.jsonl`、`check.jsonl` 时使用。

这些产物用于把推理左移。目标是在保持 MVP 行为的前提下，把补缺变更收窄到能力有限的执行模型也能跟随。

## 复杂度门槛

| 复杂度 | 必要产物 |
| --- | --- |
| 低 | 如果任务有可直接照抄的 MVP 范例和可执行检查，`prd.md` 即可。 |
| 中 | 增加 `design.md` 和 `implement.md`；如果实现/检查前必须预加载稳定 specs、调研上下文或回归说明，再增加 JSONL 上下文清单。 |
| 高 | 先拆分任务。确实无法拆分时，增加 `design.md`、`implement.md`、`implement.jsonl`、`check.jsonl`，并定死每个决策、预加载稳定实现/检查上下文。 |

## `design.md`

```markdown
# Design: <任务标题>

## 需求覆盖

| 需求 ID | 当前状态 | 设计元素 | 本任务后的预期状态 |
| --- | --- | --- | --- |
| REQ-001 | PARTIAL | <组件/契约/流程> | DONE |

## MVP 兼容性契约

| 已有行为 | 证据 | 必须保留 | 回归检查 |
| --- | --- | --- | --- |
| <behavior> | <path/test> | 是 | <command/test> |

## 上下文清单

| 类型 | 路径 | 为什么重要 | 编辑前必须读取 |
| --- | --- | --- | --- |
| MVP 代码 | <path> | <要保留或扩展的行为> | 是 |
| 现有测试 | <path> | <回归测试风格> | 是 |
| Spec | <path> | <契约来源> | 是 |

## 决策表

| 决策点 | 选定方案 | 排除方案 | 原因 | 影响文件 |
| --- | --- | --- | --- | --- |
| <bug 分支/schema/API 选择> | <确切选择> | <不用哪些方案> | <原因> | <paths> |

## 契约

### API / Interface

- Endpoint/function/class:
- Inputs:
- Outputs:
- Error cases:

### Data / State

| 字段/状态 | 类型 | 允许值 | 默认值 | 校验规则 |
| --- | --- | --- | --- | --- |
| <name> | <type> | <values> | <default> | <rules> |

## 非目标

- <明确排除的行为>
```

## `implement.md`

```markdown
# Implementation Plan: <任务标题>

## 文件计划

| 步骤 | 文件 | 操作 | 精确位置 | 验证方式 |
| --- | --- | --- | --- | --- |
| 1 | <path> | <new/modify> | <method/section> | <command or assertion> |

## 有序步骤

1. <复制或创建确切文件/章节>
2. <做确切替换或编辑>
3. <加入确切校验或 bug 修复分支>
4. <运行确切检查>

## 修改边界

- 允许修改的文件：
- 禁止修改的文件：
- 不能改变的已有 MVP 行为：
- 禁止引入的依赖：

## 失败恢复

- 如果检查 `<command>` 因 `<symptom>` 失败，检查 `<file>` 并修复 `<specific issue>`。
```

## `implement.jsonl`

每行是一个实现前需要预加载的稳定上下文项。用于 specs、调研说明、API 文档、设计参考、迁移说明等任务期间不太会变化的上下文。不要列出正在编辑的源代码文件，也不要在这里编码步骤动作。

```jsonl
{"file":"<path-to-stable-spec-or-doc>","reason":"<为什么实现前需要此上下文>"}
{"file":"<path-to-stable-reference>","reason":"<它固定了哪个决策、API、schema、迁移或领域规则>"}
```

## `check.jsonl`

每行是一个检查/验证前需要预加载的稳定上下文项。命令和预期结果写在 `implement.md` 或 `prd.md`，不要放在 JSONL manifest 里。

```jsonl
{"file":"<path-to-acceptance-spec-or-test-plan>","reason":"<为什么验证前需要此上下文>"}
{"file":"<path-to-regression-or-risk-note>","reason":"<它保护的 MVP 行为或风险>"}
```
