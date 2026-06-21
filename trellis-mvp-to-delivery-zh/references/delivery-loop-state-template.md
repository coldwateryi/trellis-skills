# 交付 Loop 状态模板

首次运行 `trellis-mvp-to-delivery-zh` 时，将本模板复制为 `.trellis/delivery-state.md`。每轮交付 loop 结束时更新它。此文件是 MVP 到完整交付多轮运行的持久记忆主干。

## 基线

- source_requirements: `<path>`
- mvp_baseline_commit: `<git-sha>`
- last_audited_commit: `<git-sha>`
- loop_mode: `L1`
- current_round: `1`
- max_rounds: `6`
- current_batch_id: `<none-or-batch-id>`

## 需求状态

| REQ ID | 状态 | 实现证据 | 测试证据 | 补缺任务 | 最近变化轮次 | Carry-over 次数 |
| --- | --- | --- | --- | --- | --- | --- |
| REQ-001 | DONE/PARTIAL/MISSING/UNTESTED/UNCLEAR | `<path-or-none>` | `<path-or-none>` | `<task-or-none>` | 1 | 0 |

## 当前批次

- batch_id: `<delivery-batch-001>`
- scope: `<P0 基础缺口 / P1 核心行为 / 回归闭环 / 最终验收>`
- selected_reqs:
  - `<REQ-xxx>`
- excluded_this_round:
  - `<REQ-yyy>: <原因>`

## 阻塞项

| 条目 | 原因 | 需要人工提供什么 | 起始轮次 |
| --- | --- | --- | --- |
| `<REQ-xxx or task>` | `<阻塞原因>` | `<需要确认的决策或输入>` | 1 |

## 人工决策

- `<date>`: `<决策及其范围影响>`

## 预算快照

- max_batches_per_day: `1`
- max_gap_tasks_per_run: `3`
- max_high_risk_tasks_per_run: `1`
- max_carry_over_rounds_per_req: `2`
- max_verifier_failures_per_task: `2`

## 下一轮建议

- action: `continue-next-batch | early-exit | pause-human-needed | run-final-acceptance | rebaseline-required`
- reason: `<具体原因>`
- next_audit_scope: `full | delta | none`
