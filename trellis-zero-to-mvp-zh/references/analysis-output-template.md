# 从 0 到 MVP 分析输出模板

此模板用于只读分析阶段。在此阶段不要创建任务，也不要编写代码。

## 项目目标摘要

用 5-10 条说明需求文档最终要求交付什么。

## Existing Implementation Baseline（已有实现基线）

当仓库已经包含手工实现功能，或 Trellis/spec 是在开发开始后才初始化时，使用本节。

| 已有能力 | 证据类型 | 代码证据 | 测试证据 | 覆盖的需求 ID | 基线依赖名 | 备注 |
| --- | --- | --- | --- | --- | --- | --- |
| <capability> | code/test/spec/task | <精确路径> | <精确路径或 "none"> | REQ-001 | existing:<capability-or-file> | <复用约束> |

规则：

- 源需求文档是需求真相来源；现有代码和 `.trellis/spec/` 是证据，不替代需求。
- 如果需求已是 `DONE`，不要为该范围创建实现任务。
- 如果需求是 `UNTESTED`，除非实现证据薄弱，否则只创建测试补齐任务。
- 如果需求是 `PARTIAL`，只为缺失行为创建补缺任务。
- 如果需求是 `MISSING`，创建新实现任务。

## Trellis 工作流上下文

| 项目 | 值 | 备注 |
| --- | --- | --- |
| Trellis 版本/来源 | <来自 `.trellis/.version` 或 "unknown"> | <beta/current/legacy 信号> |
| 工作流契约 | <`.trellis/workflow.md` 路径或 "not present"> | <发现的产物要求> |
| 配置 | <`.trellis/config.yaml` 路径或 "not present"> | <相关选项> |
| Developer identity | <来自 `.trellis/.developer` 或 "not initialized"> | <缺失时要做什么> |
| Spec 新鲜度 | <fresh/stale/missing/unknown> | <已读 spec 文件或需要的刷新任务> |

## 执行模型画像

| 项目 | 值 |
| --- | --- |
| 预期执行模型 | <如 qwen3.6 35b 本地模型 / GPT-5.5 / Opus 4.8> |
| 规划深度 | <standard / small-model-safe / high-risk> |
| 任务粒度规则 | <此画像下任务必须拆到多小> |

## Requirements Traceability Matrix

| ID | 需求 | 当前状态 | 相关代码 | 现有测试 | 缺口 | 任务动作 | 建议任务 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| REQ-001 |  | MISSING |  |  |  | new-task |  |

允许的状态：

- `DONE`：已完整实现且有测试。
- `PARTIAL`：部分实现。
- `MISSING`：未实现。
- `UNTESTED`：已实现但缺少足够测试。
- `UNCLEAR`：需求不够清楚，无法实现。

任务动作：

- `none`：需求已是 `DONE`，只作为基线证据。
- `test-only`：需求是 `UNTESTED`，只创建测试补齐任务，不重做实现。
- `gap-task`：需求是 `PARTIAL`，只实现缺失行为。
- `new-task`：需求是 `MISSING`，创建新实现任务。
- `clarify`：需求是 `UNCLEAR`，实现前先提出阻塞问题或创建澄清任务。

## 模块依赖图

| 模块 | 职责 | 依赖模块 | 被哪些模块依赖 | 风险 |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## 任务拆分

| Task ID | 标题 | 目标 | 类型 | 需求 ID | 来源状态 | 依赖 | 基线依赖 | 优先级 | 复杂度 | 规划产物 | 是否可并行 | 验收标准 | 可能涉及区域 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T0 |  |  | docs | REQ-001 | MISSING | none | none | P0 | 低 | prd.md | no |  |  |

允许的任务类型：`backend`、`frontend`、`fullstack`、`docs`、`test`、`infra`。

复杂度（按执行模型能力评估，决定拆分粒度和 PRD 详细度）：

- `低`：标准 CRUD、配置、有现成范例可照抄。弱模型可独立完成。
- `中`：含少量业务校验或跨表逻辑，需要明确实现步骤。弱模型在详细 PRD 下可完成。
- `高`：复杂事务、并发、跨模块一致性、需要大量隐性领域知识。弱模型难以独立完成，应进一步拆碎到"低/中"，或在 PRD 里把每步定死到无需推理。

优先级规则：

- `P0`：阻塞其他模块或核心正确性。
- `P1`：核心业务闭环。
- `P2`：体验、报表、通知、增强能力。
- `P3`：非必要优化。

排序规则：

1. 数据结构、API 契约和配置优先。
2. 阻塞其他模块的任务优先于依赖它们的任务。
3. 高风险和未知多的任务提前验证。
4. UI 打磨、文档和体验增强靠后。
5. 不要把互相依赖的任务标记为可并行。

已有部分实现规则：

1. 不要为 `DONE` 需求创建子任务。
2. 只有测试缺失时，才为 `UNTESTED` 需求创建 `test` 任务。
3. 为 `PARTIAL` 需求创建补缺子任务；目标必须命名缺失行为，而不是已实现行为。
4. 任务依赖已有能力时，在 `基线依赖` 中写明，例如 `existing:src/auth/session.ts`。
5. 不要把已有基线依赖伪装成新的 Trellis task。

## MVP 推荐开发顺序

1. `<task-id>`：`<原因>`
2. `<task-id>`：`<原因>`

## 父任务 PRD 草案

使用 `parent-prd-template.md` 起草父任务 PRD。

## 子任务 PRD 草案

为每个子任务使用 `child-prd-template.md` 起草 PRD。

对每个中/高复杂度子任务，同时使用 `planning-artifacts-template.md` 起草必要的 Trellis 0.6 beta 规划产物。

## 确认请求

最后输出：

```text
请确认这个任务拆分和 MVP 边界。如果确认，我将创建 Trellis 父任务、子任务和 PRD，不编写应用代码。
```
