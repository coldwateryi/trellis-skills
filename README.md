# Trellis 需求交付技能集

本仓库为 [Codex CLI](https://github.com/anthropics/codex) 以及其他支持skill的cli工具提供一套 Trellis 工作流技能，覆盖从原始需求文档到完整交付的全流程——**分析 → 规划 → 追踪 → 审计 → 补缺 → 验收**。

## 技能概览

| 技能 | 语言 | 用途 |
| --- | --- | --- |
| `trellis-zero-to-mvp` | EN | 从零开始：将需求文档转化为 MVP 任务树 |
| `trellis-mvp-to-delivery` | EN | 从 MVP 到交付：差距审计、补缺规划、最终验收 |
| `trellis-zero-to-mvp-zh` | ZH | 同上（中文版） |
| `trellis-mvp-to-delivery-zh` | ZH | 同上（中文版） |

### ✨ 新功能：自我评审循环

**所有技能现已支持自我评审循环机制，确保规划阶段输出满足小参数模型（如 qwen3.6 35b）的执行要求。**

**工作原理**：
1. 🔍 **分析** - 生成初版需求追踪矩阵、任务拆分和 PRD
2. ✅ **自我评审** - 对照 45-60 项检查清单逐项检查
3. 🔧 **针对性改进** - 只修复标记的问题，不全量重做
4. 🔄 **循环收敛** - 重复 2-3 轮直到所有检查通过
5. ✅ **用户确认** - 达标后才创建任务树

**核心优势**：
- ✅ **小模型友好** - 消除占位符、提供具体路径和步骤
- ✅ **质量保证** - 45-60 项精准检查，问题定位到具体行
- ✅ **成本可控** - ROI > 5:1（规划多花 45k tokens，执行少花 200k tokens）
- ✅ **效果显著** - 执行成功率提升 30%-50%

详见：[优化提案](doc/OPTIMIZATION_PROPOSAL.md) 和 [实施总结](doc/FINAL_SUMMARY.md)

## 推荐工作流

```
需求文档 ──→ [Zero to MVP] ──→ MVP 任务树 ──→ 编码实现 MVP
                                                    │
                                                    ▼
                              需求文档 ──→ [MVP to Delivery] ──→ 补缺任务 ──→ 交付验收
```

### 阶段一：Zero → MVP

当你拿到一份完整的需求文档（PRD / 产品说明 / 功能规格），还没有开始写代码时：

1. 将需求文档放到项目中
2. 调用 `trellis-zero-to-mvp`（或中文版 `trellis-zero-to-mvp-zh`）
3. 技能会执行**只读分析**，输出：
   - 需求追踪矩阵（Requirements Traceability Matrix）
   - 模块依赖图
   - 按能力拆分的任务清单
   - 按依赖排序的 MVP 开发顺序
   - 父/子任务 PRD 草案
4. **确认分析结果后**，技能创建 Trellis 任务树
5. 按推荐顺序开始编码

### 阶段二：MVP → Delivery

MVP 实现完成后，回到源需求文档做完整交付：

1. 调用 `trellis-mvp-to-delivery`（或中文版 `trellis-mvp-to-delivery-zh`）
2. 技能执行**差距审计**，逐条对照需求文档检查 MVP：
   - 需求追踪矩阵（含 DONE / PARTIAL / MISSING / UNTESTED / UNCLEAR 状态）
   - MVP 完成度摘要
   - 按依赖排序的补缺任务计划
   - 自动化测试覆盖要求
3. **确认审计结果后**，创建补缺 Trellis 任务
4. 按优先级补齐功能、测试，执行最终验收

## 推荐用法

### 场景 1：全新项目启动

```
你是一个新项目，需求文档在 docs/requirements.md。

请使用 trellis-zero-to-mvp-zh 将其转化为 MVP 任务计划。
```

技能会先做只读分析——不会写任何代码。确认任务拆分和 MVP 边界后，才会创建 Trellis 任务树。

**✨ 自我评审循环**：分析过程中会自动进行 2-3 轮质量检查，确保：
- ✅ 所有 `<...>` 占位符已被具体值替换
- ✅ File Manifest 包含精确的文件路径
- ✅ Implementation Steps 是可执行的具体动作
- ✅ 复杂任务已拆分到适合小模型执行

### 场景 2：已有 MVP，准备完整交付

```
MVP 已实现完成，源需求文档在 docs/requirements.md。

请使用 trellis-mvp-to-delivery-zh 审计 MVP，规划完整交付。
```

技能会逐条对照需求文档检查现有实现和测试，找出所有缺口，然后创建补缺任务。

**✨ 自我评审循环**：审计过程中会自动进行质量检查，确保：
- ✅ 每个 DONE 状态都有实现证据和测试证据
- ✅ 补缺任务的 PRD 明确不破坏 MVP 行为
- ✅ Regression Tests 覆盖 MVP 核心流程
- ✅ Bug 修复的分支逻辑已明确定死

### 场景 3：持续迭代

在实际开发中，两个技能可以循环使用：

1. 用 `zero-to-mvp` 规划首个可交付版本
2. 编码实现 MVP
3. 用 `mvp-to-delivery` 审计差距，补齐到完整交付
4. 如果有新增需求，回到步骤 1，针对新需求再次使用 `zero-to-mvp`

## 需求状态说明

两个技能使用统一的需求状态标记：

| 状态 | 含义 |
| --- | --- |
| `DONE` | 已完整实现并通过测试 |
| `PARTIAL` | 部分实现 |
| `MISSING` | 尚未实现 |
| `UNTESTED` | 已实现但缺少充分测试 |
| `UNCLEAR` | 需求不够清晰，无法实施 |

## 目录结构

```
skills/
├── trellis-zero-to-mvp/          # Zero → MVP（英文）
│   ├── SKILL.md                  # 技能定义与工作流
│   ├── agents/
│   │   └── openai.yaml           # Codex agent 配置
│   └── references/
│       ├── analysis-output-template.md   # 只读分析输出模板
│       ├── parent-prd-template.md        # 父任务 PRD 模板
│       ├── child-prd-template.md         # 子任务 PRD 模板
│       └── task-creation-checklist.md    # 任务创建检查清单
├── trellis-mvp-to-delivery/      # MVP → Delivery（英文）
│   ├── SKILL.md
│   ├── agents/
│   │   └── openai.yaml
│   └── references/
│       ├── gap-audit-template.md         # 差距审计模板
│       ├── delivery-task-prd-template.md # 补缺任务 PRD 模板
│       ├── test-coverage-matrix-template.md  # 测试覆盖矩阵模板
│       ├── final-acceptance-template.md      # 最终验收模板
│       └── bug-classification-rules.md       # Bug 分类规则
├── trellis-zero-to-mvp-zh/       # Zero → MVP（中文）
│   └── （结构同上）
├── trellis-mvp-to-delivery-zh/   # MVP → Delivery（中文）
│   └── （结构同上）
└── README.md
```

## 前置条件

- 已安装 [Codex CLI](https://github.com/anthropics/codex)或者其他cli工具
- 项目中已初始化 Trellis（`.trellis/` 目录存在）
- 首次使用前运行 `python ./.trellis/scripts/init_developer.py <name>` 设置开发者身份

## 关键原则

- **先分析，后行动** — 所有技能的第一轮均为只读，不会在用户确认前创建任务或编写代码
- **按能力拆分，不按文件拆分** — 每个子任务对应一个可独立验收的业务或技术能力
- **稳定 ID** — 需求编号（REQ-xxx）和验收标准编号（AC-xxx）在分析阶段确定，后续保持不变
- **严格依赖** — 父子任务仅表达结构，真正的执行依赖写在每个子任务的 PRD 中
