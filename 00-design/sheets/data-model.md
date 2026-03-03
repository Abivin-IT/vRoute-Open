# Data Model Summary

> Cross-app entity/table registry. Source: JPA entities (vKernel) + SQLAlchemy models (vApps).
> Total: **26 entities**, **295 columns** across 5 apps.

## Entity Registry

| #   | App              | Feature        | Table Name                       | Columns | Key Columns                                                                                 | Notes                          |
| --- | ---------------- | -------------- | -------------------------------- | ------- | ------------------------------------------------------------------------------------------- | ------------------------------ |
| 1   | vKernel          | App Engine     | `kernel_app_registry`            | 9       | PK: `id` (UUID), `app_id` (unique), `status`                                                | Installed app metadata         |
| 2   | vKernel          | App Engine     | `kernel_permissions`             | 8       | PK: `id` (UUID), `permission_code` (unique), `app_id`, `is_active`                          | Injected permission codes      |
| 3   | vKernel          | IAM            | `kernel_users`                   | 6       | PK: `id` (UUID), `email` (unique), `roles`, `tenant_id`                                     | Platform user accounts         |
| 4   | vKernel          | IAM            | `kernel_refresh_tokens`          | 9       | PK: `id` (UUID), `user_email`, `token_hash` (unique), `revoked`, `expires_at`               | JWT refresh token rotation     |
| 5   | vKernel          | IAM            | `kernel_oidc_accounts`           | 9       | PK: `id` (UUID), `user_email`, `provider`+`provider_sub` (unique composite)                 | Linked SSO accounts            |
| 6   | vKernel          | IAM            | `kernel_magic_links`             | 7       | PK: `id` (UUID), `email`, `token_hash` (unique), `used`, `expires_at`                       | Passwordless login tokens      |
| 7   | vKernel          | Data Backbone  | `kernel_tenants`                 | 9       | PK: `id` (UUID), `code` (unique), `status`, `country_code`                                  | Multi-tenant registry          |
| 8   | vKernel          | Data Backbone  | `kernel_currencies`              | 5       | PK: `code` (ISO 4217), `is_active`                                                          | Reference: currencies          |
| 9   | vKernel          | Data Backbone  | `kernel_countries`               | 5       | PK: `code` (ISO 3166-1), FK: `currency` → currencies, `is_active`                           | Reference: countries           |
| 10  | vKernel          | Data Backbone  | `kernel_stakeholders`            | 11      | PK: `id` (UUID), `tenant_id`+`code` (unique composite), `type`, `metadata` (JSONB)          | Golden Record stakeholders     |
| 11  | vKernel          | Event Bus      | `kernel_event_log`               | 9       | PK: `id` (UUID), `event_type`, `source_app`, `status`, `correlation_id`                     | Immutable audit trail          |
| 12  | vKernel          | Event Bus      | `kernel_event_subscriptions`     | 5       | PK: `id` (UUID), `subscriber_app`+`event_type` (unique composite)                           | Event subscriptions            |
| 13  | vKernel          | Search         | `kernel_search_index`            | 8       | PK: `id` (UUID), `entity_type`, `entity_id`, `tenant_id`                                    | FTS index entries              |
| 14  | vStrategy        | Plan           | `vstrategy_plans`                | 15      | PK: `id` (UUID), `tenant_id`, `status`, `period_type`, `selected_option`                    | Strategic plans                |
| 15  | vStrategy        | Alignment      | `vstrategy_alignment_nodes`      | 20      | PK: `id` (UUID), FK: `plan_id` → plans, `parent_id` → self, `node_level`, `bsc_perspective` | Recursive alignment tree       |
| 16  | vStrategy        | Pivot Signal   | `vstrategy_pivot_signals`        | 14      | PK: `id` (UUID), FK: `plan_id` → plans, `rule_code`, `triggered`, `severity`                | Automatic pivot triggers       |
| 17  | vFinacc          | Ledger         | `vfinacc_ledger_entries`         | 17      | PK: `id` (UUID), `tenant_id`, `entry_number`, `status`, `amount`, `currency`                | Journal entries (DRAFT/POSTED) |
| 18  | vFinacc          | Transaction    | `vfinacc_transactions`           | 13      | PK: `id` (UUID), `tenant_id`, `source`, `status`, FK: `ledger_entry_id` → ledger            | Raw bank/ERP transactions      |
| 19  | vFinacc          | Reconciliation | `vfinacc_reconciliation_matches` | 13      | PK: `id` (UUID), `tenant_id`, `match_type`, `confidence_pct`, `status`                      | 3-way PO/GRN/Invoice match     |
| 20  | vFinacc          | Cost Center    | `vfinacc_cost_allocations`       | 12      | PK: `id` (UUID), `tenant_id`, `cost_center_code`, `category`, `budget_amount`               | GROW/RUN/TRANSFORM/GIVE        |
| 21  | vFinacc          | Compliance     | `vfinacc_compliance_checks`      | 11      | PK: `id` (UUID), FK: `ledger_entry_id` → ledger, `check_type`, `result`                     | Tax & compliance checks        |
| 22  | vDesign Physical | Golden Sample  | `vdesign_golden_samples`         | 21      | PK: `id` (UUID), `tenant_id`, `sample_code`, `status`, `convergence_pct`                    | Physical spec vault            |
| 23  | vDesign Physical | Material       | `vdesign_material_inbox`         | 14      | PK: `id` (UUID), `tenant_id`, `item_code`, `source_type`, `status`                          | Incoming material inbox        |
| 24  | vDesign Physical | Prototype      | `vdesign_prototypes`             | 14      | PK: `id` (UUID), `tenant_id`, `proto_code`, `version_label`, `status`                       | Prototype versions             |
| 25  | vDesign Physical | Lab Test       | `vdesign_lab_tests`              | 13      | PK: `id` (UUID), FK: `golden_sample_id`, `prototype_id`, `test_type`, `result`              | Feasibility lab tests          |
| 26  | vDesign Physical | Handover Kit   | `vdesign_handover_kits`          | 14      | PK: `id` (UUID), `tenant_id`, `kit_code`, `status`, `destination`                           | Tooling handover kits          |
| 27  | vMarketing Org   | Campaign       | `campaigns`                      | 18      | PK: `id` (UUID), `tenant_id`, `campaign_code`, `stage`, `status`, `channel`                 | ABM campaigns                  |
| 28  | vMarketing Org   | Tracking       | `tracking_events`                | 12      | PK: `id` (UUID), `tenant_id`, `event_code`, `organization`, `intent_score`                  | Pixel tracking events          |
| 29  | vMarketing Org   | Segment        | `audience_segments`              | 12      | PK: `id` (UUID), `tenant_id`, `segment_code`, `tier`, `status`                              | Audience segmentation          |
| 30  | vMarketing Org   | Content Asset  | `content_assets`                 | 15      | PK: `id` (UUID), `tenant_id`, `asset_code`, `asset_type`, `status`                          | Marketing content library      |
| 31  | vMarketing Org   | Lead Score     | `lead_scores`                    | 13      | PK: `id` (UUID), `tenant_id`, `organization`, `score`, `grade`, `status`                    | AI lead grading                |

## Column Count by App

| App              | Stack                         | Entities | Total Columns | DB Prefix        |
| ---------------- | ----------------------------- | -------- | ------------- | ---------------- |
| vKernel          | Java 21 / JPA + Flyway        | 13       | 100           | `kernel_`        |
| vStrategy        | Python / SQLAlchemy + Alembic | 3        | 49            | `vstrategy_`     |
| vFinacc          | Python / SQLAlchemy + Alembic | 5        | 66            | `vfinacc_`       |
| vDesign Physical | Python / SQLAlchemy + Alembic | 5        | 76            | `vdesign_`       |
| vMarketing Org   | Python / SQLAlchemy + Alembic | 5        | 70            | — (app-specific) |
| **Total**        |                               | **31**   | **361**       |                  |

## Common Patterns

All entities share these cross-cutting columns:

| Column          | Type        | Purpose                             | Present In                                         |
| --------------- | ----------- | ----------------------------------- | -------------------------------------------------- |
| `id`            | UUID        | Primary key (`gen_random_uuid()`)   | All 31 entities                                    |
| `tenant_id`     | UUID        | Multi-tenant isolation              | All except `kernel_currencies`, `kernel_countries` |
| `created_at`    | TIMESTAMPTZ | Creation timestamp (`now()`)        | All entities                                       |
| `updated_at`    | TIMESTAMPTZ | Last update timestamp               | Most entities                                      |
| `status`        | VARCHAR(20) | State machine (app-specific values) | 25 of 31 entities                                  |
| `metadata_json` | JSONB       | Extensible metadata                 | vKernel stakeholders, all vFinacc entities         |
