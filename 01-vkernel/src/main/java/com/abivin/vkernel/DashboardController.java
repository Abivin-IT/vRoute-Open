package com.abivin.vkernel;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.ClassPathResource;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.servlet.view.RedirectView;

import com.abivin.vkernel.g0_engine.AppLifecycleService;
import com.abivin.vkernel.g0_engine.AppRegistryEntity;
import com.abivin.vkernel.g0_engine.PermissionEntity;
import com.abivin.vkernel.g2_data.CurrencyEntity;
import com.abivin.vkernel.g2_data.CountryEntity;
import com.abivin.vkernel.g2_data.StakeholderEntity;
import com.abivin.vkernel.g2_data.TenantEntity;
import com.abivin.vkernel.g3_event.EventBusService;
import com.abivin.vkernel.g3_event.EventLogEntity;
import com.abivin.vkernel.g3_event.SubscriptionEntity;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

/**
 * vKernel HTML Dashboard — serves interactive HTML pages for all endpoints.
 * HTML templates live in src/main/resources/templates/dashboard/.
 * Shared CSS is served as a static file from /css/vkernel.css.
 * Accessible without authentication (same as actuator endpoints).
 *
 * @GovernanceID 0.0.0-DASH
 */
@RestController
public class DashboardController {

    @Autowired private AppLifecycleService appLifecycle;
    @Autowired private EventBusService eventBusService;
    @Autowired private PermissionEntity.Repository permissionRepo;
    @Autowired private SubscriptionEntity.Repository subscriptionRepo;
    @Autowired private StakeholderEntity.Repository stakeholderRepo;
    @Autowired private CurrencyEntity.Repository currencyRepo;
    @Autowired private CountryEntity.Repository countryRepo;
    @Autowired private TenantEntity.Repository tenantRepo;

    // ── Template loader ──────────────────────────────────────────────────────
    // Reads from src/main/resources/templates/dashboard/<name> at runtime.
    // Files are on the classpath so they are packaged inside the JAR automatically.
    private String loadTemplate(String name) {
        var resource = new ClassPathResource("templates/dashboard/" + name);
        try (var stream = resource.getInputStream()) {
            return new String(stream.readAllBytes(), StandardCharsets.UTF_8);
        } catch (IOException e) {
            throw new IllegalStateException("Cannot load dashboard template: " + name, e);
        }
    }


    /**
     * Root redirect — GET / → /shell
     */
    @GetMapping(value = "/", produces = MediaType.TEXT_HTML_VALUE)
    public String root() {
        return "<html><head><meta http-equiv=\"refresh\" content=\"0;url=/shell\"><title>vKernel</title></head>"
             + "<body style='background:#0c0e14;color:#e4e4e7;font-family:sans-serif;padding:40px'>Redirecting to shell&hellip;</body></html>";
    }

    /**
     * API root redirect — GET /api/v1 and GET /api/v1/ → /dashboard/api
     * Lets browsers visiting the API prefix see the interactive API Explorer.
     */
    @GetMapping(value = {"/api/v1", "/api/v1/"})
    public RedirectView apiRoot() {
        return new RedirectView("/dashboard/api");
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
            String shortId = app.getAppId().contains(".") ?
                app.getAppId().substring(app.getAppId().lastIndexOf('.') + 1) : app.getAppId();
            appRows.append(String.format(
                "<tr><td><strong>%s</strong></td><td>%s</td><td>%s</td>" +
                "<td><span class=\"badge-s badge-active\">%s</span></td>" +
                "<td><a class=\"link\" href=\"/shell/%s\">&#128640; Open</a></td></tr>\n",
                app.getAppId(), app.getName(), app.getVersion(), app.getStatus(), shortId));
        }

        return loadTemplate("index.html")
            .replace("{{NOW}}",       now)
            .replace("{{APP_COUNT}}", String.valueOf(apps.size()))
            .replace("{{APP_ROWS}}",  appRows.toString());
    }

    /**
     * API Explorer — lists all available REST endpoints with docs.
     * GET /dashboard/api
     */
    @GetMapping(value = "/dashboard/api", produces = MediaType.TEXT_HTML_VALUE)
    public String apiExplorer() {
        return loadTemplate("api.html");
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
            eventRows.append(String.format(
                "<tr><td><code>%s</code></td><td>%s</td><td>%s</td><td><span class=\"badge-s badge-active\">%s</span></td><td>%s</td></tr>\n",
                ev.getId().toString().substring(0, 8), ev.getEventType(),
                ev.getSourceApp(), ev.getStatus(),
                ev.getCreatedAt() != null ? ev.getCreatedAt().toString() : ""));
        }
        String emptyState = recentEvents.isEmpty()
            ? "<p style=\'color:var(--dim);padding:16px;text-align:center\'>No events yet. Publish events via <code>POST /api/v1/events/publish</code></p>"
            : "";
        return loadTemplate("events.html")
            .replace("{{EVENT_ROWS}}",  eventRows.toString())
            .replace("{{EMPTY_STATE}}", emptyState);
    }

    /**
     * Micrometer Metrics viewer — HTML wrapper for /actuator/metrics.
     * GET /dashboard/metrics
     */
    @GetMapping(value = "/dashboard/metrics", produces = MediaType.TEXT_HTML_VALUE)
    public String metricsDashboard() {
        return loadTemplate("metrics.html");
    }

    /**
     * Health dashboard — HTML wrapper for /actuator/health.
     * GET /dashboard/health
     */
    @GetMapping(value = "/dashboard/health", produces = MediaType.TEXT_HTML_VALUE)
    public String healthPage() {
        return loadTemplate("health.html");
    }

    /**
     * Prometheus metrics page — HTML wrapper for /actuator/prometheus.
     * GET /dashboard/prometheus
     */
    @GetMapping(value = "/dashboard/prometheus", produces = MediaType.TEXT_HTML_VALUE)
    public String prometheusPage() {
        return loadTemplate("prometheus.html");
    }

    /**
     * App info page — HTML wrapper for /actuator/info.
     * GET /dashboard/info
     */
    @GetMapping(value = "/dashboard/info", produces = MediaType.TEXT_HTML_VALUE)
    public String infoPage() {
        return loadTemplate("info.html");
    }

    // ═══════════════════════════════════════════════════════════════════════
    //  SYSTEM APPS — 6 vKernel System Utility Pages
    // ═══════════════════════════════════════════════════════════════════════

    /**
     * App Store — browse, install, uninstall vApps. Industry bundles.
     * GET /dashboard/appstore
     * @GovernanceID SyR-PLAT-00.01
     */
    @GetMapping(value = "/dashboard/appstore", produces = MediaType.TEXT_HTML_VALUE)
    public String appStorePage() {
        List<AppRegistryEntity> apps = appLifecycle.listInstalled();
        Set<String> installedIds = apps.stream().map(AppRegistryEntity::getAppId).collect(Collectors.toSet());

        StringBuilder appRows = new StringBuilder();
        for (var app : apps) {
            appRows.append(String.format(
                "<tr><td>%s</td><td><code>%s</code></td><td>%s</td><td>%s</td>" +
                "<td><span class=\"badge-s badge-active\">%s</span></td>" +
                "<td class=\"app-actions\">" +
                "<a class=\"btn btn-outline btn-sm\" href=\"/shell/%s\">Open</a> " +
                "<button class=\"btn btn-danger btn-sm\" onclick=\"uninstallApp('%s')\">Uninstall</button>" +
                "</td></tr>\n",
                app.getIcon(), app.getAppId(), app.getName(), app.getVersion(), app.getStatus(),
                app.getAppId().contains(".") ? app.getAppId().substring(app.getAppId().lastIndexOf('.') + 1) : app.getAppId(),
                app.getAppId()));
        }

        // Status badges for explore cards
        String[][] cardApps = {{"vstrategy", "VSTRATEGY"}, {"vfinacc", "VFINACC"}, {"vdesign", "VDESIGN"}, {"vmarketing", "VMARKETING"}};
        String html = loadTemplate("appstore.html")
            .replace("{{APP_COUNT}}", String.valueOf(apps.size()))
            .replace("{{APP_ROWS}}",  appRows.toString());

        for (String[] ca : cardApps) {
            boolean installed = installedIds.stream().anyMatch(id -> id.toLowerCase().contains(ca[0]));
            html = html.replace("{{" + ca[1] + "_STATUS}}",
                installed ? "<span class=\"badge-installed\">&#10003; Installed</span>"
                          : "<button class=\"btn btn-primary btn-sm\" onclick=\"showDepModal('" + ca[1] + "','" + ca[1] + "')\">INSTALL</button>");
        }
        return html;
    }

    /**
     * Settings / IAM — permission matrix (CRUDIEA × Roles).
     * GET /dashboard/settings
     * @GovernanceID SyR-PLAT-00.02
     */
    @GetMapping(value = "/dashboard/settings", produces = MediaType.TEXT_HTML_VALUE)
    public String settingsPage() {
        List<PermissionEntity> perms = permissionRepo.findByActiveTrue();
        List<AppRegistryEntity> apps = appLifecycle.listInstalled();
        // Roles: CEO=full, CAO=full, FAM=CRUD finance, ITM=all, BDM=CRL, HRM=CRL people
        String[] roles = {"CEO", "CAO", "FAM", "ITM", "BDM", "HRM"};

        StringBuilder rows = new StringBuilder();
        for (var p : perms) {
            rows.append("<tr>");
            rows.append(String.format("<td><strong>%s</strong><br><span style=\"font-size:10px;color:var(--dim)\">%s</span></td>",
                p.getPermissionCode(), p.getName()));
            rows.append(String.format("<td><code style=\"font-size:11px\">%s</code></td>", p.getAppId()));
            for (String role : roles) {
                // CEO/CAO/ITM always have all perms; others are read-only by default
                boolean checked = role.equals("CEO") || role.equals("CAO") || role.equals("ITM");
                rows.append(String.format("<td><input type=\"checkbox\" class=\"matrix-check\" %s disabled></td>",
                    checked ? "checked" : ""));
            }
            rows.append(String.format("<td><span class=\"badge-s badge-active\">%s</span></td>",
                p.isActive() ? "Active" : "Inactive"));
            rows.append("</tr>\n");
        }

        // Tenant name
        String tenantName = "Default";
        try {
            var tenants = tenantRepo.findAll();
            if (!tenants.isEmpty()) tenantName = tenants.get(0).getName();
        } catch (Exception ignored) {}

        return loadTemplate("settings.html")
            .replace("{{PERMISSION_ROWS}}", rows.toString())
            .replace("{{PERM_COUNT}}",      String.valueOf(perms.size()))
            .replace("{{APP_COUNT}}",       String.valueOf(apps.size()))
            .replace("{{TENANT_NAME}}",     tenantName);
    }

    /**
     * vAudit — immutable event audit log with filters.
     * GET /dashboard/audit
     * @GovernanceID SyR-PLAT-00.04
     */
    @GetMapping(value = "/dashboard/audit", produces = MediaType.TEXT_HTML_VALUE)
    public String auditPage() {
        var events = eventBusService.getAuditLog(0, 100);

        long published = events.stream().filter(e -> "DELIVERED".equals(e.getStatus()) || "PUBLISHED".equals(e.getStatus())).count();
        long failed = events.stream().filter(e -> "FAILED".equals(e.getStatus())).count();
        Set<String> sources = events.stream().map(EventLogEntity::getSourceApp).collect(Collectors.toSet());

        // Source options for filter
        StringBuilder sourceOpts = new StringBuilder();
        for (String src : sources) {
            sourceOpts.append(String.format("<option value=\"%s\">%s</option>\n", src, src));
        }

        StringBuilder rows = new StringBuilder();
        int idx = 0;
        for (var ev : events) {
            String statusClass = "FAILED".equals(ev.getStatus()) ? "badge-method" : "badge-active";
            String payloadPreview = ev.getPayload() != null ? ev.getPayload() : "{}";
            // Main row
            rows.append(String.format(
                "<tr data-source=\"%s\" data-status=\"%s\">" +
                "<td><button class=\"audit-toggle\" data-detail=\"detail-%d\" style=\"background:none;border:none;color:var(--dim);cursor:pointer;font-size:14px\">&#9656;</button></td>" +
                "<td class=\"mono\">%s</td>" +
                "<td class=\"mono\">%s</td>" +
                "<td><strong>%s</strong></td>" +
                "<td>%s</td>" +
                "<td>%s</td>" +
                "<td><span class=\"badge-s %s\">%s</span></td>" +
                "<td>%s</td>" +
                "</tr>\n",
                ev.getSourceApp(), ev.getStatus(), idx,
                ev.getCreatedAt() != null ? ev.getCreatedAt().toString() : "",
                ev.getCorrelationId() != null ? ev.getCorrelationId().substring(0, Math.min(8, ev.getCorrelationId().length())) : "—",
                ev.getEventType(), ev.getEventVersion() != null ? ev.getEventVersion() : "1.0",
                ev.getSourceApp(), statusClass, ev.getStatus(),
                ev.getSubscribers() != null ? ev.getSubscribers() : "[]"));
            // Detail row (hidden by default)
            rows.append(String.format(
                "<tr class=\"audit-detail\" id=\"detail-%d\"><td colspan=\"8\">" +
                "<div style=\"display:grid;grid-template-columns:1fr 1fr;gap:12px\">" +
                "<div><strong style=\"font-size:11px;color:var(--dim)\">Full Correlation ID</strong><div class=\"mono\" style=\"margin-top:4px\">%s</div></div>" +
                "<div><strong style=\"font-size:11px;color:var(--dim)\">Event ID</strong><div class=\"mono\" style=\"margin-top:4px\">%s</div></div>" +
                "</div>" +
                "<div style=\"margin-top:12px\"><strong style=\"font-size:11px;color:var(--dim)\">Payload (JSONB)</strong>" +
                "<div class=\"payload-block\" style=\"margin-top:6px\">%s</div></div>" +
                "</td></tr>\n",
                idx,
                ev.getCorrelationId() != null ? ev.getCorrelationId() : "—",
                ev.getId().toString(),
                payloadPreview));
            idx++;
        }

        String emptyState = events.isEmpty()
            ? "<div class=\"card\" style=\"text-align:center;padding:48px 20px\"><div style=\"font-size:48px;margin-bottom:12px\">&#128220;</div>"
              + "<h2 style=\"font-size:16px;color:var(--text);text-transform:none;letter-spacing:0\">No Audit Events Yet</h2>"
              + "<p style=\"color:var(--dim);font-size:13px;margin-top:8px\">Events will appear here after publishing via <code>POST /api/v1/events/publish</code></p></div>"
            : "";

        return loadTemplate("audit.html")
            .replace("{{TOTAL_EVENTS}}",     String.valueOf(events.size()))
            .replace("{{PUBLISHED_COUNT}}",  String.valueOf(published))
            .replace("{{FAILED_COUNT}}",     String.valueOf(failed))
            .replace("{{SOURCE_APPS_COUNT}}", String.valueOf(sources.size()))
            .replace("{{SOURCE_OPTIONS}}",   sourceOpts.toString())
            .replace("{{EVENT_ROWS}}",       rows.toString())
            .replace("{{EMPTY_STATE}}",      emptyState);
    }

    /**
     * vData / MDM — golden records browser (stakeholders, currencies, countries).
     * GET /dashboard/data
     * @GovernanceID SyR-PLAT-00.03
     */
    @GetMapping(value = "/dashboard/data", produces = MediaType.TEXT_HTML_VALUE)
    public String dataPage() {
        var stakeholders = stakeholderRepo.findAll();
        var currencies   = currencyRepo.findAll();
        var countries    = countryRepo.findAll();
        int totalRecords = stakeholders.size() + currencies.size() + countries.size();

        // Stakeholder rows
        StringBuilder sRows = new StringBuilder();
        for (var s : stakeholders) {
            sRows.append(String.format(
                "<tr><td class=\"mono\">%s</td><td><strong>%s</strong></td><td>%s</td>" +
                "<td>%s</td><td>%s</td><td><span class=\"badge-s badge-active\">Active</span></td></tr>\n",
                s.getId().toString().substring(0, 8), s.getName(), s.getType(),
                s.getEmail() != null ? s.getEmail() : "—",
                s.getAddress() != null ? s.getAddress() : "—"));
        }

        // Currency rows
        StringBuilder cRows = new StringBuilder();
        for (var c : currencies) {
            cRows.append(String.format(
                "<tr><td><strong>%s</strong></td><td>%s</td><td>%s</td><td>%s</td><td>%d</td></tr>\n",
                c.getCode(), c.getCode(), c.getName(), c.getSymbol(), c.getDecimals()));
        }

        // Country rows
        StringBuilder coRows = new StringBuilder();
        for (var co : countries) {
            coRows.append(String.format(
                "<tr><td><strong>%s</strong></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>\n",
                co.getCode(), co.getCode(), co.getName(),
                "—", // region not in entity
                co.getPhoneCode() != null ? co.getPhoneCode() : "—"));
        }

        String emptyState = totalRecords == 0
            ? "<div class=\"card\" style=\"text-align:center;padding:48px 20px\"><div style=\"font-size:48px;margin-bottom:12px\">&#128451;</div>"
              + "<h2 style=\"font-size:16px;color:var(--text);text-transform:none;letter-spacing:0\">No Master Data Yet</h2>"
              + "<p style=\"color:var(--dim);font-size:13px;margin-top:8px\">Seed data via <code>POST /api/v1/data/stakeholders</code></p></div>"
            : "";

        return loadTemplate("data.html")
            .replace("{{TOTAL_RECORDS}}",     String.valueOf(totalRecords))
            .replace("{{STAKEHOLDER_COUNT}}", String.valueOf(stakeholders.size()))
            .replace("{{CURRENCY_COUNT}}",    String.valueOf(currencies.size()))
            .replace("{{COUNTRY_COUNT}}",     String.valueOf(countries.size()))
            .replace("{{STAKEHOLDER_ROWS}}",  sRows.toString())
            .replace("{{CURRENCY_ROWS}}",     cRows.toString())
            .replace("{{COUNTRY_ROWS}}",      coRows.toString())
            .replace("{{EMPTY_STATE}}",       emptyState);
    }

    /**
     * vFlow / Automation — event subscription wiring and run history.
     * GET /dashboard/automation
     * @GovernanceID SyR-PLAT-00.03
     */
    @GetMapping(value = "/dashboard/automation", produces = MediaType.TEXT_HTML_VALUE)
    public String automationPage() {
        var allSubs = subscriptionRepo.findAll();
        var recentEvents = eventBusService.getAuditLog(0, 20);

        long activeSubs = allSubs.stream().filter(s -> "ACTIVE".equals(s.getStatus())).count();
        Set<String> eventTypes = allSubs.stream().map(SubscriptionEntity::getEventType).collect(Collectors.toSet());
        Set<String> subscriberApps = allSubs.stream().map(SubscriptionEntity::getSubscriberApp).collect(Collectors.toSet());

        // Flow diagram (visual representation of subscriptions)
        StringBuilder flowDiagram = new StringBuilder();
        if (allSubs.isEmpty()) {
            flowDiagram.append("<div style=\"text-align:center;padding:60px 20px;color:var(--dim)\">");
            flowDiagram.append("<div style=\"font-size:48px;margin-bottom:12px\">&#9889;</div>");
            flowDiagram.append("<p>No active subscriptions. Wire events via <code>POST /api/v1/events/subscribe</code></p></div>");
        } else {
            flowDiagram.append("<div style=\"display:flex;flex-wrap:wrap;align-items:center;gap:4px\">");
            for (var sub : allSubs) {
                flowDiagram.append(String.format(
                    "<div class=\"flow-node trigger\">&#128228; %s</div>" +
                    "<div class=\"flow-arrow\">&#8594;</div>" +
                    "<div class=\"flow-node filter\">&#9881; %s</div>" +
                    "<div class=\"flow-arrow\">&#8594;</div>" +
                    "<div class=\"flow-node action\">&#127919; %s</div>" +
                    "<div style=\"width:100%%;height:8px\"></div>",
                    sub.getEventType(), sub.getStatus(), sub.getSubscriberApp()));
            }
            flowDiagram.append("</div>");
        }

        // Subscription rows
        StringBuilder subRows = new StringBuilder();
        for (var sub : allSubs) {
            String dotClass = "ACTIVE".equals(sub.getStatus()) ? "active" : "inactive";
            subRows.append(String.format(
                "<tr><td><span class=\"status-dot %s\"></span>%s</td><td><strong>%s</strong></td>" +
                "<td><code>%s</code></td><td class=\"mono\">%s</td><td class=\"mono\">%s</td></tr>\n",
                dotClass, sub.getStatus(), sub.getSubscriberApp(), sub.getEventType(),
                sub.getCreatedAt() != null ? sub.getCreatedAt().toString() : "—",
                sub.getId().toString().substring(0, 8)));
        }

        // Run history (recent events)
        StringBuilder runRows = new StringBuilder();
        if (recentEvents.isEmpty()) {
            runRows.append("<div style=\"text-align:center;padding:32px;color:var(--dim);font-size:13px\">No event processing history yet.</div>");
        } else {
            for (var ev : recentEvents) {
                String statusColor = "FAILED".equals(ev.getStatus()) ? "color:var(--red)" : "color:var(--green)";
                runRows.append(String.format(
                    "<div class=\"run-entry\"><span class=\"run-time\">%s</span>" +
                    "<span class=\"run-event\">%s → %s</span>" +
                    "<span class=\"run-status\" style=\"%s\">%s</span></div>\n",
                    ev.getCreatedAt() != null ? ev.getCreatedAt().toString() : "",
                    ev.getSourceApp(), ev.getEventType(), statusColor, ev.getStatus()));
            }
        }

        String emptyState = allSubs.isEmpty()
            ? "" // Already handled in flow diagram
            : "";

        return loadTemplate("automation.html")
            .replace("{{ACTIVE_SUBS}}",       String.valueOf(activeSubs))
            .replace("{{EVENT_TYPES}}",       String.valueOf(eventTypes.size()))
            .replace("{{SUBSCRIBER_APPS}}",   String.valueOf(subscriberApps.size()))
            .replace("{{EVENTS_24H}}",        String.valueOf(recentEvents.size()))
            .replace("{{FLOW_DIAGRAM}}",      flowDiagram.toString())
            .replace("{{SUBSCRIPTION_ROWS}}", subRows.toString())
            .replace("{{RUN_HISTORY_ROWS}}",  runRows.toString())
            .replace("{{EMPTY_STATE}}",       emptyState);
    }

    /**
     * vMonitor — health dashboard, JVM metrics, Prometheus.
     * GET /dashboard/monitor
     * @GovernanceID SyR-PLAT-00.04
     */
    @GetMapping(value = "/dashboard/monitor", produces = MediaType.TEXT_HTML_VALUE)
    public String monitorPage() {
        List<AppRegistryEntity> apps = appLifecycle.listInstalled();

        StringBuilder appHealthRows = new StringBuilder();
        for (var app : apps) {
            String statusBadge = "ACTIVE".equals(app.getStatus())
                ? "<span class=\"badge-s badge-active\">&#9679; Healthy</span>"
                : "<span class=\"badge-s badge-method\">&#9679; Degraded</span>";
            String healthCheck = "ACTIVE".equals(app.getStatus()) ? "&#9989; Pass" : "&#10060; Fail";
            appHealthRows.append(String.format(
                "<tr><td>%s</td><td><strong>%s</strong><br><span class=\"mono\">%s</span></td>" +
                "<td>%s</td><td>%s</td><td>%s</td><td class=\"mono\">—</td></tr>\n",
                app.getIcon(), app.getName(), app.getAppId(),
                app.getVersion(), statusBadge, healthCheck));
        }

        return loadTemplate("monitor.html")
            .replace("{{APP_COUNT}}",       String.valueOf(apps.size()))
            .replace("{{APP_HEALTH_ROWS}}", appHealthRows.toString());
    }
}
