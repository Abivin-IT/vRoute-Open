package com.abivin.vkernel.g1_iam;

import jakarta.persistence.*;
import org.springframework.data.jpa.repository.JpaRepository;

import java.time.Instant;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

/**
 * OIDC linked account — maps an external identity provider account to a kernel user.
 * Supports Google, Microsoft, GitHub SSO.
 *
 * @GovernanceID 1.6.0
 */
@Entity
@Table(name = "kernel_oidc_accounts",
       uniqueConstraints = @UniqueConstraint(columnNames = {"provider", "provider_sub"}))
public class OidcAccountEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(name = "user_email", nullable = false, length = 255)
    private String userEmail;

    /** GOOGLE | MICROSOFT | GITHUB */
    @Column(nullable = false, length = 30)
    private String provider;

    /** Subject claim from the identity provider */
    @Column(name = "provider_sub", nullable = false, length = 255)
    private String providerSub;

    @Column(name = "provider_email", length = 255)
    private String providerEmail;

    @Column(name = "display_name", length = 255)
    private String displayName;

    @Column(name = "picture_url")
    private String pictureUrl;

    @Column(name = "raw_claims", columnDefinition = "jsonb default '{}'")
    private String rawClaims = "{}";

    @Column(name = "linked_at", nullable = false, updatable = false)
    private Instant linkedAt = Instant.now();

    public OidcAccountEntity() {}

    public OidcAccountEntity(String userEmail, String provider, String providerSub,
                              String providerEmail, String displayName, String pictureUrl) {
        this.userEmail = userEmail;
        this.provider = provider;
        this.providerSub = providerSub;
        this.providerEmail = providerEmail;
        this.displayName = displayName;
        this.pictureUrl = pictureUrl;
    }

    public UUID getId()               { return id; }
    public String getUserEmail()      { return userEmail; }
    public String getProvider()       { return provider; }
    public String getProviderSub()    { return providerSub; }
    public String getProviderEmail()  { return providerEmail; }
    public String getDisplayName()    { return displayName; }
    public String getPictureUrl()     { return pictureUrl; }
    public String getRawClaims()      { return rawClaims; }
    public Instant getLinkedAt()      { return linkedAt; }

    public void setRawClaims(String c)  { this.rawClaims = c; }

    public interface Repository extends JpaRepository<OidcAccountEntity, UUID> {
        Optional<OidcAccountEntity> findByProviderAndProviderSub(String provider, String providerSub);
        List<OidcAccountEntity> findByUserEmail(String userEmail);
    }
}
