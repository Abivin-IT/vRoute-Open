package com.abivin.vkernel.g1_iam;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.net.URI;
import java.net.URLEncoder;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.util.Map;
import java.util.Optional;

/**
 * OIDC authentication controller — Google, Microsoft, GitHub SSO.
 * <p>
 * Flow:
 * 1. Client calls GET /api/v1/auth/oidc/{provider} → redirect URL to IdP
 * 2. IdP redirects user back to GET /api/v1/auth/oidc/{provider}/callback?code=...
 * 3. vKernel exchanges code for tokens with IdP, extracts user info
 * 4. Creates or links user, returns JWT access+refresh token
 *
 * @GovernanceID 1.6.1
 */
@RestController
@RequestMapping("/api/v1/auth/oidc")
public class OidcAuthController {

    private final UserEntity.Repository userRepo;
    private final OidcAccountEntity.Repository oidcRepo;
    private final JwtProvider jwtProvider;
    private final RefreshTokenService refreshTokenService;
    private final org.springframework.security.crypto.password.PasswordEncoder passwordEncoder;
    private final ObjectMapper objectMapper;
    private final HttpClient httpClient = HttpClient.newHttpClient();

    @Value("${vkernel.oidc.google.client-id:}")       private String googleClientId;
    @Value("${vkernel.oidc.google.client-secret:}")    private String googleClientSecret;
    @Value("${vkernel.oidc.microsoft.client-id:}")     private String msClientId;
    @Value("${vkernel.oidc.microsoft.client-secret:}") private String msClientSecret;
    @Value("${vkernel.oidc.github.client-id:}")        private String githubClientId;
    @Value("${vkernel.oidc.github.client-secret:}")    private String githubClientSecret;
    @Value("${vkernel.oidc.redirect-base:http://localhost:8080}") private String redirectBase;

    public OidcAuthController(UserEntity.Repository userRepo,
                               OidcAccountEntity.Repository oidcRepo,
                               JwtProvider jwtProvider,
                               RefreshTokenService refreshTokenService,
                               org.springframework.security.crypto.password.PasswordEncoder passwordEncoder,
                               ObjectMapper objectMapper) {
        this.userRepo = userRepo;
        this.oidcRepo = oidcRepo;
        this.jwtProvider = jwtProvider;
        this.refreshTokenService = refreshTokenService;
        this.passwordEncoder = passwordEncoder;
        this.objectMapper = objectMapper;
    }

    /** GET /api/v1/auth/oidc/{provider} → returns authorization URL. */
    @GetMapping("/{provider}")
    public ResponseEntity<?> initiateOidc(@PathVariable String provider) {
        String redirectUri = redirectBase + "/api/v1/auth/oidc/" + provider + "/callback";
        String authUrl = switch (provider.toLowerCase()) {
            case "google" -> "https://accounts.google.com/o/oauth2/v2/auth?"
                    + "client_id=" + enc(googleClientId)
                    + "&redirect_uri=" + enc(redirectUri)
                    + "&response_type=code&scope=openid+email+profile&access_type=offline";
            case "microsoft" -> "https://login.microsoftonline.com/common/oauth2/v2.0/authorize?"
                    + "client_id=" + enc(msClientId)
                    + "&redirect_uri=" + enc(redirectUri)
                    + "&response_type=code&scope=openid+email+profile+offline_access";
            case "github" -> "https://github.com/login/oauth/authorize?"
                    + "client_id=" + enc(githubClientId)
                    + "&redirect_uri=" + enc(redirectUri)
                    + "&scope=user:email+read:user";
            default -> null;
        };
        if (authUrl == null) {
            return ResponseEntity.badRequest().body(Map.of(
                    "error", "UNSUPPORTED_PROVIDER",
                    "message", "Supported: google, microsoft, github"));
        }
        return ResponseEntity.ok(Map.of(
                "authorization_url", authUrl,
                "provider", provider,
                "redirect_uri", redirectUri));
    }

    /** GET /api/v1/auth/oidc/{provider}/callback?code=... → exchanges code for JWT. */
    @GetMapping("/{provider}/callback")
    public ResponseEntity<?> callback(@PathVariable String provider,
                                       @RequestParam String code,
                                       HttpServletRequest request) {
        try {
            String redirectUri = redirectBase + "/api/v1/auth/oidc/" + provider + "/callback";
            JsonNode userInfo = switch (provider.toLowerCase()) {
                case "google"    -> exchangeGoogle(code, redirectUri);
                case "microsoft" -> exchangeMicrosoft(code, redirectUri);
                case "github"    -> exchangeGithub(code, redirectUri);
                default -> throw new IllegalArgumentException("Unsupported provider: " + provider);
            };

            String email  = userInfo.has("email") ? userInfo.get("email").asText() : null;
            String sub    = userInfo.has("sub") ? userInfo.get("sub").asText()
                          : userInfo.has("id") ? userInfo.get("id").asText() : null;
            String name   = userInfo.has("name") ? userInfo.get("name").asText() : email;
            String pic    = userInfo.has("picture") ? userInfo.get("picture").asText() : null;

            if (email == null || sub == null) {
                return ResponseEntity.badRequest().body(Map.of(
                        "error", "OIDC_MISSING_CLAIMS",
                        "message", "Could not extract email/sub from " + provider));
            }

            // Find or create kernel user
            var user = userRepo.findByEmail(email).orElseGet(() -> {
                var u = new UserEntity(email, passwordEncoder.encode("oidc-" + sub), "STAFF", "default");
                return userRepo.save(u);
            });

            // Link OIDC account (idempotent)
            if (oidcRepo.findByProviderAndProviderSub(provider.toUpperCase(), sub).isEmpty()) {
                var link = new OidcAccountEntity(email, provider.toUpperCase(), sub, email, name, pic);
                link.setRawClaims(userInfo.toString());
                oidcRepo.save(link);
            }

            // Issue JWT + refresh token
            String accessToken = jwtProvider.generateToken(user.getEmail(), user.getRoles(), user.getTenantId());
            String refreshToken = refreshTokenService.issue(user.getEmail(),
                    request.getRemoteAddr(), request.getHeader("User-Agent"));

            return ResponseEntity.ok(Map.of(
                    "access_token", accessToken,
                    "refresh_token", refreshToken,
                    "token_type", "Bearer",
                    "email", user.getEmail(),
                    "provider", provider,
                    "display_name", name != null ? name : ""));
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(Map.of(
                    "error", "OIDC_EXCHANGE_FAILED",
                    "message", e.getMessage()));
        }
    }

    /** Lists linked OIDC accounts for the authenticated user. */
    @GetMapping("/accounts")
    public ResponseEntity<?> listAccounts(@org.springframework.security.core.annotation.AuthenticationPrincipal String email) {
        if (email == null) return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(Map.of("error", "NOT_AUTHENTICATED"));
        var accounts = oidcRepo.findByUserEmail(email);
        return ResponseEntity.ok(Map.of("count", accounts.size(), "accounts", accounts));
    }

    // ── Provider-specific token exchange ─────────────────────

    private JsonNode exchangeGoogle(String code, String redirectUri) throws Exception {
        String body = "code=" + enc(code)
                + "&client_id=" + enc(googleClientId)
                + "&client_secret=" + enc(googleClientSecret)
                + "&redirect_uri=" + enc(redirectUri)
                + "&grant_type=authorization_code";
        var tokenResp = postForm("https://oauth2.googleapis.com/token", body);
        String accessToken = tokenResp.get("access_token").asText();
        return getJson("https://www.googleapis.com/oauth2/v3/userinfo", accessToken);
    }

    private JsonNode exchangeMicrosoft(String code, String redirectUri) throws Exception {
        String body = "code=" + enc(code)
                + "&client_id=" + enc(msClientId)
                + "&client_secret=" + enc(msClientSecret)
                + "&redirect_uri=" + enc(redirectUri)
                + "&grant_type=authorization_code"
                + "&scope=openid+email+profile";
        var tokenResp = postForm("https://login.microsoftonline.com/common/oauth2/v2.0/token", body);
        String accessToken = tokenResp.get("access_token").asText();
        return getJson("https://graph.microsoft.com/v1.0/me", accessToken);
    }

    private JsonNode exchangeGithub(String code, String redirectUri) throws Exception {
        String body = "code=" + enc(code)
                + "&client_id=" + enc(githubClientId)
                + "&client_secret=" + enc(githubClientSecret)
                + "&redirect_uri=" + enc(redirectUri);
        var req = HttpRequest.newBuilder(URI.create("https://github.com/login/oauth/access_token"))
                .header("Content-Type", "application/x-www-form-urlencoded")
                .header("Accept", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(body)).build();
        var resp = httpClient.send(req, HttpResponse.BodyHandlers.ofString());
        var tokenResp = objectMapper.readTree(resp.body());
        String accessToken = tokenResp.get("access_token").asText();
        JsonNode user = getJson("https://api.github.com/user", accessToken);
        // GitHub may not include email in /user; fetch primary email
        if (!user.has("email") || user.get("email").isNull()) {
            JsonNode emails = getJson("https://api.github.com/user/emails", accessToken);
            for (var e : emails) {
                if (e.has("primary") && e.get("primary").asBoolean()) {
                    return objectMapper.createObjectNode()
                            .put("id", user.get("id").asText())
                            .put("sub", user.get("id").asText())
                            .put("email", e.get("email").asText())
                            .put("name", user.has("name") ? user.get("name").asText() : user.get("login").asText());
                }
            }
        }
        return user;
    }

    // ── Helpers ──────────────────────────────────────────────

    private JsonNode postForm(String url, String formBody) throws Exception {
        var req = HttpRequest.newBuilder(URI.create(url))
                .header("Content-Type", "application/x-www-form-urlencoded")
                .POST(HttpRequest.BodyPublishers.ofString(formBody)).build();
        var resp = httpClient.send(req, HttpResponse.BodyHandlers.ofString());
        return objectMapper.readTree(resp.body());
    }

    private JsonNode getJson(String url, String bearerToken) throws Exception {
        var req = HttpRequest.newBuilder(URI.create(url))
                .header("Authorization", "Bearer " + bearerToken)
                .GET().build();
        var resp = httpClient.send(req, HttpResponse.BodyHandlers.ofString());
        return objectMapper.readTree(resp.body());
    }

    private String enc(String v) {
        return URLEncoder.encode(v != null ? v : "", StandardCharsets.UTF_8);
    }
}
