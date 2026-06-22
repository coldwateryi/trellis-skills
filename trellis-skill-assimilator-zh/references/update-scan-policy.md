# Update Scan 策略

## 输入

- Source URL。
- Current ref。
- Last analyzed ref。
- 上一版 absorption card 或 absorbed capability 列表。

## 扫描范围

只关注 `last_analyzed_ref` 之后变化的：

- README / docs。
- `SKILL.md`。
- references。
- scripts。
- license。
- release notes 或 changelog。

## Delta 输出

| Change | Impact | Action |
| --- | --- | --- |
| 新增 skill | 可能新增 capability | 生成候选 capability |
| 修改 workflow | 可能影响已吸收能力 | 标记 review |
| 修改 license | 可能影响安全边界 | 标记 needs-human-review |
| 新增 script | 可能启发自动化 | 只分析目的，不搬运 |
| 删除能力 | 可能说明设计回退 | 评估 Trellis 是否需要调整 |

## 决策

- `no-op`: 没有值得吸收的变化。
- `watch`: 有变化但不适合当前 Trellis。
- `absorb-candidate`: 值得吸收，但需要用户确认和验证场景。
- `risk-review`: license、安全或架构风险需要人工判断。

## 更新记录

每次 update-scan 输出：

- `last_analyzed_ref`。
- `current_ref`。
- changed files summary。
- new/changed/rejected capabilities。
- recommended next scan trigger。
