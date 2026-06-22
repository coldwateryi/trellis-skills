# 路由策略

## 阶段选择表

| 项目状态 | 下一阶段 | 调用 skill |
| --- | --- | --- |
| 有需求文档，无 `.trellis/tasks/` 或无 MVP 任务树 | `zero-to-mvp-readonly` | `trellis-zero-to-mvp-zh` |
| `zero-to-mvp` 只读分析已输出，用户已确认范围 | `zero-to-mvp-create-tasks` | `trellis-zero-to-mvp-zh` |
| MVP 已完成，无 `.trellis/delivery-state.md` | `mvp-to-delivery-full-audit` | `trellis-mvp-to-delivery-zh` |
| 已有 delivery state，需求文档变化 | `mvp-to-delivery-full-audit` | `trellis-mvp-to-delivery-zh` |
| 已有 delivery state，需求未变，有相关代码/测试/task 变化 | `mvp-to-delivery-delta-audit` | `trellis-mvp-to-delivery-zh` |
| 已有 delivery state，需求未变，且无相关变化 | `early-exit` | `trellis-mvp-to-delivery-zh` |
| 有 confirmed current_batch，但还没有创建/更新补缺任务 | `delivery-batch-planning` | `trellis-mvp-to-delivery-zh` |
| 有 ready 子任务，依赖满足，未开始实现 | `implement-tdd` | `trellis-implement-tdd-zh` |
| TDD 或自检命令失败，失败信号稳定 | `debug-systematic` | `trellis-debug-systematic-zh` |
| 子任务 AC 全绿，自检全绿，未评审 | `review-twostage-stage1` | `trellis-review-twostage-zh` |
| Stage 1 通过，尚未完成代码质量评审 | `review-twostage-stage2` | `trellis-review-twostage-zh` |
| 所有 P0/P1 缺口 DONE 或人工延期 | `final-acceptance` | `trellis-mvp-to-delivery-zh` |
| 范围、schema、auth、payment、infra 或安全决策不清晰 | `pause-human-needed` | 无 |

## 路由原则

- 每次只选择一个下一阶段。
- 当多个阶段都可能适用时，优先处理最早的未通过安全门。
- MVP 后的 full/delta/early-exit 判定读取 `delivery-loop-routing.md`。
- 不基于聊天记忆判断完成状态，必须读取文件证据。
- 有失败信号时，先调试，不继续实现新 AC。
- 有 critical review issue 时，先修复标注项，不推进任务状态。
- 需要强模型判断但当前不可用时，暂停并输出 evidence pack。

## Evidence Pack

暂停等待强模型或人工时，输出：

- 任务目录。
- 需求和 AC 编号。
- 相关 `prd.md`、`design.md`、`implement.md`、`check.jsonl` 路径。
- 当前 diff 摘要。
- 已运行命令和结果。
- 失败日志或评审 issue。
- 建议下一阶段。
