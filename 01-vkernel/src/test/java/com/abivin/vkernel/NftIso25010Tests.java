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

import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

/**
 * Non-Functional Tests (ISO/IEC 25010:2023) for vKernel.
 *
 * Coverage mapping:
 *   NFR-REL    → ISO 5.5  Reliability
 *   NFR-COMPAT → ISO 5.3  Compatibility
 *   NFR-SEC    → ISO 5.6  Security
 *   NFR-SAFE   → ISO 5.9  Safety
 *   NFR-FLEX   → ISO 5.8  Flexibility (Scalability)
 *
 * @GovernanceID TEST-NFR-ISO-25010
 */
@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
@TestInstance(TestInstance.Lifecycle.PER_CLASS)
class NftIso25010Tests {

    @Autowired private MockMvc mvc;
    @Autowired private ObjectMapper mapper;

    private String accessToken;

    // ── Bootstrap: register a dedicated NFT test user and capture JWT ──

    @BeforeAll
    void setupNftUser() throws Exception {
        // Register — ignore 409 if already exists from a previous run
        mvc.perform(post("/api/v1/auth/register")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"email\":\"nft25010@abivin.com\",\"password\":\"Nft123!\",\"tenantId\":\"default\"}"));

        MvcResult result = mvc.perform(post("/api/v1/auth/login")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"email\":\"nft25010@abivin.com\",\"password\":\"Nft123!\"}"))
            .andExpect(status().isOk())
            .andReturn();

        JsonNode body = mapper.readTree(result.getResponse().getContentAsString());
        accessToken = body.get("access_token").asText();
    }

    // ════════════════════════════════════════════════════════════════
    // Reliability  (ISO/IEC 25010:2023 §5.5)
    // Sub-characteristics: faultlessness, availability
    // ════════════════════════════════════════════════════════════════

    @Test @Order(10)
    @DisplayName("NFR-REL-01 — Health endpoint returns {status:UP} consistently across 5 sequential calls")
    void nfrRel01_healthAlwaysUp() throws Exception {
        for (int i = 0; i < 5; i++) {
            mvc.perform(get("/actuator/health"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("UP"));
        }
    }

    @Test @Order(11)
    @DisplayName("NFR-REL-02 — Malformed JSON body → 400 (service does not crash with 500)")
    void nfrRel02_malformedJsonReturns400() throws Exception {
        mvc.perform(post("/api/v1/auth/login")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{ malformed :: json !! }"))
            .andExpect(result ->
                assertThat(result.getResponse().getStatus())
                    .as("Malformed JSON must yield 4xx, not 500")
                    .isBetween(400, 499));
    }

    @Test @Order(12)
    @DisplayName("NFR-REL-03 — Request to unknown endpoint → 4xx (Spring Security may return 403 before 404)")
    void nfrRel03_unknownEndpointReturns4xx() throws Exception {
        // Spring Security filters may return 403 (Forbidden) for unknown protected paths
        // before the routing layer can return 404. Both are acceptable — the key assertion
        // is that the server does NOT crash with a 5xx response.
        mvc.perform(get("/api/v1/does-not-exist/endpoint/xyz"))
            .andExpect(result ->
                assertThat(result.getResponse().getStatus())
                    .as("Unknown endpoint must return 4xx, not 5xx")
                    .isBetween(400, 499));
    }

    @Test @Order(13)
    @DisplayName("NFR-REL-04 — Empty body on POST auth endpoint → 4xx (not 500)")
    void nfrRel04_emptyBodyReturns4xx() throws Exception {
        mvc.perform(post("/api/v1/auth/login")
                .contentType(MediaType.APPLICATION_JSON)
                .content(""))
            .andExpect(result ->
                assertThat(result.getResponse().getStatus())
                    .as("Empty JSON body must yield 4xx, not 500")
                    .isBetween(400, 499));
    }

    // ════════════════════════════════════════════════════════════════
    // Compatibility  (ISO/IEC 25010:2023 §5.3)
    // Sub-characteristic: interoperability (well-formed media types)
    // ════════════════════════════════════════════════════════════════

    @Test @Order(20)
    @DisplayName("NFR-COMPAT-01 — /actuator/health response Content-Type is a JSON variant")
    void nfrCompat01_healthContentTypeJson() throws Exception {
        // Spring Boot Actuator uses application/vnd.spring-boot.actuator.v3+json,
        // which is still a JSON sub-type. We assert the content type contains 'json'.
        mvc.perform(get("/actuator/health"))
            .andExpect(status().isOk())
            .andExpect(result -> {
                String ct = result.getResponse().getContentType();
                assertThat(ct)
                    .as("Content-Type must be a JSON sub-type")
                    .contains("json");
            });
    }

    @Test @Order(21)
    @DisplayName("NFR-COMPAT-02 — POST /api/v1/auth/login response Content-Type is application/json")
    void nfrCompat02_loginContentTypeJson() throws Exception {
        mvc.perform(post("/api/v1/auth/login")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"email\":\"nft25010@abivin.com\",\"password\":\"Nft123!\"}"))
            .andExpect(status().isOk())
            .andExpect(content().contentTypeCompatibleWith(MediaType.APPLICATION_JSON));
    }

    @Test @Order(22)
    @DisplayName("NFR-COMPAT-03 — GET /api/v1/apps (authenticated) response Content-Type is application/json")
    void nfrCompat03_appsEndpointContentTypeJson() throws Exception {
        mvc.perform(get("/api/v1/apps")
                .header("Authorization", "Bearer " + accessToken))
            .andExpect(status().isOk())
            .andExpect(content().contentTypeCompatibleWith(MediaType.APPLICATION_JSON));
    }

    @Test @Order(23)
    @DisplayName("NFR-COMPAT-04 — Error responses include a structured JSON body with 'error' or 'message' field")
    void nfrCompat04_errorResponseStructured() throws Exception {
        MvcResult result = mvc.perform(post("/api/v1/auth/login")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"email\":\"nobody@abivin.com\",\"password\":\"Wrong!\"}"))
            .andExpect(result2 ->
                assertThat(result2.getResponse().getStatus()).isBetween(400, 499))
            .andReturn();

        String body = result.getResponse().getContentAsString();
        assertThat(body).isNotBlank();
        // Body should be parseable JSON
        JsonNode node = mapper.readTree(body);
        assertThat(node.has("error") || node.has("message") || node.has("detail"))
            .as("Error response must include 'error', 'message', or 'detail' field")
            .isTrue();
    }

    // ════════════════════════════════════════════════════════════════
    // Security  (ISO/IEC 25010:2023 §5.6)
    // Sub-characteristics: confidentiality, integrity, authenticity,
    //                      accountability
    // ════════════════════════════════════════════════════════════════

    @Test @Order(30)
    @DisplayName("NFR-SEC-01 — Tampered JWT (last char mutated) is rejected with 401 or 403")
    void nfrSec01_tamperedJwtRejected() throws Exception {
        char last = accessToken.charAt(accessToken.length() - 1);
        String replacement = (last == 'a') ? "b" : "a";
        String tampered = accessToken.substring(0, accessToken.length() - 1) + replacement;

        mvc.perform(get("/api/v1/apps")
                .header("Authorization", "Bearer " + tampered))
            .andExpect(result ->
                assertThat(result.getResponse().getStatus())
                    .as("Tampered JWT must be rejected (401 or 403)")
                    .isIn(401, 403));
    }

    @Test @Order(31)
    @DisplayName("NFR-SEC-02 — Completely invalid token string is rejected with 401 or 403")
    void nfrSec02_garbageTokenRejected() throws Exception {
        mvc.perform(get("/api/v1/apps")
                .header("Authorization", "Bearer definitely.not.a.valid.jwt.xyz"))
            .andExpect(result ->
                assertThat(result.getResponse().getStatus())
                    .as("Garbage token must be rejected (401 or 403)")
                    .isIn(401, 403));
    }

    @Test @Order(32)
    @DisplayName("NFR-SEC-03 — Accessing protected endpoint with no Authorization header is rejected")
    void nfrSec03_missingAuthHeaderRejected() throws Exception {
        mvc.perform(get("/api/v1/apps"))
            .andExpect(result ->
                assertThat(result.getResponse().getStatus())
                    .as("Missing auth header must yield 401 or 403")
                    .isIn(401, 403));
    }

    @Test @Order(33)
    @DisplayName("NFR-SEC-04 — Duplicate registration of same email returns 409 CONFLICT (no data leak)")
    void nfrSec04_duplicateRegistrationConflict() throws Exception {
        // Attempt to register the NFT user that already exists (created in @BeforeAll)
        mvc.perform(post("/api/v1/auth/register")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"email\":\"nft25010@abivin.com\",\"password\":\"Nft123!\",\"tenantId\":\"default\"}"))
            .andExpect(status().isConflict());
    }

    // ════════════════════════════════════════════════════════════════
    // Safety  (ISO/IEC 25010:2023 §5.9)
    // Sub-characteristics: operational constraint, fail safe
    // ════════════════════════════════════════════════════════════════

    @Test @Order(40)
    @DisplayName("NFR-SAFE-01 — Oversized email field (10 000 chars) on register → 400")
    void nfrSafe01_oversizedEmailRejected() throws Exception {
        String bigEmail = "a".repeat(10_000) + "@test.com";
        mvc.perform(post("/api/v1/auth/register")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"email\":\"" + bigEmail + "\",\"password\":\"Test123!\"}"))
            .andExpect(status().isBadRequest());
    }

    @Test @Order(41)
    @DisplayName("NFR-SAFE-02 — Missing required email field on register → 400")
    void nfrSafe02_missingEmailOnRegister() throws Exception {
        mvc.perform(post("/api/v1/auth/register")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"password\":\"Test123!\"}"))
            .andExpect(status().isBadRequest());
    }

    @Test @Order(42)
    @DisplayName("NFR-SAFE-03 — SQL-injection-like content in email field → must not cause 500")
    void nfrSafe03_sqlInjectionLikeInputSanitised() throws Exception {
        mvc.perform(post("/api/v1/auth/login")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"email\":\"' OR '1'='1' --\",\"password\":\"x\"}"))
            .andExpect(result ->
                assertThat(result.getResponse().getStatus())
                    .as("SQL-injection-like input must not cause server error (500)")
                    .isNotEqualTo(500));
    }

    @Test @Order(43)
    @DisplayName("NFR-SAFE-04 — Script-injection-like content in password field → must not cause 500")
    void nfrSafe04_scriptInjectionLikeInputSanitised() throws Exception {
        mvc.perform(post("/api/v1/auth/login")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"email\":\"test@test.com\",\"password\":\"<script>alert(1)</script>\"}"))
            .andExpect(result ->
                assertThat(result.getResponse().getStatus())
                    .as("Script-injection content must not cause server error (500)")
                    .isNotEqualTo(500));
    }

    // ════════════════════════════════════════════════════════════════
    // Flexibility / Scalability  (ISO/IEC 25010:2023 §5.8)
    // Sub-characteristic: scalability (concurrent load handling)
    // ════════════════════════════════════════════════════════════════

    @Test @Order(50)
    @DisplayName("NFR-FLEX-01 — 20 concurrent GET /actuator/health all return HTTP 200")
    void nfrFlex01_concurrentHealthAllSucceed() throws Exception {
        final int threads = 20;
        ExecutorService pool = Executors.newFixedThreadPool(threads);
        AtomicInteger successCount = new AtomicInteger(0);
        CountDownLatch latch = new CountDownLatch(threads);

        for (int i = 0; i < threads; i++) {
            pool.submit(() -> {
                try {
                    MvcResult r = mvc.perform(get("/actuator/health")).andReturn();
                    if (r.getResponse().getStatus() == 200) {
                        successCount.incrementAndGet();
                    }
                } catch (Exception ignored) {
                } finally {
                    latch.countDown();
                }
            });
        }

        boolean completed = latch.await(30, TimeUnit.SECONDS);
        pool.shutdown();

        assertThat(completed).as("All threads must complete within 30s").isTrue();
        assertThat(successCount.get())
            .as("All %d concurrent health requests must return 200", threads)
            .isEqualTo(threads);
    }

    @Test @Order(51)
    @DisplayName("NFR-FLEX-02 — 20 concurrent authenticated GET /api/v1/apps all return HTTP 200")
    void nfrFlex02_concurrentAuthenticatedReadsAllSucceed() throws Exception {
        final int threads = 20;
        ExecutorService pool = Executors.newFixedThreadPool(threads);
        AtomicInteger successCount = new AtomicInteger(0);
        CountDownLatch latch = new CountDownLatch(threads);

        for (int i = 0; i < threads; i++) {
            pool.submit(() -> {
                try {
                    MvcResult r = mvc.perform(get("/api/v1/apps")
                            .header("Authorization", "Bearer " + accessToken))
                        .andReturn();
                    if (r.getResponse().getStatus() == 200) {
                        successCount.incrementAndGet();
                    }
                } catch (Exception ignored) {
                } finally {
                    latch.countDown();
                }
            });
        }

        boolean completed = latch.await(30, TimeUnit.SECONDS);
        pool.shutdown();

        assertThat(completed).as("All threads must complete within 30s").isTrue();
        assertThat(successCount.get())
            .as("All %d concurrent authenticated requests must return 200", threads)
            .isEqualTo(threads);
    }
}
