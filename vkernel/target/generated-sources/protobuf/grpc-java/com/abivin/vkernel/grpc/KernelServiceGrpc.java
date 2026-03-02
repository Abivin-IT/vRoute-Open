package com.abivin.vkernel.grpc;

import static io.grpc.MethodDescriptor.generateFullMethodName;

/**
 */
@javax.annotation.Generated(
    value = "by gRPC proto compiler (version 1.65.0)",
    comments = "Source: kernel.proto")
@io.grpc.stub.annotations.GrpcGenerated
public final class KernelServiceGrpc {

  private KernelServiceGrpc() {}

  public static final java.lang.String SERVICE_NAME = "vkernel.KernelService";

  // Static method descriptors that strictly reflect the proto.
  private static volatile io.grpc.MethodDescriptor<com.abivin.vkernel.grpc.PingRequest,
      com.abivin.vkernel.grpc.PingResponse> getPingMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "Ping",
      requestType = com.abivin.vkernel.grpc.PingRequest.class,
      responseType = com.abivin.vkernel.grpc.PingResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<com.abivin.vkernel.grpc.PingRequest,
      com.abivin.vkernel.grpc.PingResponse> getPingMethod() {
    io.grpc.MethodDescriptor<com.abivin.vkernel.grpc.PingRequest, com.abivin.vkernel.grpc.PingResponse> getPingMethod;
    if ((getPingMethod = KernelServiceGrpc.getPingMethod) == null) {
      synchronized (KernelServiceGrpc.class) {
        if ((getPingMethod = KernelServiceGrpc.getPingMethod) == null) {
          KernelServiceGrpc.getPingMethod = getPingMethod =
              io.grpc.MethodDescriptor.<com.abivin.vkernel.grpc.PingRequest, com.abivin.vkernel.grpc.PingResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "Ping"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.abivin.vkernel.grpc.PingRequest.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.abivin.vkernel.grpc.PingResponse.getDefaultInstance()))
              .setSchemaDescriptor(new KernelServiceMethodDescriptorSupplier("Ping"))
              .build();
        }
      }
    }
    return getPingMethod;
  }

  private static volatile io.grpc.MethodDescriptor<com.abivin.vkernel.grpc.GrpcEventRequest,
      com.abivin.vkernel.grpc.GrpcEventResponse> getPublishEventMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "PublishEvent",
      requestType = com.abivin.vkernel.grpc.GrpcEventRequest.class,
      responseType = com.abivin.vkernel.grpc.GrpcEventResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<com.abivin.vkernel.grpc.GrpcEventRequest,
      com.abivin.vkernel.grpc.GrpcEventResponse> getPublishEventMethod() {
    io.grpc.MethodDescriptor<com.abivin.vkernel.grpc.GrpcEventRequest, com.abivin.vkernel.grpc.GrpcEventResponse> getPublishEventMethod;
    if ((getPublishEventMethod = KernelServiceGrpc.getPublishEventMethod) == null) {
      synchronized (KernelServiceGrpc.class) {
        if ((getPublishEventMethod = KernelServiceGrpc.getPublishEventMethod) == null) {
          KernelServiceGrpc.getPublishEventMethod = getPublishEventMethod =
              io.grpc.MethodDescriptor.<com.abivin.vkernel.grpc.GrpcEventRequest, com.abivin.vkernel.grpc.GrpcEventResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "PublishEvent"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.abivin.vkernel.grpc.GrpcEventRequest.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.abivin.vkernel.grpc.GrpcEventResponse.getDefaultInstance()))
              .setSchemaDescriptor(new KernelServiceMethodDescriptorSupplier("PublishEvent"))
              .build();
        }
      }
    }
    return getPublishEventMethod;
  }

  private static volatile io.grpc.MethodDescriptor<com.abivin.vkernel.grpc.GetAppsRequest,
      com.abivin.vkernel.grpc.GetAppsResponse> getGetInstalledAppsMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "GetInstalledApps",
      requestType = com.abivin.vkernel.grpc.GetAppsRequest.class,
      responseType = com.abivin.vkernel.grpc.GetAppsResponse.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<com.abivin.vkernel.grpc.GetAppsRequest,
      com.abivin.vkernel.grpc.GetAppsResponse> getGetInstalledAppsMethod() {
    io.grpc.MethodDescriptor<com.abivin.vkernel.grpc.GetAppsRequest, com.abivin.vkernel.grpc.GetAppsResponse> getGetInstalledAppsMethod;
    if ((getGetInstalledAppsMethod = KernelServiceGrpc.getGetInstalledAppsMethod) == null) {
      synchronized (KernelServiceGrpc.class) {
        if ((getGetInstalledAppsMethod = KernelServiceGrpc.getGetInstalledAppsMethod) == null) {
          KernelServiceGrpc.getGetInstalledAppsMethod = getGetInstalledAppsMethod =
              io.grpc.MethodDescriptor.<com.abivin.vkernel.grpc.GetAppsRequest, com.abivin.vkernel.grpc.GetAppsResponse>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "GetInstalledApps"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.abivin.vkernel.grpc.GetAppsRequest.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.abivin.vkernel.grpc.GetAppsResponse.getDefaultInstance()))
              .setSchemaDescriptor(new KernelServiceMethodDescriptorSupplier("GetInstalledApps"))
              .build();
        }
      }
    }
    return getGetInstalledAppsMethod;
  }

  /**
   * Creates a new async stub that supports all call types for the service
   */
  public static KernelServiceStub newStub(io.grpc.Channel channel) {
    io.grpc.stub.AbstractStub.StubFactory<KernelServiceStub> factory =
      new io.grpc.stub.AbstractStub.StubFactory<KernelServiceStub>() {
        @java.lang.Override
        public KernelServiceStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
          return new KernelServiceStub(channel, callOptions);
        }
      };
    return KernelServiceStub.newStub(factory, channel);
  }

  /**
   * Creates a new blocking-style stub that supports unary and streaming output calls on the service
   */
  public static KernelServiceBlockingStub newBlockingStub(
      io.grpc.Channel channel) {
    io.grpc.stub.AbstractStub.StubFactory<KernelServiceBlockingStub> factory =
      new io.grpc.stub.AbstractStub.StubFactory<KernelServiceBlockingStub>() {
        @java.lang.Override
        public KernelServiceBlockingStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
          return new KernelServiceBlockingStub(channel, callOptions);
        }
      };
    return KernelServiceBlockingStub.newStub(factory, channel);
  }

  /**
   * Creates a new ListenableFuture-style stub that supports unary calls on the service
   */
  public static KernelServiceFutureStub newFutureStub(
      io.grpc.Channel channel) {
    io.grpc.stub.AbstractStub.StubFactory<KernelServiceFutureStub> factory =
      new io.grpc.stub.AbstractStub.StubFactory<KernelServiceFutureStub>() {
        @java.lang.Override
        public KernelServiceFutureStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
          return new KernelServiceFutureStub(channel, callOptions);
        }
      };
    return KernelServiceFutureStub.newStub(factory, channel);
  }

  /**
   */
  public interface AsyncService {

    /**
     * <pre>
     * Health check: vApps verify kernel is alive on startup.
     * </pre>
     */
    default void ping(com.abivin.vkernel.grpc.PingRequest request,
        io.grpc.stub.StreamObserver<com.abivin.vkernel.grpc.PingResponse> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getPingMethod(), responseObserver);
    }

    /**
     * <pre>
     * Publish a domain event to the vKernel event bus (DB-backed).
     * </pre>
     */
    default void publishEvent(com.abivin.vkernel.grpc.GrpcEventRequest request,
        io.grpc.stub.StreamObserver<com.abivin.vkernel.grpc.GrpcEventResponse> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getPublishEventMethod(), responseObserver);
    }

    /**
     * <pre>
     * Query the App Registry — installed vApps + statuses.
     * </pre>
     */
    default void getInstalledApps(com.abivin.vkernel.grpc.GetAppsRequest request,
        io.grpc.stub.StreamObserver<com.abivin.vkernel.grpc.GetAppsResponse> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getGetInstalledAppsMethod(), responseObserver);
    }
  }

  /**
   * Base class for the server implementation of the service KernelService.
   */
  public static abstract class KernelServiceImplBase
      implements io.grpc.BindableService, AsyncService {

    @java.lang.Override public final io.grpc.ServerServiceDefinition bindService() {
      return KernelServiceGrpc.bindService(this);
    }
  }

  /**
   * A stub to allow clients to do asynchronous rpc calls to service KernelService.
   */
  public static final class KernelServiceStub
      extends io.grpc.stub.AbstractAsyncStub<KernelServiceStub> {
    private KernelServiceStub(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected KernelServiceStub build(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      return new KernelServiceStub(channel, callOptions);
    }

    /**
     * <pre>
     * Health check: vApps verify kernel is alive on startup.
     * </pre>
     */
    public void ping(com.abivin.vkernel.grpc.PingRequest request,
        io.grpc.stub.StreamObserver<com.abivin.vkernel.grpc.PingResponse> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getPingMethod(), getCallOptions()), request, responseObserver);
    }

    /**
     * <pre>
     * Publish a domain event to the vKernel event bus (DB-backed).
     * </pre>
     */
    public void publishEvent(com.abivin.vkernel.grpc.GrpcEventRequest request,
        io.grpc.stub.StreamObserver<com.abivin.vkernel.grpc.GrpcEventResponse> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getPublishEventMethod(), getCallOptions()), request, responseObserver);
    }

    /**
     * <pre>
     * Query the App Registry — installed vApps + statuses.
     * </pre>
     */
    public void getInstalledApps(com.abivin.vkernel.grpc.GetAppsRequest request,
        io.grpc.stub.StreamObserver<com.abivin.vkernel.grpc.GetAppsResponse> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getGetInstalledAppsMethod(), getCallOptions()), request, responseObserver);
    }
  }

  /**
   * A stub to allow clients to do synchronous rpc calls to service KernelService.
   */
  public static final class KernelServiceBlockingStub
      extends io.grpc.stub.AbstractBlockingStub<KernelServiceBlockingStub> {
    private KernelServiceBlockingStub(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected KernelServiceBlockingStub build(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      return new KernelServiceBlockingStub(channel, callOptions);
    }

    /**
     * <pre>
     * Health check: vApps verify kernel is alive on startup.
     * </pre>
     */
    public com.abivin.vkernel.grpc.PingResponse ping(com.abivin.vkernel.grpc.PingRequest request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getPingMethod(), getCallOptions(), request);
    }

    /**
     * <pre>
     * Publish a domain event to the vKernel event bus (DB-backed).
     * </pre>
     */
    public com.abivin.vkernel.grpc.GrpcEventResponse publishEvent(com.abivin.vkernel.grpc.GrpcEventRequest request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getPublishEventMethod(), getCallOptions(), request);
    }

    /**
     * <pre>
     * Query the App Registry — installed vApps + statuses.
     * </pre>
     */
    public com.abivin.vkernel.grpc.GetAppsResponse getInstalledApps(com.abivin.vkernel.grpc.GetAppsRequest request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getGetInstalledAppsMethod(), getCallOptions(), request);
    }
  }

  /**
   * A stub to allow clients to do ListenableFuture-style rpc calls to service KernelService.
   */
  public static final class KernelServiceFutureStub
      extends io.grpc.stub.AbstractFutureStub<KernelServiceFutureStub> {
    private KernelServiceFutureStub(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected KernelServiceFutureStub build(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      return new KernelServiceFutureStub(channel, callOptions);
    }

    /**
     * <pre>
     * Health check: vApps verify kernel is alive on startup.
     * </pre>
     */
    public com.google.common.util.concurrent.ListenableFuture<com.abivin.vkernel.grpc.PingResponse> ping(
        com.abivin.vkernel.grpc.PingRequest request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getPingMethod(), getCallOptions()), request);
    }

    /**
     * <pre>
     * Publish a domain event to the vKernel event bus (DB-backed).
     * </pre>
     */
    public com.google.common.util.concurrent.ListenableFuture<com.abivin.vkernel.grpc.GrpcEventResponse> publishEvent(
        com.abivin.vkernel.grpc.GrpcEventRequest request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getPublishEventMethod(), getCallOptions()), request);
    }

    /**
     * <pre>
     * Query the App Registry — installed vApps + statuses.
     * </pre>
     */
    public com.google.common.util.concurrent.ListenableFuture<com.abivin.vkernel.grpc.GetAppsResponse> getInstalledApps(
        com.abivin.vkernel.grpc.GetAppsRequest request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getGetInstalledAppsMethod(), getCallOptions()), request);
    }
  }

  private static final int METHODID_PING = 0;
  private static final int METHODID_PUBLISH_EVENT = 1;
  private static final int METHODID_GET_INSTALLED_APPS = 2;

  private static final class MethodHandlers<Req, Resp> implements
      io.grpc.stub.ServerCalls.UnaryMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.ServerStreamingMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.ClientStreamingMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.BidiStreamingMethod<Req, Resp> {
    private final AsyncService serviceImpl;
    private final int methodId;

    MethodHandlers(AsyncService serviceImpl, int methodId) {
      this.serviceImpl = serviceImpl;
      this.methodId = methodId;
    }

    @java.lang.Override
    @java.lang.SuppressWarnings("unchecked")
    public void invoke(Req request, io.grpc.stub.StreamObserver<Resp> responseObserver) {
      switch (methodId) {
        case METHODID_PING:
          serviceImpl.ping((com.abivin.vkernel.grpc.PingRequest) request,
              (io.grpc.stub.StreamObserver<com.abivin.vkernel.grpc.PingResponse>) responseObserver);
          break;
        case METHODID_PUBLISH_EVENT:
          serviceImpl.publishEvent((com.abivin.vkernel.grpc.GrpcEventRequest) request,
              (io.grpc.stub.StreamObserver<com.abivin.vkernel.grpc.GrpcEventResponse>) responseObserver);
          break;
        case METHODID_GET_INSTALLED_APPS:
          serviceImpl.getInstalledApps((com.abivin.vkernel.grpc.GetAppsRequest) request,
              (io.grpc.stub.StreamObserver<com.abivin.vkernel.grpc.GetAppsResponse>) responseObserver);
          break;
        default:
          throw new AssertionError();
      }
    }

    @java.lang.Override
    @java.lang.SuppressWarnings("unchecked")
    public io.grpc.stub.StreamObserver<Req> invoke(
        io.grpc.stub.StreamObserver<Resp> responseObserver) {
      switch (methodId) {
        default:
          throw new AssertionError();
      }
    }
  }

  public static final io.grpc.ServerServiceDefinition bindService(AsyncService service) {
    return io.grpc.ServerServiceDefinition.builder(getServiceDescriptor())
        .addMethod(
          getPingMethod(),
          io.grpc.stub.ServerCalls.asyncUnaryCall(
            new MethodHandlers<
              com.abivin.vkernel.grpc.PingRequest,
              com.abivin.vkernel.grpc.PingResponse>(
                service, METHODID_PING)))
        .addMethod(
          getPublishEventMethod(),
          io.grpc.stub.ServerCalls.asyncUnaryCall(
            new MethodHandlers<
              com.abivin.vkernel.grpc.GrpcEventRequest,
              com.abivin.vkernel.grpc.GrpcEventResponse>(
                service, METHODID_PUBLISH_EVENT)))
        .addMethod(
          getGetInstalledAppsMethod(),
          io.grpc.stub.ServerCalls.asyncUnaryCall(
            new MethodHandlers<
              com.abivin.vkernel.grpc.GetAppsRequest,
              com.abivin.vkernel.grpc.GetAppsResponse>(
                service, METHODID_GET_INSTALLED_APPS)))
        .build();
  }

  private static abstract class KernelServiceBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoFileDescriptorSupplier, io.grpc.protobuf.ProtoServiceDescriptorSupplier {
    KernelServiceBaseDescriptorSupplier() {}

    @java.lang.Override
    public com.google.protobuf.Descriptors.FileDescriptor getFileDescriptor() {
      return com.abivin.vkernel.grpc.KernelProto.getDescriptor();
    }

    @java.lang.Override
    public com.google.protobuf.Descriptors.ServiceDescriptor getServiceDescriptor() {
      return getFileDescriptor().findServiceByName("KernelService");
    }
  }

  private static final class KernelServiceFileDescriptorSupplier
      extends KernelServiceBaseDescriptorSupplier {
    KernelServiceFileDescriptorSupplier() {}
  }

  private static final class KernelServiceMethodDescriptorSupplier
      extends KernelServiceBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoMethodDescriptorSupplier {
    private final java.lang.String methodName;

    KernelServiceMethodDescriptorSupplier(java.lang.String methodName) {
      this.methodName = methodName;
    }

    @java.lang.Override
    public com.google.protobuf.Descriptors.MethodDescriptor getMethodDescriptor() {
      return getServiceDescriptor().findMethodByName(methodName);
    }
  }

  private static volatile io.grpc.ServiceDescriptor serviceDescriptor;

  public static io.grpc.ServiceDescriptor getServiceDescriptor() {
    io.grpc.ServiceDescriptor result = serviceDescriptor;
    if (result == null) {
      synchronized (KernelServiceGrpc.class) {
        result = serviceDescriptor;
        if (result == null) {
          serviceDescriptor = result = io.grpc.ServiceDescriptor.newBuilder(SERVICE_NAME)
              .setSchemaDescriptor(new KernelServiceFileDescriptorSupplier())
              .addMethod(getPingMethod())
              .addMethod(getPublishEventMethod())
              .addMethod(getGetInstalledAppsMethod())
              .build();
        }
      }
    }
    return result;
  }
}
