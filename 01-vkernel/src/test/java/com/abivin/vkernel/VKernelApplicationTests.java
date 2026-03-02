package com.abivin.vkernel;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;

/**
 * Smoke test — verifies Spring context loads successfully.
 */
@SpringBootTest
@ActiveProfiles("test")
class VKernelApplicationTests {

    @Test
    void contextLoads() {
        // If this passes, DI wiring + JPA schema + security config are all valid.
    }
}
