(function () {
  "use strict";

  // --- API ---
  const API = "/api/v1/vstrategy";
  async function fetchJson(path) {
    const r = await fetch(API + path);
    return r.json();
  }
  const api = {
    plans:     ()   => fetchJson("/plans"),
    plan:      (id) => fetchJson("/plans/" + id),
    tree:      (id) => fetchJson("/plans/" + id + "/tree"),
    scorecard: (id) => fetchJson("/plans/" + id + "/scorecard"),
    sop:       (id) => fetchJson("/plans/" + id + "/sop/validate"),
    signals:   (id) => fetchJson("/plans/" + id + "/signals"),
  };

  // --- State ---
  let allPlans = [];
  let currentView = 0;          // 0=List  1=Tree  2=Scorecard
  let selectedPlanId = null;
  let checkedIds = new Set();
  const app = document.getElementById("app");

  // --- Helpers ---
  function esc(s){return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");}
  function tryParse(s){if(ssh-add ~/.ssh/orderchuan)return {};try{return typeof s==="string"?JSON.parse(s):s;}catch{return {};}}
  function fmtMoney(n){return "$"+Number(n||0).toLocaleString();}
  function statusClass(s){
    if(ssh-add ~/.ssh/orderchuan)return "s-draft";
    const l=s.toLowerCase();
    if(l==="active"||l==="on_track")return "s-active";
    if(l==="closed"||l==="completed")return "s-closed";
    return "s-draft";
  }

  /* ============================================================
     VIEW 0 — LIST VIEW  (default)
     ============================================================ */
  function renderListView(){
      app.innerHTML="<div class=\"loading\">No plans found. Create one via API.</div>";return;}
    let h="<table class=\"vr-list-table\"><thead><tr>"+
      "<th class=\"vr-chk-col\"><input type=\"checkbox\" id=\"chkAll\"></th>"+
      "<th>Plan ID <span class=\"vr-sort\">\u25be</span></th>"+
      "<th>Period <span class=\"vr-sort\">\u25be</span></th>"+
      "<th>Status</th>"+
      "<th>Cash Balance</th>"+
      "<th>ARR Target</th>"+
      "<th>Selected Option</th>"+
      "<th style=\"width:48px\"></th>"+
      "</tr></thead><tbody>";
    for(const p of allPlans){
      const b=tryParse(p.baseline_json);
      const o=tryParse(p.objectives_json);
      const sel=checkedIds.has(p.id);
      const cls=sel?" class=\"vr-row-selected\"":"";
      h+="<tr"+cls+" data-id=\""+esc(p.id)+"\">"+
        "<td class=\"vr-chk-col\"><input type=\"checkbox\" class=\"row-chk\" data-id=\""+esc(p.id)+"\""+(sel?" checked":"")+"></td>"+
        "<td><strong>"+esc(p.id)+"</strong></td>"+
        "<td>"+esc(p.period_label||"-")+"</td>"+
        "<td><span class=\"vr-status-pill "+statusClass(p.status)+"\">"+esc(p.status||"DRAFT")+"</span></td>"+
        "<td>"+fmtMoney(b?.fiscal?.cash_balance)+"</td>"+
        "<td>"+fmtMoney(o?.growth_targets?.arr_target)+"</td>"+
        "<td>"+esc(p.selected_option||"-")+"</td>"+
        "<td><button class=\"vr-row-action\" data-id=\""+esc(p.id)+"\" title=\"Actions\">\u22ee</button></td>"+
        "</tr>";
    }
    h+="</tbody></table>";
    app.innerHTML=h;
    bindListEvents();
  }

  function bindListEvents(){
    const chkAll=document.getElementById("chkAll");
    if(chkAll){
      chkAll.addEventListener("change",function(){
        const boxes=app.querySelectorAll(".row-chk");
        checkedIds.clear();
        boxes.forEach(function(cb){
          cb.checked=chkAll.checked;
          if(chkAll.checked)checkedIds.add(cb.dataset.id);
          cb.closest("tr").classList.toggle("vr-row-selected",chkAll.checked);
        });
        if(window.__VR_BULK_UPDATE__)window.__VR_BULK_UPDATE__(checkedIds.size);
      });
    }
    app.querySelectorAll(".row-chk").forEach(function(cb){
      cb.addEventListener("change",function(){
        if(cb.checked)checkedIds.add(cb.dataset.id);
        else checkedIds.delete(cb.dataset.id);
        cb.closest("tr").classList.toggle("vr-row-selected",cb.checked);
        if(chkAll)chkAll.checked=checkedIds.size===allPlans.length;
        if(window.__VR_BULK_UPDATE__)window.__VR_BULK_UPDATE__(checkedIds.size);
      });
    });
    app.querySelectorAll(".vr-row-action").forEach(function(btn){
      btn.addEventListener("click",function(e){
        e.stopPropagation();
        selectedPlanId=btn.dataset.id;
        updatePlanSelector();
        switchView(1);
      });
    });
    app.querySelectorAll(".vr-list-table tbody tr").forEach(function(row){
      row.addEventListener("click",function(e){
        if(e.target.closest("input")||e.target.closest("button"))return;
        selectedPlanId=row.dataset.id;
        updatePlanSelector();
      });
    });
  }

  /* ============================================================
     VIEW 1 — TREE VIEW
     ============================================================ */
  const ICONS={VISION:"\ud83d\udc51",BSC_PERSPECTIVE:"\ud83d\udcca",OKR:"\ud83c\udfaf",INITIATIVE:"\ud83d\ude80",TASK:"\ud83d\udccb"};
  const BSC_ICONS={FINANCE:"\ud83d\udcb0",CUSTOMER:"\ud83d\ude0a",PROCESS:"\u2699\ufe0f",LEARNING:"\ud83d\udcda"};

  function buildTree(nodes){
    const map={},roots=[];
    for(const n of nodes)map[n.id]={...n,children:[]};
    for(const n of nodes){if(n.parent_id&&map[n.parent_id])map[n.parent_id].children.push(map[n.id]);else roots.push(map[n.id]);}
    return roots;
  }
  function renderNode(n){
    const icon=ICONS[n.node_level]||"\u2022";
    const bsc=n.bsc_perspective?(BSC_ICONS[n.bsc_perspective]||"")+" ":"";
    const alert=tryAlert(n.metadata_json);
    const dot=n.status==="GREEN"?"\ud83d\udfe2":n.status==="YELLOW"?"\ud83d\udfe1":"\ud83d\udd34";
    let h="<li><div class=\"node "+n.status+"\"><span class=\"icon\">"+icon+"</span>"+
      "<span class=\"title\">"+bsc+esc(n.code?n.code+": ":"")+esc(n.title)+"</span>";
    if(n.owner)h+="<span class=\"owner-tag\">"+esc(n.owner)+"</span>";
    h+="<span class=\"pct\">"+dot+" "+n.progress_pct+"%</span></div>";
    if(alert)h+="<span class=\"alert-tag\">\u26a0\ufe0f "+esc(alert)+"</span>";
    if(n.children.length)h+="<ul>"+n.children.map(renderNode).join("")+"</ul>";
    return h+"</li>";
  }

  async function renderTreeView(){
    app.innerHTML="<div class=\"loading\">Loading alignment tree\u2026</div>";
    try{
      const data=await api.tree(selectedPlanId);
      const roots=buildTree(data.nodes);
      app.innerHTML="<h2>\ud83c\udf33 Alignment Tree \u2014 "+esc(selectedPlanId)+"</h2>"+
        "<div class=\"tree\"><ul>"+roots.map(renderNode).join("")+"</ul></div>";
    }catch(e){app.innerHTML="<div class=\"loading\">Error: "+esc(e.message)+"</div>";}
  }

  /* ============================================================
     VIEW 2 — SCORECARD VIEW
     ============================================================ */
  async function renderScorecardView(){
    app.innerHTML="<div class=\"loading\">Loading scorecard\u2026</div>";
    try{
      const [plan,sc,sop,sig]=await Promise.all([
        api.plan(selectedPlanId),api.scorecard(selectedPlanId),
        api.sop(selectedPlanId),api.signals(selectedPlanId),
      ]);
      let h="";
      h+="<div class=\"card full\">"+renderBSC(sc)+"</div>";
      h+="<div class=\"grid\"><div class=\"card\">"+renderSop(sop)+"</div>";
      h+="<div class=\"card\">"+renderSignals(sig.signals)+"</div></div>";
      h+="<div class=\"card full\">"+renderPlanInfo(plan)+"</div>";
      app.innerHTML=h;
    }catch(e){app.innerHTML="<div class=\"loading\">Error: "+esc(e.message)+"</div>";}
  }

  function renderBSC(sc){
    let h="<h2>\ud83d\udcca Balanced Scorecard \u2014 Overall: <span class=\""+sc.overall_status+"\">"+
      sc.overall_status+" "+sc.overall_progress_pct+"%</span></h2><div class=\"bsc-grid\">";
    for(const p of sc.perspectives){
      const icon=BSC_ICONS[p.perspective]||"\ud83d\udcca";
      h+="<div class=\"bsc-item\"><div class=\"label\">"+icon+" "+p.perspective+"</div>"+
        "<div class=\"bar-track\"><div class=\"bar-fill "+p.status+"\" style=\"width:"+p.progress_pct+"%\">"+p.progress_pct+"%</div></div></div>";
    }
    return h+"</div>";
  }

  function renderSop(sop){
    let h="<h2>\u2696\ufe0f S&amp;OP 68/27/5 \u2014 "+(sop.valid?"\u2705 VALID":"\u274c VIOLATION")+"</h2>"+
      "<p style=\"font-size:12px;color:var(--dim);margin-bottom:8px\">Budget: "+fmtMoney(sop.total_budget)+" | HC: +"+sop.total_headcount+" FTE</p>"+
      "<table><tr><th>Cat</th><th>Owner</th><th>Target</th><th>Actual</th><th>$</th><th>Status</th></tr>";
    for(const r of sop.breakdown){
      h+="<tr><td><strong>"+esc(r.category)+"</strong></td><td>"+esc(r.owner)+"</td>"+
        "<td>"+r.target_pct+"%</td><td>"+r.actual_pct+"%</td>"+
        "<td>"+fmtMoney(r.amount)+"</td>"+
        "<td class=\""+(r.status==="ON_TRACK"?"ok":"viol")+"\">"+
        (r.status==="ON_TRACK"?"\u2705":"\u274c")+" "+esc(r.status)+"</td></tr>";
    }
    return h+"</table>";
  }

  function renderSignals(signals){
    let h="<h2>\ud83d\udea8 Pivot Signals</h2>";
    for(const s of signals){
      const c=s.triggered?"crit":"safe";
      h+="<div class=\"signal "+c+"\"><span class=\"sig-icon\">"+(s.triggered?"\ud83d\udea8":"\u2705")+"</span>"+
        "<div class=\"sig-body\"><div class=\"sig-rule\">"+esc(s.rule_code)+"</div>"+
        "<div class=\"sig-detail\">"+esc(s.recommendation||"")+"</div></div>"+
        "<span class=\"sig-badge\">"+(s.triggered?"TRIGGERED":"SAFE")+"</span></div>";
    }
    return h;
  }

  function renderPlanInfo(plan){
    const b=tryParse(plan.baseline_json);
    const o=tryParse(plan.objectives_json);
    const g=tryParse(plan.gap_analysis_json);
    let h="<h2>\ud83d\udccb Plan Details &amp; MECE Options</h2><div class=\"plan-info\">";
    h+="<div class=\"kv\"><div class=\"k\">Runway</div><div class=\"v\">"+(b?.fiscal?.runway_months||"-")+" months</div></div>";
    h+="<div class=\"kv\"><div class=\"k\">Cash Balance</div><div class=\"v\">"+fmtMoney(b?.fiscal?.cash_balance)+"</div></div>";
    h+="<div class=\"kv\"><div class=\"k\">ARR Target</div><div class=\"v\">"+fmtMoney(o?.growth_targets?.arr_target)+"</div></div>";
    h+="<div class=\"kv\"><div class=\"k\">ARR Gap</div><div class=\"v\">"+fmtMoney(g?.gaps?.arr_gap)+"</div></div></div>";
    const mece=Array.isArray(plan.mece_options_json)?plan.mece_options_json:tryParse(plan.mece_options_json);
    if(Array.isArray(mece)&&mece.length){
      h+="<div class=\"mece-grid\">";
      for(const m of mece){
        const sel=m.code===plan.selected_option?"selected":"";
        h+="<div class=\"mece-card "+sel+"\"><h3>"+esc(m.name)+"</h3><p>"+esc(m.description)+"</p>"+
          "<p style=\"margin-top:6px\">Risk: "+esc(m.risk)+" | Reward: "+esc(m.reward)+"<br>Burn: "+fmtMoney(m.burn_qtr)+"/qtr</p>"+
          (sel?"<p style=\"color:var(--blue);font-weight:600;margin-top:4px\">\u2713 SELECTED</p>":"")+"</div>";
      }
      h+="</div>";
    }
    const d=tryParse(plan.decision_log_json);
    if(d?.ceo_comment){
      h+="<div style=\"margin-top:12px;padding:12px;background:rgba(255,255,255,.03);border-radius:8px;font-size:13px\">"+
        "<strong>CEO Decision:</strong> \""+esc(d.ceo_comment)+"\"<br>"+
        "<span style=\"color:var(--dim)\">"+esc(d.decided_by)+" \u2014 "+esc(d.decided_at)+"</span></div>";
    }
    return h;
  }

  /* ============================================================
     VIEW SWITCHING
     ============================================================ */
  function renderCurrentView(){
    switch(currentView){
      case 0:renderListView();break;
      case 1:renderTreeView();break;
      case 2:renderScorecardView();break;
    }
  }
  function switchView(idx){
    currentView=idx;
    document.querySelectorAll(".vr-view-btn").forEach(function(b){
      b.classList.toggle("active",parseInt(b.dataset.view,10)===idx);
    });
    renderCurrentView();
  }
  document.addEventListener("vr:view-change",function(e){
    currentView=e.detail.index;
    renderCurrentView();
  });

  /* ============================================================
     PLAN SELECTOR  (injected via entitySlot in control bar)
     ============================================================ */
  function updatePlanSelector(){
    const sel=document.getElementById("planSelect");
    if(sel&&selectedPlanId)sel.value=selectedPlanId;
  }
  function populatePlanSelector(){
    const sel=document.getElementById("planSelect");
    sel.innerHTML="";
    for(const p of allPlans){
      const o=document.createElement("option");
      o.value=p.id;
      o.textContent=p.period_label+" ("+p.status+")";
      sel.appendChild(o);
    }
    sel.addEventListener("change",function(){
      selectedPlanId=sel.value;
      if(currentView!==0)renderCurrentView();
    });
  }

  /* ============================================================
     BOOT
     ============================================================ */
  async function boot(){
    try{
      const data=await api.plans();
      allPlans=data.plans||[];
      if(allPlans.length)selectedPlanId=allPlans[0].id;
      populatePlanSelector();
      updatePlanSelector();
      renderListView();
    }catch(e){
      app.innerHTML="<div class=\"loading\">Error loading plans: "+esc(e.message)+"</div>";
    }
  }
  boot();
})();