package com.abivin.vkernel.g1_iam;

import jakarta.persistence.*;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.time.Instant;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

/**
 * DB-backed opaque refresh token.
 * Stores SHA-256 hash of the actual token value (never the plaintext).
 * Rotation: each /refresh call revokes old token and issues a new one.
 *
 * @GovernanceID 1.3.0
 */
@Entity
@Table(name = "kernel_refresh_tokens")
public class RefreshTokenEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(name = "user_email", nullable = false, length = 255)
    private String userEmail;

    /** SHA-256 hex digest of the actual opaque token. Never store plaintext. */
    @Column(name = "token_hash", nullable = false, unique = true, length = 64)
    private String tokenHash;

    @Column(name = "issued_at", nullable = false, updatable = false)
    private Instant issuedAt = Instant.now();

    @Column(name = "expires_at", nullable = false)
    private Instant expiresAt;

    @Column(nullable = false)
    private boolean revoked = false;

    @Column(name = "revoked_at")
    private Instant revokedAt;

    @Column(name = "replaced_by")
    private UUID replacedBy;

    @Column(name = "client_ip", length = 45)
    private String clientIp;

    @Column(name = "user_agent", length = 500)
    private String userAgent;

    public RefreshTokenEntity() {}

    public RefreshTokenEntity(String userEmail, String tokenHash,
                               Instant expiresAt, String clientIp, String userAgent) {
        this.userEmail = userEmail;
        this.tokenHash = tokenHash;
        this.expiresAt = expiresAt;
        this.clientIp = clientIp;
        this.userAgent = userAgent;
    }

    public UUID    getId()         { return id; }
    public String  getUserEmail()  { return userEmail; }
    public String  getTokenHash()  { return tokenHash; }
    public Instant getIssuedAt()   { return issuedAt; }
    public Instant getExpiresAt()  { return expiresAt; }
    public boolean isRevoked()     { return revoked; }
    public Instant getRevokedAt()  { return revokedAt; }
    public UUID    getReplacedBy() { return replacedBy; }
    public String  getClientIp()   { return clientIp; }
    public String  getUserAgent()  { return userAgent; }

    public void revoke(UUID replacedById) {
        this.revoked = true;
        this.revokedAt = Instant.now();
        this.replacedBy = replacedById;
    }

    public boolean isExpired() {
        return Instant.now().isAfter(expiresAt);
    }

    public boolean isValid() {
        return !revoked && !isExpired();
    }

    public interface Repository extends JpaRepository<RefreshTokenEntity, UUID> {
        Optional<RefreshTokenEntity> findByTokenHash(String tokenHash);
        List<RefreshTokenEntity> findByUserEmailAndRevokedFalse(String email);

        @Modifying
        @Query("UPDATE RefreshTokenEntity t SET t.revoked = true, t.revokedAt = :now " +
               "WHERE t.userEmail = :email AND t.revoked = false")
        int revokeAllForUser(@Param("email") String email, @Param("now") Instant now);
    }
}
