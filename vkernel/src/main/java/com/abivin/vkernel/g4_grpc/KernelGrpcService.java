package com.abivin.vkernel.g4_grpc;

import com.abivin.vkernel.g0_engine.AppRegistryEntity;
import com.abivin.vkernel.g3_event.EventBusService;
import com.abivin.vkernel.grpc.*;
import io.grpc.stub.StreamObserver;
import net.devh.boot.grpc.server.service.GrpcService;
import org.springframework.beans.factory.annotation.Autowired;

import java.lang.management.ManagementFactory;
import java.util.List;

/**
 * KernelGrpcService — gRPC server implementation.
 * Exposes KernelService on port 9090 for vApp-to-Kernel IPC.
 *
 * RPC endpoints:
 *  - Ping              : health check from vApps
 *  - PublishEvent      : vApps push events to the kernel event bus
 *  - GetInstalledApps  : vApps query the app registry
 *
 * @GovernanceID 4.0.0
 */
@GrpcService
public class KernelGrpcService extends KernelServiceGrpc.KernelServiceImplBase {

    private final EventBusService eventBusService;
    private final AppRegistryEntity.Repository appRepo;

    @Autowired
    public KernelGrpcService(EventBusService eventBusService,
                              AppRegistryEntity.Repository appRepo) {
        this.eventBusService = eventBusService;
        this.appRepo = appRepo;
    }

    /**
     * Ping — heartbeat from vApp to Kernel.
     * Returns "UP", version, and JVM uptime.
     */
    @Override
    public void ping(PingRequest request, StreamObserver<PingResponse> responseObserver) {
        long uptimeMs = ManagementFactory.getRuntimeMXBean().getUptime();
        PingResponse response = PingResponse.newBuilder()
                .setStatus("UP")
                .setVersion("0.6.0")
                .setUptimeMs(uptimeMs)
                .build();
        responseObserver.onNext(response);
        responseObserver.onCompleted();
    }

    /**
     * PublishEvent — vApps push a domain event to the kernel event bus.
     * Persisted to immutable audit log and fan-out to subscribers.
     */
    @Override
    public void publishEvent(GrpcEventRequest request, StreamObserver<GrpcEventResponse> responseObserver) {
        try {
            var log = eventBusService.publish(
                    request.getEventType(),
                    request.getEventVersion().isBlank() ? "1.0" : request.getEventVersion(),
                    request.getSource(),
                    request.getPayloadJson(),
                    request.getCorrelationId().isBlank() ? null : request.getCorrelationId()
            );
            GrpcEventResponse response = GrpcEventResponse.newBuilder()
                    .setEventId(log.getId().toString())
                    .setStatus(log.getStatus())
                    .build();
            responseObserver.onNext(response);
            responseObserver.onCompleted();
        } catch (Exception e) {
            responseObserver.onError(
                    io.grpc.Status.INTERNAL
                            .withDescription("Event publish failed: " + e.getMessage())
                            .asException()
            );
        }
    }

    /**
     * GetInstalledApps — vApps query the App Registry.
     * Returns active installed applications.
     */
    @Override
    public void getInstalledApps(GetAppsRequest request, StreamObserver<GetAppsResponse> responseObserver) {
        List<AppRegistryEntity> apps = appRepo.findAll().stream()
                .filter(a -> "ACTIVE".equals(a.getStatus()))
                .toList();

        GetAppsResponse.Builder builder = GetAppsResponse.newBuilder();
        for (AppRegistryEntity app : apps) {
            builder.addApps(AppInfo.newBuilder()
                    .setAppId(app.getAppId())
                    .setDisplayName(app.getName())
                    .setVersion(app.getVersion() != null ? app.getVersion() : "")
                    .setStatus(app.getStatus())
                    .setBaseUrl("")   // base_url resolved via manifest_json if needed
                    .build());
        }
        builder.setTotal(apps.size());
        responseObserver.onNext(builder.build());
        responseObserver.onCompleted();
    }
}
