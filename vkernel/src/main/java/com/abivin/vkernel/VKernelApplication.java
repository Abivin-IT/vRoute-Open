package com.abivin.vkernel;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;

/**
 * vKernel — vRoute Core OS Entry Point.
 * <p>
 * Single Spring Boot application serving as:
 * - API Gateway (Spring Cloud Gateway MVC)
 * - IAM Service (Auth + RBAC)
 * - App Engine (App Registry + Lifecycle)
 *
 * @GovernanceID 0.0.0-BOOT
 */
@SpringBootApplication
@EnableJpaRepositories(considerNestedRepositories = true)
public class VKernelApplication {

    public static void main(String[] args) {
        SpringApplication.run(VKernelApplication.class, args);
    }
}
