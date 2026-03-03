package com.abivin.vkernel.g5_search.controllers;

import com.abivin.vkernel.g5_search.models.SearchIndexEntity;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.*;
import java.util.stream.Collectors;

/**
 * Universal Search API — federated full-text search across all vKernel entities.
 * <p>
 * On PostgreSQL (production): uses native tsvector + plainto_tsquery with ts_rank.
 * On H2 (test): falls back to LIKE-based search via JPA query.
 * <p>
 * Endpoints:
 * - GET /api/v1/search?q=...&type=...&limit=...  — search across all indexed entities
 * - POST /api/v1/search/index                     — manually index an entity
 * - POST /api/v1/search/reindex                   — rebuild index from all known entities
 *
 * @GovernanceID 5.1.0
 */
@RestController
@RequestMapping("/api/v1/search")
public class SearchController {

    private final SearchIndexEntity.Repository searchRepo;

    @PersistenceContext
    private EntityManager em;

    @Value("${spring.datasource.url:}")
    private String datasourceUrl;

    public SearchController(SearchIndexEntity.Repository searchRepo) {
        this.searchRepo = searchRepo;
    }

    /**
     * Unified search endpoint.
     * GET /api/v1/search?q=...&type=STAKEHOLDER&limit=25
     */
    @GetMapping
    public ResponseEntity<?> search(
            @RequestParam("q") String query,
            @RequestParam(value = "type", required = false) String entityType,
            @RequestParam(value = "limit", defaultValue = "25") int limit) {

        if (query == null || query.isBlank()) {
            return ResponseEntity.badRequest().body(Map.of(
                    "error", "VALIDATION_ERROR",
                    "message", "query parameter 'q' is required"));
        }

        List<Map<String, Object>> results;

        if (isPostgres()) {
            // Native PostgreSQL Full-Text Search with ranking
            results = nativeFtsSearch(query, entityType, limit);
        } else {
            // H2 / fallback: LIKE-based search
            List<SearchIndexEntity> entities = entityType != null
                    ? searchRepo.searchFallbackByType(query, entityType)
                    : searchRepo.searchFallback(query);

            results = entities.stream()
                    .limit(limit)
                    .map(this::entityToMap)
                    .collect(Collectors.toList());
        }

        return ResponseEntity.ok(Map.of(
                "query", query,
                "total", results.size(),
                "results", results));
    }

    /**
     * Manually index an entity.
     * POST /api/v1/search/index
     * Body: {"entity_type":"STAKEHOLDER","entity_id":"...","title":"...","body":"..."}
     */
    @PostMapping("/index")
    public ResponseEntity<?> indexEntity(@RequestBody Map<String, String> body) {
        String type = body.get("entity_type");
        String id = body.get("entity_id");
        String title = body.get("title");
        String bodyText = body.getOrDefault("body", "");
        String tenantId = body.getOrDefault("tenant_id", "default");

        if (type == null || id == null || title == null) {
            return ResponseEntity.badRequest().body(Map.of(
                    "error", "VALIDATION_ERROR",
                    "message", "entity_type, entity_id, and title are required"));
        }

        // Upsert: update if same type+id exists, create otherwise
        var existing = searchRepo.findByEntityTypeAndEntityId(type, id);
        SearchIndexEntity entity;
        if (!existing.isEmpty()) {
            entity = existing.get(0);
            entity.setTitle(title);
            entity.setBody(bodyText);
            entity.setUpdatedAt(java.time.Instant.now());
        } else {
            entity = new SearchIndexEntity(type, id, title, bodyText, tenantId);
        }
        searchRepo.save(entity);

        return ResponseEntity.ok(Map.of(
                "message", "Indexed successfully",
                "entity_type", type,
                "entity_id", id));
    }

    // --- Private helpers ---

    private boolean isPostgres() {
        return datasourceUrl != null && datasourceUrl.contains("postgresql");
    }

    @SuppressWarnings("unchecked")
    private List<Map<String, Object>> nativeFtsSearch(String query, String entityType, int limit) {
        String sql = """
            SELECT id, entity_type, entity_id, title, body, tenant_id,
                   ts_rank(tsv, plainto_tsquery('simple', :query)) AS rank
            FROM kernel_search_index
            WHERE tsv @@ plainto_tsquery('simple', :query)
            """;

        if (entityType != null && !entityType.isBlank()) {
            sql += " AND entity_type = :type";
        }
        sql += " ORDER BY rank DESC LIMIT :lim";

        var nq = em.createNativeQuery(sql);
        nq.setParameter("query", query);
        nq.setParameter("lim", limit);
        if (entityType != null && !entityType.isBlank()) {
            nq.setParameter("type", entityType);
        }

        List<Object[]> rows = nq.getResultList();
        return rows.stream().map(row -> {
            Map<String, Object> m = new LinkedHashMap<>();
            m.put("id", row[0] != null ? row[0].toString() : null);
            m.put("entity_type", row[1]);
            m.put("entity_id", row[2] != null ? row[2].toString() : null);
            m.put("title", row[3]);
            m.put("body", row[4]);
            m.put("tenant_id", row[5]);
            m.put("rank", row[6]);
            return m;
        }).collect(Collectors.toList());
    }

    private Map<String, Object> entityToMap(SearchIndexEntity e) {
        Map<String, Object> m = new LinkedHashMap<>();
        m.put("id", e.getId().toString());
        m.put("entity_type", e.getEntityType());
        m.put("entity_id", e.getEntityId());
        m.put("title", e.getTitle());
        m.put("body", e.getBody());
        m.put("tenant_id", e.getTenantId());
        m.put("rank", 1.0); // no ranking in fallback mode
        return m;
    }
}
