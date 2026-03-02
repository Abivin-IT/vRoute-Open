// =============================================================
// vFinacc Frontend — DOM Renderers
// =============================================================
import {
  LedgerEntry,
  Transaction,
  ReconSummary,
  CostSummary,
  ComplianceSummary,
} from "./types";

// ──────────────────────────────────────────────────────────────
// Helpers
// ──────────────────────────────────────────────────────────────
function statusBadge(status: string): string {
  const colour: Record<string, string> = {
    POSTED: "#22c55e",
    DRAFT: "#f59e0b",
    FLAGGED: "#ef4444",
    REVERSED: "#94a3b8",
    MATCHED: "#22c55e",
    RECONCILED: "#16a34a",
    RAW: "#f59e0b",
    REJECTED: "#ef4444",
    FULL: "#22c55e",
    PARTIAL: "#f59e0b",
    NO_MATCH: "#ef4444",
    COMPLIANT: "#22c55e",
    NON_COMPLIANT: "#ef4444",
    PENDING: "#f59e0b",
  };
  const bg = colour[status] ?? "#94a3b8";
  return `<span style="background:${bg};color:#fff;padding:2px 8px;border-radius:4px;font-size:0.75rem">${status}</span>`;
}

function card(title: string, body: string): string {
  return `<div style="background:#1e293b;border:1px solid #334155;border-radius:8px;padding:16px;margin-bottom:12px"><h3 style="margin:0 0 8px;font-size:0.9rem;color:#94a3b8">${title}</h3>${body}</div>`;
}

function kv(label: string, value: string | number): string {
  return `<div style="display:flex;justify-content:space-between;padding:4px 0;border-bottom:1px solid #334155"><span style="color:#94a3b8;font-size:0.8rem">${label}</span><span style="color:#f1f5f9;font-size:0.8rem">${value}</span></div>`;
}

function inject(id: string, html: string): void {
  const el = document.getElementById(id);
  if (el) el.innerHTML = html;
}

// ──────────────────────────────────────────────────────────────
// Section renderers
// ──────────────────────────────────────────────────────────────
export function renderLedger(entries: LedgerEntry[]): void {
  const html = entries
    .slice(0, 12)
    .map((e) =>
      card(
        `${e.account_code} — ${e.description ?? "ledger"}`,
        kv("Debit", e.debit_amount.toLocaleString()) +
          kv("Credit", e.credit_amount.toLocaleString()) +
          kv("Currency", e.currency) +
          kv("Cost Center", e.cost_center ?? "—") +
          kv("Status", statusBadge(e.status)),
      ),
    )
    .join("");
  inject("ledger-list", html || "<p>No ledger entries.</p>");
}

export function renderTransactions(txns: Transaction[]): void {
  const html = txns
    .slice(0, 12)
    .map((t) =>
      card(
        `TXN ${t.tx_ref.slice(0, 8)}`,
        kv("Source", t.source) +
          kv("Amount", t.amount.toLocaleString()) +
          kv("Currency", t.currency) +
          kv("Direction", t.direction) +
          kv("Status", statusBadge(t.status)),
      ),
    )
    .join("");
  inject("txn-list", html || "<p>No transactions.</p>");
}

export function renderReconSummary(s: ReconSummary): void {
  const html =
    kv("Total", s.total) +
    kv("Full Match", s.full_match) +
    kv("Partial Match", s.partial_match) +
    kv("No Match", s.no_match);
  inject("recon-summary", card("Reconciliation Summary", html));
}

export function renderCostSummary(s: CostSummary): void {
  const html =
    kv("Total Allocated", s.total_allocated.toLocaleString()) +
    kv("Grow", s.by_category.GROW.toLocaleString()) +
    kv("Run", s.by_category.RUN.toLocaleString()) +
    kv("Transform", s.by_category.TRANSFORM.toLocaleString()) +
    kv("Give", s.by_category.GIVE.toLocaleString());
  inject("cost-summary", card("Cost Allocation Summary", html));
}

export function renderComplianceSummary(s: ComplianceSummary): void {
  const html =
    kv("Total Checks", s.total) +
    kv("Pass", s.pass) +
    kv("Flagged", s.flag) +
    kv("Failed", s.fail);
  inject("compliance-summary", card("Compliance Summary", html));
}

export function renderError(id: string, message: string): void {
  inject(id, `<p style="color:#ef4444">Error: ${message}</p>`);
}
