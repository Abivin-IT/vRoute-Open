// =============================================================
// vMarketing Org Frontend — Entry Point
// =============================================================
import {
  fetchCampaigns,
  fetchTrackingEvents,
  fetchSegments,
  fetchAssets,
  fetchLeads,
  fetchHealth,
} from "./api";
import {
  renderCampaigns,
  renderTrackingEvents,
  renderSegments,
  renderAssets,
  renderLeads,
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

  // Campaigns
  try {
    const campaigns = await fetchCampaigns();
    renderCampaigns(campaigns);
  } catch (e: unknown) {
    renderError("campaigns-list", e instanceof Error ? e.message : String(e));
  }

  // Tracking Events
  try {
    const events = await fetchTrackingEvents();
    renderTrackingEvents(events);
  } catch (e: unknown) {
    renderError("events-list", e instanceof Error ? e.message : String(e));
  }

  // Audience Segments
  try {
    const segments = await fetchSegments();
    renderSegments(segments);
  } catch (e: unknown) {
    renderError("segments-list", e instanceof Error ? e.message : String(e));
  }

  // Content Assets
  try {
    const assets = await fetchAssets();
    renderAssets(assets);
  } catch (e: unknown) {
    renderError("assets-list", e instanceof Error ? e.message : String(e));
  }

  // Leads
  try {
    const leads = await fetchLeads();
    renderLeads(leads);
  } catch (e: unknown) {
    renderError("leads-list", e instanceof Error ? e.message : String(e));
  }
}

document.addEventListener("DOMContentLoaded", init);
