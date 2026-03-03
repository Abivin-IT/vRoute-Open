package com.abivin.vkernel.g1_iam.controllers;

import com.abivin.vkernel.g1_iam.models.UserEntity;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

/**
 * Authentication endpoints — login + register + refresh + logout.
 * Public (permitAll in SecurityConfig).
 *
 * @GovernanceID 1.0.1
 */
@RestController
@RequestMapping("/api/v1/auth")
public class AuthController {

    private final UserEntity.Repository userRepo;
    private final PasswordEncoder passwordEncoder;
    private final JwtProvider jwtProvider;
    private final RefreshTokenService refreshTokenService;

    public AuthController(UserEntity.Repository userRepo,
                          PasswordEncoder passwordEncoder,
                          JwtProvider jwtProvider,
                          RefreshTokenService refreshTokenService) {
        this.userRepo = userRepo;
        this.passwordEncoder = passwordEncoder;
        this.jwtProvider = jwtProvider;
        this.refreshTokenService = refreshTokenService;
    }

    /**
     * Register a new platform user.
     * POST /api/v1/auth/register
     * Body: {"email": "...", "password": "...", "tenantId": "..."}
     */
    @PostMapping("/register")
    public ResponseEntity<?> register(@RequestBody Map<String, String> body) {
        String email = body.get("email");
        String password = body.get("password");
        String tenantId = body.getOrDefault("tenantId", "default");

        if (email == null || password == null) {
            return ResponseEntity.badRequest().body(Map.of(
                    "error", "VALIDATION_ERROR",
                    "message", "email and password are required"
            ));
        }

        // NFR-SAFE: guard against oversized inputs before reaching the DB
        if (email.length() > 255) {
            return ResponseEntity.badRequest().body(Map.of(
                    "error", "VALIDATION_ERROR",
                    "message", "Email exceeds maximum allowed length of 255 characters"
            ));
        }

        if (userRepo.findByEmail(email).isPresent()) {
            return ResponseEntity.status(HttpStatus.CONFLICT).body(Map.of(
                    "error", "USER_EXISTS",
                    "message", "Email already registered"
            ));
        }

        var user = new UserEntity(email, passwordEncoder.encode(password), "STAFF", tenantId);
        userRepo.save(user);

        String token = jwtProvider.generateToken(user.getEmail(), user.getRoles());
        return ResponseEntity.status(HttpStatus.CREATED).body(Map.of(
                "token", token,
                "email", user.getEmail(),
                "roles", user.getRoles()
        ));
    }

    /**
     * Login with email + password → JWT access token + opaque refresh token.
     * POST /api/v1/auth/login
     * Body: {"email": "...", "password": "..."}
     */
    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestBody Map<String, String> body,
                                   HttpServletRequest request) {
        String email    = body.get("email");
        String password = body.get("password");

        var userOpt = userRepo.findByEmail(email);
        if (userOpt.isEmpty() || !passwordEncoder.matches(password, userOpt.get().getPassword())) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(Map.of(
                    "error", "AUTH_FAILED",
                    "message", "Invalid email or password"
            ));
        }

        var user = userOpt.get();
        String accessToken = jwtProvider.generateToken(
                user.getEmail(), user.getRoles(), user.getTenantId()
        );
        String refreshToken = refreshTokenService.issue(
                user.getEmail(),
                request.getRemoteAddr(),
                request.getHeader("User-Agent")
        );

        return ResponseEntity.ok(Map.of(
                "access_token", accessToken,
                "refresh_token", refreshToken,
                "token_type", "Bearer",
                "email", user.getEmail(),
                "roles", user.getRoles()
        ));
    }

    /**
     * Refresh access token using an opaque refresh token (rotation).
     * POST /api/v1/auth/refresh
     * Body: {"refresh_token": "..."}
     */
    @PostMapping("/refresh")
    public ResponseEntity<?> refresh(@RequestBody Map<String, String> body,
                                     HttpServletRequest request) {
        String oldRefreshToken = body.get("refresh_token");
        if (oldRefreshToken == null || oldRefreshToken.isBlank()) {
            return ResponseEntity.badRequest().body(Map.of(
                    "error", "MISSING_TOKEN",
                    "message", "refresh_token is required"
            ));
        }

        var result = refreshTokenService.rotate(
                oldRefreshToken,
                request.getRemoteAddr(),
                request.getHeader("User-Agent")
        );

        if (result.isEmpty()) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(Map.of(
                    "error", "TOKEN_INVALID",
                    "message", "Refresh token is expired, revoked, or invalid"
            ));
        }

        var rotation = result.get();
        var userOpt  = userRepo.findByEmail(rotation.userEmail());
        if (userOpt.isEmpty()) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(Map.of(
                    "error", "USER_NOT_FOUND", "message", "User not found"
            ));
        }

        String newAccessToken = jwtProvider.generateToken(
                userOpt.get().getEmail(), userOpt.get().getRoles()
        );

        return ResponseEntity.ok(Map.of(
                "access_token", newAccessToken,
                "refresh_token", rotation.newRefreshToken(),
                "token_type", "Bearer"
        ));
    }

    /**
     * Logout — revoke all refresh tokens for the current user.
     * POST /api/v1/auth/logout
     * Requires: valid JWT in Authorization header.
     */
    @PostMapping("/logout")
    public ResponseEntity<?> logout(@AuthenticationPrincipal String email) {
        if (email == null) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(Map.of(
                    "error", "NOT_AUTHENTICATED", "message", "No active session"
            ));
        }
        refreshTokenService.revokeAll(email);
        return ResponseEntity.ok(Map.of("message", "Logged out successfully"));
    }
}
