// =============================================================
// vDesign Physical Frontend — DOM Renderers
// =============================================================
import {
  GoldenSample,
  MaterialInbox,
  Prototype,
  LabTest,
  HandoverKit,
  LabTestSummary,
} from "./types";

// ──────────────────────────────────────────────────────────────
// Helpers
// ──────────────────────────────────────────────────────────────
function statusBadge(status: string): string {
  const colour: Record<string, string> = {
    ACTIVE: "#22c55e",
    SEALED: "#3b82f6",
    COMPROMISED: "#ef4444",
    EXPIRED: "#94a3b8",
    PENDING: "#f59e0b",
    TESTED: "#22c55e",
    ARCHIVED: "#94a3b8",
    SCRAPPED: "#ef4444",
    IN_TRANSIT: "#3b82f6",
    OBSOLETE: "#94a3b8",
    DESTROYED: "#ef4444",
    RUNNING: "#f59e0b",
    PASSED: "#22c55e",
    FAILED: "#ef4444",
    CONDITIONAL: "#f97316",
    PACKING: "#f59e0b",
    READY: "#22c55e",
    DISPATCHED: "#3b82f6",
    RECEIVED: "#16a34a",
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
export function renderGoldenSamples(samples: GoldenSample[]): void {
  const html = samples
    .slice(0, 12)
    .map((s) =>
      card(
        `${s.sample_code} — ${s.product_name}`,
        kv("SKU", s.sku) +
          kv("Version", s.version) +
          kv("Sealed By", s.sealed_by) +
          kv("Status", statusBadge(s.status)),
      ),
    )
    .join("");
  inject("samples-list", html || "<p>No golden samples.</p>");
}

export function renderMaterials(materials: MaterialInbox[]): void {
  const html = materials
    .slice(0, 12)
    .map((m) =>
      card(
        `${m.po_number} — ${m.material_name}`,
        kv("Supplier", m.supplier_code) +
          kv("Qty Received", m.qty_received) +
          kv("Qty Tested", m.qty_tested) +
          kv("Status", statusBadge(m.status)),
      ),
    )
    .join("");
  inject("materials-list", html || "<p>No materials.</p>");
}

export function renderPrototypes(prototypes: Prototype[]): void {
  const html = prototypes
    .slice(0, 12)
    .map((p) =>
      card(
        `${p.prototype_code} — ${p.description}`,
        kv("Product Family", p.product_family) +
          kv("Assigned To", p.assigned_to) +
          kv("Location", p.current_location) +
          kv("Status", statusBadge(p.status)),
      ),
    )
    .join("");
  inject("prototypes-list", html || "<p>No prototypes.</p>");
}

export function renderLabTestSummary(s: LabTestSummary): void {
  const html =
    kv("Total Tests", s.total) +
    kv("Running", s.running) +
    kv("Passed", s.passed) +
    kv("Failed", s.failed) +
    kv("Pass Rate", `${s.pass_rate_pct.toFixed(1)}%`);
  inject("lab-summary", card("Lab Test Summary", html));
}

export function renderHandoverKits(kits: HandoverKit[]): void {
  const html = kits
    .slice(0, 12)
    .map((k) =>
      card(
        `Kit ${k.kit_code}`,
        kv("Prototype", k.prototype_id) +
          kv("Destination", k.destination_team) +
          kv("Items", k.items_count) +
          kv("Status", statusBadge(k.status)),
      ),
    )
    .join("");
  inject("kits-list", html || "<p>No handover kits.</p>");
}

export function renderError(id: string, message: string): void {
  inject(id, `<p style="color:#ef4444">Error: ${message}</p>`);
}
