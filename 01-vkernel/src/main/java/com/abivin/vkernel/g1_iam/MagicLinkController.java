package com.abivin.vkernel.g1_iam;

import jakarta.servlet.http.HttpServletRequest;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.*;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.SecureRandom;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.Base64;
import java.util.HexFormat;
import java.util.Map;

/**
 * Passwordless authentication via magic link.
 * <p>
 * Flow:
 * 1. POST /api/v1/auth/magic-link  body: {"email":"user@example.com"}
 *    → Creates OTP token, returns the link (in production: sends email).
 * 2. GET  /api/v1/auth/magic-link/verify?token=...
 *    → Verifies token, creates account if new, returns JWT.
 *
 * @GovernanceID 1.7.1
 */
@RestController
@RequestMapping("/api/v1/auth/magic-link")
public class MagicLinkController {

    private static final long TTL_MINUTES = 15;

    private final MagicLinkEntity.Repository magicRepo;
    private final UserEntity.Repository userRepo;
    private final PasswordEncoder passwordEncoder;
    private final JwtProvider jwtProvider;
    private final RefreshTokenService refreshTokenService;
    private final SecureRandom secureRandom = new SecureRandom();

    public MagicLinkController(MagicLinkEntity.Repository magicRepo,
                                UserEntity.Repository userRepo,
                                PasswordEncoder passwordEncoder,
                                JwtProvider jwtProvider,
                                RefreshTokenService refreshTokenService) {
        this.magicRepo = magicRepo;
        this.userRepo = userRepo;
        this.passwordEncoder = passwordEncoder;
        this.jwtProvider = jwtProvider;
        this.refreshTokenService = refreshTokenService;
    }

    /**
     * Request a magic link for passwordless login.
     * POST /api/v1/auth/magic-link
     * Body: {"email": "user@example.com"}
     *
     * In production, this would send an email. For dev, we return the link directly.
     */
    @PostMapping
    public ResponseEntity<?> requestMagicLink(@RequestBody Map<String, String> body,
                                               HttpServletRequest request) {
        String email = body.get("email");
        if (email == null || email.isBlank()) {
            return ResponseEntity.badRequest().body(Map.of(
                    "error", "VALIDATION_ERROR",
                    "message", "email is required"));
        }

        // Generate secure token
        byte[] bytes = new byte[32];
        secureRandom.nextBytes(bytes);
        String token = Base64.getUrlEncoder().withoutPadding().encodeToString(bytes);
        String hash = sha256Hex(token);

        var entity = new MagicLinkEntity(
                email, hash,
                Instant.now().plus(TTL_MINUTES, ChronoUnit.MINUTES),
                request.getRemoteAddr());
        magicRepo.save(entity);

        // Dev mode: return the link directly. Production would send via email.
        String verifyUrl = "/api/v1/auth/magic-link/verify?token=" + token;

        return ResponseEntity.ok(Map.of(
                "message", "Magic link generated (dev mode — in production this is emailed)",
                "magic_link", verifyUrl,
                "email", email,
                "expires_in_minutes", TTL_MINUTES));
    }

    /**
     * Verify a magic link token and issue JWT.
     * GET /api/v1/auth/magic-link/verify?token=...
     */
    @GetMapping("/verify")
    public ResponseEntity<?> verify(@RequestParam String token,
                                     HttpServletRequest request) {
        String hash = sha256Hex(token);
        var opt = magicRepo.findByTokenHash(hash);

        if (opt.isEmpty() || !opt.get().isValid()) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(Map.of(
                    "error", "INVALID_MAGIC_LINK",
                    "message", "Magic link is expired, used, or invalid"));
        }

        var magicLink = opt.get();
        magicLink.markUsed();
        magicRepo.save(magicLink);

        String email = magicLink.getEmail();

        // Find or create user
        var user = userRepo.findByEmail(email).orElseGet(() -> {
            var u = new UserEntity(email, passwordEncoder.encode("magic-" + hash.substring(0, 8)),
                    "STAFF", "default");
            return userRepo.save(u);
        });

        String accessToken = jwtProvider.generateToken(user.getEmail(), user.getRoles(), user.getTenantId());
        String refreshToken = refreshTokenService.issue(user.getEmail(),
                request.getRemoteAddr(), request.getHeader("User-Agent"));

        return ResponseEntity.ok(Map.of(
                "access_token", accessToken,
                "refresh_token", refreshToken,
                "token_type", "Bearer",
                "email", user.getEmail(),
                "auth_method", "magic_link"));
    }

    private String sha256Hex(String input) {
        try {
            var md = MessageDigest.getInstance("SHA-256");
            byte[] h = md.digest(input.getBytes(StandardCharsets.UTF_8));
            return HexFormat.of().formatHex(h);
        } catch (Exception e) {
            throw new RuntimeException("SHA-256 not available", e);
        }
    }
}
