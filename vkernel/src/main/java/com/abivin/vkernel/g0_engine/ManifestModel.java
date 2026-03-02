package com.abivin.vkernel.g0_engine;

import java.util.List;

/**
 * Manifest model — POJO for deserializing a vApp's manifest.json.
 * Every Business App MUST declare a valid manifest to install.
 * Structure mirrors the PRD Section 4.2 spec.
 *
 * @GovernanceID 0.2.0
 */
public class ManifestModel {

    public AppMeta app;
    public List<Dependency> dependencies;
    public List<Permission> permissions;
    public UiConfig ui;
    public ApiConfig apis;
    public EventConfig events;

    public record AppMeta(
            String id,
            String name,
            String version,
            String min_kernel_version
    ) {}

    public record Dependency(
            String app_id,
            String version_range,
            String reason
    ) {}

    public record Permission(
            String code,
            String name,
            String description,
            String category,
            List<String> default_roles
    ) {}

    public record UiConfig(
            String entry_point,
            String menu_icon,
            String menu_label,
            String route
    ) {}

    public record ApiConfig(
            List<ProvidedApi> provided,
            List<ConsumedApi> consumed
    ) {}

    public record ProvidedApi(String name, String version, String endpoint) {}
    public record ConsumedApi(String name, String source_app, String version) {}

    public record EventConfig(
            List<String> published,
            List<String> subscribed
    ) {}

    /** Validate required fields. Throws IllegalArgumentException on invalid manifest. */
    public void validate() {
        if (app == null) throw new IllegalArgumentException("Invalid manifest: missing 'app' block");
        if (isBlank(app.id())) throw new IllegalArgumentException("Invalid manifest: missing app.id");
        if (isBlank(app.name())) throw new IllegalArgumentException("Invalid manifest: missing app.name");
        if (isBlank(app.version())) throw new IllegalArgumentException("Invalid manifest: missing app.version");
        if (!app.id().matches("^[a-z0-9]+\\.[a-z0-9.]+$"))
            throw new IllegalArgumentException("Invalid manifest: app.id must follow reverse-DNS format (e.g. com.vcorp.vfinance)");
    }

    private boolean isBlank(String s) { return s == null || s.isBlank(); }
}
