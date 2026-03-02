// =============================================================
// vStrategy Frontend — TypeScript Types
// =============================================================

export interface Plan {
  id: string;
  tenant_id: string;
  period_type: string;
  period_label: string;
  status: string;
  baseline_json: Record<string, any>;
  objectives_json: Record<string, any>;
  gap_analysis_json: Record<string, any>;
  mece_options_json: MeceOption[];
  selected_option: string | null;
  decision_log_json: Record<string, any>;
  sop_config_json: Record<string, any>;
  created_by: string | null;
  created_at: string;
  updated_at: string;
}

export interface AlignmentNode {
  id: string;
  plan_id: string;
  parent_id: string | null;
  node_level: string;
  code: string | null;
  title: string;
  description: string | null;
  owner: string | null;
  bsc_perspective: string | null;
  progress_pct: number;
  status: "GREEN" | "YELLOW" | "RED";
  budget_amount: number;
  headcount_fte: number;
  resource_category: string | null;
  priority: string | null;
  metadata_json: Record<string, any>;
  sort_order: number;
}

export interface TreeNode extends AlignmentNode {
  children: TreeNode[];
}

export interface Perspective {
  perspective: string;
  title: string;
  progress_pct: number;
  status: string;
}

export interface Scorecard {
  plan_id: string;
  overall_progress_pct: number;
  overall_status: string;
  perspectives: Perspective[];
}

export interface SopRow {
  category: string;
  owner: string;
  target_pct: number;
  actual_pct: number;
  status: string;
  amount: number;
}

export interface SopValidation {
  valid: boolean;
  total_budget: number;
  total_headcount: number;
  breakdown: SopRow[];
}

export interface PivotSignal {
  id: string;
  plan_id: string;
  rule_code: string;
  rule_description: string | null;
  threshold_value: number;
  actual_value: number;
  variance_pct: number | null;
  triggered: boolean;
  severity: string;
  recommendation: string | null;
}

export interface MeceOption {
  code: string;
  name: string;
  description: string;
  risk: string;
  reward: string;
  burn_qtr: number;
}
