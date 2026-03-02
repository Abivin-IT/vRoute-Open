// =============================================================
// vStrategy Frontend — API Client
// =============================================================
import type {
  Plan,
  AlignmentNode,
  Scorecard,
  SopValidation,
  PivotSignal,
} from "./types";

const API = "/api/v1/vstrategy";

async function fetchJson<T>(path: string): Promise<T> {
  const r = await fetch(API + path);
  if (!r.ok) throw new Error(r.statusText);
  return r.json() as Promise<T>;
}

export async function getPlans(): Promise<{ count: number; plans: Plan[] }> {
  return fetchJson("/plans");
}

export async function getPlan(id: string): Promise<Plan> {
  return fetchJson(`/plans/${id}`);
}

export async function getTree(
  planId: string,
): Promise<{ plan_id: string; count: number; nodes: AlignmentNode[] }> {
  return fetchJson(`/plans/${planId}/tree`);
}

export async function getScorecard(planId: string): Promise<Scorecard> {
  return fetchJson(`/plans/${planId}/scorecard`);
}

export async function getSopValidation(planId: string): Promise<SopValidation> {
  return fetchJson(`/plans/${planId}/sop/validate`);
}

export async function getSignals(
  planId: string,
): Promise<{ count: number; signals: PivotSignal[] }> {
  return fetchJson(`/plans/${planId}/signals`);
}
