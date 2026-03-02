package com.abivin.vkernel;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.ClassPathResource;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.servlet.view.RedirectView;

import com.abivin.vkernel.g0_engine.AppLifecycleService;
import com.abivin.vkernel.g0_engine.AppRegistryEntity;
import com.abivin.vkernel.g3_event.EventBusService;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;

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
     * Root redirect — GET / → /dashboard
     */
    @GetMapping(value = "/", produces = MediaType.TEXT_HTML_VALUE)
    public String root() {
        return "<html><head><meta http-equiv=\"refresh\" content=\"0;url=/dashboard\"><title>vKernel</title></head>"
             + "<body style='background:#0c0e14;color:#e4e4e7;font-family:sans-serif;padding:40px'>Redirecting to dashboard&hellip;</body></html>";
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
}
