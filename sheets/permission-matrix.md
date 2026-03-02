# Permission Matrix

> Source: vKernel PRD Section 3.3 — Wireframe: Permission Matrix

Actions: **[C]**reate, **[R]**ead, **[U]**pdate, **[D]**elete, **[L]**ist, **[I]**mport, **[E]**xport, **[A]**pprove

Legend: `x` = Granted, `-` = Denied, `Lock` = System Lock, `A` = Accountable

## vKERNEL (System Core)

| Permission (Action)        | CEO (Vision) | CAO (Ops) | FAM (Finance) | ITM (Sec/IT) | BDM (Sales) | HRM (People) |
| -------------------------- | ------------ | --------- | ------------- | ------------ | ----------- | ------------ |
| [L] List/View Dashboard    | x            | x         | x             | x            | x           | x            |
| [U] Update Global Settings | -            | -         | -             | x            | -           | -            |
| [A] Install/Remove Apps    | A            | -         | -             | x            | -           | -            |

## vFINANCE (Bookkeeping)

| Permission (Action)       | CEO (Vision) | CAO (Ops) | FAM (Finance) | ITM (Sec/IT) | BDM (Sales) | HRM (People) |
| ------------------------- | ------------ | --------- | ------------- | ------------ | ----------- | ------------ |
| [L] List General Ledger   | x            | x         | x             | -            | -           | -            |
| [C] Create Purchase Order | -            | x         | x             | -            | x           | x            |
| [U] Update Records        | -            | -         | x             | -            | -           | -            |
| [D] Delete Transactions   | -            | -         | x             | Lock         | -           | -            |
| [I] Import Bank Data      | -            | -         | x             | -            | -           | -            |
| [E] Export Tax Reports    | x            | x         | x             | -            | -           | -            |
| [A] Approve Payment (>5k) | x            | x         | -             | -            | -           | -            |

## vSALES (GTM Strategy)

| Permission (Action)    | CEO (Vision) | CAO (Ops) | FAM (Finance) | ITM (Sec/IT) | BDM (Sales) | HRM (People) |
| ---------------------- | ------------ | --------- | ------------- | ------------ | ----------- | ------------ |
| [C] Create Leads/Deals | -            | -         | -             | -            | x           | -            |
| [R] View Customer Data | x            | x         | x             | -            | x           | -            |
| [A] Approve Discount   | x            | x         | -             | -            | x           | -            |

## Role Definitions

| Role Code | Full Name                    | Domain                       |
| --------- | ---------------------------- | ---------------------------- |
| CEO       | Chief Executive Officer      | Vision & Strategy            |
| CAO       | Chief Administrative Officer | Operations                   |
| FAM       | Finance & Accounting Manager | Finance                      |
| ITM       | IT Manager / Security Admin  | Security & IT Infrastructure |
| BDM       | Business Development Manager | Sales & Revenue              |
| HRM       | Human Resources Manager      | People & Culture             |
