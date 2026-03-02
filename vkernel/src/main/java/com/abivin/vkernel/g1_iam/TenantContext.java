package com.abivin.vkernel.g1_iam;

/**
 * ThreadLocal holder for the current request's tenant context.
 * Set by TenantContextFilter from the JWT; cleared after request.
 *
 * Usage in service layer:
 *   String tenantId = TenantContext.get();
 *
 * @GovernanceID 1.5.0
 */
public final class TenantContext {

    /** Default tenant — used for system-level operations with no user context. */
    public static final String DEFAULT_TENANT = "default";

    private static final ThreadLocal<String> CURRENT = ThreadLocal.withInitial(() -> DEFAULT_TENANT);

    private TenantContext() {}

    public static String get()                  { return CURRENT.get(); }
    public static void   set(String tenantId)   { CURRENT.set(tenantId != null ? tenantId : DEFAULT_TENANT); }
    public static void   clear()                { CURRENT.remove(); }
}
