# Project Contract Profiles

Use this file early in read-only analysis to choose the project's contract profile. This prevents applying one framework's naming/path/artifact assumptions to an unrelated repository.

## Selection Rules

1. Choose a profile from user requirements, README, module README, AGENTS.md, `.trellis/spec/`, `.trellis/workflow.md`, and existing code evidence.
2. Adopt only evidence-backed fields; write `not-applicable`, `unknown-blocked`, or use `custom` when evidence is missing.
3. Do not fill Java entity, Controller package, Mapper XML, or permission-prefix fields in non-RuoYi / non-Java CRUD projects.
4. If the repository has multiple shapes, choose the main delivery surface as the primary profile and list auxiliary surfaces in `secondary_profiles`.
5. Contract Snapshot is generated only from adopted fields. `forbidden_tokens` come from conflicting candidates, old task mistakes, framework-default misreads, or values inconsistent with evidence.

## Output Format

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

Contract Lock uses profile-driven rows. Do not copy non-applicable fields:

| Contract Item | Profile Field | adopted_value | evidence_path | forbidden_tokens | notes |
| --- | --- | --- | --- | --- | --- |
| <item> | <field> | <specific value or not-applicable> | <path> | <tokens or none> | <notes> |

## `java-ruoyi-crud`

Use when evidence shows RuoYi / Spring Boot / MyBatis / Vue Admin CRUD with Java domain, controller, mapper XML, frontend views/api, permission strings, or SQL menu scripts.

Suggested contract fields:

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

Do not use this profile without RuoYi evidence.

Common RuoYi/Vue adopted-value examples:

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

Use for TypeScript CLI / SDK / monorepo / template frameworks with `package.json`, `packages/`, CLI commands, templates, workflow docs, or script templates.

Suggested contract fields:

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

For Trellis-like projects:

- `.trellis/workflow.md` is the local workflow contract.
- `.trellis/config.yaml` platform config and `codex.dispatch_mode` affect JSONL Gate.
- If Python `.trellis/scripts` are generated from templates, lock both source template paths and generated destinations. Avoid editing generated output while leaving source templates stale.
- CLI, SDK, templates, and workflow docs are independent contract surfaces; do not express them with Java Controller or database-table fields.

## `frontend-spa`

Use for single-page apps with routes/pages/components/API client/state management/build scripts.

Suggested contract fields:

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

Do not invent backend package paths, database tables, or Java entity fields.

## `python-service`

Use for Python service, library, CLI, or data-processing projects with `pyproject.toml`, package modules, API routers, service modules, tests, or scripts.

Suggested contract fields:

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

Use when default profiles do not fit or a private framework defines the contract.

Requirements:

- List at least 5 project-specific contract fields.
- Every field has evidence.
- Explicitly mark irrelevant generic fields `not-applicable` to prevent fallback to a familiar framework.
- Add `forbidden_tokens` to prevent later artifacts from falling back to the wrong profile.

## Contract Snapshot

Contract Snapshot is the mechanical scan basis for later parent/child PRDs, `design.md`, `implement.md`, and JSONL.

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

Rules:

- `adopted_values` must be concrete paths, commands, APIs, packages/modules, routes, tables, permission prefixes, or other project contracts.
- Values without evidence cannot enter `adopted_values`.
- `forbidden_tokens` are not required for every field, but must be recorded for discovered conflicts.
- If a field does not apply to this task, write `not-applicable`; do not remove it and let the execution model guess.
