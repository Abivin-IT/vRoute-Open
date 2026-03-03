package com.abivin.vkernel.g2_data.models;

import jakarta.persistence.*;
import java.time.Instant;
import java.util.List;
import java.util.UUID;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

/**
 * Stakeholder — Golden Record for all external/internal parties.
 * Types: CUSTOMER, VENDOR, PARTNER, EMPLOYEE_REF.
 * Apps reference this via FK, never duplicate. (SyR-PLAT-02.00)
 * metadata (JSONB) allows dynamic field extension. (SyR-PLAT-02.01)
 *
 * @GovernanceID 2.0.1
 */
@Entity
@Table(name = "kernel_stakeholders",
       uniqueConstraints = @UniqueConstraint(columnNames = {"tenant_id", "code"}))
public class StakeholderEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(name = "tenant_id", nullable = false)
    private UUID tenantId;

    /** CUSTOMER | VENDOR | PARTNER | EMPLOYEE_REF */
    @Column(nullable = false, length = 30)
    private String type = "CUSTOMER";

    @Column(nullable = false, length = 100)
    private String code;

    @Column(nullable = false)
    private String name;

    private String email;

    @Column(length = 50)
    private String phone;

    private String address;

    /** JSONB — dynamic fields injected by vApps (SyR-PLAT-02.01) */
    @Column(columnDefinition = "jsonb default '{}'")
    private String metadata = "{}";

    @Column(name = "created_at", nullable = false, updatable = false)
    private Instant createdAt = Instant.now();

    @Column(name = "updated_at", nullable = false)
    private Instant updatedAt = Instant.now();

    public StakeholderEntity() {}

    public StakeholderEntity(UUID tenantId, String type, String code, String name) {
        this.tenantId = tenantId;
        this.type = type;
        this.code = code;
        this.name = name;
    }

    // --- Getters ---
    public UUID getId()            { return id; }
    public UUID getTenantId()      { return tenantId; }
    public String getType()        { return type; }
    public String getCode()        { return code; }
    public String getName()        { return name; }
    public String getEmail()       { return email; }
    public String getPhone()       { return phone; }
    public String getAddress()     { return address; }
    public String getMetadata()    { return metadata; }
    public Instant getCreatedAt()  { return createdAt; }
    public Instant getUpdatedAt()  { return updatedAt; }

    // --- Setters ---
    public void setId(UUID id)              { this.id = id; }
    public void setTenantId(UUID t)         { this.tenantId = t; }
    public void setType(String type)        { this.type = type; }
    public void setCode(String code)        { this.code = code; }
    public void setName(String name)        { this.name = name; }
    public void setEmail(String email)      { this.email = email; }
    public void setPhone(String phone)      { this.phone = phone; }
    public void setAddress(String addr)     { this.address = addr; }
    public void setMetadata(String m)       { this.metadata = m; this.updatedAt = Instant.now(); }
    public void setUpdatedAt(Instant t)     { this.updatedAt = t; }

    public interface Repository extends JpaRepository<StakeholderEntity, UUID> {
        List<StakeholderEntity> findByTenantId(UUID tenantId);
        List<StakeholderEntity> findByTenantIdAndType(UUID tenantId, String type);

        @Query(value = "SELECT * FROM kernel_stakeholders WHERE tenant_id = ?1 AND metadata @> CAST(?2 AS jsonb)",
               nativeQuery = true)
        List<StakeholderEntity> findByTenantIdAndMetadataContaining(UUID tenantId, String jsonFragment);
    }
}
