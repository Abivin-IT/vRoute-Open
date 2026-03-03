package com.abivin.vkernel.g0_engine.controllers;

import com.abivin.vkernel.g0_engine.models.AppRegistryEntity;
import com.abivin.vkernel.g0_engine.models.ManifestModel;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.List;
import java.util.Map;

/**
 * App Lifecycle REST API — DB-backed.
 * SyR-PLAT-00 (Dynamic App Engine).
 * <p>
 * GET    /api/v1/apps              → List installed (ACTIVE) apps
 * POST   /api/v1/apps/install      → Install app from manifest_url
 * DELETE /api/v1/apps/{appId}      → Uninstall app
 * GET    /api/v1/apps/permissions  → List injected permissions (optional ?app=)
 *
 * @GovernanceID 0.0.0
 */
@RestController
@RequestMapping("/api/v1/apps")
public class AppRegistryController {

    private final AppLifecycleService lifecycle;
    private final ObjectMapper objectMapper;
    private final HttpClient httpClient = HttpClient.newHttpClient();

    public AppRegistryController(AppLifecycleService lifecycle, ObjectMapper objectMapper) {
        this.lifecycle = lifecycle;
        this.objectMapper = objectMapper;
    }

    /** List all ACTIVE installed apps. */
    @GetMapping
    public ResponseEntity<?> listApps() {
        List<AppRegistryEntity> apps = lifecycle.listInstalled();
        return ResponseEntity.ok(Map.of("count", apps.size(), "apps", apps));
    }

    /**
     * Install an app.
     * Body: { "manifest_url": "https://..." }  OR  { "manifest": { ...inline... } }
     */
    @PostMapping("/install")
    public ResponseEntity<?> installApp(@RequestBody Map<String, Object> body,
                                         Authentication auth) throws Exception {
        String callerEmail = auth != null ? auth.getName() : "system";
        ManifestModel manifest;

        if (body.containsKey("manifest_url")) {
            String url = (String) body.get("manifest_url");
            var req = HttpRequest.newBuilder(URI.create(url)).GET().build();
            var resp = httpClient.send(req, HttpResponse.BodyHandlers.ofString());
            if (resp.statusCode() != 200) {
                throw new ResponseStatusException(HttpStatus.BAD_REQUEST,
                        "Could not fetch manifest from " + url + " (" + resp.statusCode() + ")");
            }
            manifest = objectMapper.readValue(resp.body(), ManifestModel.class);
        } else if (body.containsKey("manifest")) {
            String manifestJson = objectMapper.writeValueAsString(body.get("manifest"));
            manifest = objectMapper.readValue(manifestJson, ManifestModel.class);
        } else {
            return ResponseEntity.badRequest().body(Map.of(
                    "error", "VALIDATION_ERROR",
                    "message", "Provide 'manifest_url' or inline 'manifest'"));
        }

        AppRegistryEntity installed = lifecycle.install(manifest, callerEmail);
        return ResponseEntity.status(HttpStatus.CREATED).body(installed);
    }

    /** Uninstall (deactivate) an installed app. */
    @DeleteMapping("/{appId}")
    public ResponseEntity<?> uninstallApp(@PathVariable String appId,
                                           Authentication auth) throws Exception {
        String callerEmail = auth != null ? auth.getName() : "system";
        lifecycle.uninstall(appId, callerEmail);
        return ResponseEntity.ok(Map.of("uninstalled", appId));
    }

    /** List injected permissions, optionally filtered by ?app={appId}. */
    @GetMapping("/permissions")
    public ResponseEntity<?> listPermissions(@RequestParam(required = false) String app) {
        var perms = lifecycle.getPermissions(app);
        return ResponseEntity.ok(Map.of("count", perms.size(), "permissions", perms));
    }
}
