package com.abivin.vkernel.g3_event.models;

import jakarta.persistence.*;
import org.springframework.data.jpa.repository.JpaRepository;

import java.time.Instant;
import java.util.List;
import java.util.UUID;

/**
 * Subscription registry — which app listens to which event type.
 * SyR-PLAT-03.02: Pub/Sub subscription engine.
 *
 * @GovernanceID 3.0.1
 */
@Entity
@Table(name = "kernel_event_subscriptions",
       uniqueConstraints = @UniqueConstraint(columnNames = {"subscriber_app", "event_type"}))
public class SubscriptionEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(name = "subscriber_app", nullable = false, length = 100)
    private String subscriberApp;

    @Column(name = "event_type", nullable = false, length = 100)
    private String eventType;

    /** ACTIVE | PAUSED */
    @Column(nullable = false, length = 20)
    private String status = "ACTIVE";

    @Column(name = "created_at", nullable = false, updatable = false)
    private Instant createdAt = Instant.now();

    public SubscriptionEntity() {}

    public SubscriptionEntity(String subscriberApp, String eventType) {
        this.subscriberApp = subscriberApp;
        this.eventType = eventType;
    }

    public UUID getId()              { return id; }
    public String getSubscriberApp() { return subscriberApp; }
    public String getEventType()     { return eventType; }
    public String getStatus()        { return status; }
    public Instant getCreatedAt()    { return createdAt; }
    public void setStatus(String s)  { this.status = s; }

    public interface Repository extends JpaRepository<SubscriptionEntity, UUID> {
        List<SubscriptionEntity> findByEventTypeAndStatus(String eventType, String status);
        List<SubscriptionEntity> findBySubscriberApp(String subscriberApp);
        boolean existsBySubscriberAppAndEventType(String subscriberApp, String eventType);
    }
}
