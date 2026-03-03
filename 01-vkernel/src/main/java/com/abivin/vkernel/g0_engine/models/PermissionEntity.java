package com.abivin.vkernel.g0_engine.models;

import jakarta.persistence.*;
import org.springframework.data.jpa.repository.JpaRepository;

import java.time.Instant;
import java.util.List;
import java.util.UUID;

/**
 * Permission registry — stores permissions injected by Apps at install time.
 * SyR-PLAT-01.02: Dynamic Permission Injection.
 * Pattern: [domain].[resource].[action] e.g. "finance.invoice.approve"
 *
 * @GovernanceID 1.2.0
 */
@Entity
@Table(name = "kernel_permissions")
public class PermissionEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    /** App that registered this permission */
    @Column(name = "app_id", nullable = false, length = 150)
    private String appId;

    /** Unique code across all apps: domain.resource.action */
    @Column(name = "permission_code", nullable = false, unique = true, length = 150)
    private String permissionCode;

    @Column(nullable = false, length = 150)
    private String name;

    private String description;

    @Column(length = 50)
    private String category;

    @Column(name = "is_active", nullable = false)
    private boolean active = true;

    @Column(name = "registered_at", nullable = false, updatable = false)
    private Instant registeredAt = Instant.now();

    public PermissionEntity() {}

    public PermissionEntity(String appId, String permissionCode, String name,
                             String description, String category) {
        this.appId = appId;
        this.permissionCode = permissionCode;
        this.name = name;
        this.description = description;
        this.category = category;
    }

    public UUID getId()              { return id; }
    public String getAppId()         { return appId; }
    public String getPermissionCode(){ return permissionCode; }
    public String getName()          { return name; }
    public String getDescription()   { return description; }
    public String getCategory()      { return category; }
    public boolean isActive()        { return active; }
    public Instant getRegisteredAt() { return registeredAt; }

    public void setActive(boolean a) { this.active = a; }

    public interface Repository extends JpaRepository<PermissionEntity, UUID> {
        List<PermissionEntity> findByAppId(String appId);
        List<PermissionEntity> findByActiveTrue();
        boolean existsByPermissionCode(String code);
        java.util.Optional<PermissionEntity> findByPermissionCode(String code);
    }
}
