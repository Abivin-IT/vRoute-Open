// =============================================================
// vDesign Physical Frontend — API Client
// =============================================================
import {
  GoldenSample,
  MaterialInbox,
  Prototype,
  LabTest,
  HandoverKit,
  LabTestSummary,
} from "./types";

const BASE = "/api/v1/vdesign-physical";

async function get<T>(path: string): Promise<T> {
  const r = await fetch(`${BASE}${path}`);
  if (!r.ok) throw new Error(`${r.status} ${r.statusText}`);
  return r.json() as Promise<T>;
}

export async function fetchGoldenSamples(
  status?: string,
): Promise<GoldenSample[]> {
  const qs = status ? `?status=${status}` : "";
  return get<GoldenSample[]>(`/golden-samples${qs}`);
}

export async function fetchMaterials(
  status?: string,
): Promise<MaterialInbox[]> {
  const qs = status ? `?status=${status}` : "";
  return get<MaterialInbox[]>(`/materials${qs}`);
}

export async function fetchPrototypes(status?: string): Promise<Prototype[]> {
  const qs = status ? `?status=${status}` : "";
  return get<Prototype[]>(`/prototypes${qs}`);
}

export async function fetchLabTests(status?: string): Promise<LabTest[]> {
  const qs = status ? `?status=${status}` : "";
  return get<LabTest[]>(`/lab-tests${qs}`);
}

export async function fetchLabTestSummary(): Promise<LabTestSummary> {
  return get<LabTestSummary>("/lab-tests/summary");
}

export async function fetchHandoverKits(
  status?: string,
): Promise<HandoverKit[]> {
  const qs = status ? `?status=${status}` : "";
  return get<HandoverKit[]>(`/handover-kits${qs}`);
}

export async function fetchHealth(): Promise<{ app: string; status: string }> {
  return get<{ app: string; status: string }>("/health");
}
