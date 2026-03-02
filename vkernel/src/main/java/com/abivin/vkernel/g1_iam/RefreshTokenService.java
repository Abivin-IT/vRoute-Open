package com.abivin.vkernel.g1_iam;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.Base64;
import java.util.HexFormat;
import java.util.Optional;

/**
 * Manages opaque refresh tokens with rotation + revocation.
 * - Tokens are 256-bit secure random values, stored as SHA-256 hash.
 * - Each /refresh rotates: old token revoked → new token issued.
 * - Expiry: configurable, default 30 days.
 *
 * @GovernanceID 1.3.1
 */
@Service
public class RefreshTokenService {

    /** Refresh token TTL in days. */
    private static final long TTL_DAYS = 30;

    private final RefreshTokenEntity.Repository repo;
    private final SecureRandom secureRandom = new SecureRandom();

    public RefreshTokenService(RefreshTokenEntity.Repository repo) {
        this.repo = repo;
    }

    /**
     * Issue a new opaque refresh token for the given user.
     * Returns the plaintext token (caller must send this to client ONCE).
     */
    @Transactional
    public String issue(String userEmail, String clientIp, String userAgent) {
        String plaintext = generateToken();
        String hash = sha256Hex(plaintext);
        var entity = new RefreshTokenEntity(
                userEmail, hash,
                Instant.now().plus(TTL_DAYS, ChronoUnit.DAYS),
                clientIp, userAgent
        );
        repo.save(entity);
        return plaintext;
    }

    /**
     * Rotate a refresh token: validate → revoke → issue new.
     * Returns the new plaintext token, or empty if token is invalid.
     */
    @Transactional
    public Optional<RotationResult> rotate(String plaintextToken, String clientIp, String userAgent) {
        String hash = sha256Hex(plaintextToken);
        Optional<RefreshTokenEntity> opt = repo.findByTokenHash(hash);
        if (opt.isEmpty() || !opt.get().isValid()) {
            // Token not found or already revoked/expired — potential reuse attack
            if (opt.isPresent() && opt.get().isRevoked()) {
                // Revoke all tokens for this user (token theft protection)
                repo.revokeAllForUser(opt.get().getUserEmail(), Instant.now());
            }
            return Optional.empty();
        }
        RefreshTokenEntity old = opt.get();
        String newPlaintext = generateToken();
        String newHash = sha256Hex(newPlaintext);
        var newToken = new RefreshTokenEntity(
                old.getUserEmail(), newHash,
                Instant.now().plus(TTL_DAYS, ChronoUnit.DAYS),
                clientIp, userAgent
        );
        newToken = repo.save(newToken);
        old.revoke(newToken.getId());
        repo.save(old);
        return Optional.of(new RotationResult(old.getUserEmail(), newPlaintext));
    }

    /** Revoke all refresh tokens for a user (logout). */
    @Transactional
    public void revokeAll(String userEmail) {
        repo.revokeAllForUser(userEmail, Instant.now());
    }

    // ---- Helpers ——————————————————————————————————————————

    private String generateToken() {
        byte[] bytes = new byte[32];
        secureRandom.nextBytes(bytes);
        return Base64.getUrlEncoder().withoutPadding().encodeToString(bytes);
    }

    private String sha256Hex(String input) {
        try {
            MessageDigest md = MessageDigest.getInstance("SHA-256");
            byte[] hash = md.digest(input.getBytes(StandardCharsets.UTF_8));
            return HexFormat.of().formatHex(hash);
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException("SHA-256 not available", e);
        }
    }

    /** Result of a successful token rotation. */
    public record RotationResult(String userEmail, String newRefreshToken) {}
}
