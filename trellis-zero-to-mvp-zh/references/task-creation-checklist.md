# 任务创建检查清单

用户确认只读分析后使用此清单。

## 创建任务前

- [ ] 已知源需求文档路径。
- [ ] 如存在 `.trellis/workflow.md`，已读取；如存在 `.trellis/config.yaml`、`.trellis/.version`、`.trellis/.developer`，已检查。
- [ ] 相关 `.trellis/spec/` 文件足够新，或已规划在实现任务前执行 spec 刷新/bootstrap 任务。
- [ ] 需求 ID 稳定。
- [ ] MVP 边界明确。
- [ ] 用户已确认任务拆分。
- [ ] 每个子任务都有验收标准。
- [ ] 每个子任务都有测试要求。
- [ ] 依赖关系明确。
- [ ] 每个子任务已标注复杂度（低/中/高），高复杂度任务已拆碎或在 PRD 里把每步定死。
- [ ] 每个子任务 PRD 的所有 `<...>` 占位符已替换为具体值，无"待定/视情况而定"。
- [ ] 每个子任务 PRD 含参考实现路径、文件清单、有序实现步骤、自检命令。
- [ ] 中/高复杂度子任务已按项目工作流和风险，包含或明确要求 `design.md`、`implement.md`、`implement.jsonl`、`check.jsonl`。
- [ ] 验收标准写成可机器校验或可逐条勾选的断言。

## 命令

```bash
python ./.trellis/scripts/task.py create "<parent title>" --slug <parent-slug>
python ./.trellis/scripts/task.py create "<child title>" --slug <child-slug> --parent "<parent-task-dir>"
```

如果 `task.py create` 报告未设置 developer，停止并要求用户先初始化 Trellis：

```bash
trellis init -u <name>
```

如果项目使用特定平台参数，一并加上，例如 `--codex`。

只有 Trellis CLI 不可用时，才使用旧版兜底方式：

```bash
python ./.trellis/scripts/init_developer.py <name>
```

或要求用户提供可用于 `--assignee` 的 assignee。

## 创建任务后

- [ ] 写入父任务 `prd.md`。
- [ ] 写入每个子任务 `prd.md`。
- [ ] 对复杂度/风险要求且项目工作流支持的子任务，写入或起草 `design.md`、`implement.md`、`implement.jsonl` 和 `check.jsonl`。
- [ ] 输出任务树。
- [ ] 输出按依赖排序的执行计划。
- [ ] 输出被阻塞任务列表。
- [ ] 输出可并行任务列表。
- [ ] 不要开始实现。
