// =============================================================
// vMarketing Org Frontend — DOM Renderers
// =============================================================
import {
  Campaign,
  TrackingEvent,
  AudienceSegment,
  ContentAsset,
  LeadScore,
  IntentSummary,
} from "./types";

// ──────────────────────────────────────────────────────────────
// Helpers
// ──────────────────────────────────────────────────────────────
function statusBadge(status: string): string {
  const colour: Record<string, string> = {
    DRAFT: "#f59e0b",
    ACTIVE: "#22c55e",
    PAUSED: "#f97316",
    COMPLETED: "#94a3b8",
    TIER_1: "#22c55e",
    TIER_2: "#3b82f6",
    TIER_3: "#94a3b8",
    HOT: "#ef4444",
    WARM: "#f97316",
    COLD: "#3b82f6",
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
export function renderCampaigns(campaigns: Campaign[]): void {
  const html = campaigns
    .slice(0, 12)
    .map((c) =>
      card(
        `${c.campaign_name}`,
        kv("Type", c.campaign_type) +
          kv("Owner", c.owner_team) +
          kv("Budget", c.budget_usd.toLocaleString() + " USD") +
          kv("Target Org", c.target_organization) +
          kv("Status", statusBadge(c.status)),
      ),
    )
    .join("");
  inject("campaigns-list", html || "<p>No campaigns.</p>");
}

export function renderTrackingEvents(events: TrackingEvent[]): void {
  const html = events
    .slice(0, 12)
    .map((e) =>
      card(
        `${e.action_type} — ${e.organization}`,
        kv("Contact", e.contact_id) +
          kv("Campaign", e.campaign_id) +
          kv("Asset", e.asset_id ?? "—") +
          kv("Intent Score", e.intent_score),
      ),
    )
    .join("");
  inject("events-list", html || "<p>No tracking events.</p>");
}

export function renderIntentSummary(s: IntentSummary): void {
  const html =
    kv("Organization", s.organization) +
    kv("Total Interactions", s.total_interactions) +
    kv("Avg Intent Score", s.avg_intent_score.toFixed(2)) +
    kv("High Interest Events", s.high_interest_events) +
    kv("Campaigns Touched", s.campaigns_touched);
  inject("intent-summary", card("Intent Summary", html));
}

export function renderSegments(segments: AudienceSegment[]): void {
  const html = segments
    .slice(0, 12)
    .map((s) =>
      card(
        `${s.segment_name}`,
        kv("Organization", s.organization) +
          kv("Industry", s.industry) +
          kv("Size", s.company_size) +
          kv("Score Threshold", s.score_threshold) +
          kv("Tier", statusBadge(s.tier)),
      ),
    )
    .join("");
  inject("segments-list", html || "<p>No segments.</p>");
}

export function renderAssets(assets: ContentAsset[]): void {
  const html = assets
    .slice(0, 12)
    .map((a) =>
      card(
        `${a.title}`,
        kv("Type", a.asset_type) +
          kv("Topic", a.topic) +
          kv("Owner", a.owner_team) +
          kv("Downloads", a.download_count),
      ),
    )
    .join("");
  inject("assets-list", html || "<p>No assets.</p>");
}

export function renderLeads(leads: LeadScore[]): void {
  const html = leads
    .slice(0, 12)
    .map((l) =>
      card(
        `${l.contact_name} — ${l.organization}`,
        kv("Email", l.email) +
          kv("Role", l.role) +
          kv("Score", l.score) +
          kv("Grade", statusBadge(l.grade)),
      ),
    )
    .join("");
  inject("leads-list", html || "<p>No leads.</p>");
}

export function renderError(id: string, message: string): void {
  inject(id, `<p style="color:#ef4444">Error: ${message}</p>`);
}
