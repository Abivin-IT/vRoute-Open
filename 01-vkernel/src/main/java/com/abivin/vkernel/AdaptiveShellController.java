package com.abivin.vkernel;

import com.abivin.vkernel.g0_engine.AppLifecycleService;
import com.abivin.vkernel.g0_engine.AppRegistryEntity;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

/**
 * Adaptive UI Shell — micro-frontend host for all installed vApps.
 * Provides a unified navigation shell that dynamically loads vApp UIs
 * via iframes, keeping each vApp isolated in its own context.
 * <p>
 * Routes:
 * - GET /shell           → Main shell with app-switcher sidebar
 * - GET /shell/{appId}   → Shell with specific app pre-selected
 *
 * @GovernanceID 4.0.0 (SyR-PLAT-04: Adaptive UI Shell)
 */
@RestController
public class AdaptiveShellController {

    @Autowired
    private AppLifecycleService appLifecycle;

    private static final String SHELL_CSS = """
        :root{--bg:#0c0e14;--sidebar:#111318;--card:#151821;--border:#252836;
              --text:#e4e4e7;--dim:#71717a;--green:#22c55e;--blue:#3b82f6;
              --purple:#a855f7;--active:#1e293b;--hover:rgba(255,255,255,.04)}
        *{margin:0;padding:0;box-sizing:border-box}
        body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:var(--bg);color:var(--text);height:100vh;overflow:hidden}
        .shell{display:flex;height:100vh}
        .sidebar{width:240px;background:var(--sidebar);border-right:1px solid var(--border);display:flex;flex-direction:column;flex-shrink:0}
        .sidebar-header{padding:16px 20px;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:10px}
        .sidebar-header h1{font-size:16px;font-weight:700}
        .sidebar-header .badge{background:var(--blue);color:#fff;font-size:10px;padding:1px 8px;border-radius:8px;font-weight:600}
        .nav-section{padding:12px 12px 4px;font-size:10px;color:var(--dim);text-transform:uppercase;letter-spacing:1px;font-weight:600}
        .nav-item{display:flex;align-items:center;gap:10px;padding:8px 16px;margin:2px 8px;border-radius:8px;cursor:pointer;color:var(--dim);text-decoration:none;font-size:13px;transition:all .15s}
        .nav-item:hover{background:var(--hover);color:var(--text)}
        .nav-item.active{background:var(--active);color:var(--text);font-weight:600}
        .nav-item .icon{font-size:16px;width:20px;text-align:center}
        .nav-item .status{margin-left:auto;width:6px;height:6px;border-radius:50%;background:var(--green)}
        .sidebar-footer{margin-top:auto;padding:16px;border-top:1px solid var(--border);font-size:11px;color:var(--dim)}
        .main{flex:1;display:flex;flex-direction:column;overflow:hidden}
        .topbar{height:48px;background:var(--card);border-bottom:1px solid var(--border);display:flex;align-items:center;padding:0 20px;gap:12px;flex-shrink:0}
        .topbar .breadcrumb{font-size:13px;color:var(--dim)}
        .topbar .breadcrumb span{color:var(--text);font-weight:600}
        .topbar .search-box{margin-left:auto;background:rgba(255,255,255,.05);border:1px solid var(--border);border-radius:8px;padding:6px 14px;color:var(--text);font-size:12px;width:280px;outline:none}
        .topbar .search-box:focus{border-color:var(--blue)}
        .topbar-actions{display:flex;align-items:center;gap:2px;margin-left:8px}
        .topbar-btn{position:relative;width:32px;height:32px;background:none;border:none;border-radius:8px;cursor:pointer;display:flex;align-items:center;justify-content:center;color:var(--dim);font-size:15px;text-decoration:none;transition:background .15s,color .15s}
        .topbar-btn:hover{background:var(--hover);color:var(--text)}
        .notif-dot{position:absolute;top:6px;right:6px;width:6px;height:6px;border-radius:50%;background:#ef4444;border:1.5px solid var(--card)}
        .logo-mark{width:30px;height:30px;background:linear-gradient(135deg,#3b82f6,#06b6d4);border-radius:7px;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:13px;color:#fff;letter-spacing:-.5px;flex-shrink:0}
        .logo-name{font-size:13px;font-weight:700;line-height:1.1}
        .logo-sub{font-size:9px;color:var(--dim);text-transform:uppercase;letter-spacing:.6px;line-height:1.1}
        .app-frame{flex:1;border:none;width:100%;height:100%}
        .welcome{flex:1;display:flex;align-items:center;justify-content:center;text-align:center;padding:40px}
        .welcome h2{font-size:24px;margin-bottom:12px}
        .welcome p{color:var(--dim);font-size:14px;max-width:500px;line-height:1.8}
        .app-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px;margin-top:24px;padding:0 40px;max-width:800px}
        .app-card{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:20px;text-align:center;cursor:pointer;transition:all .15s;text-decoration:none;color:var(--text)}
        .app-card:hover{border-color:var(--blue);transform:translateY(-2px)}
        .app-card .app-icon{font-size:32px;margin-bottom:8px}
        .app-card .app-name{font-weight:600;font-size:14px}
        .app-card .app-ver{font-size:11px;color:var(--dim);margin-top:4px}
    """;

    /**
     * Main shell page — overview + launcher for installed vApps.
     * GET /shell
     */
    @GetMapping(value = "/shell", produces = MediaType.TEXT_HTML_VALUE)
    public String shell() {
        return renderShell(null);
    }

    /**
     * Shell with specific app loaded in iframe.
     * GET /shell/{appId}
     */
    @GetMapping(value = "/shell/{appId}", produces = MediaType.TEXT_HTML_VALUE)
    public String shellWithApp(@PathVariable String appId) {
        return renderShell(appId);
    }

    private String renderShell(String activeAppId) {
        List<AppRegistryEntity> apps = appLifecycle.listInstalled();

        // Build sidebar nav items for installed apps
        StringBuilder navItems = new StringBuilder();
        String activeAppName = "Home";
        String iframeUrl = null;

        for (var app : apps) {
            boolean isActive = app.getAppId().equals(activeAppId);
            if (isActive) {
                activeAppName = app.getName();
                // Determine iframe URL from app ID
                iframeUrl = resolveAppUrl(app.getAppId());
            }
            navItems.append(String.format("""
                <a class="nav-item %s" href="/shell/%s" data-url="%s">
                    <span class="icon">%s</span>
                    <span>%s</span>
                    %s
                </a>
                """,
                isActive ? "active" : "",
                app.getAppId(),
                resolveAppUrl(app.getAppId()),
                app.getIcon() != null ? app.getIcon() : "📦",
                app.getName(),
                "ACTIVE".equals(app.getStatus()) ? "<span class=\"status\"></span>" : ""));
        }

        // Build app cards for welcome screen
        StringBuilder appCards = new StringBuilder();
        for (var app : apps) {
            appCards.append(String.format("""
                <a class="app-card" href="/shell/%s">
                    <div class="app-icon">%s</div>
                    <div class="app-name">%s</div>
                    <div class="app-ver">%s</div>
                </a>
                """,
                app.getAppId(),
                app.getIcon() != null ? app.getIcon() : "📦",
                app.getName(),
                app.getVersion()));
        }

        // Main content: welcome screen or iframe
        String mainContent;
        if (iframeUrl != null) {
            mainContent = String.format(
                    "<iframe class=\"app-frame\" src=\"%s\" title=\"%s\"></iframe>",
                    iframeUrl, activeAppName);
        } else {
            mainContent = String.format("""
                <div class="welcome">
                    <div>
                        <h2>&#127968; Welcome to vRoute</h2>
                        <p>Select an app from the sidebar, or launch one below.<br>
                        Each vApp runs in isolation with its own database schema and UI.</p>
                        <div class="app-grid">%s</div>
                    </div>
                </div>
                """, appCards.toString());
        }

        return """
            <!doctype html><html lang="en"><head><meta charset="UTF-8">
            <meta name="viewport" content="width=device-width,initial-scale=1">
            <title>vRoute — %s</title>
            <style>%s</style></head><body>
            <div class="shell">
                <div class="sidebar">
                    <div class="sidebar-header">
                        <div class="logo-mark">Ab</div>
                        <div>
                            <div class="logo-name">Abivin</div>
                            <div class="logo-sub">vRoute OS</div>
                        </div>
                    </div>
                    <div class="nav-section">Platform</div>
                    <a class="nav-item %s" href="/shell">
                        <span class="icon">&#127968;</span><span>Home</span>
                    </a>
                    <a class="nav-item" href="/dashboard">
                        <span class="icon">&#128202;</span><span>Dashboard</span>
                    </a>
                    <a class="nav-item" href="/dashboard/api">
                        <span class="icon">&#128268;</span><span>API Explorer</span>
                    </a>
                    <a class="nav-item" href="/dashboard/metrics">
                        <span class="icon">&#128200;</span><span>Metrics</span>
                    </a>
                    <div class="nav-section">Installed Apps (%d)</div>
                    %s
                    <div class="sidebar-footer">
                        vKernel Core OS v1.3.0<br>
                        &#169; Abivin 2026
                    </div>
                </div>
                <div class="main">
                    <div class="topbar">
                        <div class="breadcrumb">vRoute &rsaquo; <span>%s</span></div>
                        <input class="search-box" type="text" placeholder="&#128269; Search across platform... (Ctrl+K)"
                               onfocus="this.placeholder='Type to search...'"
                               onblur="this.placeholder='&#128269; Search across platform... (Ctrl+K)'" />
                        <div class="topbar-actions">
                            <button class="topbar-btn" id="notif-btn" title="Notifications" aria-label="Notifications">&#128276;<span class="notif-dot" id="notif-dot" style="display:none"></span></button>
                            <a class="topbar-btn" href="/dashboard" title="Platform Settings" aria-label="Settings">&#9881;&#65039;</a>
                        </div>
                    </div>
                    %s
                </div>
            </div>
            <script>
            // Keyboard shortcut: Ctrl+K → focus search
            document.addEventListener('keydown', e => {
                if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                    e.preventDefault();
                    document.querySelector('.search-box').focus();
                }
            });
            // Search box: query universal search API
            const searchBox = document.querySelector('.search-box');
            let searchTimeout;
            searchBox.addEventListener('input', () => {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(async () => {
                    const q = searchBox.value.trim();
                    if (q.length < 2) return;
                    try {
                        const r = await fetch('/api/v1/search?q=' + encodeURIComponent(q) + '&limit=10');
                        const data = await r.json();
                        console.log('Search results:', data);
                        // TODO: render search dropdown overlay
                    } catch(e) { console.error('Search error:', e); }
                }, 300);
            });
            </script>
            </body></html>
            """.formatted(
                activeAppName, SHELL_CSS,
                activeAppId == null ? "active" : "",
                apps.size(), navItems.toString(),
                activeAppName,
                mainContent);
    }

    /**
     * Resolve the UI URL for a given app ID.
     * Convention: appId "com.vcorp.vstrategy" → /vstrategy/
     */
    private String resolveAppUrl(String appId) {
        if (appId == null) return "#";
        // Extract last part: com.vcorp.vstrategy → vstrategy
        String[] parts = appId.split("\\.");
        String shortName = parts[parts.length - 1];
        return "/" + shortName + "/";
    }
}
