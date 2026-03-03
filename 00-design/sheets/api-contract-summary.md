# API Contract Summary

> Cross-app endpoint registry. Source: PRD §4 + actual `routes.py` / `*Controller.java` files.
> Total: **97 REST API endpoints** across 5 apps (excluding HTML view routes).

## Endpoint Registry

| #   | App              | Feature          | Method | Endpoint                                                         | Auth                            | Req ID         | Description                            |
| --- | ---------------- | ---------------- | ------ | ---------------------------------------------------------------- | ------------------------------- | -------------- | -------------------------------------- |
| 1   | vKernel          | App Engine       | GET    | `/api/v1/apps`                                                   | Bearer                          | SyR-PLAT-00    | List all active installed apps         |
| 2   | vKernel          | App Engine       | POST   | `/api/v1/apps/install`                                           | Bearer + `X-Request-ID`         | SyR-PLAT-00    | Install an app from manifest           |
| 3   | vKernel          | App Engine       | DELETE | `/api/v1/apps/{appId}`                                           | Bearer                          | SyR-PLAT-00    | Uninstall (deactivate) an app          |
| 4   | vKernel          | App Engine       | GET    | `/api/v1/apps/permissions`                                       | Bearer                          | SyR-PLAT-01    | List injected permissions              |
| 5   | vKernel          | IAM — Auth       | POST   | `/api/v1/auth/register`                                          | Public                          | SyR-PLAT-01    | Register a new platform user           |
| 6   | vKernel          | IAM — Auth       | POST   | `/api/v1/auth/login`                                             | Public                          | SyR-PLAT-01    | Login (email+password → JWT + refresh) |
| 7   | vKernel          | IAM — Auth       | POST   | `/api/v1/auth/refresh`                                           | Public                          | SyR-PLAT-01    | Refresh access token (rotation)        |
| 8   | vKernel          | IAM — Auth       | POST   | `/api/v1/auth/logout`                                            | Bearer                          | SyR-PLAT-01    | Revoke all refresh tokens              |
| 9   | vKernel          | IAM — Magic Link | POST   | `/api/v1/auth/magic-link`                                        | Public                          | SyR-PLAT-01    | Request passwordless magic link        |
| 10  | vKernel          | IAM — Magic Link | GET    | `/api/v1/auth/magic-link/verify`                                 | Public                          | SyR-PLAT-01    | Verify magic link → issue JWT          |
| 11  | vKernel          | IAM — OIDC       | GET    | `/api/v1/auth/oidc/{provider}`                                   | Public                          | SyR-PLAT-01    | Initiate OIDC flow (google/ms/github)  |
| 12  | vKernel          | IAM — OIDC       | GET    | `/api/v1/auth/oidc/{provider}/callback`                          | Public                          | SyR-PLAT-01    | OIDC callback → exchange code for JWT  |
| 13  | vKernel          | IAM — OIDC       | GET    | `/api/v1/auth/oidc/accounts`                                     | Bearer                          | SyR-PLAT-01    | List linked OIDC accounts              |
| 14  | vKernel          | Data Backbone    | PATCH  | `/api/v1/data/entities/{type}/{id}/extend`                       | `X-App-ID` + `X-User-ID`        | SyR-PLAT-02    | Extend core entity with JSONB fields   |
| 15  | vKernel          | Data Backbone    | GET    | `/api/v1/data/currencies`                                        | Bearer                          | SyR-PLAT-02    | List active currencies                 |
| 16  | vKernel          | Data Backbone    | GET    | `/api/v1/data/countries`                                         | Bearer                          | SyR-PLAT-02    | List active countries                  |
| 17  | vKernel          | Data Backbone    | GET    | `/api/v1/data/stakeholders`                                      | Bearer                          | SyR-PLAT-02    | List stakeholders by tenant            |
| 18  | vKernel          | Data Backbone    | POST   | `/api/v1/data/stakeholders`                                      | Bearer                          | SyR-PLAT-02    | Create golden record stakeholder       |
| 19  | vKernel          | Event Bus        | POST   | `/api/v1/events/publish`                                         | `X-App-ID` + `X-Correlation-ID` | SyR-PLAT-03    | Publish event to bus                   |
| 20  | vKernel          | Event Bus        | POST   | `/api/v1/events/subscribe`                                       | `X-App-ID`                      | SyR-PLAT-03    | Register event subscription            |
| 21  | vKernel          | Event Bus        | GET    | `/api/v1/events/subscriptions`                                   | `X-App-ID`                      | SyR-PLAT-03    | List subscriptions for an app          |
| 22  | vKernel          | Event Bus        | GET    | `/api/v1/events/log`                                             | Bearer                          | SyR-PLAT-03    | Audit trail — paginated event log      |
| 23  | vKernel          | Search           | GET    | `/api/v1/search`                                                 | Bearer                          | SyR-PLAT-02    | Unified full-text search               |
| 24  | vKernel          | Search           | POST   | `/api/v1/search/index`                                           | `X-App-ID`                      | SyR-PLAT-02    | Index an entity for search             |
| 25  | vStrategy        | Plan             | GET    | `/api/v1/vstrategy/plans`                                        | Bearer                          | SyR-STR-00     | List plans                             |
| 26  | vStrategy        | Plan             | POST   | `/api/v1/vstrategy/plans`                                        | Bearer                          | SyR-STR-00     | Create a plan                          |
| 27  | vStrategy        | Plan             | GET    | `/api/v1/vstrategy/plans/{plan_id}`                              | Bearer                          | SyR-STR-00     | Get plan by ID                         |
| 28  | vStrategy        | Plan             | PUT    | `/api/v1/vstrategy/plans/{plan_id}`                              | Bearer                          | SyR-STR-00     | Update plan                            |
| 29  | vStrategy        | Alignment        | GET    | `/api/v1/vstrategy/plans/{plan_id}/tree`                         | Bearer                          | SyR-STR-00     | Get alignment tree                     |
| 30  | vStrategy        | Alignment        | POST   | `/api/v1/vstrategy/plans/{plan_id}/nodes`                        | Bearer                          | SyR-STR-00     | Add alignment node                     |
| 31  | vStrategy        | Alignment        | PUT    | `/api/v1/vstrategy/nodes/{node_id}`                              | Bearer                          | SyR-STR-00     | Update alignment node                  |
| 32  | vStrategy        | Alignment        | POST   | `/api/v1/vstrategy/nodes/{node_id}/propagate`                    | Bearer                          | SyR-STR-00     | Propagate status through tree          |
| 33  | vStrategy        | Scorecard        | GET    | `/api/v1/vstrategy/plans/{plan_id}/scorecard`                    | Bearer                          | SyR-STR-04     | Get scorecard for plan                 |
| 34  | vStrategy        | SOP              | GET    | `/api/v1/vstrategy/plans/{plan_id}/sop/validate`                 | Bearer                          | SyR-STR-03     | Validate S&OP                          |
| 35  | vStrategy        | Pivot Signal     | GET    | `/api/v1/vstrategy/plans/{plan_id}/signals`                      | Bearer                          | SyR-STR-04     | Get pivot signals                      |
| 36  | vStrategy        | Pivot Signal     | POST   | `/api/v1/vstrategy/plans/{plan_id}/signals/check`                | Bearer                          | SyR-STR-04     | Check pivot signal against rule        |
| 37  | vFinacc          | Ledger           | GET    | `/api/v1/vfinacc/ledger`                                         | finance.ledger.view             | SyR-FIN-00     | List journal entries                   |
| 38  | vFinacc          | Ledger           | POST   | `/api/v1/vfinacc/ledger`                                         | finance.ledger.post             | SyR-FIN-00     | Create draft journal entry             |
| 39  | vFinacc          | Ledger           | GET    | `/api/v1/vfinacc/ledger/{entry_id}`                              | finance.ledger.view             | SyR-FIN-00     | Get ledger entry by ID                 |
| 40  | vFinacc          | Ledger           | PUT    | `/api/v1/vfinacc/ledger/{entry_id}`                              | finance.ledger.post             | SyR-FIN-00     | Update draft entry                     |
| 41  | vFinacc          | Ledger           | POST   | `/api/v1/vfinacc/ledger/{entry_id}/post`                         | finance.ledger.post             | SyR-FIN-00     | Post (finalize) draft entry            |
| 42  | vFinacc          | Transaction      | GET    | `/api/v1/vfinacc/transactions`                                   | finance.ledger.view             | SyR-FIN-01     | List raw transactions                  |
| 43  | vFinacc          | Transaction      | POST   | `/api/v1/vfinacc/transactions`                                   | finance.transaction.approve     | SyR-FIN-01     | Ingest raw transaction                 |
| 44  | vFinacc          | Transaction      | GET    | `/api/v1/vfinacc/transactions/{txn_id}`                          | finance.ledger.view             | SyR-FIN-01     | Get transaction by ID                  |
| 45  | vFinacc          | Reconciliation   | GET    | `/api/v1/vfinacc/reconciliation`                                 | finance.ledger.view             | SyR-FIN-02     | List reconciliation matches            |
| 46  | vFinacc          | Reconciliation   | POST   | `/api/v1/vfinacc/reconciliation/run`                             | finance.transaction.approve     | SyR-FIN-02     | Run 3-way matching engine              |
| 47  | vFinacc          | Reconciliation   | GET    | `/api/v1/vfinacc/reconciliation/summary`                         | finance.ledger.view             | SyR-FIN-02     | Summary stats                          |
| 48  | vFinacc          | Cost Center      | GET    | `/api/v1/vfinacc/cost-centers`                                   | finance.ledger.view             | SyR-FIN-03     | List cost allocations                  |
| 49  | vFinacc          | Cost Center      | POST   | `/api/v1/vfinacc/cost-centers`                                   | finance.transaction.approve     | SyR-FIN-03     | Create cost allocation                 |
| 50  | vFinacc          | Cost Center      | GET    | `/api/v1/vfinacc/cost-centers/summary`                           | finance.ledger.view             | SyR-FIN-03     | GROW/RUN/TRANSFORM summary             |
| 51  | vFinacc          | Compliance       | GET    | `/api/v1/vfinacc/compliance`                                     | finance.compliance.manage       | SyR-FIN-04     | List compliance checks                 |
| 52  | vFinacc          | Compliance       | POST   | `/api/v1/vfinacc/compliance/check`                               | finance.compliance.manage       | SyR-FIN-04     | Run compliance check                   |
| 53  | vFinacc          | Compliance       | GET    | `/api/v1/vfinacc/compliance/summary`                             | finance.compliance.manage       | SyR-FIN-04     | Tax & compliance summary               |
| 54  | vDesign Physical | Golden Sample    | GET    | `/api/v1/vdesign-physical/golden-samples`                        | Bearer                          | SyR-PHY-00     | List golden samples                    |
| 55  | vDesign Physical | Golden Sample    | POST   | `/api/v1/vdesign-physical/golden-samples`                        | Bearer                          | SyR-PHY-00     | Create golden sample                   |
| 56  | vDesign Physical | Golden Sample    | GET    | `/api/v1/vdesign-physical/golden-samples/{sample_id}`            | Bearer                          | SyR-PHY-00     | Get golden sample by ID                |
| 57  | vDesign Physical | Golden Sample    | PUT    | `/api/v1/vdesign-physical/golden-samples/{sample_id}`            | Bearer                          | SyR-PHY-00     | Update golden sample                   |
| 58  | vDesign Physical | Golden Sample    | POST   | `/api/v1/vdesign-physical/golden-samples/{sample_id}/seal`       | Bearer                          | SyR-PHY-00     | Seal (lock) golden sample              |
| 59  | vDesign Physical | Golden Sample    | POST   | `/api/v1/vdesign-physical/golden-samples/{sample_id}/compromise` | Bearer                          | SyR-PHY-00     | Mark as compromised                    |
| 60  | vDesign Physical | Material         | GET    | `/api/v1/vdesign-physical/materials`                             | Bearer                          | SyR-PHY-01     | List materials                         |
| 61  | vDesign Physical | Material         | POST   | `/api/v1/vdesign-physical/materials`                             | Bearer                          | SyR-PHY-01     | Ingest new material                    |
| 62  | vDesign Physical | Material         | GET    | `/api/v1/vdesign-physical/materials/{material_id}`               | Bearer                          | SyR-PHY-01     | Get material by ID                     |
| 63  | vDesign Physical | Material         | POST   | `/api/v1/vdesign-physical/materials/{material_id}/scrap`         | Bearer                          | SyR-PHY-01     | Scrap a material                       |
| 64  | vDesign Physical | Prototype        | GET    | `/api/v1/vdesign-physical/prototypes`                            | Bearer                          | SyR-PHY-02     | List prototypes                        |
| 65  | vDesign Physical | Prototype        | POST   | `/api/v1/vdesign-physical/prototypes`                            | Bearer                          | SyR-PHY-02     | Create prototype                       |
| 66  | vDesign Physical | Prototype        | GET    | `/api/v1/vdesign-physical/prototypes/{proto_id}`                 | Bearer                          | SyR-PHY-02     | Get prototype by ID                    |
| 67  | vDesign Physical | Prototype        | POST   | `/api/v1/vdesign-physical/prototypes/{proto_id}/retire`          | Bearer                          | SyR-PHY-02     | Retire prototype                       |
| 68  | vDesign Physical | Lab Test         | GET    | `/api/v1/vdesign-physical/lab-tests`                             | Bearer                          | SyR-PHY-03     | List lab tests                         |
| 69  | vDesign Physical | Lab Test         | POST   | `/api/v1/vdesign-physical/lab-tests`                             | Bearer                          | SyR-PHY-03     | Create lab test                        |
| 70  | vDesign Physical | Lab Test         | GET    | `/api/v1/vdesign-physical/lab-tests/summary`                     | Bearer                          | SyR-PHY-03     | Lab test summary statistics            |
| 71  | vDesign Physical | Lab Test         | GET    | `/api/v1/vdesign-physical/lab-tests/{test_id}`                   | Bearer                          | SyR-PHY-03     | Get lab test by ID                     |
| 72  | vDesign Physical | Lab Test         | POST   | `/api/v1/vdesign-physical/lab-tests/{test_id}/complete`          | Bearer                          | SyR-PHY-03     | Complete lab test with result          |
| 73  | vDesign Physical | Handover Kit     | GET    | `/api/v1/vdesign-physical/handover-kits`                         | Bearer                          | SyR-PHY-04     | List handover kits                     |
| 74  | vDesign Physical | Handover Kit     | POST   | `/api/v1/vdesign-physical/handover-kits`                         | Bearer                          | SyR-PHY-04     | Create handover kit                    |
| 75  | vDesign Physical | Handover Kit     | GET    | `/api/v1/vdesign-physical/handover-kits/{kit_id}`                | Bearer                          | SyR-PHY-04     | Get handover kit by ID                 |
| 76  | vDesign Physical | Handover Kit     | POST   | `/api/v1/vdesign-physical/handover-kits/{kit_id}/advance`        | Bearer                          | SyR-PHY-04     | Dispatch/advance kit                   |
| 77  | vDesign Physical | Handover Kit     | POST   | `/api/v1/vdesign-physical/handover-kits/{kit_id}/receive`        | Bearer                          | SyR-PHY-04     | Mark kit as received                   |
| 78  | vMarketing Org   | Campaign         | GET    | `/api/v1/vmarketing-org/campaigns`                               | Bearer                          | SyR-MKT-ORG-00 | List campaigns                         |
| 79  | vMarketing Org   | Campaign         | GET    | `/api/v1/vmarketing-org/campaigns/{campaign_id}`                 | Bearer                          | SyR-MKT-ORG-00 | Get campaign by ID                     |
| 80  | vMarketing Org   | Campaign         | POST   | `/api/v1/vmarketing-org/campaigns`                               | Bearer                          | SyR-MKT-ORG-00 | Create campaign                        |
| 81  | vMarketing Org   | Campaign         | PATCH  | `/api/v1/vmarketing-org/campaigns/{campaign_id}`                 | Bearer                          | SyR-MKT-ORG-00 | Partial update campaign                |
| 82  | vMarketing Org   | Campaign         | POST   | `/api/v1/vmarketing-org/campaigns/{campaign_id}/launch`          | Bearer                          | SyR-MKT-ORG-00 | Launch campaign                        |
| 83  | vMarketing Org   | Campaign         | POST   | `/api/v1/vmarketing-org/campaigns/{campaign_id}/pause`           | Bearer                          | SyR-MKT-ORG-00 | Pause campaign                         |
| 84  | vMarketing Org   | Campaign         | POST   | `/api/v1/vmarketing-org/campaigns/{campaign_id}/complete`        | Bearer                          | SyR-MKT-ORG-00 | Complete campaign                      |
| 85  | vMarketing Org   | Tracking         | GET    | `/api/v1/vmarketing-org/tracking-events`                         | Bearer                          | SyR-MKT-ORG-01 | List tracking events                   |
| 86  | vMarketing Org   | Tracking         | GET    | `/api/v1/vmarketing-org/tracking-events/{event_id}`              | Bearer                          | SyR-MKT-ORG-01 | Get tracking event by ID               |
| 87  | vMarketing Org   | Tracking         | POST   | `/api/v1/vmarketing-org/tracking-events`                         | Bearer                          | SyR-MKT-ORG-01 | Ingest tracking event                  |
| 88  | vMarketing Org   | Tracking         | GET    | `/api/v1/vmarketing-org/tracking-events/intent-summary/{org}`    | Bearer                          | SyR-MKT-ORG-01 | Intent summary per org                 |
| 89  | vMarketing Org   | Segment          | GET    | `/api/v1/vmarketing-org/segments`                                | Bearer                          | SyR-MKT-ORG-02 | List audience segments                 |
| 90  | vMarketing Org   | Segment          | GET    | `/api/v1/vmarketing-org/segments/{segment_id}`                   | Bearer                          | SyR-MKT-ORG-02 | Get segment by ID                      |
| 91  | vMarketing Org   | Segment          | POST   | `/api/v1/vmarketing-org/segments`                                | Bearer                          | SyR-MKT-ORG-02 | Create audience segment                |
| 92  | vMarketing Org   | Segment          | POST   | `/api/v1/vmarketing-org/segments/{segment_id}/archive`           | Bearer                          | SyR-MKT-ORG-02 | Archive segment                        |
| 93  | vMarketing Org   | Content Asset    | GET    | `/api/v1/vmarketing-org/assets`                                  | Bearer                          | SyR-MKT-ORG-03 | List content assets                    |
| 94  | vMarketing Org   | Content Asset    | GET    | `/api/v1/vmarketing-org/assets/{asset_id}`                       | Bearer                          | SyR-MKT-ORG-03 | Get content asset by ID                |
| 95  | vMarketing Org   | Content Asset    | POST   | `/api/v1/vmarketing-org/assets`                                  | Bearer                          | SyR-MKT-ORG-03 | Create content asset                   |
| 96  | vMarketing Org   | Content Asset    | POST   | `/api/v1/vmarketing-org/assets/{asset_id}/publish`               | Bearer                          | SyR-MKT-ORG-03 | Publish content asset                  |
| 97  | vMarketing Org   | Content Asset    | POST   | `/api/v1/vmarketing-org/assets/{asset_id}/archive`               | Bearer                          | SyR-MKT-ORG-03 | Archive content asset                  |
| 98  | vMarketing Org   | Lead Score       | GET    | `/api/v1/vmarketing-org/leads`                                   | Bearer                          | SyR-MKT-ORG-04 | List leads                             |
| 99  | vMarketing Org   | Lead Score       | GET    | `/api/v1/vmarketing-org/leads/{lead_id}`                         | Bearer                          | SyR-MKT-ORG-04 | Get lead by ID                         |
| 100 | vMarketing Org   | Lead Score       | POST   | `/api/v1/vmarketing-org/leads`                                   | Bearer                          | SyR-MKT-ORG-04 | Upsert lead score                      |
| 101 | vMarketing Org   | Lead Score       | POST   | `/api/v1/vmarketing-org/leads/{lead_id}/qualify`                 | Bearer                          | SyR-MKT-ORG-04 | Qualify a lead                         |
| 102 | vMarketing Org   | Lead Score       | POST   | `/api/v1/vmarketing-org/leads/{lead_id}/handoff`                 | Bearer                          | SyR-MKT-ORG-04 | Hand off lead to sales                 |
| 103 | vMarketing Org   | Lead Score       | POST   | `/api/v1/vmarketing-org/leads/{lead_id}/disqualify`              | Bearer                          | SyR-MKT-ORG-04 | Disqualify a lead                      |

## Endpoint Count by App

| App              | Features                                                         | REST APIs | HTML Views | Total   |
| ---------------- | ---------------------------------------------------------------- | --------- | ---------- | ------- |
| vKernel          | 7 (engine, iam, data, event, search, grpc, shell)                | 24        | 17         | 41      |
| vStrategy        | 5 (plan, alignment, scorecard, sop, pivot_signal)                | 12        | —          | 12      |
| vFinacc          | 5 (ledger, transaction, reconciliation, cost_center, compliance) | 17        | —          | 17      |
| vDesign Physical | 5 (golden_sample, material, prototype, lab_test, handover_kit)   | 24        | —          | 24      |
| vMarketing Org   | 5 (campaign, tracking, segment, content_asset, lead_score)       | 26        | —          | 26      |
| **Total**        | **27**                                                           | **103**   | **17**     | **120** |

## Required Headers (All APIs)

| Header                  | Required By                                         | Purpose                    |
| ----------------------- | --------------------------------------------------- | -------------------------- |
| `Authorization: Bearer` | Most endpoints                                      | JWT access token           |
| `X-Request-ID`          | Install App                                         | Distributed tracing        |
| `X-App-ID`              | Permission Injection, Data Extension, Event Publish | Identifies calling App     |
| `X-App-Secret`          | Permission Injection                                | App-level authentication   |
| `X-User-ID`             | Data Extension                                      | Audit trail attribution    |
| `X-Correlation-ID`      | Event Publish                                       | End-to-end request tracing |

## Error Response Standard (§4.3.2)

All error responses follow this schema:

| Field            | Type   | Description                   |
| ---------------- | ------ | ----------------------------- |
| `error`          | string | `ERROR_CODE_IN_CAPS`          |
| `message`        | string | Human-readable message        |
| `details`        | object | Additional context (optional) |
| `correlation_id` | string | Request trace ID              |
