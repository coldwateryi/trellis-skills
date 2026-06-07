---
name: trellis-zero-to-mvp-zh
description: |
  从完整需求文档创建 Trellis MVP 任务树。用于 Codex 收到产品说明、需求文档、PRD、从 0 到 MVP 的新项目需求、大型能力建设请求，或已经手工实现了一部分功能的项目时，先做只读分析，分配稳定 REQ/AC 编号，生成需求追踪矩阵，识别已有实现证据，只把剩余 MVP 范围拆成 Trellis 父任务和子任务，起草 PRD，并在继续编码前规划按依赖排序的 MVP 交付路径。
---

# Trellis 从 0 到 MVP

## 概览

将原始需求文档转化为 MVP 规模的 Trellis 交付计划。输入可以是空项目，也可以是用户已经在 Trellis 初始化前手工实现了一部分需求的项目。产出物是经用户确认的父任务和面向剩余 MVP 范围的可独立验收子任务，而不是应用代码。

## 约束

- 不要编写业务代码。
- 在用户确认只读分析前，不要创建 Trellis task。
- 不要按文件拆任务。按可独立验收的业务能力或技术能力拆任务。
- 任务粒度按执行模型能力分级：若执行阶段可能用能力有限的本地模型（如离线 qwen），把任务拆得更碎，一个子任务对应一个实体的一套 CRUD 或一个接口，并标注复杂度。
- 在任务规划前先分配稳定需求编号：`REQ-001`、`REQ-002`、`AC-001`。
- 每个子任务必须包含需求 ID、验收标准、测试要求、依赖、解锁项、范围外内容和技术备注。
- PRD 是给执行模型照着做的执行规格，不是意图描述。规划阶段必须把所有 `<...>` 占位符替换为具体值（具体文件路径、可照抄的现有范例、有序实现步骤、可机器校验的验收断言、自检命令），禁止把推理判断留给执行阶段。
- 凡是需要推理的判断（用哪个注解、走哪条分支、命名、表结构、照抄哪个范例）必须在规划阶段定死。无法定死的点列入范围外或拆成独立任务，不要交给执行模型自由发挥。
- 如果现有代码已经满足某条需求，不要为已满足范围创建实现任务。把已有证据作为基线依赖。
- 对已有部分实现的项目，任务创建规则固定为：`DONE` -> 不建任务；`UNTESTED` -> 只建测试补齐任务；`PARTIAL` -> 只为缺失行为创建补缺任务；`MISSING` -> 创建新实现任务；`UNCLEAR` -> 阻塞问题或澄清任务。
- 对 Trellis 0.6 beta 项目，如果存在 `.trellis/workflow.md`，必须把它当作当前项目的本地工作流契约。不要在项目已声明 `design.md`、`implement.md`、`implement.jsonl` 或 `check.jsonl` 产物时仍按旧的纯 task/PRD 工作流假设执行。
- Trellis 的父子任务关系只表达任务结构。严格依赖必须写入每个子任务的 `prd.md`。
- 如果 `task.py create` 因 developer identity 未初始化而失败，停止并提示用户运行 `trellis init -u <name>`（加上项目使用的平台参数，例如 `--codex`），或让用户提供明确的 assignee。只有 Trellis CLI 不可用时，才把 `python ./.trellis/scripts/init_developer.py <name>` 作为旧版兜底方式。

## 工作流

### 1. 发现输入

定位并读取：

- 源需求文档。
- README 或项目概览文件。
- 如果仓库不是空项目，读取现有代码结构和测试。
- 与项目相关的 `.trellis/tasks/` 和 `.trellis/spec/` 内容。
- Trellis 0.6 beta 工作流元数据：如存在，读取 `.trellis/workflow.md`、`.trellis/config.yaml`、`.trellis/.version`、`.trellis/.developer` 和 `.trellis/workspace/`。

如果仓库不是空项目，或源需求中提到的功能已经有部分实现迹象，先生成 Existing Implementation Baseline（已有实现基线），再拆任务。原始需求文档是需求真相来源；`.trellis/spec/` 和代码只作为实现证据和上下文。

起草任务前，检查 `.trellis/spec/` 是否足够新且具体，能支撑实现。如果 spec 缺失、过于泛化或明显过期，先增加 spec 刷新/bootstrap 任务或阻塞说明，再规划代码量大的任务。

先检查仓库再提问。只问无法从本地上下文判断的阻塞性问题。

### 2. 执行只读分析（增强版 - 自我评审循环）

循环执行以下步骤，直到满足小模型执行标准：

#### 第 N 轮分析

**2.1 生成分析输出**

读取 `references/analysis-output-template.md`，输出：

- 项目目标摘要。
- 如果仓库包含手工实现功能，输出 Existing Implementation Baseline。
- Requirements Traceability Matrix。
- 模块依赖图。
- 按能力拆分的任务清单。
- 按依赖排序的 MVP 推荐开发顺序。
- 父任务 PRD 草案。
- 子任务 PRD 草案。
- 对中/高复杂度子任务，读取 `references/planning-artifacts-template.md` 起草左移设计、实现计划和上下文清单产物：当项目工作流支持时，包含 `design.md`、`implement.md`、`implement.jsonl` 和 `check.jsonl`。

需求追踪矩阵只能使用这些状态：`DONE`、`PARTIAL`、`MISSING`、`UNTESTED`、`UNCLEAR`。

任何需求标记为 `DONE`、`PARTIAL` 或 `UNTESTED` 时，必须包含代码/测试证据，并确保任务拆分只覆盖剩余工作。没有 Trellis task slug 的已有能力，可在依赖字段中写成 `existing:<capability-or-file>`。

**2.2 自我评审**

读取 `references/self-review-checklist.md`，对照检查清单逐项检查分析输出质量。

使用 `references/self-review-report-template.md` 生成评审报告，包含：
- 整体评分（5个维度）
- 检查清单通过情况
- 发现的问题清单（位置、问题描述、影响、改进建议）
- 统计信息
- 本轮结论

**2.3 判断是否达标**

- ✅ 所有检查项通过 → 跳转到步骤3（确认范围）
- ✅ 连续2轮无新问题发现 → 自动通过，跳转到步骤3
- ❌ 有未通过检查项 → 执行步骤2.4（针对性改进）
- ⚠️ 超过5轮仍有问题 → 提示用户选择：
  - 选项A：使用更强模型重新分析
  - 选项B：人工介入审查当前分析
  - 选项C：接受当前版本（风险自负）

**2.4 针对性改进**

根据评审报告中的问题清单，进行针对性改进：
- 只修改标记为问题的部分，不重新分析整个需求文档
- 保持已通过部分不变
- 完成改进后，回到步骤2.1，进入第 N+1 轮评审

**评审循环原则**：
- 逐轮收敛，不全量重做
- 问题定位要精确（到具体的 REQ-xxx、Task ID、PRD 章节）
- 改进要针对性（修复问题，不引入新问题）

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
5. 对中/高复杂度子任务，如果 `.trellis/workflow.md` 或现有任务显示项目期望这些产物，写入或起草 `design.md`、`implement.md`、`implement.jsonl` 和 `check.jsonl`。写入前必须先读取已有产物，禁止盲目覆盖。
6. 精确保留需求 ID 和依赖关系。
7. 不要开始实现。

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

## 落地阶段衔接（任务创建后）

本技能止于创建任务树，不写代码。进入"需求落地"时，对每个子任务按依赖顺序使用执行期技能形成闭环（尤其执行模型为 qwen3.6 35b 这类小模型时）：

1. **`trellis-implement-tdd-zh`** —— 对子任务每条 AC 跑红→绿→提交的 TDD 机械循环。
2. **`trellis-debug-systematic-zh`** —— 测试该绿不绿或自检失败时，用刚性脚本定位修复。
3. **`trellis-review-twostage-zh`** —— 完成前做规范符合(可小模型) + 代码质量(强模型)双阶段评审。

角色分层模型分配：规划用强模型、实现用小模型、评审 Stage 2 用强模型（Trellis 可按 agent 配 `model`）。

## 参考文件

- `references/analysis-output-template.md` - 生成初始分析前读取。
- `references/self-review-checklist.md` - 每轮分析后进行自我评审时读取。
- `references/self-review-report-template.md` - 生成评审报告时读取。
- `references/planning-artifacts-template.md` - 为中/高复杂度任务起草 Trellis 0.6 beta 的设计、实现和上下文清单产物时读取。
- `references/parent-prd-template.md` - 起草或写入父任务 PRD 时读取。
- `references/child-prd-template.md` - 起草或写入子任务 PRD 时读取。
- `references/task-creation-checklist.md` - 创建任务树前读取。
