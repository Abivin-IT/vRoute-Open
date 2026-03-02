package com.abivin.vkernel.g3_event;

import org.springframework.context.ApplicationEvent;
import java.util.List;

/**
 * Internal Spring domain event — carries IPC payload for in-process fan-out.
 * Listeners (@EventListener) in vApp modules receive this.
 *
 * @GovernanceID 3.1.1
 */
public class KernelEvent extends ApplicationEvent {

    private final String eventType;
    private final String sourceApp;
    private final String payloadJson;
    private final String correlationId;
    private final List<String> targetApps;

    public KernelEvent(Object source, String eventType, String sourceApp,
                       String payloadJson, String correlationId, List<String> targetApps) {
        super(source);
        this.eventType = eventType;
        this.sourceApp = sourceApp;
        this.payloadJson = payloadJson;
        this.correlationId = correlationId;
        this.targetApps = targetApps;
    }

    public String getEventType()     { return eventType; }
    public String getSourceApp()     { return sourceApp; }
    public String getPayloadJson()   { return payloadJson; }
    public String getCorrelationId() { return correlationId; }
    public List<String> getTargetApps() { return targetApps; }
}
