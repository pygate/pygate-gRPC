import logging

import pytest

from pygate_grpc.client import PowerGateClient
from pygate_grpc.exceptions import GRPCTimeoutException
from pygate_grpc.types import CidInfo, CidSummary, StagedFile, User

logger = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def user(pygate_client: PowerGateClient):
    return pygate_client.admin.users.create()


@pytest.fixture(scope="module")
def staged_file(pygate_client: PowerGateClient, user: User):
    original_file_contents = b"Some random bytes"
    staged_file = pygate_client.data.stage_bytes(
        original_file_contents, token=user.token
    )
    pygate_client.config.apply(staged_file.cid, token=user.token, override=True)
    return staged_file


def test_get_data(pygate_client: PowerGateClient, user: User):
    original_file_contents = b"Some random bytes"
    staged_file = pygate_client.data.stage_bytes(
        original_file_contents, token=user.token
    )
    pygate_client.config.apply(staged_file.cid, token=user.token)
    retrieved_file_contents = pygate_client.data.get(staged_file.cid, token=user.token)

    assert original_file_contents == retrieved_file_contents


def test_cid_info(pygate_client: PowerGateClient, user: User, staged_file: StagedFile):
    cid_info = pygate_client.data.cid_info(staged_file.cid, token=user.token)
    assert isinstance(cid_info, CidInfo)


def test_cid_summary(
    pygate_client: PowerGateClient, user: User, staged_file: StagedFile
):
    cid_summary_list = pygate_client.data.cid_summary(
        cids=[staged_file.cid], token=user.token
    )
    assert len(cid_summary_list) > 0
    assert isinstance(cid_summary_list[0], CidSummary)


def test_logs(pygate_client: PowerGateClient, user: User, staged_file: StagedFile):
    logs_res = pygate_client.data.watch_logs(
        staged_file.cid, user.token, history=True, timeout=5
    )

    logs = []
    try:
        for f in logs_res:
            logs.append(f)
    except GRPCTimeoutException:
        pass

    assert len(logs) > 0
