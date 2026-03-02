// =============================================================
// vMarketing Org Frontend — TypeScript Types
// =============================================================

export interface Campaign {
  id: string;
  tenant_id: string;
  campaign_code: string;
  name: string;
  target_segment: string | null;
  stage: "AWARENESS" | "CONSIDERATION" | "NURTURING" | "CLOSING";
  channel: string | null;
  budget_amount: number;
  spent_amount: number;
  currency: string;
  target_accounts: number;
  engaged_accounts: number;
  mqls_generated: number;
  status: "DRAFT" | "ACTIVE" | "PAUSED" | "COMPLETED";
  owner: string | null;
  metadata_json: Record<string, unknown>;
  created_at: string;
  updated_at: string;
}

export interface TrackingEvent {
  id: string;
  tenant_id: string;
  event_code: string;
  organization: string;
  action_type:
    | "PAGE_VIEW"
    | "DOWNLOAD_PDF"
    | "PRICING_COMPARE"
    | "VIDEO_WATCH"
    | "EXIT_INTENT";
  page_resource: string | null;
  dwell_seconds: number;
  intent_score: number;
  ip_address: string | null;
  user_agent: string | null;
  metadata_json: Record<string, unknown>;
  created_at: string;
}

export interface AudienceSegment {
  id: string;
  tenant_id: string;
  segment_code: string;
  name: string;
  description: string | null;
  criteria_json: Record<string, unknown>;
  account_count: number;
  tier: "TIER_1" | "TIER_2" | "TIER_3";
  status: "ACTIVE" | "ARCHIVED";
  created_by: string | null;
  created_at: string;
  updated_at: string;
}

export interface ContentAsset {
  id: string;
  tenant_id: string;
  asset_code: string;
  title: string;
  asset_type: "WHITEPAPER" | "CASE_STUDY" | "VIDEO" | "INFOGRAPHIC" | "BLOG";
  format_type: string | null;
  url: string | null;
  target_stage: string | null;
  downloads: number;
  views: number;
  status: "DRAFT" | "PUBLISHED" | "ARCHIVED";
  created_by: string | null;
  metadata_json: Record<string, unknown>;
  created_at: string;
  updated_at: string;
}

export interface LeadScore {
  id: string;
  tenant_id: string;
  organization: string;
  contact_name: string | null;
  contact_title: string | null;
  score: number;
  grade: "HOT" | "WARM" | "COLD";
  scoring_factors: Record<string, unknown>;
  status: "NEW" | "QUALIFIED" | "HANDED_OFF" | "DISQUALIFIED";
  handed_off_to: string | null;
  notes: string | null;
  created_at: string;
  updated_at: string;
}

export interface IntentSummary {
  organization: string;
  total_events: number;
  avg_intent_score: number;
  total_dwell_seconds: number;
}
