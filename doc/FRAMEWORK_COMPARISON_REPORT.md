# AI 编码工程化框架深度对比报告

> 对比对象：CodeStable · Trellis · trellis-skills · Superpowers · gsd-core
> 视角：多人项目团队协同开发
> 结论先行：以 **Trellis + trellis-skills 为基座**，把 Superpowers 的工程纪律与 CodeStable 的设计匠艺**提炼注入**，是多人团队的最优组合。本报告是该结论的论证，配套设计见 [`REQUIREMENT_LANDING_ENHANCEMENT.md`](./REQUIREMENT_LANDING_ENHANCEMENT.md)。

---

## 1. 一句话定位

| 项目 | 一句话 | 中心实体 | 形态 | License |
| --- | --- | --- | --- | --- |
| **CodeStable** | 围绕软件要素的人在环工作流 | 需求/架构/特性/问题/决策 | 纯技能包(MD) | MIT |
| **Trellis** | 团队级 AI 编码基础设施 | 任务 + 开发者 | npm CLI + Python 运行时 | AGPL-3.0 |
| **trellis-skills** | Trellis 上的需求→交付方法论层 | REQ/AC 可追溯 | 技能包(MD)，依附 Trellis | MIT |
| **Superpowers** | 给 agent 的工程实践方法论 | 工程实践(TDD/调试/评审) | 插件(技能+hook) | MIT |
| **gsd-core** | 上下文工程 + 阶段循环系统 | 上下文 + 阶段 + 子代理 | npm + 重型 TS 运行时 | MIT |

**谱系（按"中心实体"归派）**

```
                        AI 执行/编排派                        团队基础设施派      软件要素派
              ┌──────────────────────────────┐              ┌──────────┐      ┌──────────┐
   Superpowers(工程实践)   gsd-core(上下文+编排)   ←—→   Trellis(任务+人)   CodeStable(要素)
              └──────────────────────────────┘              └────┬─────┘      └──────────┘
                  围绕"AI 怎么把活干好/干稳"                       │ +trellis-skills(需求→交付追溯层)
                                                                 └──→ 唯一原生面向"多人团队"
```

---

## 2. 概念谱系：各自解决的"根本痛点"

理解五者差异的钥匙是它们的**痛点假设不同**：

- **CodeStable**：痛点是*软件复杂度膨胀、隐知识丢失、需求漂移* → 用"软件要素被组织/检索/复利"解决。**人在环最强**（明确反对"人干预=失败"）。
- **Trellis**：痛点是*AI 每次会话从零开始、记不住团队规范和任务* → 用"规范/任务/记忆沉淀进仓库 + 团队基础设施"解决。**唯一原生多人团队**。
- **trellis-skills**：痛点是*基础 Trellis 缺需求拆解纪律、弱模型跑不动* → 用"RTM 可追溯 + 自评循环 + 设计左移"解决。**需求完整性/交付对账最强**。
- **Superpowers**：痛点是*agent 乱写代码、不测试、ad-hoc* → 用"TDD 强制 + 系统化调试 + 子代理评审"解决。**工程实践纪律最强**。
- **gsd-core**：痛点是*context rot（上下文越填越烂）、会话间无记忆、没人验证代码真能跑* → 用"fresh-context 子代理跑重活 + STATE.md 文件记忆 + 验证阶段"解决。**上下文工程/规模化自治最强**。

> 注：CodeStable 作者曾批评 Superpowers"没有流程约束"。但当前 Superpowers v5.x 已有有序工作流（brainstorming→worktree→plans→subagent-dev→TDD→review→finishing）且**技能自动触发**——更准确的说法是：Superpowers 是**可组合的扁平技能库**，而非 CodeStable 那种**强约束的要素状态机**。

---

## 3. 量化与工程化对比

| 维度 | CodeStable | Trellis | trellis-skills | Superpowers | gsd-core |
| --- | --- | --- | --- | --- | --- |
| 代码规模 | 6 脚本 | ~32K行TS+22K行Py | 0(纯MD) | 37 脚本 | 92 .cts/~36.6K行 |
| 方法论文本 | ~9.7K行MD | 中 | ~7.3K行MD | ~17K行MD | ~158K行MD(含5语言) |
| 测试 | ❌ | 43 | ❌ | 52 | 海量 + 变异测试(stryker) |
| 子代理数 | 无(单流) | 5 | 复用Trellis | ~3(并行/子代理) | 35 专职 agent |
| Slash 命令 | `/cs` 系 | `/trellis:*` | 2 技能 | 技能自动触发 | 25+ `/gsd:*` |
| 多平台 | Claude/Skills生态 | 14 | Codex+Claude | 8(插件市场) | 8+(installer) |
| 版本管理 | 重装 | 语义化+`update` | 追 Trellis 版本 | RELEASE-NOTES+bump | changeset+i18n |
| 治理 | 个人/beta | 公司(Mindfold) | 个人 | obra/Prime Radiant | open-gsd 组织 |
| 自治程度 | 最低(人在环) | 中 | 中 | 高(长自治) | 最高(autonomous) |

**两个极值**：gsd-core 是**工程化与自治程度的天花板**（35 agent、海量测试、变异测试、i18n、原子锁并发）；CodeStable 是**最轻、最人在环**。

---

## 4. 方法论焦点对照（谁强在哪一块）

| 能力块 | CodeStable | Trellis | trellis-skills | Superpowers | gsd-core |
| --- | --- | --- | --- | --- | --- |
| 需求可追溯(REQ/AC/RTM) | 弱 | 弱 | ✅✅ | 弱 | ✅ |
| 单特性设计纪律 | ✅✅ | 中 | 中(左移) | ✅ | ✅ |
| 架构长效档案 | ✅✅ | ✅(spec) | 弱 | 弱 | ✅ |
| TDD 强制 | 中 | 中 | 测试任务 | ✅✅ | ✅ |
| 系统化调试 | issue流 | 弱 | bug分类 | ✅✅ | ✅✅ |
| 代码评审 | accept | check阶段 | 弱 | ✅✅ | ✅✅ |
| 上下文工程(防rot) | 隐式 | spec注入 | 弱 | 子代理隔离 | ✅✅✅ |
| 知识复利/记忆 | ✅✅(compound) | ✅(update-spec) | 中 | 中 | ✅✅ |
| 多agent并行编排 | ❌ | 子代理 | ❌ | ✅ | ✅✅✅ |
| 弱/本地模型适配 | ❌ | ❌ | ✅✅ | ❌ | ✅(context_window) |

**速记**：设计/架构/复利看 **CodeStable**；需求追溯/弱模型看 **trellis-skills**；TDD/调试/评审看 **Superpowers**；上下文工程/规模化自治/多agent看 **gsd-core**；团队任务/身份/PM 看 **Trellis**。

---

## 5. 多人团队协同视角（本报告的核心）

**最重要的结论**：

> 五者里，**只有 Trellis 是"多人类开发者"原生设计**。CodeStable / Superpowers / gsd-core 本质都是**"单开发者 + 其 AI agent(s)"的个人工程 harness**——它们能被团队*经 git 共享 markdown 规范*而使用，但缺少开发者身份、任务归属、冲突隔离、PM 集成。

把"团队协同"拆成子需求，逐项看谁满足：

| 团队子需求 | CodeStable | Trellis(+skills) | Superpowers | gsd-core |
| --- | --- | --- | --- | --- |
| 共享工程规范(git 化) | ✅ | ✅ | ✅ | ✅ |
| 开发者身份/任务归属/优先级 | ❌ | ✅✅ | ❌ | ❌ |
| PM 集成(Linear/飞书) | ❌ | ✅✅ | ❌ | ❌ |
| 按人冲突隔离(journal) | ❌ | ✅✅ | ⚠️worktree | ⚠️workspace隔离 |
| 需求可追溯交接(REQ/AC) | ❌ | ✅✅(skills) | ❌ | ✅ |
| 跨工具团队 | ⚠️单生态 | ✅14 | ✅8 | ✅8+ |
| 混合/弱模型成员 | ❌ | ✅(skills) | ❌ | ✅(配置) |
| 并行写入安全(并发) | ❌ | 任务级 | worktree | ✅✅✅原子锁 |
| 质量门禁(团队统一) | accept | check | ✅✅TDD/评审 | ✅✅verify+auditors |
| 规模化可靠性(长任务不退化) | 弱 | 中 | ✅ | ✅✅✅context工程 |
| 工程成熟度/可维护 | 低 | 高 | 低 | ✅✅最高 |

**要点**：

1. **协调/分工/PM 维度**：Trellis(+skills) 一骑绝尘——它本身就是一个团队为团队 dogfood 的产品（仓库里可见真实团队成员各自的 workspace journal）。
2. **"团队跑大型/长时自治任务不退化"维度**：gsd-core 最强——context rot 是团队规模化用 AI 的真实杀手。但它的"并发"是**多 agent**，不是多人。
3. **"团队统一工程素养"维度**：Superpowers 最直接——强制 TDD + 系统化调试 + 双阶段评审，把"junior 也能照做"的工程纪律固化下来。
4. **"严肃长寿软件的设计/架构不腐化"维度**：CodeStable 最深，但要团队自己用 git 维持纪律。

---

## 6. 结论与组合建议

### 6.1 为什么选 Trellis + trellis-skills 作基座

对一个多人团队，**协调/身份/任务/PM/追溯/跨工具**是不可回退的刚需，而这些**只有 Trellis(+skills) 原生具备**。其余三者是优秀的"个人工程 harness"，无法承担团队协同底座。

### 6.2 基座之上的"提炼注入"策略

这五者**抽象层不同，可叠不可替**。最优解是组合：

> **基座** = `Trellis + trellis-skills`（多人协同/身份/任务/PM/追溯/跨工具）
> **+ 注入** Superpowers 的工程纪律（TDD/调试/评审）
> **+ 注入** CodeStable 的设计匠艺（编排-计算分离/挂载点/结构健康度/架构档案）
> **+ 借鉴** gsd-core 的上下文工程思路（fresh-context 子代理、STATE.md、原子锁）——重度长时自治任务时评估

注入的具体落地方式（新技能 + 模板增强 + 角色分层模型分配），见配套设计文档 [`REQUIREMENT_LANDING_ENHANCEMENT.md`](./REQUIREMENT_LANDING_ENHANCEMENT.md)。

### 6.3 不建议的组合

- **同时上 gsd-core 和 Trellis 作为基座**：两者都是重型运行时 + 各自的状态/阶段模型（STATE.md vs `.trellis/`），并存会有双心智模型和产物冲突——**择一为基座**，另一只借思路。
- **团队 >5 人却选 CodeStable/Superpowers/gsd-core 当协同底座**：它们没有身份/归属，协调成本会显性化。

### 6.4 风险提示（对五者都诚实）

- **Trellis**：AGPL-3.0 需法务确认；双仓(+skills)版本耦合有漂移风险；运行时注入有 token 成本。
- **gsd-core**：最重、学习曲线最陡；强自治意味着人对单步把控最弱；token 消耗高。
- **Superpowers**：强制 TDD 对探索性/原型项目偏重；官方基本不收新技能(curated)，定制需自维护分支。
- **CodeStable**：无团队基础设施、单生态、单作者 beta(bus factor)。
- **trellis-skills**：依附 Trellis、无测试、个人维护、年轻。
- **共同**：全部年轻且高速迭代，结构会变。

---

*本报告基于各项目 2026-06 时点的公开仓库分析整理。*
