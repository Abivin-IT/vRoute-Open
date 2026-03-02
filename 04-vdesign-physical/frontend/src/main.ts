// =============================================================
// vDesign Physical Frontend — Entry Point
// =============================================================
import {
  fetchGoldenSamples,
  fetchMaterials,
  fetchPrototypes,
  fetchLabTestSummary,
  fetchHandoverKits,
  fetchHealth,
} from "./api";
import {
  renderGoldenSamples,
  renderMaterials,
  renderPrototypes,
  renderLabTestSummary,
  renderHandoverKits,
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

  // Golden Samples
  try {
    const samples = await fetchGoldenSamples();
    renderGoldenSamples(samples);
  } catch (e: unknown) {
    renderError("samples-list", e instanceof Error ? e.message : String(e));
  }

  // Materials
  try {
    const materials = await fetchMaterials();
    renderMaterials(materials);
  } catch (e: unknown) {
    renderError("materials-list", e instanceof Error ? e.message : String(e));
  }

  // Prototypes
  try {
    const prototypes = await fetchPrototypes();
    renderPrototypes(prototypes);
  } catch (e: unknown) {
    renderError("prototypes-list", e instanceof Error ? e.message : String(e));
  }

  // Lab Test Summary
  try {
    const labSummary = await fetchLabTestSummary();
    renderLabTestSummary(labSummary);
  } catch (e: unknown) {
    renderError("lab-summary", e instanceof Error ? e.message : String(e));
  }

  // Handover Kits
  try {
    const kits = await fetchHandoverKits();
    renderHandoverKits(kits);
  } catch (e: unknown) {
    renderError("kits-list", e instanceof Error ? e.message : String(e));
  }
}

document.addEventListener("DOMContentLoaded", init);
