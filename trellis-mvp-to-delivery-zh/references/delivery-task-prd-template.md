# 交付任务 PRD 模板

## 填写规则（规划阶段必读）

此 PRD 由强模型在**规划阶段**填写，可能由能力有限的本地模型（如离线 qwen）在**执行阶段**照此实现。因此：

- 所有 `<...>` 占位符必须替换为**具体值**，禁止把占位符或"待定/视情况而定"留给执行阶段。
- 不要只描述"要实现什么行为"，要写清"改哪个文件、照抄哪个范例、按什么顺序做、怎么自检"。
- bug 分类、走哪条分支、用哪个注解等需要推理的判断，必须在规划阶段定死，执行阶段只做机械照搬。
- 如果某点无法在规划阶段定死，列入 `Out of Scope` 或拆成独立任务，不要交给执行模型自由发挥。

## 模板

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

## Reference Implementation（参考实现）

执行时优先照抄以下现有范例，仅按本任务替换实体/字段/命名：

- 后端范例：<现有可照抄的文件路径；无则写"无，按 Technical Notes 从零实现">
- 数据层范例：<现有 Mapper / SQL / 接口契约文件路径>
- 前端范例：<现有可照抄的页面/组件路径>
- 替换说明：<把范例里的 Xxx 替换为本任务的 Yyy，字段对照见 File Manifest>

## File Manifest（文件清单）

| 操作 | 文件路径 | 说明 |
| --- | --- | --- |
| 新建 | <path> | <这个文件干什么> |
| 修改 | <path> | <在哪里加什么> |

如涉及数据结构，附字段表：

| 字段 | 类型 | 约束 | 说明 |
| --- | --- | --- | --- |
| <name> | <type> | <非空/唯一/默认值> | <含义> |

## Implementation Steps（实现步骤）

按顺序执行，每步可独立验证。步骤必须具体到"做什么动作"，不要写成抽象目标：

1. <如：执行建表/迁移语句>
2. <如：照抄 Reference Implementation，按 File Manifest 替换实体与字段>
3. <如：在 <具体方法> 加入 <具体校验/分支逻辑>，定死走哪条分支>
4. <如：编译通过>

## Implementation Scope（行为约束）

- <要实现或验证的行为，写成可判定的断言>
- <边界条件：输入为空/超长/重复时的确切行为>
- <错误处理：失败时返回的确切错误码/消息>
- <兼容性或迁移备注>

## Acceptance Criteria（验收标准）

写成可机器校验或可逐条勾选的断言，避免"正确实现"这类主观表述：

- [ ] 上述需求 ID 达到预期状态。
- [ ] <构建/编译命令> 成功通过。
- [ ] <具体调用 + 入参> 返回 <确切预期>。
- [ ] <失败路径> 返回 <确切错误码与消息>。
- [ ] 除非明确要求变更，否则保留已有 MVP 行为。
- [ ] 添加或更新必要测试。
- [ ] lint、typecheck 和相关测试通过。

## Self-Check Commands（自检命令）

执行阶段每完成一步可运行的命令，用于本地确认，无需人工判断：

```bash
<如：mvn -pl <module> compile>
<如：mvn -pl <module> test -Dtest=<TestClass>>
<如：curl -X POST <url> -d '<payload>'  # 期望返回 ...>
```

## Automated Tests Required

### Unit Tests

- <测试点：被测方法 + 输入 + 期望输出>

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
- <任何无法在规划阶段定死、不应交给执行模型自由发挥的点>

## Forbidden（禁止事项）

给执行模型的负面约束，防止它擅自发挥：

- 不要新建已有的基类/工具类，必须复用 Reference Implementation 指向的现有实现。
- 不要改动 File Manifest 之外的文件。
- 不要引入未在 Technical Notes 列出的新依赖或新框架。
- <其他项目特定红线>

## Technical Notes

- 相关文件：
- 现有模式：
- 相关规范：
- 风险：
```
