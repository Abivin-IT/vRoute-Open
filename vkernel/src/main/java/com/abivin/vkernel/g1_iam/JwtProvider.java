package com.abivin.vkernel.g1_iam;

import io.jsonwebtoken.*;
import io.jsonwebtoken.security.Keys;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import javax.crypto.SecretKey;
import java.nio.charset.StandardCharsets;
import java.util.Date;

/**
 * JWT token generation and validation.
 * Reads secret + expiration from application.yml / env vars.
 *
 * @GovernanceID 1.0.2
 */
@Component
public class JwtProvider {

    private final SecretKey key;
    private final long expirationMs;

    public JwtProvider(
            @Value("${vkernel.jwt.secret}") String secret,
            @Value("${vkernel.jwt.expiration-ms:86400000}") long expirationMs) {
        this.key = Keys.hmacShaKeyFor(secret.getBytes(StandardCharsets.UTF_8));
        this.expirationMs = expirationMs;
    }

    public String generateToken(String email, String roles) {
        return generateToken(email, roles, TenantContext.DEFAULT_TENANT);
    }

    public String generateToken(String email, String roles, String tenantId) {
        Date now = new Date();
        return Jwts.builder()
                .subject(email)
                .claim("roles", roles)
                .claim("tenant_id", tenantId != null ? tenantId : TenantContext.DEFAULT_TENANT)
                .issuedAt(now)
                .expiration(new Date(now.getTime() + expirationMs))
                .signWith(key)
                .compact();
    }

    public String getEmailFromToken(String token) {
        return parseClaims(token).getPayload().getSubject();
    }

    public String getRolesFromToken(String token) {
        return parseClaims(token).getPayload().get("roles", String.class);
    }

    public String getTenantFromToken(String token) {
        String t = parseClaims(token).getPayload().get("tenant_id", String.class);
        return t != null ? t : TenantContext.DEFAULT_TENANT;
    }

    public boolean validateToken(String token) {
        try {
            parseClaims(token);
            return true;
        } catch (JwtException | IllegalArgumentException e) {
            return false;
        }
    }

    private Jws<Claims> parseClaims(String token) {
        return Jwts.parser().verifyWith(key).build().parseSignedClaims(token);
    }
}
