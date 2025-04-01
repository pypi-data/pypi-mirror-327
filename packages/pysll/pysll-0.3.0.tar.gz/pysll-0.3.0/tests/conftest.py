import datetime
import json
import logging
import os
import random
import string
from zoneinfo import ZoneInfo

import boto3
import pytest

from pysll import Constellation


@pytest.fixture(scope="session")
def client():
    """Helper function to retrieve an actively logged in client.

    This uses AWS secrets manager to retrieve credentials.  If you do
    not have access to ECL'S AWS secrets manager, you must override this
    function in order to run the tests.
    """

    # Now, get an auth token by logging into constellation for each environment
    client = Constellation(host="https://constellation-stage.emeraldcloudlab.com")
    try:
        with open("./.auth") as handle:
            auth_token = handle.readline().strip()
    except FileNotFoundError:
        secrets_client = boto3.session.Session().client(service_name="secretsmanager")  # type: ignore
        credentials_secret = secrets_client.get_secret_value(SecretId="manifold-service-user-constellation-credentials")
        credentials_dict = json.loads(credentials_secret["SecretString"])
        username = credentials_dict["username"]
        password = credentials_dict["password"]
        client.login(username, password)
    else:
        logging.warning("Loaded credentials from .auth file")
        client._auth_token = auth_token

    return client


@pytest.fixture(scope="session")
def sample_file():
    test_file_path = f"cloud-file-test_{''.join(random.choices(string.ascii_lowercase, k=12))}.txt"

    entropy = "".join(random.choices(string.printable, k=30))
    contents = "\n".join(
        [
            "cloud file test!",
            f"generated on: {datetime.datetime.now(tz=ZoneInfo('UTC')).isoformat()}",
            f"here's some entropy: {entropy}",
        ]
    )
    with open(test_file_path, "w") as f:
        f.write(contents)

    yield test_file_path, contents

    try:
        os.remove(test_file_path)
    except FileNotFoundError:
        pass
