import json
import logging
import os
from pathlib import Path

import pytest

from pygate_grpc.client import PowerGateClient
from pygate_grpc.types import Job, User

logger = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def user(pygate_client: PowerGateClient):
    return pygate_client.admin.users.create()


def test_get_default_config(pygate_client: PowerGateClient, user: User):
    default_config = pygate_client.config.default(user.token)

    assert type(default_config) is dict


def test_replace_default_config(pygate_client: PowerGateClient, user: User):
    path = Path(os.path.abspath(__file__))
    with open(path.parent / "assets" / "cidconfig_example.json", "r") as f:
        new_config = json.load(f)

    pygate_client.config.set_default(new_config, user.token)

    default_config = pygate_client.config.default(user.token)

    assert type(default_config) == dict
    assert default_config == new_config


def test_apply_config(pygate_client: PowerGateClient, user: User):
    config = pygate_client.config.default(user.token)

    config["cold"]["filecoin"]["address"] = pygate_client.wallet.addresses(
        token=user.token
    )[-1].address

    file_bytes = b"This is a test file for stagiiing"
    staged_file = pygate_client.data.stage_bytes(file_bytes, token=user.token)

    job = pygate_client.config.apply(
        staged_file.cid,
        token=user.token,
        config=config,
        override=True,
        no_exec=False,
        import_deal_ids=[],
    )

    assert type(job) == Job


def test_remove(pygate_client: PowerGateClient, user: User):
    config = pygate_client.config.default(user.token)
    config["cold"]["enabled"] = False
    config["hot"]["enabled"] = False

    file_bytes = b"test files"
    staged_file = pygate_client.data.stage_bytes(file_bytes, token=user.token)

    pygate_client.config.apply(staged_file.cid, token=user.token, config=config)

    pygate_client.config.remove(staged_file.cid, token=user.token)
