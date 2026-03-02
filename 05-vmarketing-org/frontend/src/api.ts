// =============================================================
// vMarketing Org Frontend — API Client
// =============================================================
import {
  Campaign,
  TrackingEvent,
  AudienceSegment,
  ContentAsset,
  LeadScore,
  IntentSummary,
} from "./types";

const BASE = "/api/v1/vmarketing-org";

async function get<T>(path: string): Promise<T> {
  const r = await fetch(`${BASE}${path}`);
  if (!r.ok) throw new Error(`${r.status} ${r.statusText}`);
  return r.json() as Promise<T>;
}

export async function fetchCampaigns(status?: string): Promise<Campaign[]> {
  const qs = status ? `?status=${status}` : "";
  return get<Campaign[]>(`/campaigns${qs}`);
}

export async function fetchTrackingEvents(
  organization?: string,
): Promise<TrackingEvent[]> {
  const qs = organization
    ? `?organization=${encodeURIComponent(organization)}`
    : "";
  return get<TrackingEvent[]>(`/tracking-events${qs}`);
}

export async function fetchIntentSummary(
  organization: string,
): Promise<IntentSummary> {
  return get<IntentSummary>(
    `/tracking-events/intent-summary/${encodeURIComponent(organization)}`,
  );
}

export async function fetchSegments(tier?: string): Promise<AudienceSegment[]> {
  const qs = tier ? `?tier=${tier}` : "";
  return get<AudienceSegment[]>(`/segments${qs}`);
}

export async function fetchAssets(assetType?: string): Promise<ContentAsset[]> {
  const qs = assetType ? `?asset_type=${assetType}` : "";
  return get<ContentAsset[]>(`/assets${qs}`);
}

export async function fetchLeads(grade?: string): Promise<LeadScore[]> {
  const qs = grade ? `?grade=${grade}` : "";
  return get<LeadScore[]>(`/leads${qs}`);
}

export async function fetchHealth(): Promise<{ app: string; status: string }> {
  return get<{ app: string; status: string }>("/health");
}
