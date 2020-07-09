# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import proto.health_rpc_pb2 as health__rpc__pb2


class RPCServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Check = channel.unary_unary(
            "/RPCService/Check",
            request_serializer=health__rpc__pb2.CheckRequest.SerializeToString,
            response_deserializer=health__rpc__pb2.CheckResponse.FromString,
        )


class RPCServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Check(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_RPCServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "Check": grpc.unary_unary_rpc_method_handler(
            servicer.Check,
            request_deserializer=health__rpc__pb2.CheckRequest.FromString,
            response_serializer=health__rpc__pb2.CheckResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "RPCService", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class RPCService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Check(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/RPCService/Check",
            health__rpc__pb2.CheckRequest.SerializeToString,
            health__rpc__pb2.CheckResponse.FromString,
            options,
            channel_credentials,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )
