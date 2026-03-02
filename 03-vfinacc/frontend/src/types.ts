// =============================================================
// vFinacc Frontend — TypeScript Types
// =============================================================

export interface LedgerEntry {
  id: string;
  tenant_id: string;
  entry_code: string;
  account_code: string;
  description: string | null;
  debit_amount: number;
  credit_amount: number;
  currency: string;
  cost_center: string | null;
  status: "DRAFT" | "POSTED" | "FLAGGED" | "REVERSED";
  posted_by: string | null;
  metadata_json: Record<string, unknown>;
  created_at: string;
  updated_at: string;
}

export interface Transaction {
  id: string;
  tenant_id: string;
  tx_ref: string;
  source: string;
  amount: number;
  currency: string;
  direction: "DEBIT" | "CREDIT";
  status: "RAW" | "MATCHED" | "RECONCILED" | "REJECTED";
  bank_statement_ref: string | null;
  metadata_json: Record<string, unknown>;
  created_at: string;
}

export interface ReconciliationMatch {
  id: string;
  tenant_id: string;
  match_code: string;
  ledger_entry_id: string;
  transaction_id: string;
  bank_ref: string | null;
  match_type: "FULL" | "PARTIAL" | "NO_MATCH";
  confidence_pct: number;
  variance_amount: number;
  notes: string | null;
  created_at: string;
}

export interface CostAllocation {
  id: string;
  tenant_id: string;
  alloc_code: string;
  cost_center: string;
  category: "GROW" | "RUN" | "TRANSFORM" | "GIVE";
  allocated_amount: number;
  period_label: string;
  notes: string | null;
  created_at: string;
}

export interface ComplianceCheck {
  id: string;
  tenant_id: string;
  check_code: string;
  check_type: "VAT" | "CIT" | "THRESHOLD";
  reference_amount: number;
  result: "PASS" | "FLAG" | "FAIL";
  detail_json: Record<string, unknown>;
  checked_by: string | null;
  created_at: string;
}

export interface ReconSummary {
  total: number;
  full_match: number;
  partial_match: number;
  no_match: number;
}

export interface CostSummary {
  total_allocated: number;
  by_category: Record<string, number>;
}

export interface ComplianceSummary {
  total: number;
  pass: number;
  flag: number;
  fail: number;
}
