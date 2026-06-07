# Trellis 需求交付技能集

本仓库为 Codex CLI、Claude Code 以及其他支持 skill 的 CLI 工具提供一套 Trellis 工作流技能，覆盖从原始需求文档到完整交付的全流程——**分析 → 规划 → 追踪 → 审计 → 补缺 → 验收**。

## 技能概览

| 技能 | 语言 | 用途 |
| --- | --- | --- |
| `trellis-zero-to-mvp` | EN | 从零开始：将需求文档转化为 MVP 任务树 |
| `trellis-mvp-to-delivery` | EN | 从 MVP 到交付：差距审计、补缺规划、最终验收 |
| `trellis-zero-to-mvp-zh` | ZH | 同上（中文版） |
| `trellis-mvp-to-delivery-zh` | ZH | 同上（中文版） |
| `trellis-implement-tdd-zh` | ZH | 执行期：用严格 TDD 红绿循环逐条落地验收标准（小模型友好） |
| `trellis-debug-systematic-zh` | ZH | 执行期：刚性 4 步调试脚本——复现→定位→假设验证→最小修复 |
| `trellis-review-twostage-zh` | ZH | 执行期：规范符合(小模型)+代码质量(强模型)双阶段评审门 |

### ✨ 新功能：自我评审循环与设计左移

**所有技能现已支持自我评审循环机制，并把复杂任务的设计、实现步骤和稳定上下文清单前置到规划阶段，确保输出满足小参数模型（如 qwen3.6 35b）的执行要求。**

**工作原理**：
1. 🔍 **分析** - 生成初版需求追踪矩阵、任务拆分和 PRD
2. ✅ **自我评审** - 对照 45-60 项检查清单逐项检查
3. 🔧 **针对性改进** - 只修复标记的问题，不全量重做
4. 🔄 **循环收敛** - 重复 2-3 轮直到所有检查通过
5. ✅ **用户确认** - 达标后才创建任务树

**核心优势**：
- ✅ **小模型友好** - 消除占位符、提供具体路径和步骤
- ✅ **设计左移** - 对中/高复杂度任务补充 Context Manifest、Decision Table、`design.md`、`implement.md`、`implement.jsonl`、`check.jsonl`
- ✅ **质量保证** - 45-60 项精准检查，问题定位到具体行
- ✅ **成本可控** - ROI > 5:1（规划多花 45k tokens，执行少花 200k tokens）
- ✅ **效果显著** - 执行成功率提升 30%-50%

详见：[优化提案](doc/OPTIMIZATION_PROPOSAL.md) 和 [实施总结](doc/FINAL_SUMMARY.md)

## Trellis 0.6 Beta 适配

本技能集仍兼容 Trellis 的核心任务结构（`.trellis/tasks/`、`.trellis/spec/`、`task.py create --parent`），同时增加对 0.6 beta 工作流的适配：

- 如存在 `.trellis/workflow.md`，优先把它作为项目本地工作流契约读取。
- 如存在 `.trellis/config.yaml`、`.trellis/.version`、`.trellis/.developer`、`.trellis/workspace/`，在规划前纳入上下文。
- 对依赖 `.trellis/spec/` 的任务先检查 spec 新鲜度；缺失、泛化或过期时，先规划 spec refresh/bootstrap。
- 对中/高复杂度任务，除 `prd.md` 外，按项目工作流补充 `design.md`、`implement.md`、`implement.jsonl`、`check.jsonl`。
- 首次初始化优先使用 `trellis init -u <name>`，并按项目需要添加平台参数；`init_developer.py` 只作为旧版兜底。

## 从 GitHub 安装

脚本会优先检查当前目录是否存在 `.trellis/`。如果当前目录是已初始化的 Trellis 项目，默认安装到该项目的项目级 skill 目录；如果当前目录不是 Trellis 项目，会提示输入目标项目目录。若用户输入的目录仍未发现 `.trellis/`，脚本会询问是否改为安装到全局 skill 目录。

随后询问是否安装中文版 skill：选择是仅安装 `trellis-zero-to-mvp-zh`、`trellis-mvp-to-delivery-zh`；选择否仅安装英文版。

> **执行期技能**（`trellis-implement-tdd-zh`、`trellis-debug-systematic-zh`、`trellis-review-twostage-zh`）不通过安装脚本分发，直接从本仓库手动复制到项目的 `.agents/skills/` 或 `.claude/skills/` 目录即可。

项目级默认安装位置：

- `.agents/skills/`：Codex CLI / Trellis agent 兼容目录
- `.claude/skills/`：Claude Code 项目级 skill 自动发现目录

全局回退安装位置：

- `$CODEX_HOME/skills`，未设置 `CODEX_HOME` 时为 `~/.codex/skills`：Codex CLI 全局 skill 目录
- `~/.claude/skills`：Claude Code 用户级 skill 目录

如只想安装到单个平台目录，可设置 `TRELLIS_SKILLS_AGENT_TARGETS=codex` 或 `TRELLIS_SKILLS_AGENT_TARGETS=claude`。未设置时默认值为 `both`。

如果在本仓库的 `scripts/` 目录直接执行脚本，脚本会先从 GitHub 更新父级 `trellis-skills` 目录的 `main` 分支源码，然后再按上述逻辑安装。更新使用 fast-forward 合并；如果本地有未提交改动或分支无法快进，脚本会停止，避免覆盖本地修改。

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

脚本主要支持 `bash` 和 `zsh`。如果使用其他不兼容 shell（例如 `sh`/`dash`）执行，脚本会直接提示改用 `bash` 或 `zsh`。脚本会从当前终端读取交互输入，即使通过 `curl | bash` 或 `curl | zsh` 管道执行，也可以正常选择目标目录和语言。

安装过程中会输出带 `[trellis-skills]` 前缀的步骤日志。遇到问题时，请保留完整安装输出，便于定位当前 shell、工作目录、目标目录、源码来源和失败步骤。

本地脚本方式：

```bash
cd /path/to/trellis-skills/scripts
bash ./install-trellis-skills.sh
# 或
zsh ./install-trellis-skills.sh

# 仅安装到 Claude Code 项目级 skill 目录
TRELLIS_SKILLS_AGENT_TARGETS=claude bash ./install-trellis-skills.sh
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

# 仅安装到 Claude Code 项目级 skill 目录
.\install-trellis-skills.ps1 -AgentTargets claude
```

## Claude Code 兼容性

Claude Code 会从项目的 `.claude/skills/<skill-name>/SKILL.md` 自动发现项目级 skill，也会读取用户级 `~/.claude/skills/<skill-name>/SKILL.md`。当前四个技能目录已经包含 Claude Code 所需的 `SKILL.md` 入口和引用资料目录；`agents/openai.yaml` 是面向 Codex/OpenAI 兼容运行器的附加配置，Claude Code 可忽略该文件。

安装脚本在项目级安装时默认同时写入 `.agents/skills/` 和 `.claude/skills/`，因此同一 Trellis 项目可以被 Codex CLI 和 Claude Code 分别识别。只有当前目录和用户指定目录都不是 Trellis 项目且用户确认后，脚本才会安装到全局目录。若团队只使用其中一个运行器，通过 `TRELLIS_SKILLS_AGENT_TARGETS` 或 PowerShell 的 `-AgentTargets` 参数限制安装目标即可。

## 推荐工作流

```
需求文档 ──→ [Zero to MVP] ──→ MVP 任务树 ──→ 编码实现 MVP
                                                    │
                                                    ▼
                              需求文档 ──→ [MVP to Delivery] ──→ 补缺任务 ──→ 交付验收
```

### 阶段一：Zero → MVP

当你拿到一份完整的需求文档（PRD / 产品说明 / 功能规格），还没有开始写代码时：

1. 将需求文档放到项目中
2. 调用 `trellis-zero-to-mvp`（或中文版 `trellis-zero-to-mvp-zh`）
3. 技能会执行**只读分析**，输出：
   - 需求追踪矩阵（Requirements Traceability Matrix）
   - 模块依赖图
   - 按能力拆分的任务清单
   - 按依赖排序的 MVP 开发顺序
   - 父/子任务 PRD 草案
4. **确认分析结果后**，技能创建 Trellis 任务树
5. 按推荐顺序开始编码

### 阶段二：MVP → Delivery

MVP 实现完成后，回到源需求文档做完整交付：

1. 调用 `trellis-mvp-to-delivery`（或中文版 `trellis-mvp-to-delivery-zh`）
2. 技能执行**差距审计**，逐条对照需求文档检查 MVP：
   - 需求追踪矩阵（含 DONE / PARTIAL / MISSING / UNTESTED / UNCLEAR 状态）
   - MVP 完成度摘要
   - 按依赖排序的补缺任务计划
   - 自动化测试覆盖要求
3. **确认审计结果后**，创建补缺 Trellis 任务
4. 按优先级补齐功能、测试，执行最终验收

## 推荐用法

### 场景 1：全新项目启动

```
你是一个新项目，需求文档在 docs/requirements.md。

请使用 trellis-zero-to-mvp-zh 将其转化为 MVP 任务计划。
```

技能会先做只读分析——不会写任何代码。确认任务拆分和 MVP 边界后，才会创建 Trellis 任务树。

**✨ 自我评审循环**：分析过程中会自动进行 2-3 轮质量检查，确保：
- ✅ 所有 `<...>` 占位符已被具体值替换
- ✅ File Manifest 包含精确的文件路径
- ✅ Implementation Steps 是可执行的具体动作
- ✅ 复杂任务已拆分到适合小模型执行

### 场景 2：已有 MVP，准备完整交付

```
MVP 已实现完成，源需求文档在 docs/requirements.md。

请使用 trellis-mvp-to-delivery-zh 审计 MVP，规划完整交付。
```

技能会逐条对照需求文档检查现有实现和测试，找出所有缺口，然后创建补缺任务。

**✨ 自我评审循环**：审计过程中会自动进行质量检查，确保：
- ✅ 每个 DONE 状态都有实现证据和测试证据
- ✅ 补缺任务的 PRD 明确不破坏 MVP 行为
- ✅ Regression Tests 覆盖 MVP 核心流程
- ✅ Bug 修复的分支逻辑已明确定死

### 场景 3：已手工实现部分功能，但还没有形成 MVP

```
需求文档在 docs/requirements.md，项目中已经手工实现了一部分功能，并且中途运行过 trellis init。

请使用 trellis-zero-to-mvp-zh 基于现有代码、.trellis/spec/ 和需求文档，只规划剩余 MVP 功能任务。
```

技能会先生成 Existing Implementation Baseline（已有实现基线），再按状态处理需求：

- `DONE`：不创建实现任务，只作为已有依赖证据。
- `UNTESTED`：只创建测试补齐任务。
- `PARTIAL`：只创建缺失行为的补缺任务。
- `MISSING`：创建新实现任务。

### 场景 4：持续迭代

在实际开发中，两个技能可以循环使用：

1. 用 `zero-to-mvp` 规划首个可交付版本
2. 编码实现 MVP
3. 用 `mvp-to-delivery` 审计差距，补齐到完整交付
4. 如果有新增需求，回到步骤 1，针对新需求再次使用 `zero-to-mvp`

## 执行期技能详细使用说明

规划技能（`zero-to-mvp` / `mvp-to-delivery`）创建任务树后，使用以下**执行期技能**按依赖顺序实施每个子任务，形成**规划→实现→调试→评审**的完整闭环。

### 执行期技能概览

| 技能 | 触发时机 | 核心价值 | 小模型适配 |
| --- | --- | --- | --- |
| `trellis-implement-tdd` | 子任务进入实现阶段 | 把"实现需求"变成"让测试变绿"的机械循环，每步有客观信号 | ✅ 窄路径+客观信号，小模型只需追"让断言变绿" |
| `trellis-debug-systematic` | 测试该绿不绿、自检失败 | 刚性 4 步脚本（复现→定位→假设验证→最小修复），防小模型乱改 | ✅ 铁律"一次一处、改完必重跑、禁止猜" |
| `trellis-review-twostage` | 实现自检全绿后 | 规范符合(可小模型)+代码质量(强模型)双阶段门，critical 阻断 | ✅ 角色分层：Stage 1 小模型、Stage 2 强模型 |

### 典型工作流：从任务到完成

假设你已用 `trellis-zero-to-mvp-zh` 创建了任务树，现在要实现第一个子任务：

#### 1️⃣ 启动 TDD 循环

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

#### 2️⃣ 遇到红灯时调试

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

#### 3️⃣ 完成后评审

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

## 需求状态说明

两个技能使用统一的需求状态标记：

| 状态 | 含义 |
| --- | --- |
| `DONE` | 已完整实现并通过测试 |
| `PARTIAL` | 部分实现 |
| `MISSING` | 尚未实现 |
| `UNTESTED` | 已实现但缺少充分测试 |
| `UNCLEAR` | 需求不够清晰，无法实施 |

## 目录结构

```
skills/
├── trellis-zero-to-mvp/          # Zero → MVP（英文）
│   ├── SKILL.md                  # 技能定义与工作流
│   ├── agents/
│   │   └── openai.yaml           # OpenAI 兼容运行器配置
│   └── references/
│       ├── analysis-output-template.md   # 只读分析输出模板
│       ├── parent-prd-template.md        # 父任务 PRD 模板
│       ├── child-prd-template.md         # 子任务 PRD 模板
│       ├── planning-artifacts-template.md # 0.6 beta 设计/实现/上下文清单模板
│       └── task-creation-checklist.md    # 任务创建检查清单
├── trellis-mvp-to-delivery/      # MVP → Delivery（英文）
│   ├── SKILL.md
│   ├── agents/
│   │   └── openai.yaml
│   └── references/
│       ├── gap-audit-template.md         # 差距审计模板
│       ├── delivery-task-prd-template.md # 补缺任务 PRD 模板
│       ├── planning-artifacts-template.md # 0.6 beta 设计/实现/上下文清单模板
│       ├── test-coverage-matrix-template.md  # 测试覆盖矩阵模板
│       ├── final-acceptance-template.md      # 最终验收模板
│       └── bug-classification-rules.md       # Bug 分类规则
├── trellis-zero-to-mvp-zh/       # Zero → MVP（中文）
│   └── （结构同上）
├── trellis-mvp-to-delivery-zh/   # MVP → Delivery（中文）
│   └── （结构同上）
├── scripts/                      # 从 GitHub main 分支安装 skill 的脚本
│   ├── install-trellis-skills.sh
│   └── install-trellis-skills.ps1
└── README.md
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
