# vFinacc — API Contract

> Base path: `/api/v1/vfinacc`

## Ledger Entries

| Method | Endpoint          | Description                      | Auth                |
| ------ | ----------------- | -------------------------------- | ------------------- |
| GET    | /ledger           | List journal entries (paginated) | finance.ledger.view |
| POST   | /ledger           | Create draft journal entry       | finance.ledger.post |
| GET    | /ledger/{id}      | Get single entry                 | finance.ledger.view |
| PUT    | /ledger/{id}      | Update draft entry               | finance.ledger.post |
| POST   | /ledger/{id}/post | Post (finalize) a draft entry    | finance.ledger.post |

## Transactions

| Method | Endpoint           | Description              | Auth                        |
| ------ | ------------------ | ------------------------ | --------------------------- |
| GET    | /transactions      | List raw transactions    | finance.ledger.view         |
| POST   | /transactions      | Ingest a raw transaction | finance.transaction.approve |
| GET    | /transactions/{id} | Get single transaction   | finance.ledger.view         |

## Reconciliation

| Method | Endpoint                | Description                        | Auth                        |
| ------ | ----------------------- | ---------------------------------- | --------------------------- |
| GET    | /reconciliation         | List reconciliation matches        | finance.ledger.view         |
| POST   | /reconciliation/run     | Run 3-way matching engine          | finance.transaction.approve |
| GET    | /reconciliation/summary | Summary stats (auto-matched, etc.) | finance.ledger.view         |

## Cost Centers

| Method | Endpoint              | Description                     | Auth                        |
| ------ | --------------------- | ------------------------------- | --------------------------- |
| GET    | /cost-centers         | List cost allocations           | finance.ledger.view         |
| POST   | /cost-centers         | Create cost allocation          | finance.transaction.approve |
| GET    | /cost-centers/summary | GROW/RUN/TRANSFORM/GIVE summary | finance.ledger.view         |

## Compliance

| Method | Endpoint            | Description                   | Auth                      |
| ------ | ------------------- | ----------------------------- | ------------------------- |
| GET    | /compliance         | List compliance checks        | finance.compliance.manage |
| POST   | /compliance/check   | Run compliance check on entry | finance.compliance.manage |
| GET    | /compliance/summary | Tax & compliance summary      | finance.compliance.manage |

## Health

| Method | Endpoint | Description          | Auth |
| ------ | -------- | -------------------- | ---- |
| GET    | /health  | Service health check | None |
