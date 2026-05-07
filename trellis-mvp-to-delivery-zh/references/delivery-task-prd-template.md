# 交付任务 PRD 模板

```markdown
# <任务标题>

## Requirement IDs

- REQ-001
- AC-001

## Goal

关闭这些需求已验证的缺口，不扩大无关范围。

## Current Gap

- 当前状态：<DONE/PARTIAL/MISSING/UNTESTED/UNCLEAR>
- 证据：
  - 代码：
  - 测试：
- 缺口：
- 风险：

## Implementation Scope

- <要实现或测试的行为>
- <边界条件>
- <错误处理>
- <兼容性或迁移备注>

## Acceptance Criteria

- [ ] 上述需求 ID 达到预期状态。
- [ ] 除非明确要求变更，否则保留已有 MVP 行为。
- [ ] 添加或更新必要测试。
- [ ] lint、typecheck 和相关测试通过。

## Automated Tests Required

### Unit Tests

- <测试点>

### Integration Tests

- <测试点>

### Regression Tests

- <测试点>

### E2E / Smoke Tests

- <测试点>

### Manual Verification

- <仅在不适合自动化时填写，并说明原因>

## Dependencies

- Depends on:
  - <task slug or none>
- Reason:
  - <依赖原因>

## Unlocks

- <完成后解锁的任务>

## Out of Scope

- <明确排除项>

## Technical Notes

- 相关文件：
- 现有模式：
- 相关规范：
- 风险：
```
