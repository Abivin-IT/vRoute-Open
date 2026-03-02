package com.abivin.vkernel.g1_iam;

import jakarta.persistence.*;
import org.springframework.data.jpa.repository.JpaRepository;

import java.time.Instant;
import java.util.Optional;
import java.util.UUID;

/**
 * Magic link entity — stores hashed one-time tokens for passwordless auth.
 *
 * @GovernanceID 1.7.0
 */
@Entity
@Table(name = "kernel_magic_links")
public class MagicLinkEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(nullable = false, length = 255)
    private String email;

    @Column(name = "token_hash", nullable = false, unique = true, length = 64)
    private String tokenHash;

    @Column(name = "expires_at", nullable = false)
    private Instant expiresAt;

    @Column(nullable = false)
    private boolean used = false;

    @Column(name = "used_at")
    private Instant usedAt;

    @Column(name = "client_ip", length = 45)
    private String clientIp;

    @Column(name = "created_at", nullable = false, updatable = false)
    private Instant createdAt = Instant.now();

    public MagicLinkEntity() {}

    public MagicLinkEntity(String email, String tokenHash, Instant expiresAt, String clientIp) {
        this.email = email;
        this.tokenHash = tokenHash;
        this.expiresAt = expiresAt;
        this.clientIp = clientIp;
    }

    public UUID getId()            { return id; }
    public String getEmail()       { return email; }
    public String getTokenHash()   { return tokenHash; }
    public Instant getExpiresAt()  { return expiresAt; }
    public boolean isUsed()        { return used; }
    public Instant getUsedAt()     { return usedAt; }
    public String getClientIp()    { return clientIp; }

    public boolean isExpired() { return Instant.now().isAfter(expiresAt); }

    public boolean isValid() { return !used && !isExpired(); }

    public void markUsed() {
        this.used = true;
        this.usedAt = Instant.now();
    }

    public interface Repository extends JpaRepository<MagicLinkEntity, UUID> {
        Optional<MagicLinkEntity> findByTokenHash(String tokenHash);
    }
}
