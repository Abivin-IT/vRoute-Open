# vFinacc — Data Model

## Tables

### vfinacc_ledger_entries

| Column         | Type          | Nullable | Default           | Description                                |
| -------------- | ------------- | -------- | ----------------- | ------------------------------------------ |
| id             | UUID          | NO       | gen_random_uuid() | Primary key                                |
| tenant_id      | UUID          | NO       | default-tenant    | Multi-tenant isolation                     |
| entry_number   | VARCHAR(50)   | NO       |                   | Human-readable entry number (JE-2026-0001) |
| entry_date     | DATE          | NO       |                   | Journal entry date                         |
| description    | VARCHAR(500)  | NO       |                   | Entry description                          |
| debit_account  | VARCHAR(100)  | NO       |                   | Debit account code                         |
| credit_account | VARCHAR(100)  | NO       |                   | Credit account code                        |
| amount         | NUMERIC(15,2) | NO       | 0                 | Transaction amount                         |
| currency       | VARCHAR(3)    | NO       | VND               | ISO 4217 currency code                     |
| status         | VARCHAR(20)   | NO       | DRAFT             | DRAFT / POSTED / FLAGGED / REVERSED        |
| cost_center    | VARCHAR(100)  | YES      |                   | Associated cost center                     |
| metadata_json  | JSONB         | YES      | {}                | Extensible metadata                        |
| posted_by      | VARCHAR(255)  | YES      |                   | User who posted the entry                  |
| posted_at      | TIMESTAMPTZ   | YES      |                   | When entry was posted                      |
| created_by     | VARCHAR(255)  | YES      |                   | Creator                                    |
| created_at     | TIMESTAMPTZ   | NO       | now()             | Creation timestamp                         |
| updated_at     | TIMESTAMPTZ   | NO       | now()             | Last update timestamp                      |

### vfinacc_transactions

| Column           | Type          | Nullable | Default           | Description                            |
| ---------------- | ------------- | -------- | ----------------- | -------------------------------------- |
| id               | UUID          | NO       | gen_random_uuid() | Primary key                            |
| tenant_id        | UUID          | NO       | default-tenant    | Multi-tenant isolation                 |
| external_id      | VARCHAR(255)  | YES      |                   | External reference (bank txn ID, etc.) |
| source           | VARCHAR(50)   | NO       |                   | BANK_WEBHOOK / STRIPE / MANUAL / ERP   |
| amount           | NUMERIC(15,2) | NO       | 0                 | Transaction amount                     |
| currency         | VARCHAR(3)    | NO       | VND               | ISO 4217 currency code                 |
| counterparty     | VARCHAR(255)  | YES      |                   | Other party name                       |
| transaction_date | DATE          | NO       |                   | When the transaction occurred          |
| description      | VARCHAR(500)  | YES      |                   | Transaction memo                       |
| status           | VARCHAR(20)   | NO       | RAW               | RAW / MATCHED / RECONCILED / REJECTED  |
| ledger_entry_id  | UUID          | YES      |                   | FK to vfinacc_ledger_entries           |
| metadata_json    | JSONB         | YES      | {}                | Raw payload, bank data, etc.           |
| created_at       | TIMESTAMPTZ   | NO       | now()             | Creation timestamp                     |

### vfinacc_reconciliation_matches

| Column             | Type          | Nullable | Default           | Description                           |
| ------------------ | ------------- | -------- | ----------------- | ------------------------------------- |
| id                 | UUID          | NO       | gen_random_uuid() | Primary key                           |
| tenant_id          | UUID          | NO       | default-tenant    | Multi-tenant isolation                |
| po_reference       | VARCHAR(100)  | YES      |                   | Purchase Order reference              |
| grn_reference      | VARCHAR(100)  | YES      |                   | Goods Receipt Note reference          |
| invoice_reference  | VARCHAR(100)  | YES      |                   | Invoice reference                     |
| match_type         | VARCHAR(20)   | NO       |                   | FULL_MATCH / PARTIAL_MATCH / NO_MATCH |
| confidence_pct     | NUMERIC(5,2)  | NO       | 0                 | Match confidence (0-100)              |
| discrepancy_amount | NUMERIC(15,2) | YES      |                   | Amount difference found               |
| status             | VARCHAR(20)   | NO       | PENDING           | PENDING / APPROVED / REJECTED         |
| notes              | TEXT          | YES      |                   | Matching notes/explanation            |
| reviewed_by        | VARCHAR(255)  | YES      |                   | Reviewer                              |
| created_at         | TIMESTAMPTZ   | NO       | now()             | Creation timestamp                    |
| updated_at         | TIMESTAMPTZ   | NO       | now()             | Last update timestamp                 |

### vfinacc_cost_allocations

| Column           | Type          | Nullable | Default           | Description                           |
| ---------------- | ------------- | -------- | ----------------- | ------------------------------------- |
| id               | UUID          | NO       | gen_random_uuid() | Primary key                           |
| tenant_id        | UUID          | NO       | default-tenant    | Multi-tenant isolation                |
| cost_center_code | VARCHAR(50)   | NO       |                   | Cost center identifier                |
| cost_center_name | VARCHAR(255)  | NO       |                   | Human-readable name                   |
| category         | VARCHAR(20)   | NO       |                   | GROW / RUN / TRANSFORM / GIVE         |
| budget_amount    | NUMERIC(15,2) | NO       | 0                 | Allocated budget                      |
| actual_amount    | NUMERIC(15,2) | NO       | 0                 | Actual spend                          |
| currency         | VARCHAR(3)    | NO       | VND               | ISO 4217 currency code                |
| period_label     | VARCHAR(50)   | NO       |                   | Budget period (Q1-2026, FY2026, etc.) |
| owner            | VARCHAR(255)  | YES      |                   | Cost center owner                     |
| metadata_json    | JSONB         | YES      | {}                | Extensible metadata                   |
| created_at       | TIMESTAMPTZ   | NO       | now()             | Creation timestamp                    |
| updated_at       | TIMESTAMPTZ   | NO       | now()             | Last update timestamp                 |

### vfinacc_compliance_checks

| Column          | Type          | Nullable | Default           | Description                            |
| --------------- | ------------- | -------- | ----------------- | -------------------------------------- |
| id              | UUID          | NO       | gen_random_uuid() | Primary key                            |
| tenant_id       | UUID          | NO       | default-tenant    | Multi-tenant isolation                 |
| ledger_entry_id | UUID          | YES      |                   | FK to vfinacc_ledger_entries           |
| check_type      | VARCHAR(50)   | NO       |                   | TAX_VAT / TAX_CIT / THRESHOLD / POLICY |
| result          | VARCHAR(20)   | NO       |                   | PASS / FLAG / FAIL                     |
| tax_applicable  | BOOLEAN       | NO       | false             | Whether tax applies                    |
| tax_rate_pct    | NUMERIC(5,2)  | YES      |                   | Applied tax rate                       |
| tax_amount      | NUMERIC(15,2) | YES      |                   | Computed tax amount                    |
| notes           | TEXT          | YES      |                   | Compliance notes/explanation           |
| checked_by      | VARCHAR(255)  | YES      |                   | System or user who ran the check       |
| created_at      | TIMESTAMPTZ   | NO       | now()             | Creation timestamp                     |
