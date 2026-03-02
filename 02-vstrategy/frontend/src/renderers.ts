// =============================================================
// vStrategy Frontend — Renderers (pure functions → HTML strings)
// =============================================================
import type {
  Plan,
  AlignmentNode,
  TreeNode,
  Scorecard,
  SopValidation,
  PivotSignal,
  MeceOption,
} from "./types";

const ICONS: Record<string, string> = {
  VISION: "\u{1F451}",
  BSC_PERSPECTIVE: "\u{1F4CA}",
  OKR: "\u{1F3AF}",
  INITIATIVE: "\u{1F680}",
  TASK: "\u{1F4CB}",
};

const BSC_ICONS: Record<string, string> = {
  FINANCE: "\u{1F4B0}",
  CUSTOMER: "\u{1F60A}",
  PROCESS: "\u2699\uFE0F",
  LEARNING: "\u{1F4DA}",
};

function tryAlert(metadataJson: Record<string, any> | string | null): string {
  if (!metadataJson) return "";
  try {
    const o =
      typeof metadataJson === "string"
        ? JSON.parse(metadataJson)
        : metadataJson;
    return o.alert || "";
  } catch {
    return "";
  }
}

function tryParse(s: any): Record<string, any> {
  if (!s) return {};
  try {
    return typeof s === "string" ? JSON.parse(s) : s;
  } catch {
    return {};
  }
}

// ---- Scorecard ----
export function renderScorecard(sc: Scorecard): string {
  let h = `<h2>\u{1F4CA} Balanced Scorecard \u2014 Overall: <span class="${sc.overall_status}">${sc.overall_status} ${sc.overall_progress_pct}%</span></h2><div class="bsc-grid">`;
  for (const p of sc.perspectives) {
    const icon = BSC_ICONS[p.perspective] || "\u{1F4CA}";
    h +=
      `<div class="bsc-item"><div class="label">${icon} ${p.perspective}</div>` +
      `<div class="bar-track"><div class="bar-fill ${p.status}" style="width:${p.progress_pct}%">${p.progress_pct}%</div></div></div>`;
  }
  return h + "</div>";
}

// ---- Alignment Tree ----
function buildTree(nodes: AlignmentNode[]): TreeNode[] {
  const map: Record<string, TreeNode> = {};
  const roots: TreeNode[] = [];
  for (const n of nodes) {
    map[n.id] = { ...n, children: [] };
  }
  for (const n of nodes) {
    if (n.parent_id && map[n.parent_id]) {
      map[n.parent_id].children.push(map[n.id]);
    } else {
      roots.push(map[n.id]);
    }
  }
  return roots;
}

function renderNode(n: TreeNode): string {
  const icon = ICONS[n.node_level] || "\u2022";
  const bscIcon = n.bsc_perspective
    ? (BSC_ICONS[n.bsc_perspective] || "") + " "
    : "";
  const alert = tryAlert(n.metadata_json);
  const dot =
    n.status === "GREEN"
      ? "\u{1F7E2}"
      : n.status === "YELLOW"
        ? "\u{1F7E1}"
        : "\u{1F534}";
  let h =
    `<li><div class="node ${n.status}"><span class="icon">${icon}</span>` +
    `<span class="title">${bscIcon}${n.code ? n.code + ": " : ""}${n.title}</span>`;
  if (n.owner) h += `<span class="owner-tag">${n.owner}</span>`;
  h += `<span class="pct">${dot} ${n.progress_pct}%</span></div>`;
  if (alert) h += `<span class="alert-tag">\u26A0\uFE0F ${alert}</span>`;
  if (n.children.length)
    h += "<ul>" + n.children.map(renderNode).join("") + "</ul>";
  return h + "</li>";
}

export function renderTree(nodes: AlignmentNode[]): string {
  const roots = buildTree(nodes);
  return `<h2>\u{1F333} Alignment Tree (Vision \u2192 Task)</h2><div class="tree"><ul>${roots.map(renderNode).join("")}</ul></div>`;
}

// ---- S&OP Table ----
export function renderSop(sop: SopValidation): string {
  let h = `<h2>\u2696\uFE0F S&OP 68/27/5 \u2014 ${sop.valid ? "\u2705 VALID" : "\u274C VIOLATION"}</h2>`;
  h += `<p style="font-size:12px;color:var(--dim);margin-bottom:8px">Budget: $${Number(sop.total_budget).toLocaleString()} | HC: +${sop.total_headcount} FTE</p>`;
  h +=
    "<table><tr><th>Cat</th><th>Owner</th><th>Target</th><th>Actual</th><th>$</th><th>Status</th></tr>";
  for (const r of sop.breakdown) {
    h +=
      `<tr><td><strong>${r.category}</strong></td><td>${r.owner}</td>` +
      `<td>${r.target_pct}%</td><td>${r.actual_pct}%</td>` +
      `<td>$${Number(r.amount).toLocaleString()}</td>` +
      `<td class="${r.status === "ON_TRACK" ? "ok" : "viol"}">${r.status === "ON_TRACK" ? "\u2705" : "\u274C"} ${r.status}</td></tr>`;
  }
  return h + "</table>";
}

// ---- Pivot Signals ----
export function renderSignals(signals: PivotSignal[]): string {
  let h = "<h2>\u{1F6A8} Pivot Signals</h2>";
  if (!signals.length)
    return h + '<p style="color:var(--dim);font-size:13px">No signals.</p>';
  for (const s of signals) {
    const c = s.triggered ? "crit" : "safe";
    h +=
      `<div class="signal ${c}"><span class="sig-icon">${s.triggered ? "\u{1F6A8}" : "\u2705"}</span>` +
      `<div class="sig-body"><div class="sig-rule">${s.rule_code}</div>` +
      `<div class="sig-detail">${s.recommendation || ""}</div></div>` +
      `<span class="sig-badge">${s.triggered ? "TRIGGERED" : "SAFE"}</span></div>`;
  }
  return h;
}

// ---- Plan Info + MECE ----
export function renderPlanInfo(plan: Plan): string {
  const b = tryParse(plan.baseline_json);
  const o = tryParse(plan.objectives_json);
  const g = tryParse(plan.gap_analysis_json);

  let h =
    '<h2>\u{1F4CB} Plan Details & MECE Options</h2><div class="plan-info">';
  h += `<div class="kv"><div class="k">Runway</div><div class="v">${b?.fiscal?.runway_months || "-"} months</div></div>`;
  h += `<div class="kv"><div class="k">Cash Balance</div><div class="v">$${Number(b?.fiscal?.cash_balance || 0).toLocaleString()}</div></div>`;
  h += `<div class="kv"><div class="k">ARR Target</div><div class="v">$${Number(o?.growth_targets?.arr_target || 0).toLocaleString()}</div></div>`;
  h += `<div class="kv"><div class="k">ARR Gap</div><div class="v">$${Number(g?.gaps?.arr_gap || 0).toLocaleString()}</div></div></div>`;

  const mece: MeceOption[] = Array.isArray(plan.mece_options_json)
    ? plan.mece_options_json
    : (tryParse(plan.mece_options_json) as unknown as MeceOption[]);

  if (Array.isArray(mece) && mece.length) {
    h += '<div class="mece-grid">';
    for (const m of mece) {
      const sel = m.code === plan.selected_option ? "selected" : "";
      h +=
        `<div class="mece-card ${sel}"><h3>${m.name}</h3><p>${m.description}</p>` +
        `<p style="margin-top:6px">Risk: ${m.risk} | Reward: ${m.reward}<br>Burn: $${Number(m.burn_qtr).toLocaleString()}/qtr</p>` +
        (sel
          ? '<p style="color:var(--blue);font-weight:600;margin-top:4px">\u2713 SELECTED</p>'
          : "") +
        "</div>";
    }
    h += "</div>";
  }

  const d = tryParse(plan.decision_log_json);
  if (d?.ceo_comment) {
    h +=
      `<div style="margin-top:12px;padding:12px;background:rgba(255,255,255,.03);border-radius:8px;font-size:13px">` +
      `<strong>CEO Decision:</strong> "${d.ceo_comment}"<br>` +
      `<span style="color:var(--dim)">${d.decided_by} \u2014 ${d.decided_at}</span></div>`;
  }
  return h;
}
