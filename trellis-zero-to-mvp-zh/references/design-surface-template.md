# Design Surface Template

本文件定义 `trellis-zero-to-mvp-zh` 的设计面模板。子任务 PRD 只声明影响面；详细设计写入 `design.md`；落地文件、步骤、命令写入 `implement.md`。

## 使用规则

1. 先在子任务 PRD 的“任务影响面矩阵”标记每个影响面是否涉及。
2. 任一影响面标记为“是”，`design.md` 必须包含对应设计章节，`implement.md` 必须包含对应落地计划章节。
3. 不适用的影响面写“否”，并在风险或范围外说明原因；不要留空。
4. 本模板是章节库。只复制本任务涉及的章节，不要为了完整而生成无关空表。
5. RuoYi/Vue 项目优先复用现有页面、接口、权限、字典、SQL、实体和 Mapper 风格；不得模型自创风格。

## 影响面映射

| 影响面 | design.md 章节 | implement.md 章节 | 失败码 |
| --- | --- | --- | --- |
| 数据库/数据模型 | Database Schema Design | Database Migration Plan | DATABASE_SCHEMA_MISSING |
| API 接口 | API Contract Design | API Implementation Plan | API_CONTRACT_MISSING |
| 模块间交互 | Inter-Module Interaction Design | Inter-Module Wiring Plan | INTER_MODULE_CONTRACT_MISSING |
| 外部系统接口 | External System Interface Design | External Adapter Plan | EXTERNAL_INTERFACE_CONTRACT_MISSING |
| UI/项目风格 | UI Design and Style Contract | UI Implementation Plan | UI_DESIGN_MISSING |
| 权限/数据权限 | Permission and Data Scope Design | Permission Wiring Plan | PERMISSION_CONTRACT_MISSING |
| 字典/状态机 | Dictionary and State Design | State Implementation Plan | STATE_TRANSITION_MISSING |
| 查询/导入导出 | Query and Import Export Design | Query Export Plan | QUERY_CONTRACT_MISSING |
| 校验/错误语义 | Validation and Error Semantics | Validation Implementation Plan | VALIDATION_CONTRACT_MISSING |
| 事务/并发/幂等 | Transaction Concurrency and Idempotency Design | Transaction Implementation Plan | TRANSACTION_CONTRACT_MISSING |
| 异步任务/事件 | Async Job and Event Design | Job Event Plan | ASYNC_JOB_CONTRACT_MISSING |
| 日志/审计 | Audit and Logging Design | Audit Implementation Plan | AUDIT_LOG_CONTRACT_MISSING |
| 初始化/迁移 | Data Initialization and Migration Design | Migration Plan | MIGRATION_COMPATIBILITY_MISSING |
| 测试策略 | Test Strategy Design | Test Implementation Plan | TEST_STRATEGY_MISSING |
| 性能/容量 | Performance and Capacity Design | Performance Verification Plan | PERFORMANCE_CONSTRAINT_MISSING |
| 安全/敏感数据 | Security and Sensitive Data Design | Security Verification Plan | SECURITY_CONTRACT_MISSING |
| 配置/环境 | Configuration Design | Configuration Plan | CONFIG_CONTRACT_MISSING |
| 框架约定 | Framework Convention Design | Framework Implementation Plan | FRAMEWORK_CONVENTION_MISSING |
| 人工验收 | Manual Acceptance Design | Manual Verification Plan | MANUAL_ACCEPTANCE_UNCLEAR |
| 文档/运维 | Documentation and Operations Handoff | Docs Ops Plan | OPS_DOC_CONTRACT_MISSING |

## design.md 章节模板

### Database Schema Design

| 表名 | 用途 | 主键 | 所属模块 | 备注 |
| --- | --- | --- | --- | --- |
| <table> | <purpose> | <pk> | <module> | <notes> |

| 表名 | 字段 | DB 类型 | Java/DTO 类型 | 非空 | 默认值 | 约束 | 说明 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| <table> | <column> | <type> | <type> | yes/no | <value> | <unique/index/fk/none> | <meaning> |

| 表名 | 索引/约束名 | 字段 | 类型 | 原因 |
| --- | --- | --- | --- | --- |
| <table> | <idx_name> | <columns> | unique/index/fk | <reason> |

| 来源表 | 来源字段 | 目标表 | 目标字段 | 关系 | 删除/更新策略 |
| --- | --- | --- | --- | --- | --- |
| <table> | <field> | <table> | <field> | 1:1/1:n/n:n | <policy> |

### API Contract Design

| 接口 | 方法 | 路径 | 权限标识 | 用途 | 调用方 |
| --- | --- | --- | --- | --- | --- |
| <name> | GET/POST/PUT/DELETE | <path> | <permission or none> | <purpose> | <caller> |

| 接口 | 参数 | 位置 | 类型 | 必填 | 默认值 | 校验 | 说明 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| <method path> | <param> | path/query/body/header | <type> | yes/no | <value> | <rule> | <notes> |

| 接口 | 成功响应 | 失败响应 | 备注 |
| --- | --- | --- | --- |
| <method path> | <AjaxResult/TableDataInfo/schema> | <error schema> | <notes> |

| 场景 | 返回结构 | 错误消息 | HTTP/code |
| --- | --- | --- | --- |
| <case> | <schema> | <message> | <code> |

### Inter-Module Interaction Design

| 调用方模块 | 被调方模块 | 交互方式 | 接口/方法 | 输入 | 输出 | 事务边界 | 失败策略 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| <caller> | <callee> | Service/Event/HTTP/Adapter | <method> | <input> | <output> | <transaction> | <failure handling> |

规则：

- 跨模块读取优先通过 Service 或明确 Adapter，不直接注入对方 Mapper。
- 一个模块不得直接写入另一个模块拥有的数据表，除非本表明确授权。
- 不复制另一个模块的业务判断；复用其 Service 或抽出明确 domain service。

### External System Interface Design

| 外部系统 | 交互目的 | 协议 | 方向 | 认证方式 | 配置项 | 状态 |
| --- | --- | --- | --- | --- | --- | --- |
| <system> | <purpose> | HTTP/MQ/file/hardware | inbound/outbound | <auth> | <config keys> | FIXED/BASELINE/BLOCKED/OUT_OF_SCOPE |

| 外部系统 | 方法 | URL/Topic | 请求字段 | 响应字段 | 超时 | 重试 | 降级 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| <system> | <method> | <endpoint> | <fields> | <fields> | <timeout> | <retry> | <fallback> |

| 配置项 | 来源 | 是否必需 | 默认值 | 缺失时行为 |
| --- | --- | --- | --- | --- |
| <key> | application.yml/env/sys_config | yes/no | <value> | <behavior> |

### UI Design and Style Contract

| 项 | 采用值 |
| --- | --- |
| UI 框架 | <Element UI / Element Plus / project-specific> |
| 页面类型 | <RuoYi 列表 CRUD / 详情页 / Dashboard / 表单向导 / 弹窗> |
| 参考页面 | <existing page path> |
| 页面路径 | <target page path> |
| API 文件 | <target API file path> |
| 权限前缀 | <permission prefix> |
| 字典依赖 | <dict type or none> |

| 区域 | 组件/模式 | 说明 |
| --- | --- | --- |
| 查询区 | <query form pattern> | <fields> |
| 工具栏 | <toolbar pattern> | <buttons> |
| 表格 | <table pattern> | <columns> |
| 弹窗/表单 | <dialog/form pattern> | <fields> |

| 列 | 字段 | 显示组件 | 宽度 | 格式化 | 权限/条件 |
| --- | --- | --- | --- | --- | --- |
| <label> | <field> | <component> | <width> | <format> | <permission/condition> |

| 字段 | 组件 | 必填 | 校验 | 默认值 | 数据源 |
| --- | --- | --- | --- | --- | --- |
| <field> | <component> | yes/no | <rule> | <value> | <source> |

| 状态 | 行为 |
| --- | --- |
| loading | <behavior> |
| empty | <behavior> |
| success | <behavior> |
| failure | <behavior> |

### Permission and Data Scope Design

| 操作 | 后端权限标识 | 前端按钮权限 | 菜单权限 | 数据范围规则 | 无权限行为 |
| --- | --- | --- | --- | --- | --- |
| <operation> | <permission> | <v-hasPermi or none> | <menu/button> | <scope rule> | <behavior> |

### Dictionary and State Design

| 字段 | 类型 | 字典类型/枚举 | 允许值 | 显示文案 | 默认值 | 说明 |
| --- | --- | --- | --- | --- | --- | --- |
| <field> | dict/enum/state | <dict or enum> | <values> | <labels> | <default> | <notes> |

| 当前状态 | 操作 | 目标状态 | 允许角色 | 前置条件 | 非法时行为 |
| --- | --- | --- | --- | --- | --- |
| <from> | <action> | <to> | <role> | <condition> | <error> |

### Query and Import Export Design

| 查询项 | 字段 | 匹配方式 | 默认值 | 后端落点 | 前端组件 |
| --- | --- | --- | --- | --- | --- |
| <label> | <field> | like/eq/range | <default> | <backend location> | <component> |

| 能力 | 是否支持 | 权限 | 文件/字段 | 行为 |
| --- | --- | --- | --- | --- |
| 导出 | yes/no | <permission> | <fields/file> | <behavior> |
| 导入 | yes/no | <permission> | <fields/file> | <behavior> |

### Validation and Error Semantics

| 字段/操作 | 前端校验 | 后端校验 | 业务校验 | 错误消息 | 验收点 |
| --- | --- | --- | --- | --- | --- |
| <field/action> | <rule> | <rule> | <rule> | <message> | <AC> |

### Transaction Concurrency and Idempotency Design

| 场景 | 事务边界 | 并发风险 | 幂等策略 | 失败恢复 |
| --- | --- | --- | --- | --- |
| <scenario> | <boundary> | <risk> | <idempotency> | <recovery> |

### Async Job and Event Design

| 类型 | 名称 | 触发方式 | 输入 | 输出 | 幂等/锁 | 失败处理 |
| --- | --- | --- | --- | --- | --- | --- |
| 定时任务/事件/消息 | <name> | <trigger> | <input> | <output> | <strategy> | <failure handling> |

### Audit and Logging Design

| 场景 | 日志类型 | 落点 | 记录字段 | 脱敏规则 |
| --- | --- | --- | --- | --- |
| <scenario> | operation/business/external/security | <location> | <fields> | <masking> |

### Data Initialization and Migration Design

| 类型 | 文件 | 内容 | 回滚方式 |
| --- | --- | --- | --- |
| 菜单 SQL/字典 SQL/字段回填/配置 | <path> | <content> | <rollback> |

### Test Strategy Design

| AC | 测试类型 | 测试文件 | 输入 | 期望 |
| --- | --- | --- | --- | --- |
| <AC> | unit/service/mapper/controller/frontend/e2e/manual | <path> | <input> | <expected> |

### Performance and Capacity Design

| 场景 | 规模假设 | 设计约束 | 验证方式 |
| --- | --- | --- | --- |
| <scenario> | <scale> | <constraint> | <verification> |

### Security and Sensitive Data Design

| 数据/入口 | 风险 | 约束 | 验证 |
| --- | --- | --- | --- |
| <data/entry> | <risk> | <constraint> | <verification> |

### Configuration Design

| 配置项 | 位置 | 默认值 | 是否必需 | 缺失行为 | 环境差异 |
| --- | --- | --- | --- | --- | --- |
| <key> | <location> | <default> | yes/no | <behavior> | <dev/test/prod> |

### Framework Convention Design

| 约定 | 采用值 | 证据 |
| --- | --- | --- |
| <framework convention> | <adopted value> | <path> |

### Manual Acceptance Design

| 验收项 | 前置条件 | 操作步骤 | 通过标准 | 证据 |
| --- | --- | --- | --- | --- |
| <item> | <precondition> | <steps> | <pass criteria> | <screenshot/log/report> |

### Documentation and Operations Handoff

| 项 | 是否需要 | 文档位置 | 内容 |
| --- | --- | --- | --- |
| 配置说明/运维检查/用户说明 | yes/no | <path or none> | <content> |

## implement.md 落地计划章节模板

每个涉及面在 `implement.md` 中至少要有对应计划章节，内容可用统一格式：

```markdown
## <Surface Implementation Plan>

| 步骤 | 文件 | 操作 | 精确位置 | 验证方式 |
| --- | --- | --- | --- | --- |
| 1 | <path> | new/modify | <method/section> | <command/assertion> |
```

章节标题必须与“影响面映射”中的 implement.md 章节一致，便于机械 Gate 扫描。
