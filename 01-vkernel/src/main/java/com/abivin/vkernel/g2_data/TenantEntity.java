package com.abivin.vkernel.g2_data;

import jakarta.persistence.*;
import java.time.Instant;
import java.util.UUID;
import org.springframework.data.jpa.repository.JpaRepository;

/**
 * Tenant — represents one organization/company instance.
 * NFR-PLAT-05: Each tenant maps to a separate logical context.
 * metadata (JSONB) allows Apps to extend tenant info dynamically.
 *
 * @GovernanceID 2.0.0
 */
@Entity
@Table(name = "kernel_tenants")
public class TenantEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(nullable = false, unique = true, length = 50)
    private String code;

    @Column(nullable = false)
    private String name;

    @Column(name = "tax_id", length = 50)
    private String taxId;

    @Column(name = "country_code", length = 2)
    private String countryCode = "VN";

    @Column(nullable = false, length = 20)
    private String status = "ACTIVE";

    @Column(columnDefinition = "jsonb default '{}'")
    private String metadata = "{}";

    @Column(name = "created_at", nullable = false, updatable = false)
    private Instant createdAt = Instant.now();

    @Column(name = "updated_at", nullable = false)
    private Instant updatedAt = Instant.now();

    public TenantEntity() {}

    public TenantEntity(String code, String name, String taxId, String countryCode) {
        this.code = code;
        this.name = name;
        this.taxId = taxId;
        this.countryCode = countryCode;
    }

    // --- Getters ---
    public UUID getId()            { return id; }
    public String getCode()        { return code; }
    public String getName()        { return name; }
    public String getTaxId()       { return taxId; }
    public String getCountryCode() { return countryCode; }
    public String getStatus()      { return status; }
    public String getMetadata()    { return metadata; }
    public Instant getCreatedAt()  { return createdAt; }
    public Instant getUpdatedAt()  { return updatedAt; }

    // --- Setters ---
    public void setId(UUID id)                  { this.id = id; }
    public void setCode(String code)            { this.code = code; }
    public void setName(String name)            { this.name = name; }
    public void setTaxId(String taxId)          { this.taxId = taxId; }
    public void setCountryCode(String cc)       { this.countryCode = cc; }
    public void setStatus(String status)        { this.status = status; }
    public void setMetadata(String metadata)    { this.metadata = metadata; this.updatedAt = Instant.now(); }
    public void setUpdatedAt(Instant t)         { this.updatedAt = t; }

    public interface Repository extends JpaRepository<TenantEntity, UUID> {
        java.util.Optional<TenantEntity> findByCode(String code);
    }
}
