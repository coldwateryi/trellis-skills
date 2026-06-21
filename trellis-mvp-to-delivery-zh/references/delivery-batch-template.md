# 交付批次模板

每轮 `trellis-mvp-to-delivery-zh` 只规划一个交付批次。将批次信息写入 `.trellis/delivery-state.md`，必要时也写入对应任务 PRD。

## 批次元数据

- batch_id: `<delivery-batch-001>`
- round: `<number>`
- priority: `P0 | P1 | P2 | P3`
- risk: `low | medium | high`
- mode: `L1 | L2 | L3`
- audit_scope: `full | delta`

## 纳入本批次的缺口

| REQ ID | 缺口 | 计划任务 | 纳入原因 | 风险 |
| --- | --- | --- | --- | --- |
| REQ-001 | `<具体缺口>` | `<task slug>` | `<依赖、优先级或阻塞原因>` | low/medium/high |

## 本轮排除的缺口

| REQ ID | 原因 |
| --- | --- |
| REQ-002 | `<延期原因>` |

## 批次限制

- max_gap_tasks: `3`
- max_high_risk_tasks: `1`
- worktree_required: `true`
- verifier_required: `true`
- max_fix_attempts_per_task: `2`
- max_debug_rounds_per_task: `3`

## 排序规则

- 当基础契约、业务行为、UI 展示和最终验证依赖不同，不要放在同一批次。
- P0 foundation/API/schema 缺口先于 P1 业务行为。
- 最终验收单独成批，依赖所有 P0/P1 缺口 DONE 或被人工明确延期。
- Test-only 的 `UNTESTED` 缺口只有在保护同一功能区域时才能同批。

## 停止条件

- 出现任何 critical review issue。
- verifier 两次失败。
- 同一需求 reopen 两次。
- 出现人工 blocker。
- task 需要改动 File Manifest 外的文件。

## 下一步动作

- action: `create-tasks | update-existing-tasks | continue-existing-batch | early-exit | pause-human-needed | final-acceptance`
- reason: `<具体原因>`
