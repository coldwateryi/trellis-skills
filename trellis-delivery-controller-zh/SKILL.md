---
name: trellis-delivery-controller-zh
description: |
  Trellis 需求交付总入口和流程控制器。用于用户希望只调用一个 Trellis skill 自动判断当前阶段，并在需求分析、MVP 任务规划、MVP 后差距审计、交付 loop、TDD 实现、系统调试、双阶段评审和最终验收之间进行路由、推进和安全门控制的场景。适合基于 trellis-zero-to-mvp-zh、trellis-mvp-to-delivery-zh、trellis-implement-tdd-zh、trellis-debug-systematic-zh 和 trellis-review-twostage-zh 形成端到端交付闭环。
---

# Trellis 交付控制器

## 概览

把 Trellis 技能集当作一条分层流水线来编排，而不是让用户手动记忆每个阶段的 skill。控制器负责判断当前项目状态、选择下一个阶段、设置安全门，并要求具体阶段仍由对应的专用 skill 执行。

本技能不替代具体阶段 skill：

- 需求到 MVP 任务树：使用 `trellis-zero-to-mvp-zh`。
- MVP 后差距审计与补缺规划：使用 `trellis-mvp-to-delivery-zh`。
- 子任务实现：使用 `trellis-implement-tdd-zh`。
- 失败定位修复：使用 `trellis-debug-systematic-zh`。
- 完成前评审：使用 `trellis-review-twostage-zh`。

## 约束

- 不直接写业务代码；实现必须交给执行期 skill。
- 不跳过用户确认门：首次只读分析、首次完整差距审计、扩大范围、改 File Manifest 外文件、强模型评审缺失时必须停下。
- 不让实现者自行标记完成；完成状态必须经过自检和评审门。
- 不重复 full audit：已有 `.trellis/delivery-state.md` 且需求未变时，优先 delta audit 或 early-exit。
- 不在控制器里吸收第三方 skill 能力；外部能力吸收交给 `trellis-skill-assimilator-zh`。

## 工作流

### 1. 发现项目状态

读取 `references/route-policy.md`，并检查：

- 是否存在源需求文档。
- 是否存在 `.trellis/`。
- 是否存在 `.trellis/tasks/`、`.trellis/spec/`、`.trellis/workflow.md`。
- 是否存在 `.trellis/delivery-state.md` 和 `.trellis/delivery-run-log.jsonl`。
- 当前是否有指定的子任务目录。
- 最近是否有失败测试、自检失败或评审报告。

### 2. 选择阶段

根据 `references/route-policy.md` 输出唯一的下一阶段：

- `zero-to-mvp-readonly`
- `zero-to-mvp-create-tasks`
- `mvp-to-delivery-full-audit`
- `mvp-to-delivery-delta-audit`
- `delivery-batch-planning`
- `implement-tdd`
- `debug-systematic`
- `review-twostage-stage1`
- `review-twostage-stage2`
- `final-acceptance`
- `early-exit`
- `pause-human-needed`

同时说明选择依据、需要读取的文件、应调用的 skill 和安全门。

当下一阶段属于 delivery loop 时，读取 `references/delivery-loop-routing.md`，判定 loop 模式和审计范围。控制器的判定结果传递给 `trellis-mvp-to-delivery-zh` 执行。

### 3. 执行阶段路由

读取 `references/stage-transition-gates.md`，只推进到下一个安全门：

- 规划阶段只读分析完成后，等待用户确认再创建任务。
- 首次 full audit 完成后，等待用户确认差距矩阵和第一批补缺范围。
- 子任务执行按 `trellis-implement-tdd-zh -> trellis-debug-systematic-zh -> trellis-review-twostage-zh` 闭环推进。
- Stage 2 评审需要强模型或人工复核；如果当前模型能力不足，输出 evidence pack 并暂停。

### 4. 更新状态

当阶段涉及 delivery loop 时，使用 `trellis-mvp-to-delivery-zh` 维护：

- `.trellis/delivery-state.md`
- `.trellis/delivery-run-log.jsonl`
- Requirements Gap Matrix
- 当前批次和下一步建议

控制器只检查这些状态是否存在、是否新鲜、是否允许进入下一阶段。

### 5. 汇报

每轮输出：

- 当前阶段。
- 下一步调用的 Trellis skill。
- 需要读取的上下文。
- 自动推进范围。
- 必须停下的安全门。
- 若暂停，列出阻塞原因和所需用户/强模型输入。

## 参考文件

- `references/route-policy.md` - 判断当前项目状态和下一阶段时读取。
- `references/delivery-loop-routing.md` - 判断 MVP 后 full/delta/early-exit、loop 模式和批次边界时读取。
- `references/stage-transition-gates.md` - 阶段推进和停止条件判断时读取。
- `references/model-role-policy.md` - 判断小模型、强模型和人工复核分工时读取。
