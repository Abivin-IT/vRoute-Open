package com.abivin.vkernel.g3_event;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Map;

/**
 * Event Bus core — Pub/Sub engine backed by PostgreSQL audit log.
 * <p>
 * Publish flow: persist to event_log → notify in-process subscribers via
 * Spring ApplicationEventPublisher → update log status to DELIVERED.
 * <p>
 * Design: DB-first guarantees durability. Spring events handle in-process
 * fan-out. Redis distributed fan-out can be layered on top (Step 6+).
 *
 * @GovernanceID 3.1.0
 */
@Service
public class EventBusService {

    private final EventLogEntity.Repository eventLogRepo;
    private final SubscriptionEntity.Repository subscriptionRepo;
    private final ApplicationEventPublisher springPublisher;
    private final ObjectMapper objectMapper;

    public EventBusService(EventLogEntity.Repository eventLogRepo,
                           SubscriptionEntity.Repository subscriptionRepo,
                           ApplicationEventPublisher springPublisher,
                           ObjectMapper objectMapper) {
        this.eventLogRepo = eventLogRepo;
        this.subscriptionRepo = subscriptionRepo;
        this.springPublisher = springPublisher;
        this.objectMapper = objectMapper;
    }

    /**
     * Publish an event to the bus.
     * Returns the persisted EventLogEntity (with id).
     */
    @Transactional
    public EventLogEntity publish(String eventType, String eventVersion, String sourceApp,
                                  Object payload, String correlationId) throws Exception {
        String payloadJson = objectMapper.writeValueAsString(payload);

        // 1. Persist to immutable audit log (QUEUED)
        var log = new EventLogEntity(eventType, eventVersion, sourceApp, payloadJson, correlationId);
        log = eventLogRepo.save(log);

        // 2. Find active subscribers
        List<SubscriptionEntity> subs = subscriptionRepo
                .findByEventTypeAndStatus(eventType, "ACTIVE");
        List<String> subscriberApps = subs.stream()
                .map(SubscriptionEntity::getSubscriberApp)
                .toList();

        // 3. Fan-out via Spring ApplicationEvent (in-process)
        if (!subscriberApps.isEmpty()) {
            var domainEvent = new KernelEvent(this, eventType, sourceApp, payloadJson,
                    correlationId, subscriberApps);
            springPublisher.publishEvent(domainEvent);
        }

        // 4. Update log: DELIVERED with subscriber snapshot
        log.setStatus("DELIVERED");
        log.setSubscribers(objectMapper.writeValueAsString(subscriberApps));
        return eventLogRepo.save(log);
    }

    /** Register a subscription (idempotent). */
    @Transactional
    public SubscriptionEntity subscribe(String subscriberApp, String eventType) {
        if (subscriptionRepo.existsBySubscriberAppAndEventType(subscriberApp, eventType)) {
            return subscriptionRepo.findBySubscriberApp(subscriberApp).stream()
                    .filter(s -> s.getEventType().equals(eventType))
                    .findFirst().orElseThrow();
        }
        return subscriptionRepo.save(new SubscriptionEntity(subscriberApp, eventType));
    }

    /** Get subscriptions for an app. */
    public List<SubscriptionEntity> getSubscriptions(String subscriberApp) {
        return subscriptionRepo.findBySubscriberApp(subscriberApp);
    }

    /** Audit log — paginated, newest first. */
    public List<EventLogEntity> getAuditLog(int page, int size) {
        return eventLogRepo.findAllOrderByCreatedAtDesc(PageRequest.of(page, size)).getContent();
    }

    public List<EventLogEntity> getAuditLogByApp(String sourceApp, int page, int size) {
        return eventLogRepo
                .findBySourceAppOrderByCreatedAtDesc(sourceApp, PageRequest.of(page, size))
                .getContent();
    }
}
