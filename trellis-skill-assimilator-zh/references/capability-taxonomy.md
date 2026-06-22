# 能力分类

## 命名

使用 `CAP-<DOMAIN>-<ACTION>`，例如：

- `CAP-REQ-TRACEABILITY`
- `CAP-PLAN-SELF-REVIEW`
- `CAP-EXEC-TDD-LOOP`
- `CAP-DEBUG-SYSTEMATIC`
- `CAP-REVIEW-TWOSTAGE`
- `CAP-CONTEXT-FRESH-GATE`
- `CAP-CODE-SIMPLIFY-PASS`
- `CAP-STATE-RUN-LOG`
- `CAP-ARCH-DECISION-ARCHIVE`
- `CAP-SKILL-UPDATE-SCAN`

## 分类

| Domain | Meaning | Trellis stage |
| --- | --- | --- |
| REQ | 需求追踪、验收标准、RTM | planning / audit |
| PLAN | 任务拆分、设计左移、自评循环 | zero-to-mvp / mvp-to-delivery |
| EXEC | 实现纪律、TDD、文件边界 | implement-tdd |
| DEBUG | 复现、定位、假设、最小修复 | debug-systematic |
| REVIEW | 规范符合、代码质量、评审门 | review-twostage |
| CONTEXT | fresh context、防上下文腐化 | controller / shared policy |
| STATE | 状态文件、run log、delta audit | delivery-controller / mvp-to-delivery |
| ARCH | 架构档案、决策记录、结构健康 | planning artifacts / spec |
| SKILL | skill 吸收、更新扫描、治理 | skill-assimilator |

## 选择原则

- 一个能力只归入一个主 domain。
- 跨阶段能力拆成多个 capability。
- 能力名称描述行为，不描述来源项目。
- 来源项目只记录在 absorption card 中。
