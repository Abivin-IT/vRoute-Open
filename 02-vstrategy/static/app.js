(function () {
  "use strict";

  /* -----------------------------------------------------------
     API layer – tries real DB endpoints first, then falls back
     to the /sample/ prefix which returns hardcoded demo data.
     ----------------------------------------------------------- */
  const API = "/api/v1/vstrategy";
  const SAMPLE_API = "/api/v1/vstrategy/sample";

  async function fetchJson(path) {
    try {
      const r = await fetch(API + path);
      if (r.ok) return r.json();
    } catch (_) {
      /* real API unavailable */
    }
    const r2 = await fetch(SAMPLE_API + path);
    if (!r2.ok) throw new Error(r2.statusText);
    return r2.json();
  }

  const api = {
    plans: () => fetchJson("/plans"),
    plan: (id) => fetchJson("/plans/" + id),
    tree: (id) => fetchJson("/plans/" + id + "/tree"),
    scorecard: (id) => fetchJson("/plans/" + id + "/scorecard"),
    sop: (id) => fetchJson("/plans/" + id + "/sop/validate"),
    signals: (id) => fetchJson("/plans/" + id + "/signals"),
  };

  /* --- State ------------------------------------------------- */
  let allPlans = [];
  let activeSection = null; // nav item id (null = placeholder)
  let currentView = 0; // 0=List  1=Tree  2=Scorecard (only for 'plans' section)
  let selectedPlanId = null;
  let checkedIds = new Set();
  const appEl = document.getElementById("app");

  /* --- Nav Section → Renderer Map ---------------------------- */
  const NAV_SECTIONS = {
    plans: {
      entity: "Strategic Plans",
      views: ["☰ List", "🌳 Tree", "📊 Scorecard"],
      render: function () {
        renderCurrentPlansView();
      },
    },
    mece: {
      entity: "MECE Framework",
      views: ["📋 Detail"],
      render: renderMeceSection,
    },
    alignment: {
      entity: "Alignment Tree",
      views: ["🌳 Tree"],
      render: renderAlignmentSection,
    },
    sop: {
      entity: "S&OP Resource Allocation",
      views: ["⚖️ Table"],
      render: renderSopSection,
    },
    scorecard: {
      entity: "BSC Scorecard",
      views: ["📊 Scorecard"],
      render: renderBscSection,
    },
    signals: {
      entity: "Pivot Signals",
      views: ["🚨 List"],
      render: renderSignalsSection,
    },
    variance: {
      entity: "Variance Analysis",
      views: [],
      render: renderPlaceholder.bind(
        null,
        "Variance Analysis",
        "Coming soon — Actual vs Plan comparison (FR-STR-04).",
      ),
    },
    "sop-config": {
      entity: "S&OP Config",
      views: [],
      render: renderPlaceholder.bind(
        null,
        "S&OP Config",
        "Coming soon — Configure 68/27/5 allocation ratios and tolerance %.",
      ),
    },
    "signal-rules": {
      entity: "Signal Rules",
      views: [],
      render: renderPlaceholder.bind(
        null,
        "Signal Rules",
        "Coming soon — Configure pivot signal threshold rules.",
      ),
    },
  };

  /* --- Helpers ----------------------------------------------- */
  function esc(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
  }
  function tryParse(s) {
    if (!s) return {};
    try {
      return typeof s === "string" ? JSON.parse(s) : s;
    } catch {
      return {};
    }
  }
  function fmtMoney(n) {
    return "$" + Number(n || 0).toLocaleString();
  }
  function statusClass(s) {
    if (!s) return "s-draft";
    var l = s.toLowerCase();
    if (l === "active" || l === "on_track") return "s-active";
    if (l === "closed" || l === "completed") return "s-closed";
    return "s-draft";
  }

  /* -----------------------------------------------------------
     CONTROL BAR UPDATES
     ----------------------------------------------------------- */
  function updateControlBar(section) {
    // Update entity name
    var entityEl = document.querySelector(".vr-entity-name strong");
    if (entityEl) entityEl.textContent = section ? section.entity : "vStrategy";

    // Update view switcher buttons
    var viewSw = document.querySelector(".vr-view-sw");
    if (viewSw) {
      var views = section ? section.views : [];
      if (views.length === 0) {
        viewSw.innerHTML = "";
      } else {
        viewSw.innerHTML = views
          .map(function (v, i) {
            return (
              '<button class="vr-view-btn' +
              (i === 0 ? " active" : "") +
              '" data-view="' +
              i +
              '">' +
              v +
              "</button>"
            );
          })
          .join("");

        // Re-bind view switcher clicks
        viewSw.querySelectorAll(".vr-view-btn").forEach(function (btn) {
          btn.addEventListener("click", function () {
            viewSw.querySelectorAll(".vr-view-btn").forEach(function (b) {
              b.classList.remove("active");
            });
            btn.classList.add("active");
            var idx = parseInt(btn.dataset.view, 10);
            if (activeSection === "plans") {
              currentView = idx;
              renderCurrentPlansView();
            }
          });
        });
      }
    }

    // Show/hide plan selector based on section
    var planSelectEl = document.getElementById("planSelect");
    if (planSelectEl) {
      planSelectEl.style.display = section ? "" : "none";
    }
  }

  /* -----------------------------------------------------------
     PLACEHOLDER VIEW (no section selected / coming soon)
     ----------------------------------------------------------- */
  function renderWelcomePlaceholder() {
    appEl.innerHTML =
      '<div style="text-align:center;padding:80px 20px;color:var(--dim)">' +
      '<div style="font-size:48px;margin-bottom:16px">📋</div>' +
      '<h2 style="color:var(--text);font-size:20px;font-weight:600;margin-bottom:8px">vStrategy · S2P2R Dashboard</h2>' +
      '<p style="font-size:14px;max-width:400px;margin:0 auto">Select a section from the navigation menu above to begin.</p>' +
      '<div style="margin-top:24px;display:flex;gap:12px;justify-content:center;flex-wrap:wrap">' +
      '<span style="background:var(--card);border:1px solid var(--border);padding:6px 14px;border-radius:8px;font-size:13px">Master Data ▾ Strategic Plans</span>' +
      '<span style="background:var(--card);border:1px solid var(--border);padding:6px 14px;border-radius:8px;font-size:13px">Transactions ▾ Alignment Tree</span>' +
      '<span style="background:var(--card);border:1px solid var(--border);padding:6px 14px;border-radius:8px;font-size:13px">Reporting ▾ BSC Scorecard</span>' +
      "</div></div>";
  }

  function renderPlaceholder(title, message) {
    appEl.innerHTML =
      '<div style="text-align:center;padding:80px 20px;color:var(--dim)">' +
      '<div style="font-size:48px;margin-bottom:16px">🚧</div>' +
      '<h2 style="color:var(--text);font-size:20px;font-weight:600;margin-bottom:8px">' +
      esc(title) +
      "</h2>" +
      '<p style="font-size:14px">' +
      esc(message) +
      "</p></div>";
  }

  function renderNeedsPlan(title) {
    appEl.innerHTML =
      '<div style="text-align:center;padding:60px 20px;color:var(--dim)">' +
      '<div style="font-size:36px;margin-bottom:12px">📌</div>' +
      '<p style="font-size:14px">Select a plan from the dropdown above to view <strong>' +
      esc(title) +
      "</strong>.</p></div>";
  }

  /* =============================================================
     PLANS SECTION — LIST / TREE / SCORECARD views (3-way switch)
     ============================================================= */
  function renderCurrentPlansView() {
    switch (currentView) {
      case 0:
        renderListView();
        break;
      case 1:
        renderTreeView();
        break;
      case 2:
        renderFullScorecardView();
        break;
    }
  }

  /* VIEW 0 — LIST VIEW  (PRD FR-PLAT-04 Default List View) */
  function renderListView() {
    if (!allPlans.length) {
      appEl.innerHTML = '<div class="loading">No plans found.</div>';
      return;
    }
    var h =
      '<table class="vr-list-table"><thead><tr>' +
      '<th class="vr-chk-col"><input type="checkbox" id="chkAll"></th>' +
      '<th>Plan ID <span class="vr-sort">\u25be</span></th>' +
      '<th>Period <span class="vr-sort">\u25be</span></th>' +
      "<th>Status</th><th>Cash Balance</th>" +
      "<th>ARR Target</th><th>Selected Option</th>" +
      '<th style="width:48px"></th></tr></thead><tbody>';

    for (var i = 0; i < allPlans.length; i++) {
      var p = allPlans[i];
      var b = tryParse(p.baseline_json);
      var o = tryParse(p.objectives_json);
      var sel = checkedIds.has(p.id);
      var cls = sel ? ' class="vr-row-selected"' : "";
      h +=
        "<tr" +
        cls +
        ' data-id="' +
        esc(p.id) +
        '">' +
        '<td class="vr-chk-col"><input type="checkbox" class="row-chk" data-id="' +
        esc(p.id) +
        '"' +
        (sel ? " checked" : "") +
        "></td>" +
        "<td><strong>" +
        esc(p.id.substring(0, 8)) +
        "</strong></td>" +
        "<td>" +
        esc(p.period_label || "-") +
        "</td>" +
        '<td><span class="vr-status-pill ' +
        statusClass(p.status) +
        '">' +
        esc(p.status || "DRAFT") +
        "</span></td>" +
        "<td>" +
        fmtMoney(b?.fiscal?.cash_balance) +
        "</td>" +
        "<td>" +
        fmtMoney(o?.growth_targets?.arr_target) +
        "</td>" +
        "<td>" +
        esc(p.selected_option || "-") +
        "</td>" +
        '<td><button class="vr-row-action" data-id="' +
        esc(p.id) +
        '" title="Actions">\u22ee</button></td>' +
        "</tr>";
    }
    h += "</tbody></table>";
    appEl.innerHTML = h;
    bindListEvents();
  }

  function bindListEvents() {
    var chkAll = document.getElementById("chkAll");
    if (chkAll) {
      chkAll.addEventListener("change", function () {
        var boxes = appEl.querySelectorAll(".row-chk");
        checkedIds.clear();
        boxes.forEach(function (cb) {
          cb.checked = chkAll.checked;
          if (chkAll.checked) checkedIds.add(cb.dataset.id);
          cb.closest("tr").classList.toggle("vr-row-selected", chkAll.checked);
        });
        if (window.__VR_BULK_UPDATE__)
          window.__VR_BULK_UPDATE__(checkedIds.size);
      });
    }
    appEl.querySelectorAll(".row-chk").forEach(function (cb) {
      cb.addEventListener("change", function () {
        if (cb.checked) checkedIds.add(cb.dataset.id);
        else checkedIds.delete(cb.dataset.id);
        cb.closest("tr").classList.toggle("vr-row-selected", cb.checked);
        if (chkAll) chkAll.checked = checkedIds.size === allPlans.length;
        if (window.__VR_BULK_UPDATE__)
          window.__VR_BULK_UPDATE__(checkedIds.size);
      });
    });
    appEl.querySelectorAll(".vr-row-action").forEach(function (btn) {
      btn.addEventListener("click", function (e) {
        e.stopPropagation();
        selectedPlanId = btn.dataset.id;
        updatePlanSelector();
        // Switch to tree view for this plan
        currentView = 1;
        updateControlBar(NAV_SECTIONS["plans"]);
        renderCurrentPlansView();
      });
    });
    appEl.querySelectorAll(".vr-list-table tbody tr").forEach(function (row) {
      row.addEventListener("click", function (e) {
        if (e.target.closest("input") || e.target.closest("button")) return;
        selectedPlanId = row.dataset.id;
        updatePlanSelector();
      });
    });
  }

  /* VIEW 1 — TREE VIEW  (FR-STR-00 Alignment Tree) */
  var ICONS = {
    VISION: "\ud83d\udc51",
    BSC_PERSPECTIVE: "\ud83d\udcca",
    OKR: "\ud83c\udfaf",
    INITIATIVE: "\ud83d\ude80",
    TASK: "\ud83d\udccb",
  };
  var BSC_ICONS = {
    FINANCE: "\ud83d\udcb0",
    CUSTOMER: "\ud83d\ude0a",
    PROCESS: "\u2699\ufe0f",
    LEARNING: "\ud83d\udcda",
  };

  function buildTree(nodes) {
    var map = {},
      roots = [];
    for (var i = 0; i < nodes.length; i++)
      map[nodes[i].id] = Object.assign({}, nodes[i], { children: [] });
    for (var i = 0; i < nodes.length; i++) {
      var n = nodes[i];
      if (n.parent_id && map[n.parent_id])
        map[n.parent_id].children.push(map[n.id]);
      else roots.push(map[n.id]);
    }
    return roots;
  }

  function renderNode(n) {
    var icon = ICONS[n.node_level] || "\u2022";
    var bsc = n.bsc_perspective
      ? (BSC_ICONS[n.bsc_perspective] || "") + " "
      : "";
    var meta = tryParse(n.metadata_json);
    var alert = meta.alert || "";
    var dot =
      n.status === "GREEN"
        ? "\ud83d\udfe2"
        : n.status === "YELLOW"
          ? "\ud83d\udfe1"
          : "\ud83d\udd34";
    var h =
      '<li><div class="node ' +
      n.status +
      '"><span class="icon">' +
      icon +
      "</span>" +
      '<span class="title">' +
      bsc +
      esc(n.code ? n.code + ": " : "") +
      esc(n.title) +
      "</span>";
    if (n.owner) h += '<span class="owner-tag">' + esc(n.owner) + "</span>";
    h += '<span class="pct">' + dot + " " + n.progress_pct + "%</span></div>";
    if (alert)
      h += '<span class="alert-tag">\u26a0\ufe0f ' + esc(alert) + "</span>";
    if (n.children.length)
      h += "<ul>" + n.children.map(renderNode).join("") + "</ul>";
    return h + "</li>";
  }

  async function renderTreeView() {
    if (!selectedPlanId) {
      renderNeedsPlan("Alignment Tree");
      return;
    }
    appEl.innerHTML = '<div class="loading">Loading alignment tree\u2026</div>';
    try {
      var data = await api.tree(selectedPlanId);
      var roots = buildTree(data.nodes);
      appEl.innerHTML =
        "<h2>\ud83c\udf33 Alignment Tree \u2014 " +
        esc(selectedPlanId.substring(0, 8)) +
        "</h2>" +
        '<div class="tree"><ul>' +
        roots.map(renderNode).join("") +
        "</ul></div>";
    } catch (e) {
      appEl.innerHTML =
        '<div class="loading">Error: ' + esc(e.message) + "</div>";
    }
  }

  /* VIEW 2 — FULL SCORECARD  (BSC + S&OP + Signals + Plan Details) */
  async function renderFullScorecardView() {
    if (!selectedPlanId) {
      renderNeedsPlan("Scorecard");
      return;
    }
    appEl.innerHTML = '<div class="loading">Loading scorecard\u2026</div>';
    try {
      var results = await Promise.all([
        api.plan(selectedPlanId),
        api.scorecard(selectedPlanId),
        api.sop(selectedPlanId),
        api.signals(selectedPlanId),
      ]);
      var plan = results[0],
        sc = results[1],
        sop = results[2],
        sig = results[3];
      var h = "";
      h += '<div class="card full">' + renderBSC(sc) + "</div>";
      h += '<div class="grid"><div class="card">' + renderSop(sop) + "</div>";
      h += '<div class="card">' + renderSignals(sig.signals) + "</div></div>";
      h += '<div class="card full">' + renderPlanInfo(plan) + "</div>";
      appEl.innerHTML = h;
    } catch (e) {
      appEl.innerHTML =
        '<div class="loading">Error: ' + esc(e.message) + "</div>";
    }
  }

  /* =============================================================
     DEDICATED SECTION RENDERERS (nav item → single-focus view)
     ============================================================= */

  /* ALIGNMENT SECTION (standalone tree) */
  async function renderAlignmentSection() {
    await renderTreeView();
  }

  /* BSC SCORECARD SECTION */
  async function renderBscSection() {
    if (!selectedPlanId) {
      renderNeedsPlan("BSC Scorecard");
      return;
    }
    appEl.innerHTML = '<div class="loading">Loading BSC Scorecard\u2026</div>';
    try {
      var sc = await api.scorecard(selectedPlanId);
      appEl.innerHTML = '<div class="card full">' + renderBSC(sc) + "</div>";
    } catch (e) {
      appEl.innerHTML =
        '<div class="loading">Error: ' + esc(e.message) + "</div>";
    }
  }

  /* S&OP SECTION */
  async function renderSopSection() {
    if (!selectedPlanId) {
      renderNeedsPlan("S&OP Resource Allocation");
      return;
    }
    appEl.innerHTML = '<div class="loading">Loading S&amp;OP\u2026</div>';
    try {
      var sop = await api.sop(selectedPlanId);
      appEl.innerHTML = '<div class="card full">' + renderSop(sop) + "</div>";
    } catch (e) {
      appEl.innerHTML =
        '<div class="loading">Error: ' + esc(e.message) + "</div>";
    }
  }

  /* SIGNALS SECTION */
  async function renderSignalsSection() {
    if (!selectedPlanId) {
      renderNeedsPlan("Pivot Signals");
      return;
    }
    appEl.innerHTML = '<div class="loading">Loading Pivot Signals\u2026</div>';
    try {
      var sig = await api.signals(selectedPlanId);
      appEl.innerHTML =
        '<div class="card full">' + renderSignals(sig.signals) + "</div>";
    } catch (e) {
      appEl.innerHTML =
        '<div class="loading">Error: ' + esc(e.message) + "</div>";
    }
  }

  /* MECE SECTION (Plan details + MECE 4-option cards) */
  async function renderMeceSection() {
    if (!selectedPlanId) {
      renderNeedsPlan("MECE Framework");
      return;
    }
    appEl.innerHTML = '<div class="loading">Loading MECE Framework\u2026</div>';
    try {
      var plan = await api.plan(selectedPlanId);
      appEl.innerHTML =
        '<div class="card full">' + renderPlanInfo(plan) + "</div>";
    } catch (e) {
      appEl.innerHTML =
        '<div class="loading">Error: ' + esc(e.message) + "</div>";
    }
  }

  /* =============================================================
     SHARED SUB-RENDERERS (return HTML strings)
     ============================================================= */
  function renderBSC(sc) {
    var h =
      '<h2>\ud83d\udcca Balanced Scorecard \u2014 Overall: <span class="' +
      sc.overall_status +
      '">' +
      sc.overall_status +
      " " +
      sc.overall_progress_pct +
      '%</span></h2><div class="bsc-grid">';
    for (var i = 0; i < sc.perspectives.length; i++) {
      var p = sc.perspectives[i];
      var icon = BSC_ICONS[p.perspective] || "\ud83d\udcca";
      h +=
        '<div class="bsc-item"><div class="label">' +
        icon +
        " " +
        p.perspective +
        "</div>" +
        '<div class="bar-track"><div class="bar-fill ' +
        p.status +
        '" style="width:' +
        p.progress_pct +
        '%">' +
        p.progress_pct +
        "%</div></div></div>";
    }
    return h + "</div>";
  }

  function renderSop(sop) {
    var h =
      "<h2>\u2696\ufe0f S&amp;OP 68/27/5 \u2014 " +
      (sop.valid ? "\u2705 VALID" : "\u274c VIOLATION") +
      "</h2>" +
      '<p style="font-size:12px;color:var(--dim);margin-bottom:8px">Budget: ' +
      fmtMoney(sop.total_budget) +
      " | HC: +" +
      sop.total_headcount +
      " FTE</p>" +
      "<table><tr><th>Cat</th><th>Owner</th><th>Target</th><th>Actual</th><th>$</th><th>Status</th></tr>";
    for (var i = 0; i < sop.breakdown.length; i++) {
      var r = sop.breakdown[i];
      h +=
        "<tr><td><strong>" +
        esc(r.category) +
        "</strong></td><td>" +
        esc(r.owner) +
        "</td>" +
        "<td>" +
        r.target_pct +
        "%</td><td>" +
        r.actual_pct +
        "%</td><td>" +
        fmtMoney(r.amount) +
        "</td>" +
        '<td class="' +
        (r.status === "ON_TRACK" ? "ok" : "viol") +
        '">' +
        (r.status === "ON_TRACK" ? "\u2705" : "\u274c") +
        " " +
        esc(r.status) +
        "</td></tr>";
    }
    return h + "</table>";
  }

  function renderSignals(signals) {
    var h = "<h2>\ud83d\udea8 Pivot Signals</h2>";
    if (!signals || !signals.length)
      return h + '<p style="color:var(--dim);font-size:13px">No signals.</p>';
    for (var i = 0; i < signals.length; i++) {
      var s = signals[i];
      var c = s.triggered ? "crit" : "safe";
      h +=
        '<div class="signal ' +
        c +
        '"><span class="sig-icon">' +
        (s.triggered ? "\ud83d\udea8" : "\u2705") +
        "</span>" +
        '<div class="sig-body"><div class="sig-rule">' +
        esc(s.rule_code) +
        "</div>" +
        '<div class="sig-detail">' +
        esc(s.recommendation || "") +
        "</div></div>" +
        '<span class="sig-badge">' +
        (s.triggered ? "TRIGGERED" : "SAFE") +
        "</span></div>";
    }
    return h;
  }

  function renderPlanInfo(plan) {
    var b = tryParse(plan.baseline_json);
    var o = tryParse(plan.objectives_json);
    var g = tryParse(plan.gap_analysis_json);
    var h =
      '<h2>\ud83d\udccb Plan Details &amp; MECE Options</h2><div class="plan-info">';
    h +=
      '<div class="kv"><div class="k">Runway</div><div class="v">' +
      (b?.fiscal?.runway_months || "-") +
      " months</div></div>";
    h +=
      '<div class="kv"><div class="k">Cash Balance</div><div class="v">' +
      fmtMoney(b?.fiscal?.cash_balance) +
      "</div></div>";
    h +=
      '<div class="kv"><div class="k">ARR Target</div><div class="v">' +
      fmtMoney(o?.growth_targets?.arr_target) +
      "</div></div>";
    h +=
      '<div class="kv"><div class="k">ARR Gap</div><div class="v">' +
      fmtMoney(g?.gaps?.arr_gap) +
      "</div></div></div>";
    var mece = Array.isArray(plan.mece_options_json)
      ? plan.mece_options_json
      : tryParse(plan.mece_options_json);
    if (Array.isArray(mece) && mece.length) {
      h += '<div class="mece-grid">';
      for (var i = 0; i < mece.length; i++) {
        var m = mece[i];
        var sel = m.code === plan.selected_option ? "selected" : "";
        h +=
          '<div class="mece-card ' +
          sel +
          '"><h3>' +
          esc(m.name) +
          "</h3><p>" +
          esc(m.description) +
          "</p>" +
          '<p style="margin-top:6px">Risk: ' +
          esc(m.risk) +
          " | Reward: " +
          esc(m.reward) +
          "<br>Burn: " +
          fmtMoney(m.burn_qtr) +
          "/qtr</p>" +
          (sel
            ? '<p style="color:var(--blue);font-weight:600;margin-top:4px">\u2713 SELECTED</p>'
            : "") +
          "</div>";
      }
      h += "</div>";
    }
    var d = tryParse(plan.decision_log_json);
    if (d?.ceo_comment) {
      h +=
        '<div style="margin-top:12px;padding:12px;background:rgba(255,255,255,.03);border-radius:8px;font-size:13px">' +
        '<strong>CEO Decision:</strong> "' +
        esc(d.ceo_comment) +
        '"<br>' +
        '<span style="color:var(--dim)">' +
        esc(d.decided_by) +
        " \u2014 " +
        esc(d.decided_at) +
        "</span></div>";
    }
    return h;
  }

  /* =============================================================
     NAV SECTION SWITCHING
     ============================================================= */
  function activateSection(sectionId) {
    activeSection = sectionId;
    var section = NAV_SECTIONS[sectionId];
    if (!section) {
      updateControlBar(null);
      renderWelcomePlaceholder();
      return;
    }
    updateControlBar(section);
    section.render();
  }

  // Listen for nav menu clicks from app-layout.js
  document.addEventListener("vr:nav-change", function (e) {
    var id = e.detail.id;
    activateSection(id);
  });

  // Listen for view-change from control bar (view switcher clicks)
  document.addEventListener("vr:view-change", function (e) {
    if (activeSection === "plans") {
      currentView = e.detail.index;
      renderCurrentPlansView();
    }
  });

  /* --- Plan selector ----------------------------------------- */
  function updatePlanSelector() {
    var sel = document.getElementById("planSelect");
    if (sel && selectedPlanId) sel.value = selectedPlanId;
  }
  function populatePlanSelector() {
    var sel = document.getElementById("planSelect");
    if (!sel) return;
    sel.innerHTML = "";
    for (var i = 0; i < allPlans.length; i++) {
      var p = allPlans[i];
      var o = document.createElement("option");
      o.value = p.id;
      o.textContent = p.period_label + " (" + p.status + ")";
      sel.appendChild(o);
    }
    sel.addEventListener("change", function () {
      selectedPlanId = sel.value;
      // Re-render current section (plan-dependent sections need refresh)
      if (activeSection && NAV_SECTIONS[activeSection]) {
        NAV_SECTIONS[activeSection].render();
      }
    });
  }

  /* =============================================================
     BOOT
     ============================================================= */
  async function boot() {
    try {
      var data = await api.plans();
      allPlans = data.plans || [];
      if (allPlans.length) selectedPlanId = allPlans[0].id;
      populatePlanSelector();
      updatePlanSelector();
      // Show welcome placeholder — user picks a nav section
      renderWelcomePlaceholder();
    } catch (e) {
      appEl.innerHTML =
        '<div class="loading">Error loading plans: ' +
        esc(e.message) +
        "</div>";
    }
  }
  boot();
})();
