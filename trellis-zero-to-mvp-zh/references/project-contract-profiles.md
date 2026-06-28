# Project Contract Profiles

本文件用于在只读分析早期选择项目契约画像，避免把某一类项目的命名、目录和产物假设套到其他仓库。

## 选择规则

1. 先从用户要求、README、模块 README、AGENTS.md、`.trellis/spec/`、`.trellis/workflow.md` 和现有代码证据选择 profile。
2. 只能采用有证据的字段；没有证据的字段写 `not-applicable`、`unknown-blocked` 或放入 `custom`。
3. 不要在非 RuoYi / Java CRUD 项目中填 Java 实体、Controller 包、Mapper XML、权限前缀等字段。
4. 若仓库同时包含多个形态，选择主交付面作为主 profile，并用 `secondary_profiles` 记录辅助交付面。
5. Contract Snapshot 必须由已采用字段生成；`forbidden_tokens` 只来自冲突候选、旧任务错误、框架默认误判或与证据不一致的值。

## 输出格式

```yaml
project_contract_profile:
  selected: <java-ruoyi-crud|typescript-cli-framework|frontend-spa|python-service|custom>
  secondary_profiles:
    - <profile or none>
  evidence:
    - <path:reason>
  rejected_profiles:
    - profile: <name>
      reason: <why not applicable>
```

Contract Lock 使用 profile 驱动表，不要复制不适用字段：

| 契约项 | profile 字段 | adopted_value | evidence_path | forbidden_tokens | notes |
| --- | --- | --- | --- | --- | --- |
| <契约项> | <field> | <具体值或 not-applicable> | <path> | <tokens or none> | <说明> |

## `java-ruoyi-crud`

适用证据：RuoYi / Spring Boot / MyBatis / Vue Admin CRUD 项目，存在 Java domain、controller、mapper XML、前端 views/api、权限标识或 SQL 菜单脚本。

推荐契约字段：

- backend_module
- java_entity_pattern
- database_table_prefix
- controller_package
- controller_url_prefix
- service_mapper_xml_paths
- frontend_api_path_pattern
- frontend_views_path_pattern
- permission_prefix
- sql_file_pattern
- menu_or_route_registration
- build_and_test_commands
- database_schema_required_triggers
- database_table_design_fields
- migration_sql_path_pattern
- entity_column_mapping_policy
- api_contract_required_triggers
- api_response_envelope_policy
- inter_module_call_policy
- external_system_adapter_policy
- frontend_page_style_reference
- frontend_query_table_form_pattern
- menu_permission_policy
- dict_usage_policy
- route_component_policy
- validation_policy
- operation_log_policy
- data_scope_policy

禁止：没有 RuoYi 证据时，不要使用本 profile。

RuoYi/Vue 常见 adopted values 示例：

```yaml
api_response_envelope_policy: RuoYi AjaxResult / TableDataInfo
frontend_page_style_reference: ruoyi-ui/src/views/system/notice/index.vue
frontend_api_pattern: ruoyi-ui/src/api/<module>/<entity>.js
frontend_view_pattern: ruoyi-ui/src/views/<module>/<entity>/index.vue
permission_policy: <module>:<entity>:list/add/edit/remove/export
menu_permission_policy: sys_menu + v-hasPermi
inter_module_call_policy: service-level call, no cross-module mapper write unless explicitly designed
```

## `typescript-cli-framework`

适用证据：TypeScript CLI / SDK / monorepo / 模板型框架项目，存在 `package.json`、`packages/`、CLI commands、templates、workflow 文档或脚本模板。

推荐契约字段：

- workspace_package_manager
- package_or_workspace_layout
- cli_entrypoints_and_commands
- sdk_public_api
- template_source_paths
- generated_template_destinations
- workflow_state_blocks
- platform_configurators
- python_or_shell_script_templates
- tests_build_lint_commands
- migration_or_hash_policy
- docs_and_spec_paths

Trellis 类项目特别注意：

- `.trellis/workflow.md` 是本地工作流契约。
- `.trellis/config.yaml` 中的平台配置和 `codex.dispatch_mode` 会影响 JSONL Gate。
- Python `.trellis/scripts` 若有模板源，需锁定模板源路径与生成目标路径，避免只改生成物不改模板。
- CLI、SDK、模板、workflow 文档是独立契约面；不要用 Java Controller / 表名字段表达。

## `frontend-spa`

适用证据：前端单页应用，存在 routes/pages/components/API client/state management/build scripts。

推荐契约字段：

- app_framework
- route_definition_paths
- page_component_paths
- shared_component_paths
- api_client_paths
- state_management_paths
- style_or_design_system_paths
- auth_guard_or_permission_model
- test_build_commands
- asset_and_env_policy

禁止：不要凭空生成后端包路径、数据库表名或 Java 实体字段。

## `python-service`

适用证据：Python 服务、库、CLI 或数据处理项目，存在 `pyproject.toml`、package modules、API routers、service modules、tests、scripts。

推荐契约字段：

- package_layout
- app_or_cli_entrypoints
- router_or_command_paths
- service_module_paths
- schema_model_paths
- config_env_policy
- test_lint_typecheck_commands
- migration_or_data_paths
- docs_and_spec_paths

## `custom`

当以上 profile 都不适配，或项目契约由用户私有框架定义时使用。

要求：

- 至少列出 5 个与该项目真实结构相关的契约字段。
- 每个字段必须有证据路径。
- 明确哪些通用字段 `not-applicable`，避免模型回退到熟悉框架。
- 给出 `forbidden_tokens`，防止后续产物落回错误画像。

## Contract Snapshot 规则

Contract Snapshot 是后续父/子 PRD、`design.md`、`implement.md`、JSONL 的机械扫描依据。

```yaml
contract_snapshot:
  profile: <selected profile>
  adopted_values:
    <field>: <value>
  forbidden_tokens:
    - token: <wrong value>
      reason: <conflict/default-misread/old-task-error>
      evidence: <path>
```

规则：

- `adopted_values` 必须具体到路径、命令、API、包/模块、路由、表名或权限前缀。
- 没有证据的值不能进入 `adopted_values`。
- `forbidden_tokens` 不要求每个字段都有，但已发现冲突时必须记录。
- 如果某字段在当前任务不适用，写 `not-applicable`；不要删除字段后让执行模型自行猜。
