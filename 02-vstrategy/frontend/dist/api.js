const API = "/api/v1/vstrategy";
async function fetchJson(path) {
    const r = await fetch(API + path);
    if (!r.ok)
        throw new Error(r.statusText);
    return r.json();
}
export async function getPlans() {
    return fetchJson("/plans");
}
export async function getPlan(id) {
    return fetchJson(`/plans/${id}`);
}
export async function getTree(planId) {
    return fetchJson(`/plans/${planId}/tree`);
}
export async function getScorecard(planId) {
    return fetchJson(`/plans/${planId}/scorecard`);
}
export async function getSopValidation(planId) {
    return fetchJson(`/plans/${planId}/sop/validate`);
}
export async function getSignals(planId) {
    return fetchJson(`/plans/${planId}/signals`);
}
