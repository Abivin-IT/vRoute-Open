package com.abivin.vkernel.g2_data.models;

import jakarta.persistence.*;
import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;

/**
 * Country — reference data for localization + compliance.
 * Linked to default currency. Used for auto-configuring tenant locale.
 *
 * @GovernanceID 2.0.3
 */
@Entity
@Table(name = "kernel_countries")
public class CountryEntity {

    /** ISO 3166-1 alpha-2, e.g. "VN", "US" */
    @Id
    @Column(length = 2)
    private String code;

    @Column(nullable = false, length = 100)
    private String name;

    @Column(name = "phone_code", length = 10)
    private String phoneCode;

    /** FK to kernel_currencies.code */
    @Column(length = 3)
    private String currency;

    @Column(name = "is_active", nullable = false)
    private boolean active = true;

    public CountryEntity() {}

    public String getCode()      { return code; }
    public String getName()      { return name; }
    public String getPhoneCode() { return phoneCode; }
    public String getCurrency()  { return currency; }
    public boolean isActive()    { return active; }

    public void setCode(String c)       { this.code = c; }
    public void setName(String n)       { this.name = n; }
    public void setPhoneCode(String p)  { this.phoneCode = p; }
    public void setCurrency(String c)   { this.currency = c; }
    public void setActive(boolean a)    { this.active = a; }

    public interface Repository extends JpaRepository<CountryEntity, String> {
        List<CountryEntity> findByActiveTrue();
    }
}
