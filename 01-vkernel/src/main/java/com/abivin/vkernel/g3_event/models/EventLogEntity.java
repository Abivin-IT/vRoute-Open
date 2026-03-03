package com.abivin.vkernel.g3_event.models;

import jakarta.persistence.*;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import java.time.Instant;
import java.util.UUID;

/**
 * Immutable event log — append-only audit trail for all IPC transactions.
 * NFR-PLAT-03: Events must be logged immutably. No update/delete operations.
 *
 * @GovernanceID 3.0.0
 */
@Entity
@Table(name = "kernel_event_log")
public class EventLogEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(name = "event_type", nullable = false, length = 100)
    private String eventType;

    @Column(name = "event_version", nullable = false, length = 10)
    private String eventVersion = "1.0";

    @Column(name = "source_app", nullable = false, length = 100)
    private String sourceApp;

    /** JSON payload from publisher */
    @Column(columnDefinition = "jsonb")
    private String payload = "{}";

    @Column(name = "correlation_id", length = 100)
    private String correlationId;

    /** QUEUED → DELIVERED or FAILED */
    @Column(nullable = false, length = 20)
    private String status = "QUEUED";

    /** JSON array of app IDs that were notified */
    @Column(columnDefinition = "jsonb")
    private String subscribers = "[]";

    @Column(name = "created_at", nullable = false, updatable = false)
    private Instant createdAt = Instant.now();

    // Append-only: no setters for createdAt
    public EventLogEntity() {}

    public EventLogEntity(String eventType, String eventVersion, String sourceApp,
                          String payload, String correlationId) {
        this.eventType = eventType;
        this.eventVersion = eventVersion;
        this.sourceApp = sourceApp;
        this.payload = payload;
        this.correlationId = correlationId;
    }

    public UUID getId()            { return id; }
    public String getEventType()   { return eventType; }
    public String getEventVersion(){ return eventVersion; }
    public String getSourceApp()   { return sourceApp; }
    public String getPayload()     { return payload; }
    public String getCorrelationId(){ return correlationId; }
    public String getStatus()      { return status; }
    public String getSubscribers() { return subscribers; }
    public Instant getCreatedAt()  { return createdAt; }

    public void setStatus(String s)       { this.status = s; }
    public void setSubscribers(String s)  { this.subscribers = s; }

    public interface Repository extends JpaRepository<EventLogEntity, UUID> {
        Page<EventLogEntity> findBySourceAppOrderByCreatedAtDesc(String sourceApp, Pageable p);
        Page<EventLogEntity> findByEventTypeOrderByCreatedAtDesc(String eventType, Pageable p);

        @Query("SELECT e FROM EventLogEntity e ORDER BY e.createdAt DESC")
        Page<EventLogEntity> findAllOrderByCreatedAtDesc(Pageable p);
    }
}
