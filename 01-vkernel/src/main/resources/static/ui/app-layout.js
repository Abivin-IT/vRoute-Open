/**
 * vRoute Shared App Layout Script  ·  served by vKernel at /ui/app-layout.js
 *
 * Usage in any vApp's index.html:
 *   1. In <head>: <link rel="stylesheet" href="/ui/app-layout.css" />
 *   2. In <body>: <div id="vr-topbar" data-app-title="App Name · Subtitle"></div>
 *   3. Before </body>: <script src="/ui/app-layout.js"></script>
 *
 * The script hydrates #vr-topbar with:
 *   - Abivin logo (top-left), links back to /shell on click
 *   - App title (from data-app-title)
 *   - Search box (Ctrl+K to focus)
 *   - Notifications bell with red dot indicator
 *   - Settings gear (links to /dashboard)
 *   - Home button (links to /shell)
 *
 * @GovernanceID vkernel.ui.1.0
 */
(function () {
  "use strict";

  // ── Helper: SVG icons ─────────────────────────────────────
  const ICON = {
    bell: '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>',
    gear: '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>',
    home: '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>',
    search:
      '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>',
  };

  // ── Hydrate the topbar ────────────────────────────────────
  var bar = document.getElementById("vr-topbar");
  if (!bar) return;

  // When running inside the shell's iframe, suppress the app-level topbar
  // (the shell already provides the logo/search/notifications/settings bar).
  if (window.self !== window.top) {
    bar.style.display = "none";
    return;
  }

  var appTitle = bar.dataset.appTitle || document.title || "vApp";

  bar.className = "vr-topbar";
  bar.innerHTML =
    // Logo ─────────────────────────────────────────────────
    '<a class="vr-logo" href="/shell" target="_top" title="Abivin vRoute OS">' +
    '  <div class="vr-logo-mark">Ab</div>' +
    '  <div class="vr-logo-texts">' +
    '    <span class="vr-logo-name">Abivin</span>' +
    '    <span class="vr-logo-sub">vRoute OS</span>' +
    "  </div>" +
    "</a>" +
    // Separator + App title ────────────────────────────────
    '<div class="vr-sep"></div>' +
    '<span class="vr-app-name">' +
    _esc(appTitle) +
    "</span>" +
    // Spacer ───────────────────────────────────────────────
    '<div class="vr-spacer"></div>' +
    // Search ───────────────────────────────────────────────
    '<label class="vr-search" id="vr-search-wrap">' +
    '  <span class="vr-search-icon">' +
    ICON.search +
    "</span>" +
    '  <input class="vr-search-input" id="vr-search" type="search"' +
    '         placeholder="Search\u2026 (Ctrl+K)" aria-label="Search" />' +
    "</label>" +
    // Actions ──────────────────────────────────────────────
    '<div class="vr-actions">' +
    // Notifications
    '  <button class="vr-btn" id="vr-notif-btn" title="Notifications" aria-label="Notifications">' +
    "    " +
    ICON.bell +
    '    <span class="vr-notif-dot" id="vr-notif-dot" style="display:none"></span>' +
    "  </button>" +
    // Settings → vKernel dashboard
    '  <a class="vr-btn" href="/dashboard" target="_top" title="Platform Settings" aria-label="Settings">' +
    "    " +
    ICON.gear +
    "  </a>" +
    // Home → Shell
    '  <a class="vr-btn" href="/shell" target="_top" title="Back to Shell" aria-label="Shell">' +
    "    " +
    ICON.home +
    "  </a>" +
    "</div>";

  // ── Keyboard shortcut: Ctrl+K → focus search ─────────────
  document.addEventListener("keydown", function (e) {
    if ((e.ctrlKey || e.metaKey) && e.key === "k") {
      e.preventDefault();
      var inp = document.getElementById("vr-search");
      if (inp) {
        inp.focus();
        inp.select();
      }
    }
  });

  // ── Poll vKernel for notification count (best-effort) ─────
  _pollNotifications();

  // ── Helpers ──────────────────────────────────────────────
  function _esc(str) {
    return str
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
  }

  function _pollNotifications() {
    // Try to fetch unread count from vKernel; silently ignore errors
    fetch("/api/v1/notifications/unread-count", { credentials: "include" })
      .then(function (r) {
        return r.ok ? r.json() : null;
      })
      .then(function (data) {
        if (data && data.count > 0) {
          var dot = document.getElementById("vr-notif-dot");
          if (dot) dot.style.display = "block";
        }
      })
      .catch(function () {
        /* silently ignore */
      });
  }
})();
