# Trellis Skills 项目分析报告

生成时间: 2026-06-06（仓库状态段已刷新）

## 一、项目概览

### 1.1 项目定位
Trellis Skills 是一套面向 Codex CLI 以及其他支持 skill 的 CLI 工具的工作流技能集，覆盖从原始需求文档到完整交付的全生命周期管理。

### 1.2 核心价值
- **需求到交付的完整流程**: 分析 → 规划 → 追踪 → 审计 → 补缺 → 验收
- **双语支持**: 提供中英文双版本技能
- **规范化方法论**: 标准化的需求追踪、任务拆分和验收流程
- **面向弱模型优化**: PRD 设计考虑了执行阶段可能使用能力有限的本地模型（如离线 qwen）

### 1.3 技能组成

| 技能名称 | 语言 | 阶段 | 核心功能 |
| --- | --- | --- | --- |
| `trellis-zero-to-mvp` | 英文 | Phase 1 | 从需求文档生成 MVP 任务树 |
| `trellis-zero-to-mvp-zh` | 中文 | Phase 1 | 同上（中文版本） |
| `trellis-mvp-to-delivery` | 英文 | Phase 2 | MVP 差距审计与完整交付规划 |
| `trellis-mvp-to-delivery-zh` | 中文 | Phase 2 | 同上（中文版本） |

## 二、架构设计分析

### 2.1 目录结构

以下结构图用于说明阶段划分和主要产物，省略了部分新增的自我评审 reference 文件。

```
trellis-skills/
├── README.md                      # 中文说明文档
├── README_EN.md                   # 英文说明文档
├── LICENSE                        # MIT 许可证
│
├── trellis-zero-to-mvp/          # Phase 1: 英文版
│   ├── SKILL.md                  # 技能定义与工作流
│   ├── agents/
│   │   └── openai.yaml           # Agent 接口配置
│   └── references/               # 参考模板
│       ├── analysis-output-template.md      (77 行)
│       ├── parent-prd-template.md           (59 行)
│       ├── child-prd-template.md            (142 行)
│       └── task-creation-checklist.md       (42 行)
│
├── trellis-zero-to-mvp-zh/       # Phase 1: 中文版
│   └── （结构同上）
│
├── trellis-mvp-to-delivery/      # Phase 2: 英文版
│   ├── SKILL.md
│   ├── agents/
│   │   └── openai.yaml
│   └── references/
│       ├── gap-audit-template.md                    (65 行)
│       ├── delivery-task-prd-template.md            (148 行)
│       ├── test-coverage-matrix-template.md         (36 行)
│       ├── final-acceptance-template.md             (45 行)
│       └── bug-classification-rules.md              (34 行)
│
└── trellis-mvp-to-delivery-zh/   # Phase 2: 中文版
    └── （结构同上）
```

### 2.2 设计原则

#### 2.2.1 核心约束
1. **先分析，后行动**: 所有技能的第一轮均为只读分析，不在用户确认前创建任务或编写代码
2. **按能力拆分**: 按可独立验收的业务或技术能力拆任务，不按文件拆任务
3. **稳定 ID 机制**: 需求编号（REQ-xxx）和验收标准编号（AC-xxx）在分析阶段确定后保持不变
4. **显式依赖管理**: 父子任务仅表达结构，真正的执行依赖写在每个子任务的 PRD 中

#### 2.2.2 弱模型适配策略
项目的一个重要特点是考虑到执行阶段可能使用能力有限的本地模型：

**规划阶段责任（强模型）**:
- 消除所有 `<...>` 占位符
- 定死所有需要推理判断的点（注解选择、分支逻辑、命名、表结构等）
- 提供具体文件路径、可照抄的现有范例、有序实现步骤
- 提供可机器校验的验收断言和自检命令

**执行阶段责任（可能是弱模型）**:
- 机械照搬 PRD 中的指示
- 不做自由发挥和推理判断

**任务粒度策略**:
- 低复杂度：标准 CRUD、配置、有现成范例 → 弱模型可独立完成
- 中复杂度：少量业务校验或跨表逻辑 → 需详细 PRD
- 高复杂度：复杂事务、并发、跨模块一致性 → 进一步拆分或在 PRD 中把每步定死

## 三、工作流分析

### 3.1 Phase 1: Zero to MVP

#### 工作流程
1. **发现输入** → 读取需求文档、README、现有代码结构
2. **只读分析** → 生成需求追踪矩阵、模块依赖图、任务拆分
3. **确认范围** → 请求用户确认任务拆分和 MVP 边界
4. **创建任务树** → 创建父任务和子任务，写入 PRD
5. **汇报下一步** → 输出任务树和推荐执行顺序

#### 关键产出物
- **Requirements Traceability Matrix**: 每个需求的当前状态（DONE/PARTIAL/MISSING/UNTESTED/UNCLEAR）
- **Module Dependency Graph**: 模块职责、依赖关系和风险
- **Task Split**: 按能力拆分的任务清单（标注类型、依赖、优先级、复杂度）
- **Parent PRD**: 整体项目 PRD
- **Child PRDs**: 每个子任务的详细执行规格

#### 优先级规则
- P0: 阻塞其他模块或核心正确性
- P1: 核心业务闭环
- P2: 体验、报表、通知、增强能力
- P3: 非必要优化

#### 排序规则
1. 数据结构、API 契约和配置优先
2. 阻塞其他模块的任务优先
3. 高风险和未知多的任务提前验证
4. UI 打磨、文档和体验增强靠后
5. 互相依赖的任务不能标记为可并行

### 3.2 Phase 2: MVP to Delivery

#### 工作流程
1. **发现证据** → 读取需求文档、MVP 代码、测试、已有任务
2. **只读差距审计** → 对照需求逐条检查实现和测试证据
3. **确认交付计划** → 请求用户确认差距审计和任务计划
4. **创建补缺任务** → 为每组相关缺口创建任务
5. **规划测试闭环** → 映射每个需求到测试类型
6. **执行最终验收** → 所有功能任务完成后的验收
7. **分类 Bug** → 判断修复、创建独立任务或延期

#### 关键产出物
- **Gap Audit Report**: 包含需求追踪矩阵和完成度摘要
- **Delivery Task Plan**: 按依赖排序的补缺任务计划
- **Test Coverage Matrix**: 每个需求映射到测试类型（unit/integration/e2e/smoke/regression）
- **Final Acceptance Report**: 最终验收结果
- **Bug Classification**: 发现的缺陷分类和处理建议

#### 证据规则
- DONE: 必须有实现证据和测试证据
- UNTESTED: 必须有实现证据和明确测试缺口
- PARTIAL: 必须说明哪些已完成、哪些缺失
- MISSING: 没有实现证据或只有无关脚手架
- UNCLEAR: 必须给出阻塞问题或歧义说明

## 四、PRD 模板分析

### 4.1 Child PRD Template 结构（Zero to MVP）

```markdown
# <任务标题>

## Requirement IDs
## Goal
## Current Gap
## Reference Implementation（参考实现）
## File Manifest（文件清单）
## Implementation Steps（实现步骤）
## Requirements（行为约束）
## Acceptance Criteria（验收标准）
## Self-Check Commands（自检命令）
## Automated Tests Required
## Dependencies
## Unlocks
## Out of Scope
## Forbidden（禁止事项）
## Technical Notes
```

### 4.2 Delivery Task PRD Template 结构（MVP to Delivery）

结构与 Child PRD 基本相同，但增加了更多细节：
- Goal: 明确"关闭这些需求已验证的缺口，不扩大无关范围"
- Current Gap: 更详细的当前状态、证据、缺口和风险说明
- Implementation Scope: 替代 Requirements，更强调行为约束

### 4.3 PRD 设计亮点

#### 4.3.1 Reference Implementation（参考实现）
- 后端范例：现有可照抄的文件路径
- 数据层范例：现有 Mapper/SQL/接口契约
- 前端范例：现有页面/组件路径
- 替换说明：明确如何从范例映射到当前任务

**优势**: 通过"照抄+替换"模式大幅降低执行难度，特别适合弱模型。

#### 4.3.2 File Manifest（文件清单）
- 明确列出每个要操作的文件
- 标注新建/修改操作
- 精确到路径，说明目的

**优势**: 执行阶段无需推理"改哪些文件"，只需机械执行。

#### 4.3.3 Self-Check Commands（自检命令）
- 提供可直接运行的验证命令
- 附带期望结果说明
- 无需人工判断

**优势**: 使弱模型也能进行自我验证。

#### 4.3.4 Forbidden（禁止事项）
- 不要新建已有的基类/工具类
- 不要改动 File Manifest 之外的文件
- 不要引入未列出的新依赖或新框架

**优势**: 防止弱模型"擅自发挥"，保持实现可控。

## 五、当前状态分析

### 5.1 运行时仓库状态说明

Git 分支、最近提交和工作区是否干净都属于**运行时信息**，不适合静态写死在分析报告里。查看当前真实状态时，应以实时命令输出为准：

- `git status --short --branch`
- `git log --oneline -5`

本文档不再维护“未提交更改列表”，以避免文档在后续提交和评审后迅速过期。

### 5.2 文件统计（2026-06-06 刷新）

**Git 跟踪文件数**: 44

**Markdown 文件数**: 39
- 2 个 README
- 4 个 SKILL.md
- 26 个 reference 模板文件
- 7 个 `doc/` 文档

**YAML 文件数**: 4
- 4 个 `agents/openai.yaml`

**其他文件**: 1
- `LICENSE`

**模板文件规模**:
- 最小: `bug-classification-rules.md` (34 行)
- 最大: `delivery-task-prd-template.md` (148 行)
- 覆盖阶段: Zero to MVP（12 个 reference 模板）+ MVP to Delivery（14 个 reference 模板）

## 六、优势分析

### 6.1 方法论优势
1. **双阶段设计**: 只读分析 + 确认执行，避免误操作
2. **追溯性强**: 稳定的 REQ/AC ID 机制保证需求可追踪
3. **状态清晰**: 5 种明确的需求状态（DONE/PARTIAL/MISSING/UNTESTED/UNCLEAR）
4. **依赖显式**: 不依赖父子任务关系，在 PRD 中明确写依赖

### 6.2 工程化优势
1. **模板驱动**: 所有产出物都有标准模板，保证输出一致性
2. **可自动化**: PRD 包含自检命令，支持 CI/CD 集成
3. **弱模型友好**: PRD 设计充分考虑执行模型能力限制
4. **双语支持**: 中英文版本并行，扩大适用范围

### 6.3 协作优势
1. **人机协作**: 强模型规划 + 弱模型执行，充分利用各自优势
2. **验收标准机械化**: 避免主观判断，减少理解偏差
3. **禁止事项清单**: 明确边界，防止"过度发挥"

## 七、潜在问题与改进建议

### 7.1 发现的问题

#### 7.1.1 文档问题
1. **agents/openai.yaml 功能不明确**: 文件仅包含接口描述，缺少实际的 agent 配置逻辑
2. **缺少使用示例**: README 中有使用场景描述，但缺少完整的端到端示例
3. **缺少架构图**: 文字描述较多，缺少直观的流程图或架构图

#### 7.1.2 工程问题
1. **缺少文档一致性校验**: 路径迁移、命令示例和状态型报告容易在后续迭代中失真
2. **缺少测试**: 项目是技能集，但没有验证技能本身正确性的测试
3. **缺少版本管理**: SKILL.md 没有版本号字段

#### 7.1.3 功能缺口
1. **缺少增量更新支持**: 需求变更后如何更新已有任务树？
2. **缺少任务状态同步**: 如何将执行状态反馈到需求追踪矩阵？
3. **缺少冲突检测**: 多人协作时如何检测需求 ID 冲突？

### 7.2 改进建议

#### 7.2.1 立即可做
1. **减少静态 Git 状态描述**: 将动态仓库状态改为实时命令说明，避免报告快速过期
2. **添加 CHANGELOG.md**: 记录版本变更历史
3. **完善 agents/openai.yaml**: 补充完整的 agent 配置示例
4. **添加端到端示例**: 在 `examples/` 目录下提供完整的使用示例

#### 7.2.2 短期改进
5. **添加流程图**: 在 README 中添加 Mermaid 流程图
6. **版本管理**: 在 SKILL.md 中添加 `version` 字段
7. **集成测试**: 创建测试脚本验证技能定义的完整性
8. **状态同步机制**: 设计从任务状态到需求追踪矩阵的自动同步方案

#### 7.2.3 长期规划
9. **增量更新支持**: 设计需求变更时的任务树更新策略
10. **协作冲突检测**: 实现需求 ID 和任务 slug 的冲突检测
11. **度量指标**: 添加任务完成度、测试覆盖率等度量能力
12. **IDE 插件**: 为 VS Code 等 IDE 提供技能调用插件

## 八、技术栈与依赖

### 8.1 核心依赖
- **Codex CLI**: 技能执行环境
- **Trellis**: 任务管理系统（需要 `.trellis/` 目录；0.6 beta 项目应优先读取 `.trellis/workflow.md`、`.trellis/config.yaml`、`.trellis/.version`）
- **Python**: 用于 Trellis 脚本（task.py；init_developer.py 仅作为旧版兜底）

### 8.2 前置条件
1. 已安装 Codex CLI 或其他支持 skill 的 CLI 工具
2. 项目中已初始化 Trellis（存在 `.trellis/` 目录）
3. 首次使用前优先运行 `trellis init -u <name>`，按项目需要添加平台参数；Trellis CLI 不可用时，再使用 `python ./.trellis/scripts/init_developer.py <name>` 兜底

### 8.3 文件格式标准
- **Markdown**: 所有文档和模板
- **YAML**: Agent 配置
- **YAML Frontmatter**: SKILL.md 中的元数据

## 九、质量评估

### 9.1 完整性评估 ⭐⭐⭐⭐☆ (4/5)
- ✅ 核心功能完整：Zero to MVP + MVP to Delivery 覆盖完整流程
- ✅ 双语支持完整：中英文版本并行
- ✅ 模板齐全：所有关键产出物都有模板
- ❌ 缺少示例：没有端到端使用示例
- ❌ 缺少测试：没有自动化测试

### 9.2 一致性评估 ⭐⭐⭐⭐⭐ (5/5)
- ✅ 中英文版本结构完全一致
- ✅ 术语使用统一（REQ-xxx, AC-xxx, DONE/PARTIAL/MISSING/UNTESTED/UNCLEAR）
- ✅ 模板格式一致
- ✅ 文件组织规范

### 9.3 可用性评估 ⭐⭐⭐⭐☆ (4/5)
- ✅ 文档清晰：README 提供了清晰的使用指导
- ✅ 模板详细：PRD 模板包含详细的填写规则
- ✅ 约束明确：每个技能都有清晰的 Guardrails
- ❌ 缺少可视化：没有流程图或架构图
- ❌ 学习曲线：首次使用需要理解较多概念

### 9.4 创新性评估 ⭐⭐⭐⭐⭐ (5/5)
- ✅ 弱模型适配策略：规划与执行分离，PRD 消除推理需求
- ✅ Reference Implementation 模式：照抄+替换范式
- ✅ Self-Check Commands：可机器验证的自检机制
- ✅ Forbidden 约束：明确负面清单防止过度发挥

## 十、总结

### 10.1 核心发现

**Trellis Skills 是一个设计精良的需求管理工作流系统**，具有以下特点：

1. **完整的方法论**: 从需求到交付的双阶段流程（Zero to MVP → MVP to Delivery）
2. **创新的弱模型适配设计**: 通过详细的 PRD 规格和 Reference Implementation 模式，使能力有限的模型也能执行复杂任务
3. **强大的追溯性**: 稳定的需求 ID 和明确的状态管理
4. **工程化程度高**: 模板驱动、可自动化验证、双语支持

### 10.2 适用场景

**最适合**:
- 中大型项目的需求管理
- 需要多人协作的项目
- 需要严格验收的项目
- 可能使用弱模型执行的场景

**不太适合**:
- 快速原型验证
- 需求高度不确定的探索性项目
- 极简单的单文件脚本项目

### 10.3 建议行动

**优先级 P0（立即执行）**:
1. 提交当前未提交的 14 个文件更改
2. 添加 CHANGELOG.md 记录变更

**优先级 P1（本周内）**:
3. 添加端到端使用示例到 `examples/` 目录
4. 在 README 中添加流程图（使用 Mermaid）
5. 完善 agents/openai.yaml 配置

**优先级 P2（本月内）**:
6. 添加集成测试验证技能定义完整性
7. 设计任务状态到需求追踪矩阵的同步机制
8. 在 SKILL.md 中添加版本字段

**优先级 P3（长期规划）**:
9. 增量更新支持
10. IDE 插件开发
11. 度量指标系统

---

**分析完成日期**: 2026-06-05  
**分析工具**: Claude Code (Opus 4.8)  
**项目版本**: Git commit ae79581
