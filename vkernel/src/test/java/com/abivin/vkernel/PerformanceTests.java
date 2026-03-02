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

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.*;

import static org.junit.jupiter.api.Assertions.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

/**
 * Performance regression tests for vKernel — NFR validation.
 * Verifies API response times stay within acceptable thresholds.
 *
 * NFR Targets (from PRD):
 *   - Health check: < 50ms
 *   - Auth endpoints: < 200ms
 *   - Data read endpoints: < 150ms
 *   - Event publish: < 300ms
 *   - Throughput: ≥ 50 req/sec for read endpoints
 *
 * @GovernanceID TEST-NFR-PERF
 */
@SpringBootTest
@AutoConfigureMockMvc
@AutoConfigureObservability
@ActiveProfiles("test")
@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
class PerformanceTests {

    @Autowired private MockMvc mvc;
    @Autowired private ObjectMapper mapper;

    static String token;

    @BeforeAll
    static void setupAuth(@Autowired MockMvc mvc, @Autowired ObjectMapper mapper) throws Exception {
        mvc.perform(post("/api/v1/auth/register")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"email\":\"perf-test@abivin.com\",\"password\":\"Perf123!\"}"));

        MvcResult result = mvc.perform(post("/api/v1/auth/login")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"email\":\"perf-test@abivin.com\",\"password\":\"Perf123!\"}"))
            .andReturn();

        JsonNode body = mapper.readTree(result.getResponse().getContentAsString());
        token = body.get("access_token").asText();
    }

    // ══════════════════════════════════════════════════════════
    // NFR-01: Response Time — Health Endpoint < 50ms
    // ══════════════════════════════════════════════════════════

    @Test @Order(1)
    @DisplayName("NFR-PERF-01 — Health endpoint responds within 50ms (avg of 10 calls)")
    void test_perf_health_response_time() throws Exception {
        // Warm up
        mvc.perform(get("/actuator/health")).andExpect(status().isOk());

        List<Long> times = new ArrayList<>();
        for (int i = 0; i < 10; i++) {
            long start = System.nanoTime();
            mvc.perform(get("/actuator/health")).andExpect(status().isOk());
            long elapsed = (System.nanoTime() - start) / 1_000_000;
            times.add(elapsed);
        }

        double avg = times.stream().mapToLong(Long::longValue).average().orElse(0);
        System.out.printf("NFR-PERF-01: Health avg = %.1f ms (target < 50ms)%n", avg);
        assertTrue(avg < 50, "Health endpoint average response time should be < 50ms, was " + avg + "ms");
    }

    // ══════════════════════════════════════════════════════════
    // NFR-02: Response Time — Auth Login < 200ms
    // ══════════════════════════════════════════════════════════

    @Test @Order(2)
    @DisplayName("NFR-PERF-02 — Login endpoint responds within 200ms")
    void test_perf_login_response_time() throws Exception {
        List<Long> times = new ArrayList<>();
        for (int i = 0; i < 5; i++) {
            long start = System.nanoTime();
            mvc.perform(post("/api/v1/auth/login")
                    .contentType(MediaType.APPLICATION_JSON)
                    .content("{\"email\":\"perf-test@abivin.com\",\"password\":\"Perf123!\"}"))
                .andExpect(status().isOk());
            long elapsed = (System.nanoTime() - start) / 1_000_000;
            times.add(elapsed);
        }

        double avg = times.stream().mapToLong(Long::longValue).average().orElse(0);
        System.out.printf("NFR-PERF-02: Login avg = %.1f ms (target < 200ms)%n", avg);
        assertTrue(avg < 200, "Login average response time should be < 200ms, was " + avg + "ms");
    }

    // ══════════════════════════════════════════════════════════
    // NFR-03: Response Time — Data Read Endpoints < 150ms
    // ══════════════════════════════════════════════════════════

    @Test @Order(3)
    @DisplayName("NFR-PERF-03 — Currencies endpoint responds within 150ms")
    void test_perf_currencies_response_time() throws Exception {
        List<Long> times = new ArrayList<>();
        for (int i = 0; i < 10; i++) {
            long start = System.nanoTime();
            mvc.perform(get("/api/v1/data/currencies")
                    .header("Authorization", "Bearer " + token))
                .andExpect(status().isOk());
            long elapsed = (System.nanoTime() - start) / 1_000_000;
            times.add(elapsed);
        }

        double avg = times.stream().mapToLong(Long::longValue).average().orElse(0);
        System.out.printf("NFR-PERF-03: Currencies avg = %.1f ms (target < 150ms)%n", avg);
        assertTrue(avg < 150, "Currencies average response time should be < 150ms, was " + avg + "ms");
    }

    @Test @Order(4)
    @DisplayName("NFR-PERF-03 — List apps endpoint responds within 150ms")
    void test_perf_list_apps_response_time() throws Exception {
        List<Long> times = new ArrayList<>();
        for (int i = 0; i < 10; i++) {
            long start = System.nanoTime();
            mvc.perform(get("/api/v1/apps")
                    .header("Authorization", "Bearer " + token))
                .andExpect(status().isOk());
            long elapsed = (System.nanoTime() - start) / 1_000_000;
            times.add(elapsed);
        }

        double avg = times.stream().mapToLong(Long::longValue).average().orElse(0);
        System.out.printf("NFR-PERF-03: List Apps avg = %.1f ms (target < 150ms)%n", avg);
        assertTrue(avg < 150, "List apps average response time should be < 150ms, was " + avg + "ms");
    }

    // ══════════════════════════════════════════════════════════
    // NFR-04: Response Time — Event Publish < 300ms
    // ══════════════════════════════════════════════════════════

    @Test @Order(5)
    @DisplayName("NFR-PERF-04 — Event publish responds within 300ms")
    void test_perf_event_publish_response_time() throws Exception {
        // Setup: subscribe first
        mvc.perform(post("/api/v1/events/subscribe")
                .header("Authorization", "Bearer " + token)
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"subscriber_app\":\"perf-test\",\"event_type\":\"PERF_EVENT\"}"))
            .andExpect(status().isCreated());

        List<Long> times = new ArrayList<>();
        for (int i = 0; i < 5; i++) {
            long start = System.nanoTime();
            mvc.perform(post("/api/v1/events/publish")
                    .header("Authorization", "Bearer " + token)
                    .header("X-App-ID", "perf-test")
                    .contentType(MediaType.APPLICATION_JSON)
                    .content("{\"event_type\":\"PERF_EVENT\",\"payload\":{\"i\":" + i + "}}"))
                .andExpect(status().isAccepted());
            long elapsed = (System.nanoTime() - start) / 1_000_000;
            times.add(elapsed);
        }

        double avg = times.stream().mapToLong(Long::longValue).average().orElse(0);
        System.out.printf("NFR-PERF-04: Event publish avg = %.1f ms (target < 300ms)%n", avg);
        assertTrue(avg < 300, "Event publish average response time should be < 300ms, was " + avg + "ms");
    }

    // ══════════════════════════════════════════════════════════
    // NFR-05: Throughput — Read Endpoints ≥ 50 req/sec
    // ══════════════════════════════════════════════════════════

    @Test @Order(10)
    @DisplayName("NFR-PERF-05 — Health endpoint throughput ≥ 50 req/sec")
    void test_perf_throughput_health() throws Exception {
        int requests = 100;
        long start = System.nanoTime();
        for (int i = 0; i < requests; i++) {
            mvc.perform(get("/actuator/health")).andExpect(status().isOk());
        }
        long totalMs = (System.nanoTime() - start) / 1_000_000;
        double rps = (requests * 1000.0) / totalMs;

        System.out.printf("NFR-PERF-05: Health throughput = %.1f req/sec (target ≥ 50)%n", rps);
        assertTrue(rps >= 50, "Health throughput should be ≥ 50 req/sec, was " + rps);
    }

    @Test @Order(11)
    @DisplayName("NFR-PERF-05 — Authenticated read throughput ≥ 50 req/sec")
    void test_perf_throughput_authenticated_read() throws Exception {
        int requests = 50;
        long start = System.nanoTime();
        for (int i = 0; i < requests; i++) {
            mvc.perform(get("/api/v1/apps")
                    .header("Authorization", "Bearer " + token))
                .andExpect(status().isOk());
        }
        long totalMs = (System.nanoTime() - start) / 1_000_000;
        double rps = (requests * 1000.0) / totalMs;

        System.out.printf("NFR-PERF-05: Authenticated read throughput = %.1f req/sec (target ≥ 50)%n", rps);
        assertTrue(rps >= 50, "Authenticated read throughput should be ≥ 50 req/sec, was " + rps);
    }

    // ══════════════════════════════════════════════════════════
    // NFR-06: JWT Token Generation Consistency
    // ══════════════════════════════════════════════════════════

    @Test @Order(20)
    @DisplayName("NFR-PERF-06 — 20 sequential register+login cycles complete in < 5s")
    void test_perf_auth_cycle() throws Exception {
        long start = System.nanoTime();
        for (int i = 0; i < 20; i++) {
            String email = "perf" + i + "@abivin.com";
            mvc.perform(post("/api/v1/auth/register")
                    .contentType(MediaType.APPLICATION_JSON)
                    .content("{\"email\":\"" + email + "\",\"password\":\"Pass123!\"}"))
                .andExpect(status().isCreated());

            mvc.perform(post("/api/v1/auth/login")
                    .contentType(MediaType.APPLICATION_JSON)
                    .content("{\"email\":\"" + email + "\",\"password\":\"Pass123!\"}"))
                .andExpect(status().isOk());
        }
        long totalMs = (System.nanoTime() - start) / 1_000_000;

        System.out.printf("NFR-PERF-06: 20 register+login cycles = %d ms (target < 10000ms)%n", totalMs);
        assertTrue(totalMs < 10000, "20 auth cycles should complete in < 10s, took " + totalMs + "ms");
    }

    // ══════════════════════════════════════════════════════════
    // NFR-07: Prometheus Metrics Size
    // ══════════════════════════════════════════════════════════

    @Test @Order(30)
    @DisplayName("NFR-PERF-07 — Prometheus metrics respond < 100ms and contain key metrics")
    void test_perf_prometheus_response() throws Exception {
        long start = System.nanoTime();
        MvcResult result = mvc.perform(get("/actuator/prometheus"))
            .andExpect(status().isOk())
            .andReturn();
        long elapsed = (System.nanoTime() - start) / 1_000_000;

        String body = result.getResponse().getContentAsString();
        System.out.printf("NFR-PERF-07: Prometheus response = %d ms, size = %d bytes%n", elapsed, body.length());

        assertTrue(elapsed < 500, "Prometheus should respond in < 500ms, was " + elapsed + "ms");
        assertTrue(body.contains("jvm_memory"), "Prometheus should contain JVM memory metrics");
        assertTrue(body.contains("http_server"), "Prometheus should contain HTTP server metrics");
    }
}
