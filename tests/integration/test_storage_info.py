import logging

import pytest

from pygate_grpc.client import PowerGateClient
from pygate_grpc.exceptions import GRPCTimeoutException
from pygate_grpc.types import CidInfo, StagedFile, User

logger = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def user(pygate_client: PowerGateClient):
    return pygate_client.admin.users.create()


@pytest.fixture(scope="module")
def staged_file(pygate_client: PowerGateClient, user: User):
    original_file_contents = b"Another file for staging and testing"
    staged_file = pygate_client.data.stage_bytes(
        original_file_contents, token=user.token
    )
    pygate_client.config.apply(staged_file.cid, token=user.token, override=True)
    return staged_file


def test_storage_info(
    pygate_client: PowerGateClient, user: User, staged_file: StagedFile
):
    storage_info_list = pygate_client.storage_info.list(
        cids=[staged_file.cid], token=user.token
    )
    assert len(storage_info_list) == 0
