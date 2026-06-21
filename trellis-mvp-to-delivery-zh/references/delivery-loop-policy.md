# 交付 Loop 策略

每轮 `trellis-mvp-to-delivery-zh` 开始前读取本策略，用于选择 loop 模式、审计范围、early-exit 行为和停止条件。

## Loop 模式

| 模式 | 名称 | 允许动作 | 人工门 |
| --- | --- | --- | --- |
| L1 | 只审计 | full/delta 差距审计、更新状态/日志、给出批次建议 | 创建任务前始终需要 |
| L2 | 辅助交付 | 创建/更新已确认的补缺任务，每轮一个批次，强制 worktree + verifier | 高风险、schema、auth、payment、security 必须 |
| L3 | 受控持续运行 | 在显式授权后按 L2 规则运行，必须 early-exit，每天最多一个批次 | 出现 critical 或范围变化时必须 |

`.trellis/delivery-state.md` 不存在时，默认使用 L1。

## 审计范围选择

使用 **full audit** 的情况：

- `.trellis/delivery-state.md` 不存在。
- 源需求文档发生变化。
- 缺少 `mvp_baseline_commit` 或 `last_audited_commit`。
- 最终验收失败。
- 用户要求重新设定基线。

使用 **delta audit** 的情况：

- 已存在交付状态文件。
- 源需求未变化。
- 自 `last_audited_commit` 后只变更实现文件、测试或相关 Trellis task。
- 未关闭缺口已有稳定的需求 ID 和 task 关联。

使用 **early exit** 的情况：

- 自 `last_audited_commit` 后没有相关文件变化。
- 未关闭 blocker 没变化。
- 补缺 task 状态没变化。
- 需求证据没变化。

early-exit 时，只向 `.trellis/delivery-run-log.jsonl` 追加 `outcome: "no-op"`，不要重跑 full audit，也不要创建任务。

## 批次限制

- 每轮最多批次：`1`
- 每轮最多补缺任务：`3`
- 每轮最多高风险任务：`1`
- 每个任务最多调试假设轮数：`3`
- 每个任务最多 verifier 失败次数：`2`
- 每个 REQ 最多 carry-over 轮数：`2`

## 停止并升级

出现以下情况时暂停 loop 并询问用户：

- 同一个 `REQ-*` 超过 2 轮没有状态推进。
- 同一个 task verifier 或 review 失败两次。
- `trellis-review-twostage-zh` 报告任何 critical。
- `trellis-debug-systematic-zh` 超过 3 轮假设/修复仍未变绿。
- task 需要改动 File Manifest 外的文件。
- 需求、schema、security、payment、auth 或 infrastructure 决策存在歧义。
- full audit 与 delivery state 对 DONE/PARTIAL/MISSING 状态判断冲突。

## 轮次上限

典型交付 loop 应在 3-6 个外层轮次内收敛。若 `current_round > max_rounds`，停止并建议重新切 scope、重新设基线或人工评审。
