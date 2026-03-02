# vFinacc — Acceptance Criteria

## AC-FIN-01: Continuous Ledger

```gherkin
Scenario: Create and post a journal entry
  Given A CFO creates a draft journal entry with debit $2,400 to "R&D Infra" and credit $2,400 to "Accounts Payable"
  When The CFO posts the entry
  Then The entry status changes from "DRAFT" to "POSTED"
  And A TRANSACTION_POSTED event is published to the Event Bus
  And The General Ledger balance is updated accordingly
```

## AC-FIN-02: Transaction Ingestor

```gherkin
Scenario: Ingest bank transaction via webhook
  Given The system receives a bank transaction webhook for $2,400 from AWS
  When The Transaction Ingestor processes the payload
  Then A raw transaction record is created with source "BANK_WEBHOOK"
  And A draft ledger entry is auto-generated for review
```

## AC-FIN-03: Reconciliation Engine (3-Way Match)

```gherkin
Scenario: 3-way matching succeeds
  Given A Purchase Order (PO) for $2,400 exists
  And A Goods Receipt Note (GRN) confirms delivery
  And An Invoice for $2,400 is received
  When The Reconciliation Engine runs
  Then A FULL_MATCH record is created linking PO, GRN, and Invoice
  And The match confidence_pct is 100.00
```

```gherkin
Scenario: 3-way matching finds discrepancy
  Given A PO for $2,400 exists
  And An Invoice for $2,600 is received (no GRN yet)
  When The Reconciliation Engine runs
  Then A PARTIAL_MATCH record is created
  And The discrepancy_amount is $200
  And The system flags the entry for manual review
```

## AC-FIN-04: Cost Center Manager

```gherkin
Scenario: Cost allocation follows GROW/RUN/TRANSFORM/GIVE targets
  Given Budget allocations: GROW $680K, RUN $270K, TRANSFORM $50K
  When The Cost Center summary is requested
  Then Actual percentages are calculated against total budget
  And Each category shows ON_TRACK or VIOLATION status based on tolerance
```

## AC-FIN-05: Tax & Compliance Guard

```gherkin
Scenario: Compliance check passes for standard transaction
  Given A posted ledger entry of $2,400 for domestic services
  When A compliance check is run
  Then The result is PASS
  And tax_applicable is true
  And tax_rate is 10% (VAT Vietnam)
```

```gherkin
Scenario: Compliance check flags threshold violation
  Given A posted ledger entry of $50,000 (exceeds review threshold)
  When A compliance check is run
  Then The result is FLAG
  And notes indicate "Amount exceeds review threshold $25,000"
```
