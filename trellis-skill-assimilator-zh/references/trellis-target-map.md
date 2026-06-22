# Trellis 落点映射

| Capability Type | Primary Target | Allowed Artifact |
| --- | --- | --- |
| 需求追踪 / RTM | `trellis-zero-to-mvp-zh` / `trellis-mvp-to-delivery-zh` | analysis/gap templates, checklist |
| MVP 后审计 | `trellis-mvp-to-delivery-zh` | gap audit, delivery state, run log |
| 阶段路由 / 自动推进 | `trellis-delivery-controller-zh` | route policy, gates, model policy |
| TDD 实现 | `trellis-implement-tdd-zh` | TDD protocol, progress template |
| 系统调试 | `trellis-debug-systematic-zh` | debug protocol, debug report |
| 评审门 | `trellis-review-twostage-zh` | stage checklists, report template |
| 设计左移 | planning references | `design.md`, `implement.md`, JSONL context templates |
| 架构档案 | `.trellis/spec/` guidance | planning artifact templates, final acceptance |
| 外部能力吸收 | `trellis-skill-assimilator-zh` | absorption card, update scan policy |
| 评测 | future `evaluation/` | scenario, expected output, regression note |

## 不允许的落点

- 不把外部项目说明直接塞进主 `SKILL.md`。
- 不在执行期 skill 中加入规划期判断。
- 不在 `mvp-to-delivery` 中继续扩大阶段路由职责。
- 不把 license 风险内容写进模板正文供模型复用。

## 修改级别

| Level | Meaning | User confirmation |
| --- | --- | --- |
| L0 | 只生成 absorption card | 不需要 |
| L1 | 新增 reference/checklist 条目 | 建议确认 |
| L2 | 修改现有 workflow 或 SKILL.md | 必须确认 |
| L3 | 改安装脚本、默认入口或状态格式 | 必须确认并增加验证场景 |
