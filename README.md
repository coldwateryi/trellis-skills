# Trellis 需求交付技能集

本仓库为 Codex CLI、Claude Code 以及其他支持 skill 的 CLI 工具提供一套 Trellis 工作流技能，覆盖从原始需求文档到完整交付的全流程——**分析 → 规划 → 追踪 → 审计 → 补缺 → 验收**。

## 快速开始

在 Trellis 项目根目录运行安装脚本，选择中文或英文 skill：

```bash
curl -fsSL https://raw.githubusercontent.com/coldwateryi/trellis-skills/main/scripts/install-trellis-skills.sh | bash
```

如果你还没有 MVP，从需求文档开始：

```text
需求文档在 docs/requirements.md。
请使用 trellis-zero-to-mvp-zh 进行只读分析，输出 MVP 任务计划，先不要写代码。
```

如果 MVP 已经完成，进入完整交付 loop：

```text
MVP 已完成。请使用 trellis-mvp-to-delivery-zh 以 L1 模式执行首次 full audit，输出完整 Requirements Gap Matrix，并初始化 .trellis/delivery-state.md。
```

## 技能概览

| 技能 | 语言 | 用途 |
| --- | --- | --- |
| `trellis-zero-to-mvp` | EN | 从零开始：将需求文档转化为 MVP 任务树 |
| `trellis-mvp-to-delivery` | EN | 从 MVP 到交付：差距审计、补缺规划、最终验收 |
| `trellis-zero-to-mvp-zh` | ZH | 同上（中文版） |
| `trellis-mvp-to-delivery-zh` | ZH | 同上（中文版） |
| `trellis-implement-tdd` | EN | 执行期：用严格 TDD 红绿循环逐条落地验收标准（小模型友好） |
| `trellis-debug-systematic` | EN | 执行期：刚性 4 步调试脚本——复现→定位→假设验证→最小修复 |
| `trellis-review-twostage` | EN | 执行期：规范符合(小模型)+代码质量(强模型)双阶段评审门 |
| `trellis-implement-tdd-zh` | ZH | 同上（中文版） |
| `trellis-debug-systematic-zh` | ZH | 同上（中文版） |
| `trellis-review-twostage-zh` | ZH | 同上（中文版） |

## 由浅到深的使用路径

先把这套技能理解成一条交付流水线，而不是一组彼此独立的提示词：

```text
源需求文档
  └─ trellis-zero-to-mvp-zh：只读分析 → MVP 任务树
       └─ trellis-implement-tdd-zh / debug-systematic-zh / review-twostage-zh：实现 MVP
            └─ trellis-mvp-to-delivery-zh：L1 full audit → L2 批次补缺 → delta audit → final acceptance
```

### 先选哪个 skill

| 你现在的状态 | 应使用的 skill | 本轮产物 |
| --- | --- | --- |
| 只有需求文档，还没形成 Trellis 任务树 | `trellis-zero-to-mvp-zh` | Requirements Traceability Matrix、MVP 边界、父/子任务 PRD |
| 已经有 MVP，要对比完整需求 | `trellis-mvp-to-delivery-zh` | 完整 Requirements Gap Matrix、交付状态、第一批补缺建议 |
| 已经有 Trellis 子任务，要开始写代码 | `trellis-implement-tdd-zh` | 按 AC 红绿循环落地代码和测试 |
| 测试该绿不绿或自检失败 | `trellis-debug-systematic-zh` | 稳定复现、单一假设、最小修复 |
| 子任务自检全绿，要过门 | `trellis-review-twostage-zh` | Stage 1 规范符合 + Stage 2 代码质量评审 |

### 路径 A：从完整需求开始做 MVP

适用于新项目、重构项目或已有需求文档但尚未形成 Trellis 任务树的场景。

```text
需求文档在 docs/requirements.md。

请使用 trellis-zero-to-mvp-zh 进行只读分析：
- 为每条源需求分配稳定 REQ ID
- 输出 Requirements Traceability Matrix
- 明确 MVP 边界和暂不纳入范围
- 按依赖顺序拆分 Trellis 父任务和子任务
- 先不要写代码，等我确认后再创建任务树
```

`trellis-zero-to-mvp-zh` 会在规划阶段运行自我评审循环，重点检查占位符、文件路径、Implementation Steps、验收断言和复杂任务拆分。确认分析结果后，再让它创建 Trellis 任务树。

如果项目已经手工实现了一部分功能，可以改用下面的提示词：

```text
需求文档在 docs/requirements.md，项目中已经手工实现了一部分功能，并且中途运行过 trellis init。

请使用 trellis-zero-to-mvp-zh 基于现有代码、.trellis/spec/ 和需求文档，只规划剩余 MVP 功能任务。
已实现且有证据的需求标记为 DONE；已实现但缺测试的标记为 UNTESTED；只为 PARTIAL/MISSING 创建后续任务。
```

### 路径 B：MVP 已完成，进入可持续 Delivery Loop

适用于已经跑完 MVP、现在要从“能用”推进到“完整交付”的场景。`trellis-mvp-to-delivery-zh` 不是一次性审计工具，而是外层交付状态机：先完整对比需求和 MVP，再按有边界的批次推进。

#### 第 1 轮：L1 full audit

首次运行仍然必须完整对比 MVP 与实际需求，并输出完整差异矩阵。它会初始化 `.trellis/delivery-state.md` 和 `.trellis/delivery-run-log.jsonl`，作为后续 loop 的持久记忆。

```text
MVP 已完成。请使用 trellis-mvp-to-delivery-zh 以 L1 模式执行首次 full audit：
- 对比 docs/requirements.md 与当前 MVP
- 输出完整 Requirements Gap Matrix，覆盖每条源需求
- 标记 DONE / PARTIAL / MISSING / UNTESTED / UNCLEAR
- 初始化 .trellis/delivery-state.md
- 初始化 .trellis/delivery-run-log.jsonl
- 只给出第一批补缺建议，不创建实现任务
```

#### 第 2-N 轮：L2 batch progress

确认差距矩阵后，每轮只推进一个批次。默认每批最多 3 个补缺任务，最多 1 个高风险任务；代码变更任务必须带 worktree、verifier 和 `trellis-review-twostage-zh` 门。

```text
请使用 trellis-mvp-to-delivery-zh 以 L2 模式推进当前 delivery batch：
- 读取 .trellis/delivery-state.md
- 只处理 current_batch
- 每个代码变更任务都要求 worktree + verifier + trellis-review-twostage-zh
- 不直接实现功能，只创建或更新本批次 Trellis tasks 和 PRD
- 更新 .trellis/delivery-state.md
- 追加 .trellis/delivery-run-log.jsonl
```

#### 后续审计：delta audit 或 early-exit

当已经存在 delivery state，且源需求没有变化时，后续不应反复 full audit。只检查 `last_audited_commit` 之后与 open gaps 相关的代码、测试和 Trellis task 变化；如果没有相关变化，直接 early-exit。

```text
请使用 trellis-mvp-to-delivery-zh 执行 delta audit：
- 从 .trellis/delivery-state.md 读取 last_audited_commit
- 从 last_audited_commit 到当前 HEAD 检查与 open gaps 相关的代码、测试和 task 变化
- 更新 Requirements Gap Matrix 中受影响的 REQ
- 如果没有相关变化，early-exit 并只追加 .trellis/delivery-run-log.jsonl
```

#### 收尾轮：final acceptance

所有 P0/P1 缺口完成或被人工明确延期后，再进入最终验收。最终验收不新增功能，只分类阻塞 bug。

```text
所有 P0/P1 补缺任务已完成或已明确延期。

请使用 trellis-mvp-to-delivery-zh 执行 final acceptance：
- 读取 final-acceptance-template.md
- 验证 Requirements Gap Matrix 中所有交付范围内 REQ
- 汇总自动化测试、回归测试和人工验收证据
- 不新增功能，只分类阻塞 bug
```

典型项目一般 3-6 个外层 loop 收敛：首次 full audit → P0/foundation batch → P1/core behavior batch → regression/final acceptance。超过 6 轮、同一 REQ 连续 2 轮无进展、verifier 两次失败或 review 出现 critical 时，应暂停并人工确认范围或基线。

## 执行期技能详细使用说明

规划技能（`zero-to-mvp` / `mvp-to-delivery`）创建任务树后，使用以下**执行期技能**按依赖顺序实施每个子任务，形成**规划→实现→调试→评审**的完整闭环。

### 执行期技能概览

| 技能 | 触发时机 | 核心价值 | 小模型适配 |
| --- | --- | --- | --- |
| `trellis-implement-tdd` | 子任务进入实现阶段 | 把"实现需求"变成"让测试变绿"的机械循环，每步有客观信号 | 窄路径+客观信号，小模型只需追"让断言变绿" |
| `trellis-debug-systematic` | 测试该绿不绿、自检失败 | 刚性 4 步脚本（复现→定位→假设验证→最小修复），防小模型乱改 | 铁律"一次一处、改完必重跑、禁止猜" |
| `trellis-review-twostage` | 实现自检全绿后 | 规范符合(小模型)+代码质量(强模型)双阶段门，critical 阻断 | 角色分层：Stage 1 小模型、Stage 2 强模型 |

### 典型工作流：从任务到完成

假设你已用 `trellis-zero-to-mvp-zh` 创建了任务树，现在要实现第一个子任务：

#### 1. 启动 TDD 循环

```
现在开始实现子任务 .trellis/tasks/feature-user-auth/01-implement-login/

请使用 trellis-implement-tdd-zh 进行 TDD 落地。
```

**技能会做什么**：
- 读取子任务的 `prd.md`（验收标准、文件清单、决策表、自检命令）
- 如有 `design.md`，读取编排-计算分离、挂载点清单
- 为每条验收标准（AC-001, AC-002...）执行红绿循环：
  1. **RED**：写一个失败的测试（照抄 `prd.md` 参考实现的测试范例）
  2. **看红**：运行测试，必须看到失败（没失败 = 测试没覆盖行为，回去修测试）
  3. **GREEN**：写刚好让它变绿的最小代码，落点按文件清单+设计分层
  4. **看绿**：再次运行测试，看到通过
  5. **自检**：运行 `prd.md` 全部自检命令，确认无回归
  6. **记录**：标记 AC 为 done，暂存（不 commit），进入下一条 AC

**关键约束**：
- 没有失败测试，不写实现代码
- 一次只让一条 AC 变绿
- 不动文件清单/禁止事项之外的文件
- 不执行 `git commit`（Trellis 实现执行体禁止 commit）

#### 2. 遇到红灯时调试

如果某条 AC 的测试该绿不绿，或自检命令失败：

```
AC-003 的测试该绿却一直红，错误信息是 "AssertionError: Expected 200, got 401"

请使用 trellis-debug-systematic-zh 定位并修复。
```

**技能会做什么**：
1. **固定失败信号**：贴出错误原文，确认稳定复现
2. **定位**（三招按代价从低到高）：
   - 读栈：直接看报错堆栈指向的文件与行
   - 二分注释：对可疑代码段二分注释，看失败是否消失
   - 加一行日志：打印关键变量实际值，对比期望值
3. **单一假设**：写一句话假设（具体到变量/分支），先验证真假再修
4. **最小修复**：只改已验证的根因那一处，改完立刻重跑原失败命令
5. **防御性回归**：问"这个 bug 还能从别处再发生吗？"→ 能则补回归测试

**铁律**：
- 一次只改一处
- 改完必重跑原失败命令
- 禁止猜（定位只用三招）
- 超 3 轮仍红 → 停止，升级给强模型

#### 3. 完成后评审

所有 AC 变绿、自检全绿后：

```
子任务实现自检全绿，现在交给评审。

请使用 trellis-review-twostage-zh 评审此次改动。
```

**技能会做什么**：

**Stage 1 · 规范符合**（可小模型，机械核对）：
- 每条 AC 有对应测试且为绿？ ⛔ 缺失/红灯 = critical
- 改动文件都在文件清单内？ ⛔ 改了清单外文件 = critical
- 违反禁止事项（新建已有基类、引入未列依赖）？ ⛔ critical
- 决策表选择被遵守（注解/命名/schema/分支）？
- 挂载点逐项接线（路由/配置/订阅/DI）？ ⛔ 漏接 = critical

**Stage 2 · 代码质量**（强模型执行）：
- 编排-计算分离：编排逻辑与计算逻辑没混在一处？
- 结构健康度：没往偏胖文件继续堆？没制造"什么都装的筐"？
- 简化/复用：没重复实现已有能力？没过度抽象（YAGNI）？
- 正确性：边界/错误路径真的被处理（不止 happy path）？ ⛔ 漏处理 = critical
- 规范符合：命名/分层/错误语义符合 `.trellis/spec/`？

**裁决**：
- 有 **critical** → 阻断，打回 `trellis-implement-tdd-zh`，只修标注项，修后重审
- 仅 major/minor → 放行（major 建议本轮修，minor 记入备注）
- 全通过 → 交回编排会话推进任务状态

### 角色分层模型分配（小模型友好）

| 阶段 | 推荐模型 | 原因 |
| --- | --- | --- |
| 规划（zero-to-mvp / mvp-to-delivery） | 强模型（Opus 4.8 / GPT-5.5） | 需判断：拆分、边界、设计决策 |
| 实现（trellis-implement-tdd） | 小模型（qwen3.6 35b） | 机械执行：照 PRD 让测试变绿 |
| 调试（trellis-debug-systematic） | 小模型 → 超 3 轮升强模型 | 前期机械定位；复杂根因升级 |
| 评审 Stage 1 | 小模型 | 机械核对规范符合 |
| 评审 Stage 2 | 强模型 | 需判断：设计纪律、代码质量 |

**小模型能胜任实现/调试/评审 Stage 1 的原因**：
- 判断已左移到规划期（命名/分支/schema/落点/重构方案全由强模型定死）
- 执行期只面对"让断言变绿""一次改一处""逐项核对清单"这类窄路径机械活
- 每步有客观信号（测试红/绿、命令退出码），不靠小模型主观判断

### 调用示例（组合使用）

**场景：团队用 qwen3.6 35b 本地模型落地任务**

```
# 规划阶段用强模型（Opus 4.8）
[Opus] 请使用 trellis-zero-to-mvp-zh 规划 docs/requirements.md

# 实现阶段切换到本地 qwen
[qwen3.6 35b] 请使用 trellis-implement-tdd-zh 实现 .trellis/tasks/.../01-implement-login/

# 遇到红灯，仍用 qwen 调试（前 3 轮）
[qwen3.6 35b] AC-003 该绿不绿，请用 trellis-debug-systematic-zh 定位修复

# 如 3 轮未绿，升级强模型
[Opus] 这个调试已 3 轮仍红（附失败信号 + 已排除假设），请用 trellis-debug-systematic-zh 接手

# 实现完成，评审 Stage 1 用 qwen
[qwen3.6 35b] 请用 trellis-review-twostage-zh Stage 1 核对规范符合

# 评审 Stage 2 用强模型
[Opus] 请用 trellis-review-twostage-zh Stage 2 评审代码质量
```

**关键价值**：
- 算力受限成员（只有本地 qwen）也能按统一质量贡献代码
- TDD 测试 + 双阶段评审 = 团队信任小模型/他人产出的客观依据
- 挂载点清单 = 跨人交接时的集成验证单
- 角色分层模型分配 = 成本最优（小模型干机械活、强模型做判断）

### 与规划技能的衔接

两个规划技能的 SKILL.md 已包含「落地阶段衔接」节，在创建任务树后会提示使用执行期技能。典型流程：

1. **`trellis-zero-to-mvp-zh`** 输出任务树 + 按依赖排序的执行计划
2. 对第一个可执行子任务（依赖已满足）：
   - 调用 **`trellis-implement-tdd-zh`** 逐 AC 红绿循环
   - 遇红灯触发 **`trellis-debug-systematic-zh`**
   - 自检全绿后触发 **`trellis-review-twostage-zh`**
3. 评审通过 → 推进任务状态 → 下一个子任务
4. 所有子任务完成 → **`trellis-mvp-to-delivery-zh`** 最终验收 + 架构档案回写

### 尽量全自动执行模式

“尽量全自动”指的是：AI 自动推进到下一个安全门，而不是跳过确认门无人值守。适合任务树较大、希望少手动点名 skill 的场景。

默认自动继续的范围：

- 读取需求、代码、测试、`.trellis/` 和相关 spec。
- 选择下一个依赖已满足的子任务或 delivery batch。
- 对实现任务自动执行 `trellis-implement-tdd-zh` → `trellis-debug-systematic-zh` → `trellis-review-twostage-zh`。
- 自检失败时自动调试，单任务最多 3 轮假设/修复。
- 评审通过后推进到下一个 ready task 或下一轮 delta audit。
- 追加 `.trellis/delivery-run-log.jsonl` 并更新 `.trellis/delivery-state.md`。

必须停下询问的安全门：

- 首次只读分析后，创建或修改 Trellis 任务树前。
- `mvp-to-delivery` 首次 L1 full audit 后，确认差距矩阵和第一批补缺范围前。
- 需要改动 File Manifest 外的文件，或需求/schema/auth/payment/security/infrastructure 决策不清晰。
- verifier 连续失败 2 次、调试超过 3 轮仍未变绿、review 出现 critical。
- 当前小模型走到 `trellis-review-twostage-zh` Stage 2，或需要强模型判断设计质量。
- 任何 destructive git 操作、commit、push、tag、release；除非用户在当前请求中明确授权。
- 外层 delivery loop 超过 6 轮，或同一 `REQ-*` 连续 2 轮无进展。

#### 样例 A：从需求到 MVP，尽量全自动落地

```text
请尽量全自动执行 Trellis 需求落地流程，自动推进到下一个安全门。

目标：
- 需求文档在 docs/requirements.md
- 先创建 MVP 任务树
- 然后按依赖顺序落地所有 MVP 子任务
- MVP 完成后运行 trellis-mvp-to-delivery-zh 的 L1 full audit

执行规则：
1. 使用 trellis-zero-to-mvp-zh 先做只读分析，输出 Requirements Traceability Matrix、MVP 边界、任务拆分和 PRD 草案。
2. 创建或修改 Trellis 任务树前停下，等待我确认。
3. 我确认后，按依赖顺序自动选择下一个 ready 子任务。
4. 每个子任务使用 trellis-implement-tdd-zh 逐 AC 红绿循环。
5. 测试该绿不绿或自检失败时，自动使用 trellis-debug-systematic-zh；超过 3 轮仍失败时停下。
6. 子任务自检全绿后，自动使用 trellis-review-twostage-zh；Stage 2 需要强模型时停下提示。
7. 评审通过后推进任务状态，继续下一个子任务。
8. 所有 MVP 子任务完成后，使用 trellis-mvp-to-delivery-zh 执行 L1 full audit，输出完整 Requirements Gap Matrix，并初始化 .trellis/delivery-state.md 和 .trellis/delivery-run-log.jsonl。

除上述安全门外，请不要每一步都问我。
```

#### 样例 B：已有 MVP，尽量全自动跑 Delivery Loop

```text
MVP 已完成。请尽量全自动运行 trellis-mvp-to-delivery-zh 交付 loop，自动推进到下一个安全门。

目标：
- 对比 docs/requirements.md 和当前 MVP
- 完成首次 L1 full audit
- 按批次补齐 P0/P1 缺口
- 每批结束后执行 delta audit
- 条件满足后执行 final acceptance

执行规则：
1. 如果 .trellis/delivery-state.md 不存在，先执行 L1 full audit，输出完整 Requirements Gap Matrix，并初始化 delivery state/run log。
2. L1 审计后停下，等待我确认差距矩阵、延期项和第一批补缺范围。
3. 我确认后，进入 L2 batch progress；每轮只处理 current_batch，最多 3 个 gap tasks，最多 1 个高风险任务。
4. 需要写代码的任务必须使用隔离 worktree，并要求 verifier + trellis-review-twostage-zh。
5. 对批次内每个任务自动执行 trellis-implement-tdd-zh → trellis-debug-systematic-zh → trellis-review-twostage-zh。
6. 批次完成后自动执行 delta audit，更新 Requirements Gap Matrix、.trellis/delivery-state.md 和 .trellis/delivery-run-log.jsonl。
7. 如果没有相关变化，early-exit，只追加 run log。
8. 当所有 P0/P1 缺口 DONE 或被我明确延期后，执行 final acceptance；最终验收不新增功能，只分类阻塞 bug。

遇到 critical review、verifier 两次失败、同一 REQ 两轮无进展、需要改 File Manifest 外文件、或外层 loop 超过 6 轮时停下。
```

#### 样例 C：已有任务树，只自动跑一个子任务

```text
对子任务 .trellis/tasks/feature-user-auth/01-implement-login/ 执行尽量全自动闭环：

trellis-implement-tdd-zh（TDD 实现）→ trellis-debug-systematic-zh（遇红灯时）→ trellis-review-twostage-zh（评审）→ 推进状态。

只处理这个子任务，不扩大范围。遇到 critical review、调试超过 3 轮、需要改 File Manifest 外文件或需要强模型 Stage 2 判断时停下。
```

#### 小模型专用自动执行提示词

```text
任务树已创建。现在由我（qwen3.6 35b 小模型）负责实现和机械核对，遇到需要判断的环节时自动提示切换到强模型。

对每个子任务：
1. [小模型] 使用 trellis-implement-tdd-zh 进行 TDD 实现
2. [小模型] 遇红灯使用 trellis-debug-systematic-zh（超 3 轮提示升级强模型）
3. [小模型] trellis-review-twostage-zh Stage 1 规范符合核对
4. [提示切换强模型] trellis-review-twostage-zh Stage 2 代码质量评审
5. [小模型] 评审通过后推进任务状态

请按上述角色分工自动执行，到 Stage 2 评审时提示"请切换到强模型继续 Stage 2 评审"。
```

使用尽量全自动模式的价值：

- **减少手动调用**：一次提示覆盖规划、实现、调试、评审和下一轮审计。
- **流程标准化**：保证每个子任务都经过 TDD→调试→评审的完整质量门。
- **状态可恢复**：通过 `.trellis/delivery-state.md` 和 `.trellis/delivery-run-log.jsonl` 支持后续 delta audit。
- **边界清晰**：自动执行只发生在已确认范围内，遇到高风险判断或破坏性操作会停下。

## 需求状态说明

两个技能使用统一的需求状态标记：

| 状态 | 含义 |
| --- | --- |
| `DONE` | 已完整实现并通过测试 |
| `PARTIAL` | 部分实现 |
| `MISSING` | 尚未实现 |
| `UNTESTED` | 已实现但缺少充分测试 |
| `UNCLEAR` | 需求不够清晰，无法实施 |

## 安装与兼容性

脚本会优先检查当前目录是否存在 `.trellis/`。如果当前目录是已初始化的 Trellis 项目，默认安装到该项目的项目级 skill 目录；如果当前目录不是 Trellis 项目，会提示输入目标项目目录。若用户输入的目录仍未发现 `.trellis/`，脚本会询问是否改为安装到全局 skill 目录。

随后询问是否安装中文版 skill：选择是安装 5 个中文版 skill（`trellis-zero-to-mvp-zh`、`trellis-mvp-to-delivery-zh`、`trellis-implement-tdd-zh`、`trellis-debug-systematic-zh`、`trellis-review-twostage-zh`）；选择否安装 5 个英文版 skill（`trellis-zero-to-mvp`、`trellis-mvp-to-delivery`、`trellis-implement-tdd`、`trellis-debug-systematic`、`trellis-review-twostage`）。

项目级默认安装位置：

- `.agents/skills/`：Codex CLI / Trellis agent 兼容目录
- `.claude/skills/`：Claude Code 项目级 skill 自动发现目录

全局回退安装位置：

- `$CODEX_HOME/skills`，未设置 `CODEX_HOME` 时为 `~/.codex/skills`：Codex CLI 全局 skill 目录
- `~/.claude/skills`：Claude Code 用户级 skill 目录

如只想安装到单个平台目录，可设置 `TRELLIS_SKILLS_AGENT_TARGETS=codex` 或 `TRELLIS_SKILLS_AGENT_TARGETS=claude`。未设置时默认值为 `both`。

### macOS / Linux / Git Bash

```bash
curl -fsSL https://raw.githubusercontent.com/coldwateryi/trellis-skills/main/scripts/install-trellis-skills.sh | bash
```

仅安装 Codex / Trellis agent 目录：

```bash
curl -fsSL https://raw.githubusercontent.com/coldwateryi/trellis-skills/main/scripts/install-trellis-skills.sh | TRELLIS_SKILLS_AGENT_TARGETS=codex bash
```

仅安装 Claude Code 目录：

```bash
curl -fsSL https://raw.githubusercontent.com/coldwateryi/trellis-skills/main/scripts/install-trellis-skills.sh | TRELLIS_SKILLS_AGENT_TARGETS=claude bash
```

macOS 默认 zsh 也可以直接执行：

```bash
curl -fsSL https://raw.githubusercontent.com/coldwateryi/trellis-skills/main/scripts/install-trellis-skills.sh | zsh
```

本地脚本方式：

```bash
cd /path/to/trellis-skills/scripts
bash ./install-trellis-skills.sh
# 或
zsh ./install-trellis-skills.sh
```

### PowerShell

```powershell
irm https://raw.githubusercontent.com/coldwateryi/trellis-skills/main/scripts/install-trellis-skills.ps1 | iex
```

仅安装 Claude Code 目录：

```powershell
$env:TRELLIS_SKILLS_AGENT_TARGETS = "claude"
irm https://raw.githubusercontent.com/coldwateryi/trellis-skills/main/scripts/install-trellis-skills.ps1 | iex
```

本地脚本方式：

```powershell
cd C:\path\to\trellis-skills\scripts
.\install-trellis-skills.ps1
.\install-trellis-skills.ps1 -AgentTargets claude
```

脚本主要支持 `bash` 和 `zsh`。如果使用其他不兼容 shell（例如 `sh`/`dash`）执行，脚本会直接提示改用 `bash` 或 `zsh`。脚本会从当前终端读取交互输入，即使通过 `curl | bash` 或 `curl | zsh` 管道执行，也可以正常选择目标目录和语言。

如果在本仓库的 `scripts/` 目录直接执行脚本，脚本会先从 GitHub 更新父级 `trellis-skills` 目录的 `main` 分支源码，然后再按上述逻辑安装。更新使用 fast-forward 合并；如果本地有未提交改动或分支无法快进，脚本会停止，避免覆盖本地修改。

Claude Code 会从项目的 `.claude/skills/<skill-name>/SKILL.md` 自动发现项目级 skill，也会读取用户级 `~/.claude/skills/<skill-name>/SKILL.md`。`agents/openai.yaml` 是面向 Codex/OpenAI 兼容运行器的附加配置，Claude Code 可忽略该文件。

## 进阶机制

### 自我评审循环与设计左移

所有技能支持自我评审循环机制，并把复杂任务的设计、实现步骤和稳定上下文清单前置到规划阶段，确保输出满足小参数模型（如 qwen3.6 35b）的执行要求。

工作原理：

1. **分析**：生成初版需求追踪矩阵、任务拆分和 PRD
2. **自我评审**：对照 45-60 项检查清单逐项检查
3. **针对性改进**：只修复标记的问题，不全量重做
4. **循环收敛**：重复 2-3 轮直到所有检查通过
5. **用户确认**：达标后才创建任务树

核心优势：

- 小模型友好：消除占位符、提供具体路径和步骤
- 设计左移：对中/高复杂度任务补充 Context Manifest、Decision Table、`design.md`、`implement.md`、`implement.jsonl`、`check.jsonl`
- 质量保证：45-60 项精准检查，问题定位到具体行
- 成本可控：ROI > 5:1（规划多花 45k tokens，执行少花 200k tokens）

详见：[优化提案](doc/OPTIMIZATION_PROPOSAL.md) 和 [实施总结](doc/FINAL_SUMMARY.md)。

### Trellis 0.6 Beta 适配

本技能集仍兼容 Trellis 的核心任务结构（`.trellis/tasks/`、`.trellis/spec/`、`task.py create --parent`），同时增加对 0.6 beta 工作流的适配：

- 如存在 `.trellis/workflow.md`，优先把它作为项目本地工作流契约读取。
- 如存在 `.trellis/config.yaml`、`.trellis/.version`、`.trellis/.developer`、`.trellis/workspace/`，在规划前纳入上下文。
- 对依赖 `.trellis/spec/` 的任务先检查 spec 新鲜度；缺失、泛化或过期时，先规划 spec refresh/bootstrap。
- 对中/高复杂度任务，除 `prd.md` 外，按项目工作流补充 `design.md`、`implement.md`、`implement.jsonl`、`check.jsonl`。
- 首次初始化优先使用 `trellis init -u <name>`，并按项目需要添加平台参数；`init_developer.py` 只作为旧版兜底。

## 目录结构

```
trellis-skills/
├── trellis-zero-to-mvp/          # 规划技能：Zero → MVP（英文）
│   ├── SKILL.md                  # 技能定义与工作流
│   ├── agents/
│   │   └── openai.yaml           # OpenAI 兼容运行器配置
│   └── references/
│       ├── analysis-output-template.md   # 只读分析输出模板
│       ├── parent-prd-template.md        # 父任务 PRD 模板
│       ├── child-prd-template.md         # 子任务 PRD 模板
│       ├── planning-artifacts-template.md # 0.6 beta 设计/实现/上下文清单模板
│       ├── self-review-checklist.md      # 自我评审检查清单
│       ├── self-review-report-template.md # 自我评审报告模板
│       └── task-creation-checklist.md    # 任务创建检查清单
├── trellis-mvp-to-delivery/      # 规划技能：MVP → Delivery（英文）
│   ├── SKILL.md
│   ├── agents/
│   │   └── openai.yaml
│   └── references/
│       ├── gap-audit-template.md         # 差距审计模板
│       ├── delivery-loop-policy.md       # 可持续交付 loop 策略
│       ├── delivery-loop-state-template.md # .trellis/delivery-state.md 模板
│       ├── delivery-batch-template.md    # 单轮补缺批次模板
│       ├── delivery-run-log-template.md  # .trellis/delivery-run-log.jsonl 模板
│       ├── delivery-task-prd-template.md # 补缺任务 PRD 模板
│       ├── planning-artifacts-template.md # 0.6 beta 设计/实现/上下文清单模板
│       ├── test-coverage-matrix-template.md  # 测试覆盖矩阵模板
│       ├── final-acceptance-template.md      # 最终验收模板
│       ├── bug-classification-rules.md       # Bug 分类规则
│       ├── self-review-checklist.md      # 自我评审检查清单
│       └── self-review-report-template.md # 自我评审报告模板
├── trellis-zero-to-mvp-zh/       # 规划技能：Zero → MVP（中文）
│   └── （结构同 trellis-zero-to-mvp）
├── trellis-mvp-to-delivery-zh/   # 规划技能：MVP → Delivery（中文）
│   └── （结构同 trellis-mvp-to-delivery）
├── trellis-implement-tdd/        # 执行期技能：TDD 实现（英文）
│   ├── SKILL.md
│   ├── agents/
│   │   └── openai.yaml
│   └── references/
│       ├── tdd-loop-protocol.md      # RED-GREEN 循环协议
│       └── tdd-progress-template.md  # 进度表模板
├── trellis-debug-systematic/     # 执行期技能：系统化调试（英文）
│   ├── SKILL.md
│   ├── agents/
│   │   └── openai.yaml
│   └── references/
│       ├── debug-protocol.md         # 4 步调试脚本
│       └── debug-report-template.md  # 调试记录模板
├── trellis-review-twostage/      # 执行期技能：双阶段评审（英文）
│   ├── SKILL.md
│   ├── agents/
│   │   └── openai.yaml
│   └── references/
│       ├── review-stage1-checklist.md # Stage 1 规范符合检查清单
│       ├── review-stage2-checklist.md # Stage 2 代码质量检查清单
│       └── review-report-template.md  # 评审报告模板
├── trellis-implement-tdd-zh/     # 执行期技能：TDD 实现（中文）
│   └── （结构同 trellis-implement-tdd）
├── trellis-debug-systematic-zh/  # 执行期技能：系统化调试（中文）
│   └── （结构同 trellis-debug-systematic）
├── trellis-review-twostage-zh/   # 执行期技能：双阶段评审（中文）
│   └── （结构同 trellis-review-twostage）
├── doc/                          # 设计文档
│   ├── FRAMEWORK_COMPARISON_REPORT.md       # 五框架深度对比
│   ├── REQUIREMENT_LANDING_ENHANCEMENT.md   # 需求落地能力增强设计
│   ├── OPTIMIZATION_PROPOSAL.md             # 优化提案
│   └── FINAL_SUMMARY.md                     # 实施总结
├── scripts/                      # 安装脚本（从 GitHub main 分支安装）
│   ├── install-trellis-skills.sh
│   └── install-trellis-skills.ps1
├── README.md                     # 中文说明
└── README_EN.md                  # English documentation
```

## 前置条件

- 已安装 Codex CLI、Claude Code 或其他支持 skill 的 CLI 工具
- 项目中已初始化 Trellis（`.trellis/` 目录存在）
- 首次使用前优先运行 `trellis init -u <name>` 设置开发者身份，并按项目需要添加平台参数（如 `--codex`）
- 如果 Trellis CLI 不可用，再使用旧版兜底命令：`python ./.trellis/scripts/init_developer.py <name>`

## 关键原则

- **先分析，后行动** — 所有技能的第一轮均为只读，不会在用户确认前创建任务或编写代码
- **按能力拆分，不按文件拆分** — 每个子任务对应一个可独立验收的业务或技术能力
- **稳定 ID** — 需求编号（REQ-xxx）和验收标准编号（AC-xxx）在分析阶段确定，后续保持不变
- **严格依赖** — 父子任务仅表达结构，真正的执行依赖写在每个子任务的 PRD 中

## 致谢

本项目在设计上参考了以下开源项目的相关思路与实践：

- [obra/superpowers](https://github.com/obra/superpowers)
- [open-gsd/gsd-core](https://github.com/open-gsd/gsd-core)
- [liuzhengdongfortest/CodeStable](https://github.com/liuzhengdongfortest/CodeStable)

感谢这些项目对 skill 组织方式、需求落地流程和工程质量约束设计提供的启发。
