package com.abivin.vkernel.g0_engine.models;

import jakarta.persistence.*;
import org.springframework.data.jpa.repository.JpaRepository;

import java.time.Instant;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

/**
 * DB-backed App Registry — replaces hardcoded list in AppRegistryController.
 * Stores installed apps with their manifest snapshot. (SyR-PLAT-00)
 *
 * @GovernanceID 0.1.0
 */
@Entity
@Table(name = "kernel_app_registry")
public class AppRegistryEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    /** Reverse-DNS app identifier, e.g. com.vcorp.vfinance */
    @Column(name = "app_id", nullable = false, unique = true, length = 150)
    private String appId;

    @Column(nullable = false, length = 100)
    private String name;

    @Column(nullable = false, length = 30)
    private String version;

    @Column(length = 10)
    private String icon = "📦";

    /** ACTIVE | INACTIVE | FAILED */
    @Column(nullable = false, length = 20)
    private String status = "ACTIVE";

    @Column(name = "manifest_json", columnDefinition = "jsonb")
    private String manifestJson = "{}";

    @Column(name = "installed_at", nullable = false, updatable = false)
    private Instant installedAt = Instant.now();

    @Column(name = "installed_by", length = 255)
    private String installedBy;

    @Column(name = "uninstalled_at")
    private Instant uninstalledAt;

    public AppRegistryEntity() {}

    public AppRegistryEntity(String appId, String name, String version,
                              String icon, String manifestJson, String installedBy) {
        this.appId = appId;
        this.name = name;
        this.version = version;
        this.icon = icon;
        this.manifestJson = manifestJson;
        this.installedBy = installedBy;
    }

    public UUID getId()              { return id; }
    public String getAppId()         { return appId; }
    public String getName()          { return name; }
    public String getVersion()       { return version; }
    public String getIcon()          { return icon; }
    public String getStatus()        { return status; }
    public String getManifestJson()  { return manifestJson; }
    public Instant getInstalledAt()  { return installedAt; }
    public String getInstalledBy()   { return installedBy; }
    public Instant getUninstalledAt(){ return uninstalledAt; }

    public void setStatus(String s)           { this.status = s; }
    public void setVersion(String v)          { this.version = v; }
    public void setManifestJson(String m)     { this.manifestJson = m; }
    public void setUninstalledAt(Instant t)   { this.uninstalledAt = t; }

    public interface Repository extends JpaRepository<AppRegistryEntity, UUID> {
        Optional<AppRegistryEntity> findByAppId(String appId);
        List<AppRegistryEntity> findByStatus(String status);
        boolean existsByAppId(String appId);
    }
}
