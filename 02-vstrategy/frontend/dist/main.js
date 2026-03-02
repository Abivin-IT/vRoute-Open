// =============================================================
// vStrategy Frontend — Main Entry Point
// @GovernanceID vstrategy.3.0
// =============================================================
import { getPlans, getPlan, getTree, getScorecard, getSopValidation, getSignals, } from "./api";
import { renderScorecard, renderTree, renderSop, renderSignals, renderPlanInfo, } from "./renderers";
async function loadPlans() {
    const data = await getPlans();
    const sel = document.getElementById("planSelect");
    sel.innerHTML = "";
    for (const p of data.plans) {
        const o = document.createElement("option");
        o.value = p.id;
        o.textContent = `${p.period_label} (${p.status})`;
        sel.appendChild(o);
    }
    sel.onchange = () => loadDashboard(sel.value);
    if (data.plans.length > 0) {
        await loadDashboard(data.plans[0].id);
    }
    else {
        document.getElementById("app").innerHTML =
            '<div class="loading">No plans found. Create one via API.</div>';
    }
}
async function loadDashboard(planId) {
    const app = document.getElementById("app");
    app.innerHTML = '<div class="loading">Loading...</div>';
    try {
        const [plan, treeData, scorecard, sop, signalsData] = await Promise.all([
            getPlan(planId),
            getTree(planId),
            getScorecard(planId),
            getSopValidation(planId),
            getSignals(planId),
        ]);
        app.innerHTML =
            '<div class="grid">' +
                '<div class="card full">' +
                renderScorecard(scorecard) +
                "</div>" +
                '<div class="card full">' +
                renderTree(treeData.nodes) +
                "</div>" +
                '<div class="card">' +
                renderSop(sop) +
                "</div>" +
                '<div class="card">' +
                renderSignals(signalsData.signals) +
                "</div>" +
                '<div class="card full">' +
                renderPlanInfo(plan) +
                "</div>" +
                "</div>";
    }
    catch (e) {
        app.innerHTML = `<div class="loading">Error: ${e.message}</div>`;
    }
}
// Boot
loadPlans();
