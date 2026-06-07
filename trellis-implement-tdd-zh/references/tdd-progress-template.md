# TDD 进度表模板

载入任务后，把 `prd.md` 的每条 AC 抽成一行。全程回写状态，确保"一次只一条 AC 在进行中"。

## 进度表

| AC ID | 期望可观察结果 | 测试文件 | 测试命令 | 状态 | 备注 |
| --- | --- | --- | --- | --- | --- |
| AC-001 | <输入 X → 返回 Y> | <test path> | <command> | red / green / done | <如触发过调试> |
| AC-002 | <失败路径 → 错误码 Z> | <test path> | <command> | pending | |

状态取值：

- `pending` —— 尚未开始
- `red` —— 已写失败测试并看到红，正在写实现
- `green` —— 测试已通过，正在跑自检
- `done` —— 自检全绿、无回归、已暂存

## 收尾核对

- [ ] 所有 AC 状态为 `done`。
- [ ] 无任何 AC 停留在 `red` / `green`。
- [ ] `prd.md` 自检命令全集最后一次运行全绿。
- [ ] `design.md` 挂载点清单逐项已接线（若有）。
- [ ] 未 commit；改动已暂存，等待 `trellis-review-twostage-zh`。
