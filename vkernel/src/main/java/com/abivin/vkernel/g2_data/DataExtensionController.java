package com.abivin.vkernel.g2_data;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.*;

/**
 * Data Extension API — allows vApps to extend Core Entities
 * with custom JSONB fields without altering DB schema. (SyR-PLAT-02.01)
 * <p>
 * Supported entity types: stakeholder, tenant.
 * <p>
 * Also provides read endpoints for reference data (currencies, countries).
 *
 * @GovernanceID 2.1.0
 */
@RestController
@RequestMapping("/api/v1/data")
public class DataExtensionController {

    private final StakeholderEntity.Repository stakeholderRepo;
    private final TenantEntity.Repository tenantRepo;
    private final CurrencyEntity.Repository currencyRepo;
    private final CountryEntity.Repository countryRepo;
    private final ObjectMapper objectMapper;

    public DataExtensionController(StakeholderEntity.Repository stakeholderRepo,
                                   TenantEntity.Repository tenantRepo,
                                   CurrencyEntity.Repository currencyRepo,
                                   CountryEntity.Repository countryRepo,
                                   ObjectMapper objectMapper) {
        this.stakeholderRepo = stakeholderRepo;
        this.tenantRepo = tenantRepo;
        this.currencyRepo = currencyRepo;
        this.countryRepo = countryRepo;
        this.objectMapper = objectMapper;
    }

    // ===== JSONB Extension (SyR-PLAT-02.01) =====

    /**
     * Extend a Core Entity with custom fields via JSONB merge.
     * PATCH /api/v1/data/entities/{type}/{id}/extend
     * Body: { "fields": { "facebook_url": {"value":"...","label":"...","visibility":["vmarketing"]} } }
     */
    @PatchMapping("/entities/{type}/{id}/extend")
    public ResponseEntity<?> extendEntity(
            @PathVariable String type,
            @PathVariable UUID id,
            @RequestHeader(value = "X-App-ID", defaultValue = "unknown") String appId,
            @RequestBody Map<String, Object> body) {

        @SuppressWarnings("unchecked")
        Map<String, Object> fields = (Map<String, Object>) body.get("fields");
        if (fields == null || fields.isEmpty()) {
            return ResponseEntity.badRequest().body(Map.of(
                    "error", "VALIDATION_ERROR",
                    "message", "'fields' is required and must not be empty"
            ));
        }

        try {
            return switch (type.toLowerCase()) {
                case "stakeholder" -> extendStakeholder(id, fields, appId);
                case "tenant"      -> extendTenant(id, fields, appId);
                default -> ResponseEntity.badRequest().body(Map.of(
                        "error", "UNKNOWN_ENTITY_TYPE",
                        "message", "Supported types: stakeholder, tenant"
                ));
            };
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(Map.of(
                    "error", "EXTENSION_FAILED",
                    "message", e.getMessage()
            ));
        }
    }

    private ResponseEntity<?> extendStakeholder(UUID id, Map<String, Object> fields, String appId) throws Exception {
        var entity = stakeholderRepo.findById(id);
        if (entity.isEmpty()) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(Map.of(
                    "error", "NOT_FOUND", "message", "Stakeholder not found: " + id));
        }
        var sh = entity.get();
        String merged = mergeMetadata(sh.getMetadata(), fields);
        sh.setMetadata(merged);
        stakeholderRepo.save(sh);
        return ResponseEntity.ok(Map.of(
                "entity_id", id, "entity_type", "stakeholder",
                "extended_by", appId, "custom_fields", fields.keySet()
        ));
    }

    private ResponseEntity<?> extendTenant(UUID id, Map<String, Object> fields, String appId) throws Exception {
        var entity = tenantRepo.findById(id);
        if (entity.isEmpty()) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(Map.of(
                    "error", "NOT_FOUND", "message", "Tenant not found: " + id));
        }
        var t = entity.get();
        String merged = mergeMetadata(t.getMetadata(), fields);
        t.setMetadata(merged);
        tenantRepo.save(t);
        return ResponseEntity.ok(Map.of(
                "entity_id", id, "entity_type", "tenant",
                "extended_by", appId, "custom_fields", fields.keySet()
        ));
    }

    /** Deep-merge new fields into existing JSONB metadata. */
    private String mergeMetadata(String existing, Map<String, Object> newFields) throws Exception {
        Map<String, Object> current = objectMapper.readValue(
                existing == null || existing.isBlank() ? "{}" : existing,
                new TypeReference<>() {});
        current.putAll(newFields);
        return objectMapper.writeValueAsString(current);
    }

    // ===== Reference Data Read APIs =====

    /** GET /api/v1/data/currencies */
    @GetMapping("/currencies")
    public ResponseEntity<?> listCurrencies() {
        return ResponseEntity.ok(Map.of("currencies", currencyRepo.findByActiveTrue()));
    }

    /** GET /api/v1/data/countries */
    @GetMapping("/countries")
    public ResponseEntity<?> listCountries() {
        return ResponseEntity.ok(Map.of("countries", countryRepo.findByActiveTrue()));
    }

    /** GET /api/v1/data/stakeholders?tenantId=...&type=... */
    @GetMapping("/stakeholders")
    public ResponseEntity<?> listStakeholders(
            @RequestParam UUID tenantId,
            @RequestParam(required = false) String type) {
        var list = (type != null && !type.isBlank())
                ? stakeholderRepo.findByTenantIdAndType(tenantId, type.toUpperCase())
                : stakeholderRepo.findByTenantId(tenantId);
        return ResponseEntity.ok(Map.of("count", list.size(), "stakeholders", list));
    }

    /** POST /api/v1/data/stakeholders — Create new Golden Record */
    @PostMapping("/stakeholders")
    public ResponseEntity<?> createStakeholder(@RequestBody Map<String, String> body) {
        String tenantIdStr = body.get("tenantId");
        String type = body.getOrDefault("type", "CUSTOMER");
        String code = body.get("code");
        String name = body.get("name");

        if (tenantIdStr == null || code == null || name == null) {
            return ResponseEntity.badRequest().body(Map.of(
                    "error", "VALIDATION_ERROR",
                    "message", "tenantId, code, and name are required"
            ));
        }

        UUID tenantId = UUID.fromString(tenantIdStr);
        var sh = new StakeholderEntity(tenantId, type.toUpperCase(), code, name);
        sh.setEmail(body.get("email"));
        sh.setPhone(body.get("phone"));
        sh.setAddress(body.get("address"));
        stakeholderRepo.save(sh);

        return ResponseEntity.status(HttpStatus.CREATED).body(Map.of(
                "id", sh.getId(), "code", sh.getCode(),
                "name", sh.getName(), "type", sh.getType()
        ));
    }
}
