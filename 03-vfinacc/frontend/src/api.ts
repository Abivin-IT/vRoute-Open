// =============================================================
// vFinacc Frontend — API Client
// =============================================================
import {
  LedgerEntry,
  Transaction,
  ReconciliationMatch,
  CostAllocation,
  ComplianceCheck,
  ReconSummary,
  CostSummary,
  ComplianceSummary,
} from "./types";

const BASE = "/api/v1/vfinacc";

async function get<T>(path: string): Promise<T> {
  const r = await fetch(`${BASE}${path}`);
  if (!r.ok) throw new Error(`${r.status} ${r.statusText}`);
  return r.json() as Promise<T>;
}

export async function fetchLedgerEntries(
  status?: string,
): Promise<LedgerEntry[]> {
  const qs = status ? `?status=${status}` : "";
  return get<LedgerEntry[]>(`/ledger${qs}`);
}

export async function fetchTransactions(): Promise<Transaction[]> {
  return get<Transaction[]>("/transactions");
}

export async function fetchReconciliation(): Promise<ReconciliationMatch[]> {
  return get<ReconciliationMatch[]>("/reconciliation");
}

export async function fetchReconSummary(): Promise<ReconSummary> {
  return get<ReconSummary>("/reconciliation/summary");
}

export async function fetchCostCenters(): Promise<CostAllocation[]> {
  return get<CostAllocation[]>("/cost-centers");
}

export async function fetchCostSummary(): Promise<CostSummary> {
  return get<CostSummary>("/cost-centers/summary");
}

export async function fetchComplianceChecks(): Promise<ComplianceCheck[]> {
  return get<ComplianceCheck[]>("/compliance");
}

export async function fetchComplianceSummary(): Promise<ComplianceSummary> {
  return get<ComplianceSummary>("/compliance/summary");
}

export async function fetchHealth(): Promise<{ app: string; status: string }> {
  return get<{ app: string; status: string }>("/health");
}
