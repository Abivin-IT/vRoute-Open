package com.abivin.vkernel.g1_iam.controllers;

import jakarta.servlet.*;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.time.Instant;
import java.util.Deque;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentLinkedDeque;

/**
 * In-process sliding-window rate limiter for auth endpoints.
 * Protects /api/v1/auth/login and /api/v1/auth/register from brute force.
 *
 * Config:
 *  - vkernel.rate-limit.enabled : true (disable in test profile)
 *  - Window  : 60 seconds
 *  - Max reqs: 10 per IP per window
 *
 * @GovernanceID 1.4.0
 */
@Component
@Order(1)
public class RateLimitFilter implements Filter {

    @Value("${vkernel.rate-limit.enabled:true}")
    private boolean enabled;

    /** Sliding window size in seconds. */
    private static final long WINDOW_SECONDS = 60;

    /** Max requests per IP within the window. */
    private static final int MAX_REQUESTS = 10;

    /** Rate-limited endpoints. */
    private static final String[] RATE_LIMITED_PATHS = {
        "/api/v1/auth/login",
        "/api/v1/auth/register"
    };

    /** Per-IP request timestamps. Cleaned up on each access. */
    private final ConcurrentHashMap<String, Deque<Instant>> requestLog = new ConcurrentHashMap<>();

    @Override
    public void doFilter(ServletRequest servletRequest,
                         ServletResponse servletResponse,
                         FilterChain chain) throws IOException, ServletException {

        HttpServletRequest  req  = (HttpServletRequest) servletRequest;
        HttpServletResponse resp = (HttpServletResponse) servletResponse;

        String path = req.getRequestURI();
        if (enabled && isRateLimited(path)) {
            String ip = resolveClientIp(req);
            if (!allowRequest(ip)) {
                resp.setStatus(429);
                resp.setContentType("application/json");
                resp.getWriter().write(
                    "{\"error\":\"RATE_LIMIT_EXCEEDED\"," +
                    "\"message\":\"Too many requests. Try again in 60 seconds.\"}"
                );
                return;
            }
        }
        chain.doFilter(req, resp);
    }

    private boolean isRateLimited(String path) {
        for (String p : RATE_LIMITED_PATHS) {
            if (path.startsWith(p)) return true;
        }
        return false;
    }

    private boolean allowRequest(String ip) {
        Instant now    = Instant.now();
        Instant cutoff = now.minusSeconds(WINDOW_SECONDS);

        Deque<Instant> timestamps = requestLog.computeIfAbsent(ip, k -> new ConcurrentLinkedDeque<>());
        // Evict stale entries outside the window
        while (!timestamps.isEmpty() && timestamps.peekFirst().isBefore(cutoff)) {
            timestamps.pollFirst();
        }
        if (timestamps.size() >= MAX_REQUESTS) {
            return false;
        }
        timestamps.addLast(now);
        return true;
    }

    private String resolveClientIp(HttpServletRequest req) {
        String forwarded = req.getHeader("X-Forwarded-For");
        if (forwarded != null && !forwarded.isBlank()) {
            return forwarded.split(",")[0].trim();
        }
        return req.getRemoteAddr();
    }
}
