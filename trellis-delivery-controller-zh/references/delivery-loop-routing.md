# Delivery Loop 路由

## 职责边界

控制器负责判断是否进入 full audit、delta audit、early-exit、batch planning 或 final acceptance。`trellis-mvp-to-delivery-zh` 负责执行已选定阶段：产出差距矩阵、更新 delivery state/run log、规划批次、创建/更新补缺任务和最终验收。

如果用户直接调用 `trellis-mvp-to-delivery-zh`，该 skill 可以按自己的 `references/delivery-loop-policy.md` 做 standalone 判定；如果用户调用控制器，则以本文件的路由结果为准。

## Loop 模式

| 模式 | 名称 | 控制器判定 | 允许动作 |
| --- | --- | --- | --- |
| L1 | 只审计 | 首次 MVP 后审计，或用户要求只读审计 | full/delta 审计、状态/日志更新、批次建议 |
| L2 | 辅助交付 | 用户确认差距矩阵和当前批次后 | 创建/更新本批次补缺任务，要求 verifier/review 门 |
| L3 | 受控持续运行 | 用户显式授权自动推进到安全门 | 按 L2 规则推进，遇安全门必须暂停 |

`.trellis/delivery-state.md` 不存在时，默认进入 `L1 + full audit`。

## 审计范围

### Full Audit

进入 full audit 的条件：

- `.trellis/delivery-state.md` 不存在。
- 源需求文档变化。
- 缺少 `mvp_baseline_commit` 或 `last_audited_commit`。
- 最终验收失败，需要重新对齐完整需求矩阵。
- 用户要求重新设定基线。

### Delta Audit

进入 delta audit 的条件：

- `.trellis/delivery-state.md` 已存在。
- 源需求未变化。
- `last_audited_commit` 之后存在相关代码、测试或 Trellis task 变化。
- open gaps 已有稳定 `REQ-*` 和 task 关联。

### Early Exit

进入 early-exit 的条件：

- 源需求未变化。
- `last_audited_commit` 之后没有相关代码、测试或 task 变化。
- blocker、人工决策和 current batch 均无变化。

early-exit 只允许追加 run log，不允许重跑 full audit，也不允许创建任务。

## 批次路由

- L1 只推荐批次，不创建任务。
- L2/L3 每轮只处理一个 confirmed/current batch。
- 每轮最多 3 个补缺任务。
- 每轮最多 1 个高风险任务。
- 最终验收必须单独成批。

## 停止条件

出现以下情况，控制器必须输出 `pause-human-needed`：

- 同一 `REQ-*` 连续 2 轮无进展。
- verifier 连续失败 2 次。
- review 出现 critical。
- 调试超过 3 轮仍未变绿。
- 需要改 File Manifest 外文件。
- 需求、schema、auth、payment、security 或 infrastructure 决策不清晰。
- full audit 结果与 delivery state 的状态判断冲突。
