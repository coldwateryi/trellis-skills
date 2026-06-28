# Design Surface Template

This file defines the design-surface template for `trellis-zero-to-mvp`. Child PRDs declare impact surfaces only; detailed design goes in `design.md`; files, steps, and commands go in `implement.md`.

## Usage Rules

1. First mark whether each surface is involved in the child PRD `Task Impact Matrix`.
2. If any surface is marked `yes`, `design.md` must contain the matching design section and `implement.md` must contain the matching implementation-plan section.
3. For non-applicable surfaces, write `no` and explain the reason in risk or out-of-scope notes. Do not leave rows blank.
4. This template is a section library. Copy only the sections involved in the task; do not generate irrelevant empty tables just for completeness.
5. For RuoYi/Vue projects, reuse existing page, API, permission, dictionary, SQL, entity, and Mapper style first. Do not invent a new style.

## Surface Mapping

| Surface | design.md Section | implement.md Section | Failure Code |
| --- | --- | --- | --- |
| Database / data model | Database Schema Design | Database Migration Plan | DATABASE_SCHEMA_MISSING |
| API interface | API Contract Design | API Implementation Plan | API_CONTRACT_MISSING |
| Inter-module interaction | Inter-Module Interaction Design | Inter-Module Wiring Plan | INTER_MODULE_CONTRACT_MISSING |
| External system interface | External System Interface Design | External Adapter Plan | EXTERNAL_INTERFACE_CONTRACT_MISSING |
| UI / project style | UI Design and Style Contract | UI Implementation Plan | UI_DESIGN_MISSING |
| Permission / data scope | Permission and Data Scope Design | Permission Wiring Plan | PERMISSION_CONTRACT_MISSING |
| Dictionary / state machine | Dictionary and State Design | State Implementation Plan | STATE_TRANSITION_MISSING |
| Query / import / export | Query and Import Export Design | Query Export Plan | QUERY_CONTRACT_MISSING |
| Validation / error semantics | Validation and Error Semantics | Validation Implementation Plan | VALIDATION_CONTRACT_MISSING |
| Transaction / concurrency / idempotency | Transaction Concurrency and Idempotency Design | Transaction Implementation Plan | TRANSACTION_CONTRACT_MISSING |
| Async job / event | Async Job and Event Design | Job Event Plan | ASYNC_JOB_CONTRACT_MISSING |
| Audit / logging | Audit and Logging Design | Audit Implementation Plan | AUDIT_LOG_CONTRACT_MISSING |
| Initialization / migration | Data Initialization and Migration Design | Migration Plan | MIGRATION_COMPATIBILITY_MISSING |
| Test strategy | Test Strategy Design | Test Implementation Plan | TEST_STRATEGY_MISSING |
| Performance / capacity | Performance and Capacity Design | Performance Verification Plan | PERFORMANCE_CONSTRAINT_MISSING |
| Security / sensitive data | Security and Sensitive Data Design | Security Verification Plan | SECURITY_CONTRACT_MISSING |
| Configuration / environment | Configuration Design | Configuration Plan | CONFIG_CONTRACT_MISSING |
| Framework conventions | Framework Convention Design | Framework Implementation Plan | FRAMEWORK_CONVENTION_MISSING |
| Manual acceptance | Manual Acceptance Design | Manual Verification Plan | MANUAL_ACCEPTANCE_UNCLEAR |
| Documentation / operations | Documentation and Operations Handoff | Docs Ops Plan | OPS_DOC_CONTRACT_MISSING |

## design.md Section Templates

### Database Schema Design

| Table | Purpose | Primary Key | Owning Module | Notes |
| --- | --- | --- | --- | --- |
| <table> | <purpose> | <pk> | <module> | <notes> |

| Table | Column | DB Type | Java/DTO Type | Non-null | Default | Constraint | Meaning |
| --- | --- | --- | --- | --- | --- | --- | --- |
| <table> | <column> | <type> | <type> | yes/no | <value> | <unique/index/fk/none> | <meaning> |

| Table | Index/Constraint Name | Columns | Type | Reason |
| --- | --- | --- | --- | --- |
| <table> | <idx_name> | <columns> | unique/index/fk | <reason> |

| Source Table | Source Field | Target Table | Target Field | Relationship | Delete/Update Policy |
| --- | --- | --- | --- | --- | --- |
| <table> | <field> | <table> | <field> | 1:1/1:n/n:n | <policy> |

### API Contract Design

| Interface | Method | Path | Permission | Purpose | Caller |
| --- | --- | --- | --- | --- | --- |
| <name> | GET/POST/PUT/DELETE | <path> | <permission or none> | <purpose> | <caller> |

| Interface | Parameter | Location | Type | Required | Default | Validation | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| <method path> | <param> | path/query/body/header | <type> | yes/no | <value> | <rule> | <notes> |

| Interface | Success Response | Failure Response | Notes |
| --- | --- | --- | --- |
| <method path> | <AjaxResult/TableDataInfo/schema> | <error schema> | <notes> |

| Scenario | Response Shape | Error Message | HTTP/code |
| --- | --- | --- | --- |
| <case> | <schema> | <message> | <code> |

### Inter-Module Interaction Design

| Caller Module | Callee Module | Interaction | Interface/Method | Input | Output | Transaction Boundary | Failure Strategy |
| --- | --- | --- | --- | --- | --- | --- | --- |
| <caller> | <callee> | Service/Event/HTTP/Adapter | <method> | <input> | <output> | <transaction> | <failure handling> |

Rules:

- Prefer Service or explicit Adapter for cross-module reads; do not inject another module's Mapper directly.
- A module must not write another module's owned tables unless the table is explicitly authorized.
- Do not copy another module's business judgment. Reuse its Service or extract an explicit domain service.

### External System Interface Design

| External System | Purpose | Protocol | Direction | Auth | Config Keys | Status |
| --- | --- | --- | --- | --- | --- | --- |
| <system> | <purpose> | HTTP/MQ/file/hardware | inbound/outbound | <auth> | <config keys> | FIXED/BASELINE/BLOCKED/OUT_OF_SCOPE |

| External System | Method | URL/Topic | Request Fields | Response Fields | Timeout | Retry | Fallback |
| --- | --- | --- | --- | --- | --- | --- | --- |
| <system> | <method> | <endpoint> | <fields> | <fields> | <timeout> | <retry> | <fallback> |

| Config Key | Source | Required | Default | Behavior When Missing |
| --- | --- | --- | --- | --- |
| <key> | application.yml/env/sys_config | yes/no | <value> | <behavior> |

### UI Design and Style Contract

| Item | Adopted Value |
| --- | --- |
| UI framework | <Element UI / Element Plus / project-specific> |
| Page type | <RuoYi list CRUD / detail / dashboard / wizard form / dialog> |
| Reference page | <existing page path> |
| Page path | <target page path> |
| API file | <target API file path> |
| Permission prefix | <permission prefix> |
| Dictionary dependencies | <dict type or none> |

| Area | Component/Pattern | Notes |
| --- | --- | --- |
| Query area | <query form pattern> | <fields> |
| Toolbar | <toolbar pattern> | <buttons> |
| Table | <table pattern> | <columns> |
| Dialog/Form | <dialog/form pattern> | <fields> |

| Column | Field | Display Component | Width | Formatting | Permission/Condition |
| --- | --- | --- | --- | --- | --- |
| <label> | <field> | <component> | <width> | <format> | <permission/condition> |

| Field | Component | Required | Validation | Default | Data Source |
| --- | --- | --- | --- | --- | --- |
| <field> | <component> | yes/no | <rule> | <value> | <source> |

| State | Behavior |
| --- | --- |
| loading | <behavior> |
| empty | <behavior> |
| success | <behavior> |
| failure | <behavior> |

### Permission and Data Scope Design

| Operation | Backend Permission | Frontend Button Permission | Menu Permission | Data Scope Rule | No-Permission Behavior |
| --- | --- | --- | --- | --- | --- |
| <operation> | <permission> | <v-hasPermi or none> | <menu/button> | <scope rule> | <behavior> |

### Dictionary and State Design

| Field | Type | Dict Type / Enum | Allowed Values | Display Labels | Default | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| <field> | dict/enum/state | <dict or enum> | <values> | <labels> | <default> | <notes> |

| Current State | Action | Target State | Allowed Role | Precondition | Illegal Behavior |
| --- | --- | --- | --- | --- | --- |
| <from> | <action> | <to> | <role> | <condition> | <error> |

### Query and Import Export Design

| Query Item | Field | Match Type | Default | Backend Landing | Frontend Component |
| --- | --- | --- | --- | --- | --- |
| <label> | <field> | like/eq/range | <default> | <backend location> | <component> |

| Capability | Supported | Permission | File/Fields | Behavior |
| --- | --- | --- | --- | --- |
| Export | yes/no | <permission> | <fields/file> | <behavior> |
| Import | yes/no | <permission> | <fields/file> | <behavior> |

### Validation and Error Semantics

| Field/Operation | Frontend Validation | Backend Validation | Business Validation | Error Message | Acceptance Point |
| --- | --- | --- | --- | --- | --- |
| <field/action> | <rule> | <rule> | <rule> | <message> | <AC> |

### Transaction Concurrency and Idempotency Design

| Scenario | Transaction Boundary | Concurrency Risk | Idempotency Strategy | Failure Recovery |
| --- | --- | --- | --- | --- |
| <scenario> | <boundary> | <risk> | <idempotency> | <recovery> |

### Async Job and Event Design

| Type | Name | Trigger | Input | Output | Idempotency/Lock | Failure Handling |
| --- | --- | --- | --- | --- | --- | --- |
| scheduled job/event/message | <name> | <trigger> | <input> | <output> | <strategy> | <failure handling> |

### Audit and Logging Design

| Scenario | Log Type | Location | Recorded Fields | Masking Rule |
| --- | --- | --- | --- | --- |
| <scenario> | operation/business/external/security | <location> | <fields> | <masking> |

### Data Initialization and Migration Design

| Type | File | Content | Rollback |
| --- | --- | --- | --- |
| menu SQL/dictionary SQL/field backfill/config | <path> | <content> | <rollback> |

### Test Strategy Design

| AC | Test Type | Test File | Input | Expected |
| --- | --- | --- | --- | --- |
| <AC> | unit/service/mapper/controller/frontend/e2e/manual | <path> | <input> | <expected> |

### Performance and Capacity Design

| Scenario | Scale Assumption | Design Constraint | Verification |
| --- | --- | --- | --- |
| <scenario> | <scale> | <constraint> | <verification> |

### Security and Sensitive Data Design

| Data/Entry | Risk | Constraint | Verification |
| --- | --- | --- | --- |
| <data/entry> | <risk> | <constraint> | <verification> |

### Configuration Design

| Config Key | Location | Default | Required | Missing Behavior | Environment Difference |
| --- | --- | --- | --- | --- | --- |
| <key> | <location> | <default> | yes/no | <behavior> | <dev/test/prod> |

### Framework Convention Design

| Convention | Adopted Value | Evidence |
| --- | --- | --- |
| <framework convention> | <adopted value> | <path> |

### Manual Acceptance Design

| Item | Preconditions | Steps | Pass Criteria | Evidence |
| --- | --- | --- | --- | --- |
| <item> | <precondition> | <steps> | <pass criteria> | <screenshot/log/report> |

### Documentation and Operations Handoff

| Item | Needed | Document Location | Content |
| --- | --- | --- | --- |
| config notes/ops check/user notes | yes/no | <path or none> | <content> |

## implement.md Implementation Plan Section Template

Each involved surface needs at least one corresponding plan section in `implement.md`. Use this common format:

```markdown
## <Surface Implementation Plan>

| Step | File | Action | Exact Location | Verification |
| --- | --- | --- | --- | --- |
| 1 | <path> | new/modify | <method/section> | <command/assertion> |
```

Section titles must match the `implement.md` section names in Surface Mapping so the mechanical Gate can scan them.
