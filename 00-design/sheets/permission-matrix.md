# Permission Matrix

> Source: vKernel PRD §3.3 + Business App PRDs.
> Actions: **[C]**reate, **[R]**ead, **[U]**pdate, **[D]**elete, **[L]**ist, **[I]**mport, **[E]**xport, **[A]**pprove
> Legend: `x` = Granted, `-` = Denied, `Lock` = System Lock, `A` = Accountable

## Unified Permission Matrix

| App | Permission (Action) | CEO (Vision) | CAO (Ops) | FAM (Finance) | ITM (Sec/IT) | BDM (Sales) | HRM (People) |
|-----|---------------------|--------------|-----------|---------------|--------------|-------------|--------------|
| vKernel | [L] List/View Dashboard | x | x | x | x | x | x |
| vKernel | [U] Update Global Settings | - | - | - | x | - | - |
| vKernel | [A] Install/Remove Apps | A | - | - | x | - | - |
| vFinacc | [L] List General Ledger | x | x | x | - | - | - |
| vFinacc | [C] Create Purchase Order | - | x | x | - | x | x |
| vFinacc | [U] Update Records | - | - | x | - | - | - |
| vFinacc | [D] Delete Transactions | - | - | x | Lock | - | - |
| vFinacc | [I] Import Bank Data | - | - | x | - | - | - |
| vFinacc | [E] Export Tax Reports | x | x | x | - | - | - |
| vFinacc | [A] Approve Payment (>5k) | x | x | - | - | - | - |
| vStrategy | [L] List Plans & Trees | x | x | x | - | - | - |
| vStrategy | [C] Create Plan | x | x | - | - | - | - |
| vStrategy | [U] Update Alignment Nodes | x | x | - | - | - | - |
| vStrategy | [R] View Scorecard | x | x | x | x | x | x |
| vStrategy | [A] Approve S&OP | A | x | - | - | - | - |
| vDesign Physical | [L] List Golden Samples | x | x | - | - | - | - |
| vDesign Physical | [C] Create Prototype | - | x | - | - | - | - |
| vDesign Physical | [A] Seal Golden Sample | A | x | - | - | - | - |
| vDesign Physical | [R] View Lab Tests | x | x | - | x | - | - |
| vDesign Physical | [U] Advance Handover Kit | - | x | - | - | - | - |
| vMarketing Org | [L] List Campaigns | x | x | - | - | x | - |
| vMarketing Org | [C] Create Campaign | - | x | - | - | x | - |
| vMarketing Org | [A] Launch Campaign | A | x | - | - | - | - |
| vMarketing Org | [R] View Tracking Events | x | x | - | - | x | - |
| vMarketing Org | [C] Create Audience Segment | - | x | - | - | x | - |
| vMarketing Org | [R] View Lead Scores | x | x | - | - | x | - |
| vMarketing Org | [A] Hand Off Lead to Sales | - | - | - | - | x | - |

## Role Definitions

| Role Code | Full Name | Domain |
|-----------|-----------|--------|
| CEO | Chief Executive Officer | Vision & Strategy |
| CAO | Chief Administrative Officer | Operations |
| FAM | Finance & Accounting Manager | Finance |
| ITM | IT Manager / Security Admin | Security & IT Infrastructure |
| BDM | Business Development Manager | Sales & Revenue |
| HRM | Human Resources Manager | People & Culture |

## Permission Count by App

| App | Permissions | Primary Roles |
|-----|-------------|---------------|
| vKernel | 3 | ITM, CEO |
| vFinacc | 7 | FAM, CEO, CAO |
| vStrategy | 5 | CEO, CAO |
| vDesign Physical | 5 | CAO, CEO |
| vMarketing Org | 7 | CAO, BDM, CEO |
| **Total** | **27** | |
