# 阶段转换门

## 可以自动推进

- 读取需求、代码、测试、`.trellis/` 和相关 spec。
- 判断当前阶段和下一步 skill。
- 对已确认范围内的 ready 子任务执行 TDD、调试和 Stage 1 规范核对。
- 自检失败时进入系统调试，最多 3 轮假设/修复。
- 评审通过后建议推进任务状态。
- delivery state 存在且无相关变化时 early-exit 并记录建议。

## 必须暂停

- 首次只读分析后，创建或修改 Trellis 任务树前。
- 首次 full audit 后，确认差距矩阵、延期项和第一批补缺范围前。
- 需要改 File Manifest 外的文件。
- 需求、schema、auth、payment、security、infrastructure 决策不清晰。
- verifier 连续失败 2 次。
- 调试超过 3 轮仍未变绿。
- review 出现 critical。
- Stage 2 代码质量评审需要强模型但当前只有小模型。
- 外层 delivery loop 超过 6 轮。
- 同一 `REQ-*` 连续 2 轮无进展。
- 任何 destructive git 操作、commit、push、tag 或 release 未被用户明确授权。

## 阶段完成条件

| 阶段 | 完成条件 |
| --- | --- |
| `zero-to-mvp-readonly` | 输出 RTM、MVP 边界、任务拆分和 PRD 草案 |
| `zero-to-mvp-create-tasks` | Trellis 父/子任务和 PRD 已创建，不写业务代码 |
| `mvp-to-delivery-full-audit` | 完整 Requirements Gap Matrix 和 delivery state 已准备 |
| `mvp-to-delivery-delta-audit` | 只更新受影响 REQ 和 run log |
| `delivery-batch-planning` | 当前批次任务已创建/更新，未开始实现 |
| `implement-tdd` | 每条 AC 有红绿记录，自检命令全绿 |
| `debug-systematic` | 原失败命令变绿，或明确升级强模型/人工 |
| `review-twostage-stage1` | 规范符合检查无 critical |
| `review-twostage-stage2` | 强模型或人工完成代码质量评审，无阻断 issue |
| `final-acceptance` | 交付范围内 REQ 均有验收证据或人工延期记录 |
