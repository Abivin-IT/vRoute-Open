package com.abivin.vkernel.g1_iam.models;

import jakarta.persistence.*;
import java.time.Instant;
import java.util.Optional;
import java.util.UUID;
import org.springframework.data.jpa.repository.JpaRepository;

/**
 * Core user entity — stored in kernel_users table.
 * Represents a platform-level identity (not app-specific).
 *
 * @GovernanceID 1.1.0
 */
@Entity
@Table(name = "kernel_users", uniqueConstraints = @UniqueConstraint(columnNames = "email"))
public class UserEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(nullable = false, unique = true)
    private String email;

    @Column(nullable = false)
    private String password;

    /** Comma-separated roles, e.g. "CEO,ITM" */
    @Column(nullable = false)
    private String roles = "STAFF";

    @Column(name = "tenant_id")
    private String tenantId;

    @Column(name = "created_at", nullable = false, updatable = false)
    private Instant createdAt = Instant.now();

    // --- Constructors ---
    public UserEntity() {}

    public UserEntity(String email, String password, String roles, String tenantId) {
        this.email = email;
        this.password = password;
        this.roles = roles;
        this.tenantId = tenantId;
    }

    // --- Getters / Setters ---
    public UUID getId()           { return id; }
    public String getEmail()      { return email; }
    public String getPassword()   { return password; }
    public String getRoles()      { return roles; }
    public String getTenantId()   { return tenantId; }
    public Instant getCreatedAt() { return createdAt; }

    public void setId(UUID id)              { this.id = id; }
    public void setEmail(String email)      { this.email = email; }
    public void setPassword(String pw)      { this.password = pw; }
    public void setRoles(String roles)      { this.roles = roles; }
    public void setTenantId(String t)       { this.tenantId = t; }

    // --- Repository (compact: single-method interface, co-located) ---
    public interface Repository extends JpaRepository<UserEntity, UUID> {
        Optional<UserEntity> findByEmail(String email);
    }
}
