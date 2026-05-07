# Bug 分类规则

在 MVP 到完整交付过程中，验证发现 bug 时使用这些规则。

## 分类输出

```markdown
## Bug Classification

- Bug:
- Affected Requirement IDs:
- Blocks current task: yes/no
- Recommended action:
  - fix in current task
  - create bug task
  - defer with documented risk

## Proposed Bug Task

- Title:
- Slug:
- Priority:
- Dependencies:
- Acceptance criteria:
- Tests required:
```

## 判断规则

1. 如果 bug 导致当前需求 ID 无法满足验收标准，就在当前任务中修复。
2. 如果 bug 与当前任务无关但影响最终交付，创建独立 bug task。
3. 如果 bug 涉及历史行为变化或产品歧义，记录风险并请求确认。
4. 不要把无关 bug 修复隐藏进当前功能任务。
5. 每个 bug 修复都必须包含回归测试，或记录不适合自动化的原因。
