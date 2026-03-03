package com.abivin.vkernel.g3_event.controllers;

import com.abivin.vkernel.g3_event.models.SubscriptionEntity;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

import com.fasterxml.jackson.databind.ObjectMapper;

/**
 * Event Bus REST API — publish, subscribe, audit trail.
 * SyR-PLAT-03: Inter-process communication.
 *
 * @GovernanceID 3.2.0
 */
@RestController
@RequestMapping("/api/v1/events")
public class EventBusController {

    private final EventBusService eventBusService;
    private final ObjectMapper objectMapper;

    public EventBusController(EventBusService eventBusService, ObjectMapper objectMapper) {
        this.eventBusService = eventBusService;
        this.objectMapper = objectMapper;
    }

    /**
     * Publish a business event to the Event Bus.
     * POST /api/v1/events/publish
     * Headers: X-App-ID, X-Correlation-ID
     * Body: { "event_type":"SALES_ORDER_CONFIRMED", "event_version":"1.0",
     *         "payload": {...}, "metadata": {"priority":"HIGH"} }
     */
    @PostMapping("/publish")
    public ResponseEntity<?> publish(
            @RequestHeader(value = "X-App-ID", defaultValue = "unknown") String appId,
            @RequestHeader(value = "X-Correlation-ID", defaultValue = "") String correlationId,
            @RequestBody Map<String, Object> body) {

        String eventType = (String) body.get("event_type");
        String eventVersion = (String) body.getOrDefault("event_version", "1.0");
        Object payload = body.getOrDefault("payload", Map.of());

        if (eventType == null || eventType.isBlank()) {
            return ResponseEntity.badRequest().body(Map.of(
                    "error", "VALIDATION_ERROR",
                    "message", "event_type is required"
            ));
        }

        try {
            var log = eventBusService.publish(eventType, eventVersion, appId, payload, correlationId);
            var subscribersNode = objectMapper.readTree(log.getSubscribers());
            int subscriberCount = subscribersNode.isArray() ? subscribersNode.size() : 0;
            return ResponseEntity.status(HttpStatus.ACCEPTED).body(Map.of(
                    "event_id", log.getId().toString(),
                    "status", log.getStatus(),
                    "subscribers_notified", subscriberCount
            ));
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(Map.of(
                    "error", "PUBLISH_FAILED",
                    "message", e.getMessage()
            ));
        }
    }

    /**
     * Register a subscription (idempotent).
     * POST /api/v1/events/subscribe
     * Body: { "subscriber_app": "vfinance", "event_type": "SALES_ORDER_CONFIRMED" }
     */
    @PostMapping("/subscribe")
    public ResponseEntity<?> subscribe(@RequestBody Map<String, String> body) {
        String subscriberApp = body.get("subscriber_app");
        String eventType = body.get("event_type");

        if (subscriberApp == null || eventType == null) {
            return ResponseEntity.badRequest().body(Map.of(
                    "error", "VALIDATION_ERROR",
                    "message", "subscriber_app and event_type are required"
            ));
        }

        var sub = eventBusService.subscribe(subscriberApp, eventType);
        return ResponseEntity.status(HttpStatus.CREATED).body(Map.of(
                "id", sub.getId(),
                "subscriber_app", sub.getSubscriberApp(),
                "event_type", sub.getEventType(),
                "status", sub.getStatus()
        ));
    }

    /**
     * Get subscriptions for an app.
     * GET /api/v1/events/subscriptions?app=vfinance
     */
    @GetMapping("/subscriptions")
    public ResponseEntity<?> getSubscriptions(
            @RequestParam(required = false) String app) {
        List<SubscriptionEntity> subs = app != null
                ? eventBusService.getSubscriptions(app)
                : List.of();
        return ResponseEntity.ok(Map.of("count", subs.size(), "subscriptions", subs));
    }

    /**
     * Audit trail — paginated event log (SyR-PLAT-03.03).
     * GET /api/v1/events/log?page=0&size=20&sourceApp=vsales
     */
    @GetMapping("/log")
    public ResponseEntity<?> getAuditLog(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size,
            @RequestParam(required = false) String sourceApp) {
        var logs = sourceApp != null
                ? eventBusService.getAuditLogByApp(sourceApp, page, size)
                : eventBusService.getAuditLog(page, size);
        return ResponseEntity.ok(Map.of("count", logs.size(), "events", logs));
    }
}
