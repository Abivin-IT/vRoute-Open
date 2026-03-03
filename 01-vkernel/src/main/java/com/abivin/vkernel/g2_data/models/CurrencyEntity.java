package com.abivin.vkernel.g2_data.models;

import jakarta.persistence.*;
import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;

/**
 * Currency — reference data for monetary operations.
 * Golden Record: all Apps reference this, never create own currency tables.
 *
 * @GovernanceID 2.0.2
 */
@Entity
@Table(name = "kernel_currencies")
public class CurrencyEntity {

    /** ISO 4217 code, e.g. "VND", "USD" */
    @Id
    @Column(length = 3)
    private String code;

    @Column(nullable = false, length = 100)
    private String name;

    @Column(nullable = false, length = 10)
    private String symbol;

    @Column(nullable = false)
    private short decimals = 2;

    @Column(name = "is_active", nullable = false)
    private boolean active = true;

    public CurrencyEntity() {}

    public CurrencyEntity(String code, String name, String symbol, short decimals) {
        this.code = code;
        this.name = name;
        this.symbol = symbol;
        this.decimals = decimals;
    }

    public String getCode()     { return code; }
    public String getName()     { return name; }
    public String getSymbol()   { return symbol; }
    public short getDecimals()  { return decimals; }
    public boolean isActive()   { return active; }

    public void setCode(String c)        { this.code = c; }
    public void setName(String n)        { this.name = n; }
    public void setSymbol(String s)      { this.symbol = s; }
    public void setDecimals(short d)     { this.decimals = d; }
    public void setActive(boolean a)     { this.active = a; }

    public interface Repository extends JpaRepository<CurrencyEntity, String> {
        List<CurrencyEntity> findByActiveTrue();
    }
}
