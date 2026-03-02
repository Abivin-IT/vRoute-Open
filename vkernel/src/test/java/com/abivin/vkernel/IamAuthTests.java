package com.abivin.vkernel;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;

import static org.hamcrest.Matchers.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

/**
 * Comprehensive functional tests for vKernel — SyR-PLAT-01 (IAM).
 * Covers: register, login, JWT auth, refresh tokens, logout.
 * Test IDs mapped to vKernel PRD requirements.
 *
 * @GovernanceID TEST-SyR-PLAT-01
 */
@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
class IamAuthTests {

    @Autowired private MockMvc mvc;
    @Autowired private ObjectMapper mapper;

    static String accessToken;
    static String refreshToken;

    // ── SyR-PLAT-01.1: User Registration ─────────────────────

    @Test @Order(1)
    @DisplayName("SyR-PLAT-01.1 — Register new user → 201 + token")
    void test_01_register() throws Exception {
        mvc.perform(post("/api/v1/auth/register")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"email\":\"test@abivin.com\",\"password\":\"Test123!\",\"tenantId\":\"default\"}"))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.token").isNotEmpty())
            .andExpect(jsonPath("$.email").value("test@abivin.com"))
            .andExpect(jsonPath("$.roles").value("STAFF"));
    }

    @Test @Order(2)
    @DisplayName("SyR-PLAT-01.1 — Register duplicate email → 409")
    void test_02_register_duplicate() throws Exception {
        mvc.perform(post("/api/v1/auth/register")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"email\":\"test@abivin.com\",\"password\":\"Test123!\"}"))
            .andExpect(status().isConflict())
            .andExpect(jsonPath("$.error").value("USER_EXISTS"));
    }

    @Test @Order(3)
    @DisplayName("SyR-PLAT-01.1 — Register without email → 400")
    void test_03_register_validation() throws Exception {
        mvc.perform(post("/api/v1/auth/register")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"password\":\"Test123!\"}"))
            .andExpect(status().isBadRequest())
            .andExpect(jsonPath("$.error").value("VALIDATION_ERROR"));
    }

    // ── SyR-PLAT-01.1: Login ─────────────────────────────────

    @Test @Order(10)
    @DisplayName("SyR-PLAT-01.1 — Login with valid creds → access_token + refresh_token")
    void test_10_login() throws Exception {
        MvcResult result = mvc.perform(post("/api/v1/auth/login")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"email\":\"test@abivin.com\",\"password\":\"Test123!\"}"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.access_token").isNotEmpty())
            .andExpect(jsonPath("$.refresh_token").isNotEmpty())
            .andExpect(jsonPath("$.token_type").value("Bearer"))
            .andExpect(jsonPath("$.email").value("test@abivin.com"))
            .andReturn();

        JsonNode body = mapper.readTree(result.getResponse().getContentAsString());
        accessToken  = body.get("access_token").asText();
        refreshToken = body.get("refresh_token").asText();
    }

    @Test @Order(11)
    @DisplayName("SyR-PLAT-01.1 — Login with wrong password → 401")
    void test_11_login_bad_creds() throws Exception {
        mvc.perform(post("/api/v1/auth/login")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"email\":\"test@abivin.com\",\"password\":\"Wrong!\"}"))
            .andExpect(status().isUnauthorized())
            .andExpect(jsonPath("$.error").value("AUTH_FAILED"));
    }

    // ── SyR-PLAT-01.0: JWT Protected Endpoints ─────────────────

    @Test @Order(20)
    @DisplayName("SyR-PLAT-01.0 — Access protected endpoint without JWT → 403")
    void test_20_protected_no_token() throws Exception {
        mvc.perform(get("/api/v1/apps"))
            .andExpect(status().isForbidden());
    }

    @Test @Order(21)
    @DisplayName("SyR-PLAT-01.0 — Access protected endpoint with valid JWT → 200")
    void test_21_protected_with_token() throws Exception {
        mvc.perform(get("/api/v1/apps")
                .header("Authorization", "Bearer " + accessToken))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.apps").isArray());
    }

    // ── SyR-PLAT-01.2: Refresh Token Rotation ────────────────

    @Test @Order(30)
    @DisplayName("SyR-PLAT-01.2 — Refresh token rotation → new tokens")
    void test_30_refresh_rotation() throws Exception {
        MvcResult result = mvc.perform(post("/api/v1/auth/refresh")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"refresh_token\":\"" + refreshToken + "\"}"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.access_token").isNotEmpty())
            .andExpect(jsonPath("$.refresh_token").isNotEmpty())
            .andExpect(jsonPath("$.token_type").value("Bearer"))
            .andReturn();

        JsonNode body = mapper.readTree(result.getResponse().getContentAsString());
        String newRefresh = body.get("refresh_token").asText();
        accessToken = body.get("access_token").asText();

        // Old token should now be revoked (reuse → 401)
        mvc.perform(post("/api/v1/auth/refresh")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"refresh_token\":\"" + refreshToken + "\"}"))
            .andExpect(status().isUnauthorized());

        refreshToken = newRefresh;
    }

    @Test @Order(31)
    @DisplayName("SyR-PLAT-01.2 — Refresh with missing token → 400")
    void test_31_refresh_missing() throws Exception {
        mvc.perform(post("/api/v1/auth/refresh")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{}"))
            .andExpect(status().isBadRequest())
            .andExpect(jsonPath("$.error").value("MISSING_TOKEN"));
    }

    @Test @Order(32)
    @DisplayName("SyR-PLAT-01.2 — Refresh with invalid token → 401")
    void test_32_refresh_invalid() throws Exception {
        mvc.perform(post("/api/v1/auth/refresh")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"refresh_token\":\"totally-invalid-token-abc123\"}"))
            .andExpect(status().isUnauthorized());
    }

    // ── SyR-PLAT-01.2: Logout ────────────────────────────────

    @Test @Order(40)
    @DisplayName("SyR-PLAT-01.2 — Logout revokes all refresh tokens")
    void test_40_logout() throws Exception {
        // Login fresh to get a token
        MvcResult loginResult = mvc.perform(post("/api/v1/auth/login")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"email\":\"test@abivin.com\",\"password\":\"Test123!\"}"))
            .andExpect(status().isOk())
            .andReturn();

        JsonNode loginBody = mapper.readTree(loginResult.getResponse().getContentAsString());
        String freshAccess  = loginBody.get("access_token").asText();
        String freshRefresh = loginBody.get("refresh_token").asText();

        // Logout
        mvc.perform(post("/api/v1/auth/logout")
                .header("Authorization", "Bearer " + freshAccess))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.message").value("Logged out successfully"));

        // Post-logout refresh should fail
        mvc.perform(post("/api/v1/auth/refresh")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"refresh_token\":\"" + freshRefresh + "\"}"))
            .andExpect(status().isUnauthorized());
    }
}
