package com.abivin.vkernel.g0_engine;

import com.abivin.vkernel.g3_event.EventBusService;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.server.ResponseStatusException;

import java.time.Instant;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

/**
 * App Lifecycle engine — install, uninstall, dependency check,
 * permission injection. Replaces all hardcoded stubs in AppRegistryController.
 * SyR-PLAT-00.01 + SyR-PLAT-00.02 + SyR-PLAT-01.02.
 *
 * @GovernanceID 0.3.0
 */
@Service
public class AppLifecycleService {

    private static final String KERNEL_VERSION = "0.2.0";

    private final AppRegistryEntity.Repository appRepo;
    private final PermissionEntity.Repository permRepo;
    private final EventBusService eventBus;
    private final ObjectMapper objectMapper;

    public AppLifecycleService(AppRegistryEntity.Repository appRepo,
                                PermissionEntity.Repository permRepo,
                                EventBusService eventBus,
                                ObjectMapper objectMapper) {
        this.appRepo = appRepo;
        this.permRepo = permRepo;
        this.eventBus = eventBus;
        this.objectMapper = objectMapper;
    }

    /** List all ACTIVE installed apps. */
    public List<AppRegistryEntity> listInstalled() {
        return appRepo.findByStatus("ACTIVE");
    }

    /**
     * Install an app from a manifest object.
     * Steps: validate → dep check → save registry → inject permissions → publish event.
     */
    @Transactional
    public AppRegistryEntity install(ManifestModel manifest, String installedBy) throws Exception {
        // 1. Validate manifest
        manifest.validate();
        String appId = manifest.app.id();

        // 2. Already installed?
        if (appRepo.existsByAppId(appId)) {
            throw new ResponseStatusException(HttpStatus.CONFLICT,
                    "App '" + appId + "' is already installed");
        }

        // 3. Dependency resolution
        if (manifest.dependencies != null) {
            List<String> missing = manifest.dependencies.stream()
                    .filter(dep -> !appRepo.existsByAppId(dep.app_id()))
                    .map(dep -> dep.app_id() + " (" + dep.version_range() + ")")
                    .toList();
            if (!missing.isEmpty()) {
                throw new ResponseStatusException(HttpStatus.BAD_REQUEST,
                        "MISSING_DEPENDENCY: " + String.join(", ", missing));
            }
        }

        // 4. min_kernel_version check
        if (manifest.app.min_kernel_version() != null &&
                compareVersions(KERNEL_VERSION, manifest.app.min_kernel_version()) < 0) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST,
                    "KERNEL_TOO_OLD: requires kernel " + manifest.app.min_kernel_version()
                    + ", current " + KERNEL_VERSION);
        }

        // 5. Persist to registry
        String manifestJson = objectMapper.writeValueAsString(manifest);
        String icon = (manifest.ui != null && manifest.ui.menu_icon() != null)
                ? manifest.ui.menu_icon() : "📦";
        var entity = new AppRegistryEntity(appId, manifest.app.name(),
                manifest.app.version(), icon, manifestJson, installedBy);
        entity = appRepo.save(entity);

        // 6. Inject permissions (SyR-PLAT-01.02)
        if (manifest.permissions != null) {
            for (var perm : manifest.permissions) {
                if (permRepo.existsByPermissionCode(perm.code())) continue; // idempotent
                permRepo.save(new PermissionEntity(appId, perm.code(), perm.name(),
                        perm.description(), perm.category()));
            }
        }

        // 7. Auto-subscribe to declared events (SyR-PLAT-03.02)
        if (manifest.events != null && manifest.events.subscribed() != null) {
            for (String evtType : manifest.events.subscribed()) {
                eventBus.subscribe(appId, evtType);
            }
        }

        // 8. Publish APP_INSTALLED event
        try {
            eventBus.publish("APP_INSTALLED", "1.0", "vkernel",
                    Map.of("app_id", appId, "version", manifest.app.version(),
                           "installed_by", installedBy),
                    "install_" + appId);
        } catch (Exception ignored) { /* don't fail install if event publish fails */ }

        return entity;
    }

    /**
     * Uninstall an app — deactivates registry entry + permissions.
     * Does NOT remove permissions from DB (audit trail).
     */
    @Transactional
    public void uninstall(String appId, String uninstalledBy) throws Exception {
        var entityOpt = appRepo.findByAppId(appId);
        if (entityOpt.isEmpty()) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND,
                    "App '" + appId + "' not found");
        }

        // Check no other ACTIVE app depends on this one
        List<AppRegistryEntity> activeApps = appRepo.findByStatus("ACTIVE");
        for (var app : activeApps) {
            if (app.getAppId().equals(appId)) continue;
            try {
                ManifestModel m = objectMapper.readValue(app.getManifestJson(), ManifestModel.class);
                if (m.dependencies != null && m.dependencies.stream()
                        .anyMatch(d -> d.app_id().equals(appId))) {
                    throw new ResponseStatusException(HttpStatus.CONFLICT,
                            "Cannot uninstall: '" + app.getAppId() + "' depends on this app");
                }
            } catch (ResponseStatusException e) { throw e; }
            catch (Exception ignored) {}
        }

        var entity = entityOpt.get();
        entity.setStatus("INACTIVE");
        entity.setUninstalledAt(Instant.now());
        appRepo.save(entity);

        // Deactivate permissions
        permRepo.findByAppId(appId).forEach(p -> {
            p.setActive(false);
            permRepo.save(p);
        });

        // Publish APP_UNINSTALLED event
        try {
            eventBus.publish("APP_UNINSTALLED", "1.0", "vkernel",
                    Map.of("app_id", appId, "uninstalled_by", uninstalledBy),
                    "uninstall_" + appId);
        } catch (Exception ignored) {}
    }

    /** Installed permissions for a given app. */
    public List<PermissionEntity> getPermissions(String appId) {
        return appId != null ? permRepo.findByAppId(appId) : permRepo.findByActiveTrue();
    }

    /** Simple semver comparison: -1 if a < b, 0 if equal, 1 if a > b. */
    private int compareVersions(String a, String b) {
        String[] pa = a.split("\\.");
        String[] pb = b.split("\\.");
        int len = Math.max(pa.length, pb.length);
        for (int i = 0; i < len; i++) {
            int na = i < pa.length ? Integer.parseInt(pa[i].replaceAll("[^0-9]", "")) : 0;
            int nb = i < pb.length ? Integer.parseInt(pb[i].replaceAll("[^0-9]", "")) : 0;
            if (na != nb) return Integer.compare(na, nb);
        }
        return 0;
    }
}
