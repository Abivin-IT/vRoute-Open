package com.abivin.vkernel.g1_iam.controllers;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;
import java.util.Arrays;

/**
 * Central security configuration for vKernel.
 * - Stateless JWT auth (no sessions)
 * - Public: /api/v1/auth/** (login, register)
 * - Protected: everything else requires Bearer token
 *
 * @GovernanceID 1.0.0
 */
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    private final JwtProvider jwtProvider;

    public SecurityConfig(JwtProvider jwtProvider) {
        this.jwtProvider = jwtProvider;
    }

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .csrf(csrf -> csrf.disable())
            .headers(headers -> headers.frameOptions(fo -> fo.sameOrigin()))
            .sessionManagement(sm -> sm.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/v1/auth/register",
                                 "/api/v1/auth/login",
                                 "/api/v1/auth/refresh").permitAll()
                .requestMatchers("/api/v1/auth/oidc/**",
                                 "/api/v1/auth/magic-link/**").permitAll()
                .requestMatchers("/api/v1/search").permitAll()
                .requestMatchers("/actuator/health",
                                 "/actuator/info",
                                 "/actuator/prometheus",
                                 "/actuator/metrics").permitAll()
                .requestMatchers("/").permitAll()
                .requestMatchers("/api/v1", "/api/v1/").permitAll()
                .requestMatchers("/dashboard").permitAll() // legacy redirect
                .requestMatchers("/vkernel", "/vkernel/**").permitAll()
                .requestMatchers("/css/**").permitAll()
                .requestMatchers("/ui/**").permitAll()
                .requestMatchers("/shell", "/shell/**").permitAll()
                // Gateway proxy routes — vApps are internal-only; vKernel is the auth boundary
                .requestMatchers("/api/v1/vstrategy/**", "/vstrategy/**").permitAll()
                .requestMatchers("/api/v1/vfinacc/**", "/vfinacc/**").permitAll()
                .requestMatchers("/api/v1/vdesign-physical/**", "/vdesign-physical/**").permitAll()
                .requestMatchers("/api/v1/vmarketing-org/**", "/vmarketing-org/**").permitAll()
                .anyRequest().authenticated()
            )
            .addFilterBefore(jwtAuthFilter(), UsernamePasswordAuthenticationFilter.class);

        return http.build();
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }

    @Bean
    public OncePerRequestFilter jwtAuthFilter() {
        return new OncePerRequestFilter() {
            @Override
            protected void doFilterInternal(HttpServletRequest request,
                                            HttpServletResponse response,
                                            FilterChain chain) throws ServletException, IOException {
                try {
                    String header = request.getHeader("Authorization");
                    if (header != null && header.startsWith("Bearer ")) {
                        String token = header.substring(7);
                        if (jwtProvider.validateToken(token)) {
                            String email    = jwtProvider.getEmailFromToken(token);
                            String roles    = jwtProvider.getRolesFromToken(token);
                            String tenantId = jwtProvider.getTenantFromToken(token);
                            var authorities = Arrays.stream(roles.split(","))
                                    .map(r -> new SimpleGrantedAuthority("ROLE_" + r.trim()))
                                    .toList();
                            var auth = new UsernamePasswordAuthenticationToken(email, null, authorities);
                            SecurityContextHolder.getContext().setAuthentication(auth);
                            TenantContext.set(tenantId);   // Step 7: multi-tenant propagation
                        }
                    }
                    chain.doFilter(request, response);
                } finally {
                    TenantContext.clear();                  // always clear after request
                }
            }
        };
    }
}
