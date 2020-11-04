from proto.powergate.v1 import powergate_pb2, powergate_pb2_grpc
from pygate_grpc.errors import ErrorHandlerMeta
from google.protobuf.json_format import Parse


class StorageConfigClient(object, metaclass=ErrorHandlerMeta):
    def __init__(self, channel, get_metadata):
        self.client = powergate_pb2_grpc.PowergateServiceStub(channel)
        self.get_metadata = get_metadata

    def default(self, token: str = None):
        req = powergate_pb2.DefaultStorageConfigRequest()
        return self.client.DefaultStorageConfig(req, metadata=self.get_metadata(token))

    # Currently you need to pass in the powergate_pb2.DefaultConfig. However, this is not a good design.
    def set_default(self, config: str, token: str = None):
        config = Parse(config, powergate_pb2.StorageConfig())
        req = powergate_pb2.SetDefaultStorageConfigRequest(config=config)
        return self.client.SetDefaultStorageConfig(
            req, metadata=self.get_metadata(token)
        )

    def apply(
        self,
        cid,
        token: str = None,
        override: bool = False,
        config: str = None,
    ):
        if config:
            config = Parse(config, powergate_pb2.StorageConfig())

        req = powergate_pb2.ApplyStorageConfigRequest(
            cid=cid,
            override_config=override,
            has_override_config=override,
            config=config,
            has_config=config is not None,
        )
        return self.client.ApplyStorageConfig(req, metadata=self.get_metadata(token))

    def remove(self, cid: str, token: str = None):
        req = powergate_pb2.RemoveRequest(cid=cid)
        return self.client.Remove(req, metadata=self.get_metadata(token))
