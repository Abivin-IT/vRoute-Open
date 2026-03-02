package com.abivin.vkernel;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import com.abivin.vkernel.g0_engine.AppLifecycleService;
import com.abivin.vkernel.g0_engine.AppRegistryEntity;
import com.abivin.vkernel.g3_event.EventBusService;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;

/**
 * vKernel HTML Dashboard — serves interactive HTML pages for all endpoints.
 * Accessible without authentication (same as actuator endpoints).
 *
 * @GovernanceID 0.0.0-DASH
 */
@RestController
public class DashboardController {

    @Autowired private AppLifecycleService appLifecycle;
    @Autowired private EventBusService eventBusService;

    private static final String CSS = """
        :root{--bg:#0c0e14;--card:#151821;--border:#252836;--text:#e4e4e7;--dim:#71717a;
              --green:#22c55e;--yellow:#eab308;--red:#ef4444;--blue:#3b82f6;--purple:#a855f7}
        *{margin:0;padding:0;box-sizing:border-box}
        body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:var(--bg);color:var(--text);line-height:1.6}
        .header{background:var(--card);border-bottom:1px solid var(--border);padding:14px 24px;display:flex;align-items:center;gap:16px}
        .header h1{font-size:20px;font-weight:700}
        .header .badge{background:var(--blue);color:#fff;font-size:11px;padding:2px 10px;border-radius:10px;font-weight:600}
        .header nav{margin-left:auto;display:flex;gap:12px}
        .header nav a{color:var(--dim);text-decoration:none;font-size:13px;padding:6px 12px;border-radius:6px;transition:all .15s}
        .header nav a:hover,.header nav a.active{color:var(--text);background:rgba(255,255,255,.06)}
        .container{max-width:1400px;margin:0 auto;padding:24px}
        .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px;margin-bottom:20px}
        .card{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:20px}
        .card h2{font-size:13px;font-weight:600;color:var(--dim);text-transform:uppercase;letter-spacing:.5px;margin-bottom:12px}
        .full{grid-column:1/-1}
        .stat{font-size:32px;font-weight:700;margin-bottom:4px}
        .stat-label{font-size:12px;color:var(--dim)}
        .stat-green{color:var(--green)}.stat-blue{color:var(--blue)}.stat-purple{color:var(--purple)}
        table{width:100%;border-collapse:collapse;font-size:13px}
        th{text-align:left;padding:10px 12px;border-bottom:1px solid var(--border);color:var(--dim);font-size:11px;text-transform:uppercase;font-weight:500}
        td{padding:10px 12px;border-bottom:1px solid rgba(255,255,255,.04)}
        .badge-s{font-size:11px;padding:2px 8px;border-radius:8px;font-weight:600}
        .badge-active{background:rgba(34,197,94,.15);color:var(--green)}
        .badge-method{background:rgba(59,130,246,.12);color:var(--blue);font-family:monospace}
        .badge-public{background:rgba(234,179,8,.12);color:var(--yellow)}
        .badge-auth{background:rgba(168,85,247,.12);color:var(--purple)}
        a.link{color:var(--blue);text-decoration:none}a.link:hover{text-decoration:underline}
        code{background:rgba(255,255,255,.06);padding:2px 6px;border-radius:4px;font-size:12px}
        .footer{text-align:center;color:var(--dim);font-size:12px;padding:32px 0;border-top:1px solid var(--border);margin-top:32px}
    """;

    /**
     * Root redirect — GET / → /dashboard
     */
    @GetMapping(value = "/", produces = MediaType.TEXT_HTML_VALUE)
    public String root() {
        return "<html><head><meta http-equiv=\"refresh\" content=\"0;url=/dashboard\"><title>vKernel</title></head>"
             + "<body style='background:#0c0e14;color:#e4e4e7;font-family:sans-serif;padding:40px'>Redirecting to dashboard&hellip;</body></html>";
    }

    /**
     * Main dashboard — overview of vKernel system status.
     * GET /dashboard
     */
    @GetMapping(value = "/dashboard", produces = MediaType.TEXT_HTML_VALUE)
    public String dashboard() {
        List<AppRegistryEntity> apps = appLifecycle.listInstalled();
        String now = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"));

        StringBuilder appRows = new StringBuilder();
        for (var app : apps) {
            appRows.append(String.format("""
                <tr><td><strong>%s</strong></td><td>%s</td><td>%s</td>
                <td><span class="badge-s badge-active">%s</span></td></tr>
                """, app.getAppId(), app.getName(), app.getVersion(), app.getStatus()));
        }

        return """
            <!doctype html><html lang="en"><head><meta charset="UTF-8">
            <meta name="viewport" content="width=device-width,initial-scale=1">
            <title>vKernel — Platform Dashboard</title>
            <style>%s</style></head><body>
            <div class="header">
                <h1>&#9881; vKernel</h1>
                <span class="badge">Core OS</span>
                <nav>
                    <a class="active" href="/dashboard">Dashboard</a>
                    <a href="/dashboard/api">API Explorer</a>
                    <a href="/dashboard/events">Event Bus</a>
                    <a href="/dashboard/metrics">Metrics</a>
                </nav>
            </div>
            <div class="container">
                <div class="grid">
                    <div class="card">
                        <h2>System Status</h2>
                        <div class="stat stat-green">● ONLINE</div>
                        <div class="stat-label">Last checked: %s</div>
                    </div>
                    <div class="card">
                        <h2>Installed vApps</h2>
                        <div class="stat stat-blue">%d</div>
                        <div class="stat-label">Active applications</div>
                    </div>
                    <div class="card">
                        <h2>Platform Services</h2>
                        <div class="stat stat-purple">6</div>
                        <div class="stat-label">IAM · App Engine · Data · Events · gRPC · Observability</div>
                    </div>
                </div>
                <div class="grid">
                    <div class="card full">
                        <h2>Installed Applications</h2>
                        <table>
                            <thead><tr><th>App ID</th><th>Name</th><th>Version</th><th>Status</th></tr></thead>
                            <tbody>%s</tbody>
                        </table>
                    </div>
                </div>
                <div class="grid">
                    <div class="card">
                        <h2>Quick Links</h2>
                        <p style="margin-bottom:8px"><a class="link" href="/actuator/health">Health Check</a> — <code>GET /actuator/health</code></p>
                        <p style="margin-bottom:8px"><a class="link" href="/actuator/prometheus">Prometheus Metrics</a> — <code>GET /actuator/prometheus</code></p>
                        <p style="margin-bottom:8px"><a class="link" href="/actuator/info">Info</a> — <code>GET /actuator/info</code></p>
                        <p style="margin-bottom:8px"><a class="link" href="/dashboard/api">API Explorer</a> — All vKernel endpoints</p>
                    </div>
                    <div class="card">
                        <h2>Architecture</h2>
                        <p style="font-size:13px;color:var(--dim)">
                            <strong>Tier 1:</strong> Business Apps (vStrategy, vFinance, ...)<br>
                            <strong>Tier 2:</strong> vKernel Core OS (this dashboard)<br>
                            <strong>Tier 3:</strong> PostgreSQL 16 + Redis 7
                        </p>
                    </div>
                </div>
            </div>
            <div class="footer">vKernel Core OS — Corp as Code Platform &copy; Abivin 2025</div>
            </body></html>
            """.formatted(CSS, now, apps.size(), appRows.toString());
    }

    /**
     * API Explorer — lists all available REST endpoints with docs.
     * GET /dashboard/api
     */
    @GetMapping(value = "/dashboard/api", produces = MediaType.TEXT_HTML_VALUE)
    public String apiExplorer() {
        return """
            <!doctype html><html lang="en"><head><meta charset="UTF-8">
            <meta name="viewport" content="width=device-width,initial-scale=1">
            <title>vKernel — API Explorer</title>
            <style>%s</style></head><body>
            <div class="header">
                <h1>&#9881; vKernel</h1>
                <span class="badge">Core OS</span>
                <nav>
                    <a href="/dashboard">Dashboard</a>
                    <a class="active" href="/dashboard/api">API Explorer</a>
                    <a href="/dashboard/events">Event Bus</a>
                    <a href="/dashboard/metrics">Metrics</a>
                </nav>
            </div>
            <div class="container">
                <div class="card full" style="margin-bottom:20px">
                    <h2>Authentication (SyR-PLAT-01)</h2>
                    <table>
                        <thead><tr><th>Method</th><th>Endpoint</th><th>Auth</th><th>Description</th></tr></thead>
                        <tbody>
                            <tr><td><span class="badge-s badge-method">POST</span></td><td><code>/api/v1/auth/register</code></td><td><span class="badge-s badge-public">Public</span></td><td>Register new user</td></tr>
                            <tr><td><span class="badge-s badge-method">POST</span></td><td><code>/api/v1/auth/login</code></td><td><span class="badge-s badge-public">Public</span></td><td>Login → access_token + refresh_token</td></tr>
                            <tr><td><span class="badge-s badge-method">POST</span></td><td><code>/api/v1/auth/refresh</code></td><td><span class="badge-s badge-public">Public</span></td><td>Rotate refresh token</td></tr>
                            <tr><td><span class="badge-s badge-method">POST</span></td><td><code>/api/v1/auth/logout</code></td><td><span class="badge-s badge-auth">Bearer</span></td><td>Revoke all refresh tokens</td></tr>
                            <tr><td><span class="badge-s badge-method">GET</span></td><td><code>/api/v1/auth/oidc/{provider}</code></td><td><span class="badge-s badge-public">Public</span></td><td>OIDC SSO → authorization URL (google/microsoft/github)</td></tr>
                            <tr><td><span class="badge-s badge-method">GET</span></td><td><code>/api/v1/auth/oidc/{provider}/callback</code></td><td><span class="badge-s badge-public">Public</span></td><td>OIDC callback → JWT (code exchange)</td></tr>
                            <tr><td><span class="badge-s badge-method">GET</span></td><td><code>/api/v1/auth/oidc/accounts</code></td><td><span class="badge-s badge-auth">Bearer</span></td><td>List linked OIDC accounts</td></tr>
                            <tr><td><span class="badge-s badge-method">POST</span></td><td><code>/api/v1/auth/magic-link</code></td><td><span class="badge-s badge-public">Public</span></td><td>Request magic link (passwordless login)</td></tr>
                            <tr><td><span class="badge-s badge-method">GET</span></td><td><code>/api/v1/auth/magic-link/verify</code></td><td><span class="badge-s badge-public">Public</span></td><td>Verify magic link → JWT</td></tr>
                        </tbody>
                    </table>
                </div>
                <div class="card full" style="margin-bottom:20px">
                    <h2>App Engine (SyR-PLAT-00)</h2>
                    <table>
                        <thead><tr><th>Method</th><th>Endpoint</th><th>Auth</th><th>Description</th></tr></thead>
                        <tbody>
                            <tr><td><span class="badge-s badge-method">GET</span></td><td><code>/api/v1/apps</code></td><td><span class="badge-s badge-auth">Bearer</span></td><td>List installed apps</td></tr>
                            <tr><td><span class="badge-s badge-method">POST</span></td><td><code>/api/v1/apps/install</code></td><td><span class="badge-s badge-auth">Bearer</span></td><td>Install app from manifest</td></tr>
                            <tr><td><span class="badge-s badge-method">DELETE</span></td><td><code>/api/v1/apps/{appId}</code></td><td><span class="badge-s badge-auth">Bearer</span></td><td>Uninstall app</td></tr>
                            <tr><td><span class="badge-s badge-method">GET</span></td><td><code>/api/v1/apps/permissions</code></td><td><span class="badge-s badge-auth">Bearer</span></td><td>List app permissions</td></tr>
                        </tbody>
                    </table>
                </div>
                <div class="card full" style="margin-bottom:20px">
                    <h2>Data Backbone (SyR-PLAT-02)</h2>
                    <table>
                        <thead><tr><th>Method</th><th>Endpoint</th><th>Auth</th><th>Description</th></tr></thead>
                        <tbody>
                            <tr><td><span class="badge-s badge-method">GET</span></td><td><code>/api/v1/data/currencies</code></td><td><span class="badge-s badge-auth">Bearer</span></td><td>List ISO 4217 currencies</td></tr>
                            <tr><td><span class="badge-s badge-method">GET</span></td><td><code>/api/v1/data/countries</code></td><td><span class="badge-s badge-auth">Bearer</span></td><td>List ISO 3166 countries</td></tr>
                            <tr><td><span class="badge-s badge-method">GET</span></td><td><code>/api/v1/data/stakeholders</code></td><td><span class="badge-s badge-auth">Bearer</span></td><td>List stakeholders (Golden Records)</td></tr>
                            <tr><td><span class="badge-s badge-method">POST</span></td><td><code>/api/v1/data/stakeholders</code></td><td><span class="badge-s badge-auth">Bearer</span></td><td>Create stakeholder</td></tr>
                            <tr><td><span class="badge-s badge-method">PATCH</span></td><td><code>/api/v1/data/entities/{type}/{id}/extend</code></td><td><span class="badge-s badge-auth">Bearer</span></td><td>JSONB field extension</td></tr>
                        </tbody>
                    </table>
                </div>
                <div class="card full" style="margin-bottom:20px">
                    <h2>Universal Search (SyR-PLAT-02.02)</h2>
                    <table>
                        <thead><tr><th>Method</th><th>Endpoint</th><th>Auth</th><th>Description</th></tr></thead>
                        <tbody>
                            <tr><td><span class="badge-s badge-method">GET</span></td><td><code>/api/v1/search?q=...&amp;type=...&amp;limit=25</code></td><td><span class="badge-s badge-public">Public</span></td><td>Full-text search across all entities (PG tsvector + ts_rank)</td></tr>
                            <tr><td><span class="badge-s badge-method">POST</span></td><td><code>/api/v1/search/index</code></td><td><span class="badge-s badge-auth">Bearer</span></td><td>Manually index an entity for search</td></tr>
                        </tbody>
                    </table>
                </div>
                <div class="card full" style="margin-bottom:20px">
                    <h2>Event Bus (SyR-PLAT-03)</h2>
                    <table>
                        <thead><tr><th>Method</th><th>Endpoint</th><th>Auth</th><th>Description</th></tr></thead>
                        <tbody>
                            <tr><td><span class="badge-s badge-method">POST</span></td><td><code>/api/v1/events/publish</code></td><td><span class="badge-s badge-auth">Bearer</span></td><td>Publish business event</td></tr>
                            <tr><td><span class="badge-s badge-method">POST</span></td><td><code>/api/v1/events/subscribe</code></td><td><span class="badge-s badge-auth">Bearer</span></td><td>Register subscription</td></tr>
                            <tr><td><span class="badge-s badge-method">GET</span></td><td><code>/api/v1/events/subscriptions</code></td><td><span class="badge-s badge-auth">Bearer</span></td><td>List subscriptions</td></tr>
                            <tr><td><span class="badge-s badge-method">GET</span></td><td><code>/api/v1/events/log</code></td><td><span class="badge-s badge-auth">Bearer</span></td><td>Audit trail (paginated)</td></tr>
                        </tbody>
                    </table>
                </div>
                <div class="card full" style="margin-bottom:20px">
                    <h2>Observability (SyR-PLAT-05)</h2>
                    <table>
                        <thead><tr><th>Method</th><th>Endpoint</th><th>Auth</th><th>Description</th></tr></thead>
                        <tbody>
                            <tr><td><span class="badge-s badge-method">GET</span></td><td><code>/actuator/health</code></td><td><span class="badge-s badge-public">Public</span></td><td>Health check (show-details: always)</td></tr>
                            <tr><td><span class="badge-s badge-method">GET</span></td><td><code>/actuator/prometheus</code></td><td><span class="badge-s badge-public">Public</span></td><td>Prometheus metrics scrape endpoint</td></tr>
                            <tr><td><span class="badge-s badge-method">GET</span></td><td><code>/actuator/info</code></td><td><span class="badge-s badge-public">Public</span></td><td>Application info</td></tr>
                            <tr><td><span class="badge-s badge-method">GET</span></td><td><code>/actuator/metrics</code></td><td><span class="badge-s badge-public">Public</span></td><td>Micrometer metrics</td></tr>
                        </tbody>
                    </table>
                </div>
                <div class="card full">
                    <h2>Gateway Routes (vApp Proxy)</h2>
                    <table>
                        <thead><tr><th>Method</th><th>Endpoint</th><th>Auth</th><th>Description</th></tr></thead>
                        <tbody>
                            <tr><td><span class="badge-s badge-method">ALL</span></td><td><code>/api/v1/vstrategy/**</code></td><td><span class="badge-s badge-public">Proxy</span></td><td>→ vstrategy:8081 (S2P2R API)</td></tr>
                            <tr><td><span class="badge-s badge-method">ALL</span></td><td><code>/vstrategy/**</code></td><td><span class="badge-s badge-public">Proxy</span></td><td>→ vstrategy:8081 (Frontend)</td></tr>
                            <tr><td><span class="badge-s badge-method">GET</span></td><td><code>/dashboard</code></td><td><span class="badge-s badge-public">Public</span></td><td>This dashboard page</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>
            <div class="footer">vKernel Core OS — Corp as Code Platform &copy; Abivin 2025</div>
            </body></html>
            """.formatted(CSS);
    }

    /**
     * Event Bus viewer — shows recent events and subscriptions.
     * GET /dashboard/events
     */
    @GetMapping(value = "/dashboard/events", produces = MediaType.TEXT_HTML_VALUE)
    public String eventDashboard() {
        var recentEvents = eventBusService.getAuditLog(0, 20);
        StringBuilder eventRows = new StringBuilder();
        for (var ev : recentEvents) {
            eventRows.append(String.format("""
                <tr><td><code>%s</code></td><td>%s</td><td>%s</td>
                <td><span class="badge-s badge-active">%s</span></td><td>%s</td></tr>
                """, ev.getId().toString().substring(0, 8), ev.getEventType(),
                ev.getSourceApp(), ev.getStatus(), 
                ev.getCreatedAt() != null ? ev.getCreatedAt().toString() : ""));
        }

        return """
            <!doctype html><html lang="en"><head><meta charset="UTF-8">
            <meta name="viewport" content="width=device-width,initial-scale=1">
            <title>vKernel — Event Bus</title>
            <style>%s</style></head><body>
            <div class="header">
                <h1>&#9881; vKernel</h1>
                <span class="badge">Core OS</span>
                <nav>
                    <a href="/dashboard">Dashboard</a>
                    <a href="/dashboard/api">API Explorer</a>
                    <a class="active" href="/dashboard/events">Event Bus</a>
                    <a href="/dashboard/metrics">Metrics</a>
                </nav>
            </div>
            <div class="container">
                <div class="card full">
                    <h2>Recent Events (Audit Log)</h2>
                    <table>
                        <thead><tr><th>ID</th><th>Type</th><th>Source App</th><th>Status</th><th>Time</th></tr></thead>
                        <tbody>%s</tbody>
                    </table>
                    %s
                </div>
            </div>
            <div class="footer">vKernel Core OS — Corp as Code Platform &copy; Abivin 2025</div>
            </body></html>
            """.formatted(CSS, eventRows.toString(),
                recentEvents.isEmpty() ? "<p style='color:var(--dim);padding:16px;text-align:center'>No events yet. Publish events via <code>POST /api/v1/events/publish</code></p>" : "");
    }

    /**
     * Metrics viewer — embeds Prometheus metrics and links.
     * GET /dashboard/metrics
     */
    @GetMapping(value = "/dashboard/metrics", produces = MediaType.TEXT_HTML_VALUE)
    public String metricsDashboard() {
        return """
            <!doctype html><html lang="en"><head><meta charset="UTF-8">
            <meta name="viewport" content="width=device-width,initial-scale=1">
            <title>vKernel — Metrics</title>
            <style>%s</style></head><body>
            <div class="header">
                <h1>&#9881; vKernel</h1>
                <span class="badge">Core OS</span>
                <nav>
                    <a href="/dashboard">Dashboard</a>
                    <a href="/dashboard/api">API Explorer</a>
                    <a href="/dashboard/events">Event Bus</a>
                    <a class="active" href="/dashboard/metrics">Metrics</a>
                </nav>
            </div>
            <div class="container">
                <div class="grid">
                    <div class="card">
                        <h2>Prometheus</h2>
                        <p style="font-size:13px;margin-bottom:12px">Scrape endpoint for Prometheus/Grafana integration.</p>
                        <p><a class="link" href="/actuator/prometheus" target="_blank">/actuator/prometheus</a></p>
                    </div>
                    <div class="card">
                        <h2>Health</h2>
                        <p style="font-size:13px;margin-bottom:12px">Comprehensive health check with component details.</p>
                        <p><a class="link" href="/actuator/health" target="_blank">/actuator/health</a></p>
                    </div>
                    <div class="card">
                        <h2>Micrometer Metrics</h2>
                        <p style="font-size:13px;margin-bottom:12px">All registered metric names.</p>
                        <p><a class="link" href="/actuator/metrics" target="_blank">/actuator/metrics</a></p>
                    </div>
                    <div class="card">
                        <h2>Application Info</h2>
                        <p style="font-size:13px;margin-bottom:12px">Build info, environment details.</p>
                        <p><a class="link" href="/actuator/info" target="_blank">/actuator/info</a></p>
                    </div>
                </div>
                <div class="card full">
                    <h2>Live Metrics (auto-refresh every 5s)</h2>
                    <div id="metricsDisplay" style="font-family:monospace;font-size:12px;white-space:pre-wrap;max-height:500px;overflow-y:auto;background:rgba(0,0,0,.3);padding:16px;border-radius:8px">
                        Loading metrics...
                    </div>
                </div>
            </div>
            <div class="footer">vKernel Core OS — Corp as Code Platform &copy; Abivin 2025</div>
            <script>
            async function loadMetrics(){
                try{
                    const r=await fetch('/actuator/health');
                    const h=await r.json();
                    const m=await fetch('/actuator/metrics');
                    const metrics=await m.json();
                    const el=document.getElementById('metricsDisplay');
                    el.textContent='Health Status: '+h.status+'\\n\\n'
                        +'Components:\\n'+JSON.stringify(h.components||{},null,2)+'\\n\\n'
                        +'Available Metrics ('+metrics.names.length+'):\\n'+metrics.names.join('\\n');
                }catch(e){
                    document.getElementById('metricsDisplay').textContent='Error loading metrics: '+e.message;
                }
            }
            loadMetrics();
            setInterval(loadMetrics,5000);
            </script>
            </body></html>
            """.formatted(CSS);
    }
}
