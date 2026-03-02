// =============================================================
// vDesign Physical Frontend — TypeScript Types
// =============================================================

export interface GoldenSample {
  id: string;
  tenant_id: string;
  sample_code: string;
  product_name: string;
  version: string;
  status: "ACTIVE" | "SEALED" | "COMPROMISED" | "EXPIRED";
  convergence_pct: number;
  specs_json: Record<string, unknown>;
  sealed_by: string | null;
  sealed_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface MaterialInbox {
  id: string;
  tenant_id: string;
  material_code: string;
  name: string;
  source_type: "SUPPLIER" | "INTERNAL" | "RECYCLE" | "PROTOTYPE";
  status: "PENDING" | "TESTED" | "ARCHIVED" | "SCRAPPED";
  quantity: number;
  unit: string;
  properties_json: Record<string, unknown>;
  created_at: string;
  updated_at: string;
}

export interface Prototype {
  id: string;
  tenant_id: string;
  proto_code: string;
  name: string;
  version: string;
  iteration: number;
  status: "ACTIVE" | "IN_TRANSIT" | "OBSOLETE" | "DESTROYED";
  location: string | null;
  rfid_tag: string | null;
  design_files_json: Record<string, unknown>;
  created_at: string;
  updated_at: string;
}

export interface LabTest {
  id: string;
  tenant_id: string;
  test_code: string;
  test_type: "STRESS" | "DIMENSION" | "CHEMICAL" | "ELECTRICAL" | "VISUAL";
  status: "RUNNING" | "PASSED" | "FAILED" | "CONDITIONAL";
  result: string | null;
  golden_sample_id: string | null;
  prototype_id: string | null;
  pass_threshold: number;
  actual_value: number | null;
  notes: string | null;
  completed_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface HandoverKit {
  id: string;
  tenant_id: string;
  kit_code: string;
  name: string;
  status: "PACKING" | "READY" | "DISPATCHED" | "RECEIVED";
  destination: string | null;
  total_weight_kg: number;
  item_count: number;
  items_json: Record<string, unknown>;
  dispatched_at: string | null;
  received_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface LabTestSummary {
  total: number;
  passed: number;
  failed: number;
  running: number;
  conditional: number;
  pass_rate_pct: number;
}
