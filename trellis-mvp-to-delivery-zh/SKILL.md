---
name: trellis-mvp-to-delivery-zh
description: |
  根据源需求文档审计已有 MVP，并执行 Trellis 完整交付 loop 的审计、状态维护、批次规划和最终验收。用于 Codex 被要求在 MVP 后继续、补齐剩余需求、执行 full/delta 差距审计、维护 Requirements Traceability Matrix、分类 DONE/PARTIAL/MISSING/UNTESTED/UNCLEAR 条目、初始化或更新 .trellis/delivery-state.md、规划有边界的补缺批次、要求 worktree + verifier 门、设计自动化测试覆盖、分类发现的 bug，或在交付前执行最终验收的场景。若由 trellis-delivery-controller-zh 调用，则遵循控制器已选定的 loop 模式和审计范围；若单独调用，则按本技能的 delivery-loop-policy 自行判定。
---

# Trellis 从 MVP 到完整交付

## 概览

通过回到源需求文档、审计证据、维护交付状态文件、规划有边界的补缺批次和最终验收，将已有 MVP 推进到完整交付。第一轮始终是只读审计，并且必须输出完整的"需求 vs MVP"差异矩阵；后续轮次在没有相关变化时可以 delta audit 或 early-exit。若使用 `trellis-delivery-controller-zh`，阶段路由和安全门由控制器负责，本技能执行控制器选定的交付阶段。

## 约束

- MVP 之后不要直接“继续开发”，必须先做需求审计。
- 没有实现证据和测试证据时，不要把需求标记为 `DONE`。
- 在用户确认差距审计前，不要创建交付任务。
- 不要把无关缺口混进同一个任务。
- 任务粒度按执行模型能力分级：若执行阶段可能用能力有限的本地模型（如离线 qwen），把任务拆得更碎并标注复杂度。
- 交付任务 PRD 是给执行模型照着做的执行规格。规划阶段必须把所有 `<...>` 占位符替换为具体值（具体文件路径、可照抄的现有范例、有序实现步骤、可机器校验的验收断言、自检命令），禁止把推理判断（含 bug 修复走哪条分支）留给执行阶段。
- 对 Trellis 0.6 beta 项目，如果存在 `.trellis/workflow.md`，必须把它当作当前项目的本地工作流契约。如果已有任务使用 `design.md`、`implement.md`、`implement.jsonl` 或 `check.jsonl`，补缺任务应保留并延续这些产物。
- 不要把所有测试都推到最终兜底任务。每个功能任务必须包含自己的基础测试。
- 最终验证任务只能在功能补缺任务规划完成后创建。
- 如果 bug 不阻塞当前需求验收，先分类，再创建或建议独立 bug task。
- 将本技能视为交付审计和状态维护者，而不是实现者。阶段路由优先交给 `trellis-delivery-controller-zh`；实现交给 `trellis-implement-tdd-zh`；调试交给 `trellis-debug-systematic-zh`；完成前评审交给 `trellis-review-twostage-zh`。
- 对 L2/L3 补缺实现任务，必须要求隔离 worktree 和 verifier/review 门。禁止实现者自行标记任务完成。
- 作为重复运行的 delivery loop 时，必须持续更新 `.trellis/delivery-state.md` 和 `.trellis/delivery-run-log.jsonl`。
- 当自 `last_audited_commit` 后没有相关变化时 early-exit，禁止无意义 full audit 消耗 token。

## 工作流

### 0. 加载交付 Loop 状态

读取 `references/delivery-loop-policy.md`。

如果 `.trellis/delivery-state.md` 存在，审计前先读取它。如果不存在，说明这是首次运行：

1. 读取 `references/delivery-loop-state-template.md`。
2. 计划在 full gap audit 后初始化 `.trellis/delivery-state.md`。
3. 默认 `loop_mode` 为 `L1`。
4. 除非用户提供其他基线，否则把当前 commit 作为 MVP baseline。

如果 `.trellis/delivery-run-log.jsonl` 不存在，读取 `references/delivery-run-log-template.md`，并计划在本轮结束时创建它。

### 1. 接收或判断 Loop 模式和审计范围

如果由 `trellis-delivery-controller-zh` 调用，使用控制器已经选定的 loop 模式和审计范围，并只做一致性检查。如果用户直接调用本技能，使用 `references/delivery-loop-policy.md` 选择：

- Loop 模式：`L1` 只审计、`L2` 辅助交付、`L3` 受控持续运行。
- 审计范围：`full`、`delta` 或 `early-exit`。

规则：

- MVP 完成后的首次运行始终是 `L1 + full audit`。
- full audit 必须对比源需求和 MVP，并输出完整 Requirements Traceability Matrix。
- 只有已有 delivery state 且源需求未变化时，才允许 delta audit。
- 当自 `last_audited_commit` 后需求证据、task 状态、代码或测试都没有相关变化时，追加 run log 并 early-exit。
- 如果 `current_round` 超过 `max_rounds`、需求 carry-over 过多、verifier 两次失败或存在 critical review issue，停止并询问用户；若由控制器调用，返回 `pause-human-needed` 所需证据。

### 2. 发现证据

定位并读取：

- 源需求文档。
- 已有 MVP 代码和测试。
- 现有 `.trellis/tasks/`，尤其是已完成或进行中的任务。
- 已有需求 ID、追踪矩阵和验收备注。
- 现有 `.trellis/delivery-state.md` 和 `.trellis/delivery-run-log.jsonl`（如存在）。
- 受影响 package 的相关 `.trellis/spec/` 索引。
- Trellis 0.6 beta 工作流元数据：如存在，读取 `.trellis/workflow.md`、`.trellis/config.yaml`、`.trellis/.version`、`.trellis/.developer` 和 `.trellis/workspace/`。

规划补缺任务前，检查 `.trellis/spec/` 和已有任务产物是否足够新，能解释当前行为。如果它们过期或过于泛化，先增加 spec 刷新/bootstrap 或任务产物刷新任务，再规划实现任务。

先使用本地证据再提问。只问无法从需求文档或仓库判断的阻塞性问题。

### 3. 执行差距审计（增强版 - 自我评审循环）

循环执行以下步骤，直到满足小模型执行标准：

#### 第 N 轮审计

**3.1 生成差距审计输出**

读取 `references/gap-audit-template.md`，输出：

- Requirements Traceability Matrix。
- MVP 完成度摘要。
- 阻塞性问题。
- 按依赖排序的任务计划。
- 推荐优先级。
- 自动化测试要求。
- 对中/高复杂度补缺任务，读取 `references/planning-artifacts-template.md` 起草左移设计、实现计划和上下文清单产物：当项目工作流支持时，包含 `design.md`、`implement.md`、`implement.jsonl` 和 `check.jsonl`。

只能使用这些状态：`DONE`、`PARTIAL`、`MISSING`、`UNTESTED`、`UNCLEAR`。

首次运行时，Requirements Traceability Matrix 是后续 delivery loop 的基线，必须包含每条源需求，即使本轮还不创建任务。

**3.2 自我评审**

读取 `references/self-review-checklist.md`，对照检查清单逐项检查审计输出质量。

使用 `references/self-review-report-template.md` 生成评审报告，包含：
- 整体评分（8个维度）
- 检查清单通过情况
- 发现的问题清单（位置、问题描述、影响、改进建议）
- MVP 兼容性检查
- 统计信息
- 本轮结论

**3.3 判断是否达标**

- ✅ 所有检查项通过 → 跳转到步骤4（更新交付状态）
- ✅ 连续2轮无新问题发现 → 自动通过，跳转到步骤4
- ❌ 有未通过检查项 → 执行步骤3.4（针对性改进）
- ⚠️ 超过5轮仍有问题 → 提示用户选择：
  - 选项A：使用更强模型重新审计
  - 选项B：人工介入审查当前审计
  - 选项C：接受当前版本（风险自负）

**3.4 针对性改进**

根据评审报告中的问题清单，进行针对性改进：
- 只修改标记为问题的部分，不重新审计整个 MVP
- 保持已通过部分不变
- 特别关注 MVP 兼容性（不破坏已有行为）
- 完成改进后，回到步骤3.1，进入第 N+1 轮评审

**评审循环原则**：
- 逐轮收敛，不全量重做
- 问题定位要精确（到具体的 REQ-xxx、Task ID、PRD 章节）
- 改进要针对性（修复问题，不引入新问题）
- 强调 MVP 兼容性（所有补缺任务不能破坏 MVP 行为）

### 4. 更新交付状态

使用 `references/delivery-loop-state-template.md` 初始化或更新 `.trellis/delivery-state.md`：

- 记录 `source_requirements`、`mvp_baseline_commit`、`last_audited_commit`、`loop_mode`、`current_round` 和 `max_rounds`。
- 写入每个 `REQ-*` 的当前状态。
- 保留历史人工决策和 blocker。
- 当某需求仍未关闭且没有进展时，增加 carry-over count。
- 对超过策略上限的需求标记暂停。
- 将 `Next Loop Recommendation` 设置为：`continue-next-batch`、`early-exit`、`pause-human-needed`、`run-final-acceptance` 或 `rebaseline-required`。

### 5. 选择交付批次

读取 `references/delivery-batch-template.md`，为本轮规划且只规划一个批次。

批次规则：

- L1 可以推荐批次，但未经确认不得创建任务。
- L2/L3 只能创建或更新已确认/当前批次。
- 每轮最多 3 个补缺任务。
- 每轮最多 1 个高风险任务。
- 当基础契约、业务行为、UI、测试和最终验证依赖不同，不要混进同一批次。
- 最终验收单独成批，并且只能在 P0/P1 缺口 DONE 或被人工明确延期后进行。
- 任一 critical review issue、重复 verifier 失败或同一 REQ reopen 两次，必须停止 loop。

### 6. 确认交付计划

在创建或修改 Trellis task 前请求一次确认：

```text
请确认这个差距审计、交付状态更新和选定批次。如果确认，我将为本批次创建或更新 Trellis tasks 和 PRD，但暂不实现功能。
```

如果用户调整优先级或范围，先更新矩阵和任务计划，再创建任务。

### 7. 创建或更新补缺任务

用户确认后：

1. 创建或复用一个完整需求和验证的父任务。
2. 为每组高度相关的缺口创建一个子任务。
3. 使用 `references/delivery-task-prd-template.md` 写入子任务 PRD。
4. 如果基础契约、业务行为、UI、测试和最终验证的依赖不同，就分开任务。
5. 对中/高复杂度子任务，如果 `.trellis/workflow.md` 或现有任务显示项目期望这些产物，写入或起草 `design.md`、`implement.md`、`implement.jsonl` 和 `check.jsonl`。写入前必须先读取已有产物，禁止盲目覆盖。
6. 为每个 PRD 加入交付 loop 控制字段：worktree required、verifier required、implementation skill、debug skill、review skill、human gate、max fix attempts、rollback trigger。
7. 不要开始编码。

### 8. 记录运行日志

读取 `references/delivery-run-log-template.md`，向 `.trellis/delivery-run-log.jsonl` 追加一条 JSON 对象。

记录：

- run id、loop mode、round、audit scope、baseline commit、head commit
- requirements changed、open gaps、tasks created/updated/completed
- critical review issues、debug escalations、carry-over requirements
- tokens estimate、outcome 和 next action

full audit、delta audit、创建任务、暂停、final-acceptance-ready 和 early-exit 都必须记录。

### 9. 规划测试闭环

当用户要求规划或补齐测试覆盖时，读取 `references/test-coverage-matrix-template.md`。将每个 `REQ-*` 或 `AC-*` 映射到至少一个 unit、integration、e2e、smoke、regression 或 manual verification 条目。

### 10. 执行最终验收

所有功能任务完成后，读取 `references/final-acceptance-template.md`。最终验收阶段不要新增功能，除非阻塞性 bug 导致无法验收。

### 11. 分类 Bug

验证发现 bug 时，读取 `references/bug-classification-rules.md`。判断是在当前任务修复、创建独立 bug task，还是记录风险后延期。

## 落地阶段衔接（补缺任务创建后）

本技能负责审计与规划补缺任务，不写代码。进入"需求落地"时，对每个补缺子任务按依赖顺序使用执行期技能形成闭环（尤其执行模型为 qwen3.6 35b 这类小模型时）：

1. **`trellis-implement-tdd-zh`** —— 对补缺任务每条 AC 跑红→绿→提交的 TDD 机械循环，回归测试守住 MVP 兼容性契约。
2. **`trellis-debug-systematic-zh`** —— 测试该绿不绿或自检失败时，用刚性脚本定位修复。
3. **`trellis-review-twostage-zh`** —— 完成前做规范符合(可小模型) + 代码质量(强模型)双阶段评审。

角色分层模型分配：规划用强模型、实现用小模型、评审 Stage 2 用强模型（Trellis 可按 agent 配 `model`）。

## 参考文件

- `references/delivery-loop-policy.md` - 单独调用本技能或校验控制器路由时读取，用于 loop mode、full/delta/early-exit 审计范围、批次限制和停止条件。
- `references/delivery-loop-state-template.md` - 初始化或更新 `.trellis/delivery-state.md` 时读取。
- `references/delivery-batch-template.md` - 为每轮选择唯一补缺批次时读取。
- `references/delivery-run-log-template.md` - 追加 `.trellis/delivery-run-log.jsonl` 时读取。
- `references/gap-audit-template.md` - full 或 delta MVP 差距审计时读取。
- `references/self-review-checklist.md` - 每轮审计后进行自我评审时读取。
- `references/self-review-report-template.md` - 生成评审报告时读取。
- `references/planning-artifacts-template.md` - 为中/高复杂度任务起草 Trellis 0.6 beta 的设计、实现和上下文清单产物时读取。
- `references/delivery-task-prd-template.md` - 创建补缺任务 PRD 前读取。
- `references/test-coverage-matrix-template.md` - 规划或补齐测试覆盖时读取。
- `references/final-acceptance-template.md` - 最终交付验收时读取。
- `references/bug-classification-rules.md` - 验证发现缺陷时读取。
