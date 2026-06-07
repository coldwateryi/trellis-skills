---
name: trellis-review-twostage-zh
description: |
  在 Trellis 子任务自检全绿、标记完成之前，做两阶段代码评审：先机械核对规范符合（对照 PRD 验收标准/决策表/禁止事项/文件清单/挂载点），再做代码质量评审（对照 .trellis/spec/guides 的工程规范与设计纪律）。用于 Codex / Claude Code 等团队协作场景，尤其当实现由 qwen3.6 35b 小模型完成时——小模型评审自己的代码不可靠，Stage 2 应升级到强模型；critical 问题阻断完成。
---

# Trellis 双阶段评审

## 概览

子任务实现自检全绿后、标记完成前的质量门。分两段独立评审：

- **Stage 1 规范符合**：对照 `prd.md` 机械核对，可由小模型 + 检查清单完成。
- **Stage 2 代码质量**：对照工程规范与设计纪律，**应由强模型**完成（小模型评审自己产出不可靠）。

任一阶段发现 **critical** 问题即阻断，打回 `trellis-implement-tdd-zh` 修复；修复后重新评审。

触发：`trellis-implement-tdd-zh` 收尾自检全绿、交接评审时。

每次评审都写入任务目录下固定的 `<task-dir>/review-report.md`。第一次评审时从 `references/review-report-template.md` 创建，后续重审在同一个文件里追加新的 review round 块；不要改 skill 目录里的模板文件。

## 约束

- **评审基于 diff + `prd.md`**，不重读整个需求文档。
- **Stage 1 与 Stage 2 分开做，不合并**——合并会让"是否照规范实现"和"代码好不好"互相掩盖。
- **Stage 2 用强模型**（角色分层模型分配）。若只有小模型可用，Stage 2 至少严格走 `references/review-stage2-checklist.md` 逐项核对，并在报告里标注"未经强模型评审"风险。
- **按严重度分级**：critical（阻断）/ major（应修）/ minor（可记录后续）。只有 critical 阻断完成。
- 评审者**不直接改代码**：产出问题清单交回实现技能修，保持"写"与"审"分离。

## 工作流

### 1. 准备

- 取本任务 diff（相对任务起点）。
- 读 `prd.md`：`验收标准`、`决策表`、`禁止事项`、`文件清单`、`行为约束`；若有 `design.md` 读`挂载点清单`、`编排-计算分离`。
- 若有 `check.jsonl`：预加载其中的回归/风险上下文。

### 2. Stage 1 · 规范符合（机械核对，可小模型）

逐项走 `references/review-stage1-checklist.md`，核对实现是否**照规划做了**：

- 每条 `AC-xxx` 是否有对应测试且为绿？
- 改动文件是否都在「文件清单」内？有无清单外文件被改？
- 是否违反任何「禁止事项」（新建已有基类、引入未列依赖等）？
- 「决策表」的选择是否被遵守（注解 / 命名 / schema / 分支）？
- 「挂载点清单」是否逐项接线（路由 / 配置 / 订阅 / DI）？
- 任一不符 → 记为 issue。AC 无测试、改了禁止改的文件、挂载点漏接 = **critical**。

### 3. Stage 2 · 代码质量（强模型）

逐项走 `references/review-stage2-checklist.md`，对照 `.trellis/spec/guides/` 与设计纪律评审**代码本身**：

- **编排-计算分离**：编排逻辑与计算逻辑是否混在一处？纯计算是否被塞进编排层导致难测？
- **结构健康度**：是否往本就偏胖的文件继续堆？是否制造了"什么都装的筐"？
- **简化/复用**：有无重复实现已有能力？有无未被要求的过度抽象（违反 YAGNI）？
- **正确性**：边界 / 错误路径是否真的被处理（而非只让 happy path 测试变绿）？
- **规范符合**：命名 / 分层 / 错误语义是否符合 `.trellis/spec/`？
- 按严重度记录；引入正确性缺陷或破坏既有行为 = **critical**。

### 4. 出报告并裁决

用 `references/review-report-template.md` 生成/更新 `<task-dir>/review-report.md`：

- 有 **critical** → 阻断，打回 `trellis-implement-tdd-zh`，只修标注项，修后回到第 1 步重审。
- 仅 major/minor → 可放行；major 建议本轮修，minor 记入任务备注/后续。
- 全通过 → 交回编排会话推进任务状态（`task.py` 推进 / 进入 finish）。

## 小模型适配要点

- **写审分离 + 模型分层**：实现用小模型，Stage 2 评审用强模型——这是小模型产出可被信任的关键。
- **Stage 1 机械化**：规范符合是逐条对照 PRD 的机械活，小模型可胜任，先用它过滤掉低级偏差。
- **critical 阻断**：把"质量是否达标"变成客观门，不靠主观感觉放行。
- 对团队：双阶段评审 + 严重度分级让 PR 可审、让他人/小模型的产出有客观接受依据。

## 参考文件

- `references/review-stage1-checklist.md` —— 规范符合机械核对清单，Stage 1 读取。
- `references/review-stage2-checklist.md` —— 代码质量与设计纪律清单（含编排-计算分离/结构健康度），Stage 2 读取。
- `references/review-report-template.md` —— `<task-dir>/review-report.md` 的只读模板；出报告时更新任务目录下的固定文件。
