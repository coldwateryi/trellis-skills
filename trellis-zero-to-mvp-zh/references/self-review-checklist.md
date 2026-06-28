# 自我评审检查清单

本检查清单用于评估只读分析输出是否满足小参数模型（如 qwen3.6 35b）的执行要求。

## 使用说明

1. 在完成每轮只读分析后，对照本清单逐项检查
2. 所有检查项必须通过（或明确标记"不适用"），且 Full MVP Planning Gate 与 Pre-Confirmation Gate 均为 `PASS`，才能进入用户确认阶段
3. 如有不通过项，标记具体问题并进行针对性改进

---

## 0. Trellis 0.6+ 工作流适配检查

### 0.0 Project Contract Lock
- [ ] 已读取用户要求、README、模块 README、AGENTS.md、`.trellis/spec/` 和现有代码结构中的本地约定
- [ ] 已选择 Project Contract Profile，并说明选择证据与拒绝其他 profile 的原因
- [ ] 已输出 Project Contract Lock；所选 profile 的适用字段都有 adopted value 和证据路径
- [ ] 不适用字段写 `not-applicable`，没有把 RuoYi/Java 字段套到 CLI、SDK、前端、Python 服务或自定义项目
- [ ] 如 README/spec/现有代码之间冲突，已输出 `CONTRACT_CONFLICT` 表
- [ ] 存在 `CONTRACT_CONFLICT` 时，已阻塞用户确认，没有继续创建任务
- [ ] 子任务候选的命名、路径、API、命令、路由、数据/状态对象与 Project Contract Lock 一致
- [ ] 没有同一任务中混用两套命名体系、路径体系、API/命令体系或包/模块结构
- [ ] 已输出 Contract Snapshot 与 forbidden_tokens，并为每个 forbidden token 写明证据来源
- [ ] 已扫描父/子 PRD、`design.md`、`implement.md`、JSONL，确认 forbidden token 未命中

### 0.1 工作流发现
- [ ] 如存在 `.trellis/workflow.md`，已读取
- [ ] 如存在 `.trellis/config.yaml`、`.trellis/.version`、`.trellis/.developer`，已检查
- [ ] 分析结果说明了项目是旧版 PRD-only task，还是 Trellis 0.6+ 规划产物工作流
- [ ] 已读取 `codex.dispatch_mode`；Codex inline、sub-agent 和 optional JSONL 的 Gate 模式已区分
- [ ] Developer identity 设置以 `trellis init -u <name>` 为主要提示，`init_developer.py` 只作为旧版兜底

### 0.2 Spec 新鲜度
- [ ] 列出了相关 `.trellis/spec/` 文件
- [ ] Spec 新鲜度标记为 fresh/stale/missing/unknown
- [ ] Spec 过期或缺失时，已形成 spec 刷新/bootstrap 任务或阻塞说明

### 0.3 规划产物门槛
- [ ] 每个任务都说明必要产物（`prd.md`、`design.md`、`implement.md`、`implement.jsonl`、`check.jsonl`）
- [ ] 已输出规划产物矩阵，并能作为创建后文件存在性核验依据
- [ ] 中/高复杂度任务已包含设计和实现产物，或已进一步拆小
- [ ] 高复杂度任务没有 PRD-only；若不生成 `design.md` 和 `implement.md`，必须已拆成低/中复杂度
- [ ] 需要在实现/检查前预加载稳定 specs、调研说明或外部上下文时，要求 JSONL 上下文清单
- [ ] 详细文件计划、有序实现步骤、自检命令、失败恢复和评审门位于 `implement.md`；低复杂度 PRD-only 例外有明确证据
- [ ] 每个子任务都有“任务影响面矩阵”
- [ ] 任一影响面为“是”时，`design.md` 包含对应设计章节，`implement.md` 包含对应实现计划章节
- [ ] RuoYi/Vue CRUD 或 fullstack 任务没有无理由把数据库、API、UI、权限、查询、校验、测试等常见影响面全部标为“否”

### 0.4 已有部分实现回填
- [ ] 如果仓库不是空项目，已输出 Existing Implementation Baseline（已有实现基线）
- [ ] 基线条目列出精确代码证据和测试证据，或明确说明测试证据缺失
- [ ] 源需求仍是需求真相来源；没有把 `.trellis/spec/` 当作唯一需求来源
- [ ] `DONE` 需求没有创建实现任务
- [ ] `UNTESTED` 需求只创建测试补齐任务，没有重复创建实现任务
- [ ] `PARTIAL` 需求只为缺失行为创建补缺任务
- [ ] `MISSING` 需求创建新实现任务
- [ ] 需求追踪矩阵每一行都有与当前状态匹配的任务动作（`none`、`test-only`、`gap-task`、`new-task` 或 `clarify`）
- [ ] 作为依赖的已有能力以 `existing:<path-or-capability>` 形式列入基线依赖
- [ ] 任务拆分和 PRD 写回路径以 `task.py create` 返回的真实任务目录为准，不是按逻辑 Task ID/slug 另造一棵目录树

### 0.5 状态机与 Gate
- [ ] 已读取 `workflow-state-machine.md` 和 `gate-definitions.md`
- [ ] 当前输出标明所处状态（S0-S10）和下一状态
- [ ] Requirement Ledger Gate 已输出 PASS/FAIL、失败码和证据
- [ ] Contract Gate 已输出 PASS/FAIL、失败码和证据
- [ ] Full MVP Planning Gate 已输出 PASS/FAIL、失败码和证据
- [ ] Batch Completeness Gate 已输出 PASS/FAIL、失败码和证据
- [ ] Pre-Confirmation Gate 已输出 PASS/FAIL、失败码和证据
- [ ] Gate 为 FAIL 时没有请求用户确认、没有创建任务、没有建议开发

---

## A. 需求完整性检查

### A1. 需求标识
- [ ] 每个需求都分配了唯一的 REQ-xxx ID（如 REQ-001, REQ-002）
- [ ] 每个验收标准都分配了唯一的 AC-xxx ID（如 AC-001, AC-002）
- [ ] ID 编号连续无跳号
- [ ] 需求追踪矩阵中的每个需求都有明确的状态（DONE/PARTIAL/MISSING/UNTESTED/UNCLEAR）
- [ ] `REQ-xxx` 绑定源需求功能点，不因任务合并、拆分、重排而改变语义

### A1.1 原始需求覆盖
- [ ] 已列出源需求文档中的全部可验收功能点
- [ ] 每个源功能点都映射到稳定 `REQ-xxx`
- [ ] Full Requirement Matrix 和 MVP Coverage Matrix 分开输出
- [ ] 没有把当前 MVP 覆盖数量写成原始功能点总数
- [ ] 父 PRD 的覆盖汇总数量由 MVP Coverage Matrix 机械统计得出，`TASK+MERGED+BASELINE+OUT_OF_SCOPE+BLOCKED` 等于 Full Requirement Matrix 行数
- [ ] 完整平台范围与当前 MVP 边界差异已显式说明
- [ ] 每个 `REQ-xxx` 都有覆盖状态（TASK/MERGED/BASELINE/OUT_OF_SCOPE/BLOCKED）
- [ ] `MERGED` 需求写明目标子任务和覆盖 AC
- [ ] `BASELINE` 需求写明已有代码/测试证据
- [ ] `OUT_OF_SCOPE` 需求写明排除原因，并计划在用户确认阶段显式提示
- [ ] 所有 `OUT_OF_SCOPE` 需求已进入 Backlog 表，写明推荐阶段和恢复条件
- [ ] 没有源功能点无记录地从任务树中消失

### A2. 需求描述清晰性
- [ ] 没有"待定"、"视情况而定"、"根据需要"等模糊表述
- [ ] 没有"等"、"诸如"、"类似"等不完整列举
- [ ] 所有"可能"、"或许"、"建议"等不确定词汇已消除或明确化

### A3. 边界条件
- [ ] 输入为空值时的行为已明确
- [ ] 输入超长（超出限制）时的行为已明确
- [ ] 输入重复（如重复提交）时的行为已明确
- [ ] 并发场景（如果适用）的行为已明确
- [ ] 输入非法格式时的行为已明确

### A4. 错误处理
- [ ] 每个失败场景都定义了具体的错误码（如 400, 404, 500）
- [ ] 每个失败场景都定义了具体的错误消息（不是"操作失败"）
- [ ] 错误响应的数据结构已明确

---

## B. 任务拆分质量检查

### B1. 拆分原则
- [ ] 每个子任务对应一个可独立验收的业务或技术能力
- [ ] 没有按文件拆分的任务（如"完成 UserController.java"）
- [ ] 没有按时间拆分的任务（如"第一周任务"）
- [ ] 每个子任务可以由单个开发者独立完成
- [ ] 任务合并/拆分记录完整，任务数量变化有明确理由
- [ ] MVP 任务树和完整平台范围的差异已显式说明
- [ ] Small Model Mode 下，每个子任务只覆盖一个实体 CRUD、一个接口组、一个状态流转、一个前端页面或一个后端聚合查询
- [ ] Small Model Mode 下，没有子任务同时包含两个以上主实体、两套 CRUD、CRUD+状态机+报表、后端流程+小程序页面、地图/GIS+多表聚合+高级分析
- [ ] 模型没有用“强耦合”“同一流程”“拆分会增加依赖”为理由自行豁免超大任务；如保留合并，已有用户明确确认记录
- [ ] Small Model Mode 下，单批创建任务数和完整 PRD 数未超过技能上限；超过时已分批
- [ ] 分批规划覆盖所有 MVP `TASK` 子任务，而不是只覆盖 P0/P1
- [ ] 不存在 `P0P1_ONLY_PLAN`

### B2. 复杂度评估
- [ ] 每个任务都标注了复杂度（低/中/高）
- [ ] 复杂度评估基于小模型能力而非人类开发者能力
- [ ] 高复杂度任务已进一步拆分为多个低/中复杂度任务，或有非常详细的步骤
- [ ] 低复杂度：有现成范例可照抄，或是标准 CRUD
- [ ] 中复杂度：有少量业务逻辑，PRD 中有明确实现步骤
- [ ] 高复杂度：已拆分或 PRD 中每步都定死到无需推理

### B3. 依赖关系
- [ ] 每个任务的依赖关系已明确列出
- [ ] 没有循环依赖
- [ ] 被标记为"可并行"的任务之间确实无依赖关系
- [ ] 阻塞性任务（P0）已识别并优先排序
- [ ] 基线依赖和 Trellis task 依赖已分开表达
- [ ] 已有代码依赖没有被伪装成新的 Trellis 子任务

### B4. 优先级
- [ ] 每个任务都分配了优先级（P0/P1/P2/P3）
- [ ] P0：阻塞其他模块或核心正确性
- [ ] P1：核心业务闭环
- [ ] P2：体验、报表、通知、增强能力
- [ ] P3：非必要优化

### B5. 渐进式规划账本
- [ ] 已输出 Subtask Planning Ledger
- [ ] MVP Coverage Matrix 中每个 `TASK` 都有账本行
- [ ] 每个账本行都有 Task ID、REQ IDs、标题、批次、依赖、可并行组、复杂度、PRD 状态、产物需求和下一步
- [ ] 已输出 Batch Completion Rollup
- [ ] 每个 MVP 子任务都有批次；不存在 `UNBATCHED_TASK`
- [ ] 进入用户确认前，所有 MVP 子任务为 `READY_TO_CONFIRM`、`BLOCKED` 或 `OUT_OF_SCOPE`
- [ ] 后续批次不是“待规划”；已有冻结的任务边界、REQ 覆盖、依赖、复杂度和产物需求

---

## C. PRD 质量检查（关键！）

### C1. 占位符消除
- [ ] PRD 中没有任何 `<...>` 形式的占位符
- [ ] PRD/design/implement/JSONL 中没有 Contract Snapshot forbidden token
- [ ] PRD 中没有 `{Entity}`、`{domain}`、`{entity}`、`<PageComponent>` 等泛化模板占位符
- [ ] PRD 中没有"具体路径"、"相关文件"等抽象表述
- [ ] PRD 中没有 `TBD`、"待定"、"视情况"、"根据实际情况"等未决表达
- [ ] PRD 中没有"根据实际情况"、"视需要而定"等推理留白
- [ ] PRD/design/implement 中没有 `YOUR_KEY`、`API_KEY_HERE`、`待用户提供` 等未决外部配置
- [ ] 所有外部配置都标为 `FIXED`、`BASELINE`、`BLOCKED` 或 `OUT_OF_SCOPE`，并写明执行期行为

### C1.1 标题与正文一致性
- [ ] 每个子任务的标题、目标、文件清单、主实体、表名、API 路由、权限标识属于同一业务域
- [ ] `design.md` 和 `implement.md` 没有复制其他任务的页面路径、Service 类、状态机或业务流程
- [ ] 如果引用其他任务实体/路径，已在依赖或基线中列出并说明原因
- [ ] 任一任务的主实体名、路由、表名没有与另一个无关任务串用
- [ ] 每个子任务都有 Project Contract Reference 或等价契约引用
- [ ] 子任务 Project Contract Reference 与父任务 Project Contract Lock 一致
- [ ] 每个子任务 PRD 的“任务影响面矩阵”与任务类型、语义锚点、文件计划一致
- [ ] 涉及数据库/数据模型时，`design.md` 有 `Database Schema Design`，`implement.md` 有 `Database Migration Plan`
- [ ] 涉及 API 时，`design.md` 有 `API Contract Design`，`implement.md` 有 `API Implementation Plan`
- [ ] 涉及 UI/项目风格时，`design.md` 有 `UI Design and Style Contract`，并指向当前项目参考页面/组件风格
- [ ] 涉及权限/数据权限时，后端权限、前端按钮权限、菜单权限和数据范围规则一致

### C2. Reference Implementation（参考实现）
- [ ] 如果有现成范例可照抄，指向了具体文件的完整路径
- [ ] 如果无现成范例，明确写"无，按 Technical Notes 从零实现"
- [ ] 替换说明具体（如"把范例里的 User 替换为 Order"）
- [ ] 不是"参考相关代码"、"照抄类似实现"等模糊指引

### C3. File Manifest（文件清单）
- [ ] Trellis 0.6+ 中，文件清单位于 `implement.md`；PRD 只说明实现计划定位
- [ ] PRD-only 低复杂度任务如把文件清单放在 PRD，已有本地工作流允许证据
- [ ] 列出了所有要操作的文件，精确到完整路径
- [ ] 每个文件标注了操作类型（新建/修改），修改操作说明了具体位置
- [ ] 如涉及数据结构，附带了完整的字段表

### C4. Implementation Steps（实现步骤）
- [ ] Trellis 0.6+ 中，实现步骤位于 `implement.md`；PRD-only 低复杂度任务可放在 PRD 精简执行附录
- [ ] 步骤是有序的（1, 2, 3...）
- [ ] 每步是具体动作，不是抽象目标
- [ ] 每步可独立验证
- [ ] 需要推理的决策已在步骤中定死

### C5. Acceptance Criteria（验收标准）
- [ ] 验收标准是可判定的断言，不是主观描述
- [ ] 包含正常路径的验收（成功场景）
- [ ] 包含异常路径的验收（失败场景）
- [ ] 包含边界条件的验收

### C6. Self-Check Commands（自检命令）
- [ ] Trellis 0.6+ 中，自检命令位于 `implement.md`；PRD 可保留验收级命令摘要
- [ ] 提供了可直接运行的验证命令
- [ ] 命令是具体的，不是"运行测试"、"验证功能"
- [ ] 命令附带了期望结果说明
- [ ] 命令无需人工判断即可确认通过/失败

### C7. Automated Tests Required
- [ ] 明确列出了需要的测试类型（unit/integration/e2e等）
- [ ] 每个测试点具体（被测方法 + 输入 + 期望输出）
- [ ] 不是"添加必要测试"、"确保充分测试覆盖"等抽象要求

---

## D. 小模型执行友好性检查

### D1. 决策点已定死
- [ ] 所有"用哪个注解"的决策已在 PRD 中明确
- [ ] 所有"走哪条分支"的决策已在 PRD 中明确
- [ ] 所有"命名规则/路径/API/命令/包或模块"已明确
- [ ] 所有"表结构/schema/state/config"已明确（字段名、类型、约束都已定义）
- [ ] 所有第三方 key、外部接口、地图、硬件协议等未决项已定死、阻塞或排除

### D2. 照抄范例可行性
- [ ] 如果指向了范例，该范例与本任务场景高度相似
- [ ] 范例到任务的映射关系清晰（哪些照抄，哪些替换）
- [ ] 如果无法照抄，from-scratch 的步骤非常详细

### D3. Forbidden（禁止事项）清单
- [ ] 明确列出了不该做的事
- [ ] 明确了文件修改范围
- [ ] 明确了依赖约束

### D4. 技术栈和工具约束
- [ ] 使用的框架/库已在 Technical Notes 中列出
- [ ] 构建命令已明确
- [ ] 测试命令已明确

### D5. 上下文与设计左移
- [ ] 上下文清单列出了执行模型编辑前必须读取的确切文件
- [ ] 决策表定死了命名、分支、schema、API、校验等选择
- [ ] 契约快照在编码前定义了 API/interface/data/state 行为
- [ ] 使用 `implement.jsonl` 时，条目列出稳定实现上下文文件，而不是源代码文件或步骤动作
- [ ] 使用 `check.jsonl` 时，条目列出稳定验证上下文文件，而不是测试命令
- [ ] `implement.jsonl` / `check.jsonl` 不只包含 `_example` 种子行；如果无需 JSONL，已说明原因
- [ ] JSONL 模式为 `required/optional/inline` 之一，并与 `.trellis/config.yaml` 和规划产物矩阵一致
- [ ] 工作流要求复杂任务有 `design.md` 时，也已准备 `implement.md`，或明确说明为何不需要
- [ ] PRD 中写明"需要"的规划产物，在任务创建后都有真实文件；不存在声明和文件系统不一致

### D6. Artifact Gate
- [ ] 已规划创建后的 Artifact Gate 检查
- [ ] Artifact Gate 包含 placeholder 扫描、JSONL `_example` 扫描、Project Contract Check、Small Model Grain Check、高复杂度产物检查、外部配置检查
- [ ] Artifact Gate 使用 `scripts/trellis_zero_gate.py` 或等价机械扫描作为证据，不由模型手填
- [ ] Artifact Gate 检查包含通用 `<...>` 占位扫描和父 PRD 声明值/机械扫描值一致性检查
- [ ] Artifact Gate `FAIL` 时不会汇报任务树可执行，必须先修正或明确阻塞
- [ ] Artifact Gate `PENDING` 视同 `FAIL`，不会汇报任务树可执行
- [ ] Artifact Gate 输出包含 `jsonl_mode`、`forbidden_token_hits`、`contract_mismatch_hits`、`coverage_count_mismatch_hits`、`missing_declared_artifacts`、`angle_placeholder_hits`、`declared_gate_mismatch_hits` 和 `external_config_hits`
- [ ] Artifact Gate 输出包含 `design_surface_prd_without_matrix` 和 `design_surface_missing_hits`，且 PASS 条件均为 0

### D7. 开发建议门槛
- [ ] Development Recommendation Gate 已定义并输出结果
- [ ] Artifact Gate 不是 `PASS` 时没有输出“第一个建议开始的任务”
- [ ] 存在未解释非终态 MVP 子任务时，输出 `development_ready: false`
- [ ] 只完成本批或 P0/P1 时，输出下一批规划动作而非开发建议

---

## E. 风险点检查

### E1. 风险识别
- [ ] 高风险模块已标记风险说明
- [ ] 跨团队依赖已明确
- [ ] 技术债务已记录到 Out of Scope

### E2. Out of Scope 清晰性
- [ ] Out of Scope 列出了明确排除的功能
- [ ] Out of Scope 列出了无法在规划阶段定死的点（如果有）
- [ ] Out of Scope 不是"其他功能"等模糊表述

---

## F. TDD 就绪检查（落地阶段）

### F1. AC 可测化
- [ ] 每条验收标准（AC-xxx）能转成一个可独立运行的失败测试
- [ ] 每条 AC 的期望可观察结果具体到可写断言（不是"正确实现"）
- [ ] 测试命令可直接运行并附期望结果
- [ ] 自动化测试要求逐条对应到 AC/REQ，而非泛泛"加测试"

### F2. 红绿可行性
- [ ] 有可照抄的测试范例路径，或明确写"无，从零写测试"
- [ ] 边界与错误路径各有对应的测试点（不只 happy path）

---

## G. 落地纪律检查（设计左移）

### G1. 编排-计算分离
- [ ] 中/高复杂度任务的 `design.md` 标注了编排层与计算层，并各自指向文件清单落点
- [ ] 可独立测试的计算逻辑没有被塞进编排层

### G2. 挂载点
- [ ] 挂载点清单齐全（一般 3-5 条，按"删了它特性就消失"判据）
- [ ] 每个挂载点是可勾选的接线项（路由/配置/订阅/DI/入口）

### G3. 结构健康度
- [ ] 对要改的文件/目录做了阈值预检
- [ ] 命中阈值的任务有"只搬不改行为"的微重构第 0 步且独立验证

### G4. 执行期闭环挂载
- [ ] 中/高复杂度任务在工作流中挂上了调试脚本（`trellis-debug-systematic-zh`）与评审门（`trellis-review-twostage-zh`）
- [ ] 评审 Stage 2 指定由强模型执行（角色分层模型分配）

---

## 检查结果判定

### 通过标准
- 所有适用的检查项都勾选 ✅
- 不适用的检查项已标记"N/A"并说明原因
- Full MVP Planning Gate = PASS
- Pre-Confirmation Gate = PASS
- 不存在 `UNASSIGNED_MVP_REQ`、`UNBATCHED_TASK`、`P0P1_ONLY_PLAN`、`DEFERRED_PRD_WITHOUT_PLAN`

### 不通过处理
- 未通过的检查项 → 标记为问题
- 生成问题清单（位置、问题描述、影响、改进建议）
- 进行针对性改进，进入下一轮评审

### 收敛条件
- 所有检查项通过，且 Full MVP Planning Gate / Pre-Confirmation Gate 均 PASS → 进入用户确认阶段
- 连续2轮无新问题，但 Gate 仍 FAIL → 不得自动通过，继续规划或阻塞
- 超过5轮仍有问题 → 提示用户选择（换强模型/人工介入/接受风险）
