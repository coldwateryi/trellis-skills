# Trellis 0.6+ 规划产物模板

用于中/高复杂度子任务，或当 `.trellis/workflow.md`、邻近任务显示项目期望 `design.md`、`implement.md`、`implement.jsonl`、`check.jsonl` 时使用。

这些产物用于把推理左移。目标是让能力有限的执行模型沿着窄路径实现，而不是在编码阶段重新设计。

## 复杂度门槛

| 复杂度 | 必要产物 |
| --- | --- |
| 低 | 如果任务有可直接照抄的参考实现和可执行检查，`prd.md` 即可。 |
| 中 | 增加 `design.md` 和 `implement.md`；如果实现/检查前必须预加载稳定 specs 或调研上下文，再增加 JSONL 上下文清单。 |
| 高 | 先拆分任务。确实无法拆分时，增加 `design.md`、`implement.md`、`implement.jsonl`、`check.jsonl`，并定死每个决策、预加载稳定上下文。 |

## 通用规则

- `design.md` 和 `implement.md` 必须继承父任务 Project Contract Lock；命名、路径、API、命令、包/模块、路由、表名和权限模型不得与 PRD 不一致。
- Small Model Mode 下，复杂任务优先拆小；保留为中/高复杂度时，必须把设计和执行步骤定死到无需执行模型重新推理。
- 外部配置和第三方 key 必须写成 `FIXED`、`BASELINE`、`BLOCKED` 或 `OUT_OF_SCOPE`，禁止保留 `YOUR_KEY`、`API_KEY_HERE`、`待用户提供`。
- 同一产物中不得混用两套命名体系或路径体系。
- `design.md`、`implement.md` 必须复制本任务 Contract Snapshot；命中 forbidden token 时 Artifact Gate 必须 FAIL。
- 详细文件计划、有序步骤、自检命令、失败恢复和评审门默认写在 `implement.md`，不要在 PRD 中重复维护两份互相漂移的实现计划。
- JSONL 模式必须显式写入规划产物矩阵：`required` 表示 sub-agent 或稳定上下文预加载必需；`optional` 表示可删除或说明不需要；`inline` 表示 Codex inline 模式下不作为规划就绪门槛。
- 外部配置为 `BLOCKED` 时，不得写“先用占位符/执行期替换/待用户提供”；依赖真实配置的能力必须阻塞或列入范围外。
- 子任务 PRD 的“任务影响面矩阵”中任一影响面为“是”时，`design.md` 和 `implement.md` 必须包含对应章节。章节模板见 `design-surface-template.md`。

## `design.md`

```markdown
# Design: <任务标题>

## Project Contract Reference

| 契约项 | 本任务采用值 | 父任务证据路径 |
| --- | --- | --- |
| <契约项> | <具体路径/命名/API/命令/模块或 not-applicable> | <path> |

## 需求覆盖

| 需求 ID | 设计元素 | 说明 |
| --- | --- | --- |
| REQ-001 | <组件/契约/流程> | <此设计如何满足需求> |

## Design Surface Coverage

从子任务 PRD 的“任务影响面矩阵”复制涉及项。任一 `状态` 为 `missing` 时，Artifact Gate 必须 FAIL。

| 影响面 | PRD 声明 | design.md 章节 | implement.md 章节 | 状态 |
| --- | --- | --- | --- | --- |
| 数据库/数据模型 | 是/否 | Database Schema Design | Database Migration Plan | ready/missing/not-applicable |
| API 接口 | 是/否 | API Contract Design | API Implementation Plan | ready/missing/not-applicable |
| UI/项目风格 | 是/否 | UI Design and Style Contract | UI Implementation Plan | ready/missing/not-applicable |

涉及的设计面按 `design-surface-template.md` 补齐对应章节；未涉及的设计面不要生成空壳章节。

## 上下文清单

| 类型 | 路径 | 为什么重要 | 编辑前必须读取 |
| --- | --- | --- | --- |
| 现有范例 | <path> | <要照抄的模式> | 是 |
| 契约 | <path> | <API/schema/state 契约> | 是 |
| 测试 | <path> | <期望的测试风格> | 是 |

## 决策表

| 决策点 | 选定方案 | 排除方案 | 原因 | 影响文件 |
| --- | --- | --- | --- | --- |
| <命名/分支/schema/API 选择> | <确切选择> | <不用哪些方案> | <原因> | <paths> |

## 外部配置与未决项

| 配置/外部依赖 | 状态 | 规划期处理 | 执行期行为 |
| --- | --- | --- | --- |
| <地图 key / 外部接口 / 硬件协议等> | FIXED/BASELINE/BLOCKED/OUT_OF_SCOPE | <配置名、证据或排除原因> | <确切行为> |

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

## 编排-计算分离

把本次改动按"编排层 / 计算层"分开，并各自指向文件清单里的落点。执行阶段照此放置，不另选文件。

| 层 | 本次涉及的元素 | 落点(文件清单路径) |
| --- | --- | --- |
| 编排层(主流程/控制流/分支编排/workflow) | <编排元素> | <path> |
| 计算层(纯算法/纯函数/数据变换) | <可独立测试的计算逻辑> | <path> |

- 编排层只负责调度；可独立测试的计算逻辑下沉到计算层，便于按 AC 单测。
- 模块 ≤2 个、调用线性时本表可精简，但仍要写明落点。

## 挂载点清单

判据："删了它，本特性在用户/系统视角就消失。" 一般 3-5 条。这是给执行阶段的**接线清单**、给评审阶段的**核对项**——防止"写了实现却没接线"。

| 挂载点 | 类型 | 位置 | 接线动作 |
| --- | --- | --- | --- |
| <名称> | 路由注册/配置项/事件订阅/DI 绑定/菜单入口 | <path> | <注册或绑定的确切动作> |

## 非目标

- <明确排除的行为>
```

## `implement.md`

```markdown
# Implementation Plan: <任务标题>

## Project Contract Reference

| 契约项 | profile 字段 | 本任务采用值 | 父任务证据路径 |
| --- | --- | --- | --- |
| <契约项> | <profile field> | <具体路径/命名/API/命令/模块或 not-applicable> | <path> |

## 文件计划

| 步骤 | 文件 | 操作 | 精确位置 | 验证方式 |
| --- | --- | --- | --- | --- |
| 1 | <path> | <new/modify> | <method/section> | <command or assertion> |

## Design Surface Implementation Plans

从 `design.md#Design Surface Coverage` 复制所有涉及项，逐项写落地计划。章节标题必须与子任务 PRD 的“实现计划位置”一致，便于机械 Gate 扫描。

| 影响面 | implement.md 章节 | 状态 |
| --- | --- | --- |
| <影响面> | <对应章节标题> | ready/missing |

示例章节：

```markdown
## API Implementation Plan

| 步骤 | 文件 | 操作 | 精确位置 | 验证方式 |
| --- | --- | --- | --- | --- |
| 1 | <path> | new/modify | <method/section> | <command/assertion> |
```

## 结构健康度预检

规划阶段对每个要改的文件做机械阈值预检（强模型在规划期定死，执行阶段只机械执行结论）：

| 目标文件/目录 | 当前行数/文件数 | 阈值 | 是否需微重构 | 微重构方案(只搬不改行为) |
| --- | --- | --- | --- | --- |
| <path> | <n> | 文件 400 行 / 目录 15 文件 | 是/否 | <搬什么→搬到哪→怎么验证不变> |

- 命中阈值 → 在「有序步骤」第 0 步放一个"只搬不改行为"的微重构（编译器全程绿灯），独立验证后再做主体。
- **执行阶段不得自行判断是否重构**；只照本表结论执行。改函数签名/返回结构/调用语义等超出"只搬不改"的，写入非目标，留后续处理。

## 有序步骤

0. <若结构健康度预检命中：先做"只搬不改行为"的微重构，编译/测试全绿后再继续；未命中则跳过>
1. <复制或创建确切文件/章节>
2. <做确切替换或编辑>
3. <加入确切校验或分支>
4. <运行确切检查>

## 修改边界

- 允许修改的文件：
- 禁止修改的文件：
- 禁止引入的依赖：
- 禁止改变的契约：命名、路径、API、命令、包/模块、路由、表名、权限模型必须与 PRD 一致。
- 禁止保留的占位：`YOUR_KEY`、`API_KEY_HERE`、`TBD`、`待定`、`视情况`。

## 失败恢复

- 如果检查 `<command>` 因 `<symptom>` 失败，检查 `<file>` 并修复 `<specific issue>`。
```

## `implement.jsonl`

每行是一个实现前需要预加载的稳定上下文项。用于 specs、调研说明、API 文档、设计参考等任务期间不太会变化的上下文。不要列出正在编辑的源代码文件，也不要在这里编码步骤动作。

创建任务后必须删除 `_example` 种子行。若本任务不需要 JSONL，删除该文件或在规划产物矩阵中标记 `NOT_NEEDED_WITH_REASON`；不得保留空壳种子。

JSONL 模式：

- `required`：sub-agent-dispatch 模式，或实现/检查前确实需要稳定上下文预加载；seed-only 必须 FAIL。
- `optional`：任务可以通过 PRD/design/implement 完成上下文约束；JSONL 可删除或说明不需要，seed-only 不阻塞 Artifact Gate，但必须在矩阵中解释。
- `inline`：Codex `dispatch_mode: inline`；JSONL 不作为规划就绪门槛，创建任务后的 seed JSONL 应删除或标记 `NOT_NEEDED_WITH_REASON`，Gate 使用 `--jsonl-mode inline`。

```jsonl
{"file":"<path-to-stable-spec-or-doc>","reason":"<为什么实现前需要此上下文>"}
{"file":"<path-to-stable-reference>","reason":"<它固定了哪个决策、API、schema 或领域规则>"}
```

## `check.jsonl`

每行是一个检查/验证前需要预加载的稳定上下文项。命令和预期结果写在 `implement.md` 或 `prd.md`，不要放在 JSONL manifest 里。

```jsonl
{"file":"<path-to-acceptance-spec-or-test-plan>","reason":"<为什么验证前需要此上下文>"}
{"file":"<path-to-regression-or-risk-note>","reason":"<它保护的行为或风险>"}
```
