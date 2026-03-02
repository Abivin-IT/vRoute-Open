// =============================================================
// vFinacc Frontend — Entry Point
// =============================================================
import {
  fetchLedgerEntries,
  fetchTransactions,
  fetchReconSummary,
  fetchCostSummary,
  fetchComplianceSummary,
  fetchHealth,
} from "./api";
import {
  renderLedger,
  renderTransactions,
  renderReconSummary,
  renderCostSummary,
  renderComplianceSummary,
  renderError,
} from "./renderers";

async function init(): Promise<void> {
  // Health
  try {
    const h = await fetchHealth();
    const el = document.getElementById("health-status");
    if (el) el.textContent = `${h.app} — ${h.status}`;
  } catch {
    const el = document.getElementById("health-status");
    if (el) el.textContent = "Service unavailable";
  }

  // Ledger
  try {
    const entries = await fetchLedgerEntries();
    renderLedger(entries);
  } catch (e: unknown) {
    renderError("ledger-list", e instanceof Error ? e.message : String(e));
  }

  // Transactions
  try {
    const txns = await fetchTransactions();
    renderTransactions(txns);
  } catch (e: unknown) {
    renderError("txn-list", e instanceof Error ? e.message : String(e));
  }

  // Reconciliation summary
  try {
    const recon = await fetchReconSummary();
    renderReconSummary(recon);
  } catch (e: unknown) {
    renderError("recon-summary", e instanceof Error ? e.message : String(e));
  }

  // Cost summary
  try {
    const cost = await fetchCostSummary();
    renderCostSummary(cost);
  } catch (e: unknown) {
    renderError("cost-summary", e instanceof Error ? e.message : String(e));
  }

  // Compliance summary
  try {
    const compliance = await fetchComplianceSummary();
    renderComplianceSummary(compliance);
  } catch (e: unknown) {
    renderError(
      "compliance-summary",
      e instanceof Error ? e.message : String(e),
    );
  }
}

document.addEventListener("DOMContentLoaded", init);
