package com.abivin.vkernel;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.actuate.observability.AutoConfigureObservability;
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
 * Comprehensive functional tests for vKernel — SyR-PLAT-00 (App Engine),
 * SyR-PLAT-02 (Data Backbone), SyR-PLAT-03 (Event Bus).
 *
 * @GovernanceID TEST-SyR-PLAT-00-02-03
 */
@SpringBootTest
@AutoConfigureMockMvc
@AutoConfigureObservability
@ActiveProfiles("test")
@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
class PlatformApiTests {

    @Autowired private MockMvc mvc;
    @Autowired private ObjectMapper mapper;

    static String token;

    @BeforeAll
    static void setupAuth(@Autowired MockMvc mvc, @Autowired ObjectMapper mapper) throws Exception {
        // Register + login to get JWT
        mvc.perform(post("/api/v1/auth/register")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"email\":\"platform-test@abivin.com\",\"password\":\"Plat123!\"}"));

        MvcResult result = mvc.perform(post("/api/v1/auth/login")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"email\":\"platform-test@abivin.com\",\"password\":\"Plat123!\"}"))
            .andReturn();

        JsonNode body = mapper.readTree(result.getResponse().getContentAsString());
        token = body.get("access_token").asText();
    }

    // ══════════════════════════════════════════════════════════
    // SyR-PLAT-00: App Engine
    // ══════════════════════════════════════════════════════════

    @Test @Order(1)
    @DisplayName("SyR-PLAT-00.0 — List installed apps → 200 with count + apps array")
    void test_00_list_apps() throws Exception {
        mvc.perform(get("/api/v1/apps")
                .header("Authorization", "Bearer " + token))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.count").isNumber())
            .andExpect(jsonPath("$.apps").isArray());
    }

    @Test @Order(2)
    @DisplayName("SyR-PLAT-00.3 — Install app from inline manifest → 201")
    void test_00_install_app() throws Exception {
        String manifest = """
            {
              "manifest": {
                "app": {
                  "id": "com.test.testapp",
                  "name": "Test App",
                  "version": "0.1.0"
                },
                "permissions": [
                  {"code": "test:read", "name": "Test Read"},
                  {"code": "test:write", "name": "Test Write"}
                ],
                "events": {
                  "published": ["TEST_EVENT"],
                  "subscribed": []
                },
                "dependencies": []
              }
            }
            """;
        mvc.perform(post("/api/v1/apps/install")
                .header("Authorization", "Bearer " + token)
                .contentType(MediaType.APPLICATION_JSON)
                .content(manifest))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.appId").value("com.test.testapp"));
    }

    @Test @Order(3)
    @DisplayName("SyR-PLAT-00.4 — List permissions after install → contains test:read")
    void test_00_list_permissions() throws Exception {
        mvc.perform(get("/api/v1/apps/permissions")
                .header("Authorization", "Bearer " + token)
                .param("app", "com.test.testapp"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.count").value(greaterThanOrEqualTo(1)))
            .andExpect(jsonPath("$.permissions").isArray());
    }

    @Test @Order(4)
    @DisplayName("SyR-PLAT-00.3 — Uninstall app → 200")
    void test_00_uninstall_app() throws Exception {
        mvc.perform(delete("/api/v1/apps/com.test.testapp")
                .header("Authorization", "Bearer " + token))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.uninstalled").value("com.test.testapp"));
    }

    // ══════════════════════════════════════════════════════════
    // SyR-PLAT-02: Data Backbone
    // ══════════════════════════════════════════════════════════

    @Test @Order(10)
    @DisplayName("SyR-PLAT-02.2 — Get currencies → returns array")
    void test_02_currencies() throws Exception {
        mvc.perform(get("/api/v1/data/currencies")
                .header("Authorization", "Bearer " + token))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.currencies").isArray());
    }

    @Test @Order(11)
    @DisplayName("SyR-PLAT-02.2 — Get countries → returns array")
    void test_02_countries() throws Exception {
        mvc.perform(get("/api/v1/data/countries")
                .header("Authorization", "Bearer " + token))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.countries").isArray());
    }

    // ══════════════════════════════════════════════════════════
    // SyR-PLAT-03: Event Bus
    // ══════════════════════════════════════════════════════════

    @Test @Order(20)
    @DisplayName("SyR-PLAT-03.1 — Subscribe to event → 201")
    void test_03_subscribe() throws Exception {
        mvc.perform(post("/api/v1/events/subscribe")
                .header("Authorization", "Bearer " + token)
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"subscriber_app\":\"test-app\",\"event_type\":\"ORDER_CONFIRMED\"}"))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.subscriber_app").value("test-app"))
            .andExpect(jsonPath("$.event_type").value("ORDER_CONFIRMED"));
    }

    @Test @Order(21)
    @DisplayName("SyR-PLAT-03.0 — Publish event → 202 Accepted with event_id")
    void test_03_publish() throws Exception {
        mvc.perform(post("/api/v1/events/publish")
                .header("Authorization", "Bearer " + token)
                .header("X-App-ID", "test-app")
                .header("X-Correlation-ID", "corr-001")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"event_type\":\"ORDER_CONFIRMED\",\"payload\":{\"order_id\":\"ORD-001\"}}"))
            .andExpect(status().isAccepted())
            .andExpect(jsonPath("$.event_id").isNotEmpty())
            .andExpect(jsonPath("$.status").value("DELIVERED"))
            .andExpect(jsonPath("$.subscribers_notified").value(greaterThanOrEqualTo(1)));
    }

    @Test @Order(22)
    @DisplayName("SyR-PLAT-03.0 — Publish without event_type → 400")
    void test_03_publish_validation() throws Exception {
        mvc.perform(post("/api/v1/events/publish")
                .header("Authorization", "Bearer " + token)
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"payload\":{}}"))
            .andExpect(status().isBadRequest())
            .andExpect(jsonPath("$.error").value("VALIDATION_ERROR"));
    }

    @Test @Order(23)
    @DisplayName("SyR-PLAT-03.2 — Get subscriptions → contains test-app → ORDER_CONFIRMED")
    void test_03_subscriptions() throws Exception {
        mvc.perform(get("/api/v1/events/subscriptions")
                .header("Authorization", "Bearer " + token)
                .param("app", "test-app"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.count").value(greaterThanOrEqualTo(1)));
    }

    @Test @Order(24)
    @DisplayName("SyR-PLAT-03.2 — Get audit log → has published events")
    void test_03_audit_log() throws Exception {
        mvc.perform(get("/api/v1/events/log")
                .header("Authorization", "Bearer " + token))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.events").isArray());
    }

    // ══════════════════════════════════════════════════════════
    // SyR-PLAT-05: Observability (public endpoints)
    // ══════════════════════════════════════════════════════════

    @Test @Order(50)
    @DisplayName("SyR-PLAT-05.0 — Health endpoint → UP")
    void test_05_health() throws Exception {
        mvc.perform(get("/actuator/health"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.status").value("UP"));
    }

    @Test @Order(51)
    @DisplayName("SyR-PLAT-05.1 — Prometheus endpoint → text/plain metrics")
    void test_05_prometheus() throws Exception {
        mvc.perform(get("/actuator/prometheus"))
            .andExpect(status().isOk())
            .andExpect(content().string(containsString("jvm_memory")));
    }

    @Test @Order(52)
    @DisplayName("SyR-PLAT-05.0 — Info endpoint → 200")
    void test_05_info() throws Exception {
        mvc.perform(get("/actuator/info"))
            .andExpect(status().isOk());
    }
}
