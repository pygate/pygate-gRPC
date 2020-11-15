import json

from google.protobuf.json_format import Parse
from powergate.user.v1 import user_pb2, user_pb2_grpc

from pygate_grpc.decorators import unmarshal_with
from pygate_grpc.errors import ErrorHandlerMeta
from pygate_grpc.types import Job


class ConfigClient(object, metaclass=ErrorHandlerMeta):
    def __init__(self, channel, get_metadata):
        self.client = user_pb2_grpc.UserServiceStub(channel)
        self.get_metadata = get_metadata

    @unmarshal_with()
    def default(self, token: str = None) -> dict:
        req = user_pb2.DefaultStorageConfigRequest()
        return self.client.DefaultStorageConfig(
            req, metadata=self.get_metadata(token)
        ).default_storage_config

    # Currently you need to pass in the user_pb2.DefaultConfig. However, this is not a good design.
    def set_default(self, config: str, token: str = None):
        if type(config) == dict:
            config = json.dumps(config)

        config = Parse(config, user_pb2.StorageConfig())
        req = user_pb2.SetDefaultStorageConfigRequest(config=config)
        return self.client.SetDefaultStorageConfig(
            req, metadata=self.get_metadata(token)
        )

    @unmarshal_with(Job)
    def apply(
        self, cid, token: str = None, override: bool = False, config: str = None,
    ) -> Job:
        if type(config) == dict:
            config = json.dumps(config)

        if config:
            config = Parse(config, user_pb2.StorageConfig())

        req = user_pb2.ApplyStorageConfigRequest(
            cid=cid,
            override_config=override,
            has_override_config=override,
            config=config,
            has_config=config is not None,
        )
        return self.client.ApplyStorageConfig(req, metadata=self.get_metadata(token))

    def remove(self, cid: str, token: str = None):
        req = user_pb2.RemoveRequest(cid=cid)
        return self.client.Remove(req, metadata=self.get_metadata(token))
