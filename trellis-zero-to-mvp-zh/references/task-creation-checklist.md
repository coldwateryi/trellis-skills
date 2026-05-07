# 任务创建检查清单

用户确认只读分析后使用此清单。

## 创建任务前

- [ ] 已知源需求文档路径。
- [ ] 需求 ID 稳定。
- [ ] MVP 边界明确。
- [ ] 用户已确认任务拆分。
- [ ] 每个子任务都有验收标准。
- [ ] 每个子任务都有测试要求。
- [ ] 依赖关系明确。

## 命令

```bash
python ./.trellis/scripts/task.py create "<parent title>" --slug <parent-slug>
python ./.trellis/scripts/task.py create "<child title>" --slug <child-slug> --parent "<parent-task-dir>"
```

如果 `task.py create` 报告未设置 developer，停止并要求用户运行：

```bash
python ./.trellis/scripts/init_developer.py <name>
```

或要求用户提供可用于 `--assignee` 的 assignee。

## 创建任务后

- [ ] 写入父任务 `prd.md`。
- [ ] 写入每个子任务 `prd.md`。
- [ ] 输出任务树。
- [ ] 输出按依赖排序的执行计划。
- [ ] 输出被阻塞任务列表。
- [ ] 输出可并行任务列表。
- [ ] 不要开始实现。
