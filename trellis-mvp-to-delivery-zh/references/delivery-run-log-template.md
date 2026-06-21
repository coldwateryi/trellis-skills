# 交付运行日志模板

每轮向 `.trellis/delivery-run-log.jsonl` 追加一个 JSON 对象。不要重写旧记录。

## JSONL 条目结构

```json
{
  "run_id": "2026-06-21T12:00:00Z",
  "skill": "trellis-mvp-to-delivery-zh",
  "mode": "L1",
  "round": 1,
  "audit_scope": "full",
  "baseline_commit": "abc123",
  "head_commit": "def456",
  "requirements_changed": 0,
  "open_gaps": 4,
  "tasks_created": 0,
  "tasks_updated": 0,
  "tasks_completed": 0,
  "critical_review_issues": 0,
  "debug_escalations": 0,
  "carry_over_requirements": 0,
  "tokens_estimate": 120000,
  "outcome": "audit-only",
  "next_action": "confirm-batch"
}
```

## Outcome 取值

- `audit-only`
- `batch-planned`
- `tasks-created`
- `tasks-updated`
- `no-op`
- `pause-human-needed`
- `final-acceptance-ready`
- `rebaseline-required`

## Token 预算默认值

- L1 只审计：最多 `120k` tokens/run
- L2 辅助批次：最多 `350k` tokens/run
- L3 受控 loop：最多 `500k` tokens/day
- 每天最多批次：`1`
- 每轮最多补缺任务：`3`
- 每个 REQ 最多 carry-over 轮数：`2`
