# 小模型长程安全规范（MVP 到交付）

用于本地小/中参数模型执行多轮 MVP 交付审计时降低幻觉、漂移和自证通过。

## Stage State Packet

每次进入新阶段、恢复上下文、调用子代理、写入 `delivery-state.md` 前，都先输出并复核本状态包：

```yaml
stage_state:
  state: S0_LOAD_STATE | S1_DETERMINE_LOOP | S2_DISCOVER_EVIDENCE | S3_GAP_AUDIT | S4_UPDATE_STATE | S5_PICK_BATCH | S6_CONFIRM | S7_CREATE_TASKS | S8_RUN_LOG | S9_PLAN_TESTS | S10_FINAL_ACCEPTANCE
  loop_mode: L1 | L2 | L3
  audit_scope: full | delta | early-exit
  current_round: <n>
  max_rounds: <n>
  open_gaps: <n>
  tasks_created: <n>
  tasks_completed: <n>
  carry_over: <n>
  critical_review_issues: <n>
  next_legal_action: <one action>
  stop_conditions:
    - <none or condition>
```

规则：
- `next_legal_action` 只能有一个。
- `stop_conditions` 非空时停止 loop。

## Context Budget Table

| 阶段 | 预算 | 策略 |
|:---|:---|:---|
| S0 加载状态 | ≤4K tokens | 读 `.trellis/delivery-state.md` + `delivery-loop-policy.md` |
| S1 判断 Loop | ≤4K tokens | 只判断 full/delta/early-exit，不读取代码 |
| S2 发现证据 | ≤12K tokens | 读源需求 + 关键代码结构 + `.trellis/tasks/` |
| S3 差距审计 | ≤15K tokens | 输出 RTM + 自我评审，写完即写文件 |
| S4 更新状态 | ≤4K tokens | 写 `delivery-state.md` |
| S5 选择批次 | ≤4K tokens | 读 `delivery-batch-template.md` |
| S6 确认 | ≤4K tokens | 只展示汇总 |
| S7 创建任务 | ≤6K tokens | 一次一个任务 |
| S8 运行日志 | ≤2K tokens | 追加一行 JSON |
| S9 测试规划 | ≤8K tokens | 读 `test-coverage-matrix-template.md` |
| S10 验收 | ≤8K tokens | 读 `final-acceptance-template.md` |

### 阶段满载警告

- S3 审计超过 8 个需求且中间结果未写入文件 → 先写文件再继续
- 单轮审计后存在超过 5 个 open gap 但未选批次 → 先冻结批次
- 自审连续 2 轮相同问题未修复 → `STALLED_CONVERGENCE`，停止

## Evidence Discipline

以下结论必须有证据路径或命令输出摘要：
- 需求追踪矩阵中每条需求的状态判定
- DONE 需求的代码和测试证据
- MVP 完成度百分比
- 依赖关系和阻塞原因

禁止：
- 用"已检查""看起来一致""应当没问题"作为证据
- 无本地证据时自创完成度百分比
- 在存在 critical review issue 时继续推进

## Drift Reset

出现以下情况时立即重建 Stage State Packet：
- 需求状态在未修改时变化
- carry-over count 与上次不一致
- loop_mode 在无用户确认时变化
- 任务创建数可 batch 规则不一致

重建时只读取：`delivery-state.md`、`delivery-run-log.jsonl`、源需求、已有任务目录。

## 阶段原子检查清单

### S0 加载状态
- [ ] `.trellis/delivery-state.md` 已读取（存在时）或计划初始化
- [ ] `delivery-loop-policy.md` 已读取
- [ ] Level 1 参考文件已读取

### S1 判断 Loop 模式
- [ ] loop_mode 已确定（L1/L2/L3）
- [ ] audit_scope 已确定（full/delta/early-exit）
- [ ] 首次运行始终为 L1 + full audit

### S2 发现证据
- [ ] 源需求文档已定位
- [ ] `.trellis/tasks/` 已完成任务已读取
- [ ] 已有 `.trellis/delivery-state.md` 和 `.trellis/delivery-run-log.jsonl` 已读取（存在时）

### S3 差距审计（重点）
- [ ] RTM 中每条需求有明确状态（DONE/PARTIAL/MISSING/UNTESTED/UNCLEAR）
- [ ] DONE 需求有代码和测试证据
- [ ] 覆盖率百分比由机械统计得出
- [ ] 所有 open gap 有精准描述
- [ ] 累计 carry-over 有计数
- [ ] 不存在未解占位符

### S4 更新状态
- [ ] `delivery-state.md` 已写入/更新
- [ ] `current_round` 已递增
- [ ] `Next Loop Recommendation` 已设置

### S5 选择批次
- [ ] 每轮最多 3 个补缺任务
- [ ] 每轮最多 1 个高风险任务
- [ ] 未创建未经确认的任务

## 单调收敛保护

如果审计循环连续 2 轮发现完全相同的问题且未修复：
1. 输出 `STALLED_CONVERGENCE`
2. 停止当前路径
3. 建议用户换强模型或人工介入
4. 记录已在哪些轮次尝试修复