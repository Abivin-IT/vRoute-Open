package com.abivin.vkernel.g5_search;

import jakarta.persistence.*;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.time.Instant;
import java.util.List;
import java.util.UUID;

/**
 * Unified search index — stores denormalized content for PostgreSQL FTS.
 * Each row = one searchable entity (stakeholder, currency, user, app, event…).
 * <p>
 * The actual tsvector column is maintained by a DB trigger (V7 migration).
 * For H2 (tests), we fall back to LIKE-based search.
 *
 * @GovernanceID 5.0.0
 */
@Entity
@Table(name = "kernel_search_index")
public class SearchIndexEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    /** Entity type: STAKEHOLDER, CURRENCY, COUNTRY, USER, APP, EVENT */
    @Column(name = "entity_type", nullable = false, length = 50)
    private String entityType;

    /** Original entity UUID (for linking back) */
    @Column(name = "entity_id", nullable = false, length = 100)
    private String entityId;

    /** Primary text for search (weighted A in tsvector) */
    @Column(nullable = false)
    private String title;

    /** Secondary text for search (weighted B in tsvector) */
    @Column(columnDefinition = "TEXT")
    private String body;

    /** Tenant scoping */
    @Column(name = "tenant_id", length = 100)
    private String tenantId;

    @Column(name = "created_at", updatable = false, nullable = false)
    private Instant createdAt = Instant.now();

    @Column(name = "updated_at")
    private Instant updatedAt = Instant.now();

    public SearchIndexEntity() {}

    public SearchIndexEntity(String entityType, String entityId, String title,
                              String body, String tenantId) {
        this.entityType = entityType;
        this.entityId = entityId;
        this.title = title;
        this.body = body;
        this.tenantId = tenantId;
    }

    // --- Getters ---
    public UUID getId()            { return id; }
    public String getEntityType()  { return entityType; }
    public String getEntityId()    { return entityId; }
    public String getTitle()       { return title; }
    public String getBody()        { return body; }
    public String getTenantId()    { return tenantId; }
    public Instant getCreatedAt()  { return createdAt; }
    public Instant getUpdatedAt()  { return updatedAt; }

    // --- Setters ---
    public void setTitle(String t)     { this.title = t; }
    public void setBody(String b)      { this.body = b; }
    public void setUpdatedAt(Instant i){ this.updatedAt = i; }

    /**
     * Repository with both native PostgreSQL FTS and H2-compatible fallback.
     */
    public interface Repository extends JpaRepository<SearchIndexEntity, UUID> {

        /**
         * H2-compatible search using LIKE — used in test profile.
         * In production, SearchController uses native query for FTS ranking.
         */
        @Query("SELECT s FROM SearchIndexEntity s WHERE " +
               "LOWER(s.title) LIKE LOWER(CONCAT('%', :q, '%')) OR " +
               "LOWER(s.body) LIKE LOWER(CONCAT('%', :q, '%'))")
        List<SearchIndexEntity> searchFallback(@Param("q") String query);

        /** Filter by entity type */
        @Query("SELECT s FROM SearchIndexEntity s WHERE s.entityType = :type AND " +
               "(LOWER(s.title) LIKE LOWER(CONCAT('%', :q, '%')) OR " +
               "LOWER(s.body) LIKE LOWER(CONCAT('%', :q, '%')))")
        List<SearchIndexEntity> searchFallbackByType(@Param("q") String query,
                                                      @Param("type") String entityType);

        List<SearchIndexEntity> findByEntityTypeAndEntityId(String entityType, String entityId);
    }
}
