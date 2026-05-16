import pytest
import threading
import time
import json
from semver import VersionInfo
from pactman.verifier.verify import Interaction
from pactman.verifier.result import PytestResult
from pactman.mock.pact import Pact
from provider.src.order_service import app

PROVIDER_HOST = "localhost"
PROVIDER_PORT = 5001
PACT_FILE = "pacts/OrderConsumer-OrderProvider-pact.json"


@pytest.fixture(scope="module")
def provider_server():
    server = threading.Thread(
        target=lambda: app.run(host=PROVIDER_HOST, port=PROVIDER_PORT, use_reloader=False),
        daemon=True,
    )
    server.start()
    time.sleep(1)
    yield


def provider_state_setup(state, **kwargs):
    pass


def test_provider_honors_consumer_pact(provider_server):
    with open(PACT_FILE) as f:
        pact_data = json.load(f)

    version = pact_data["metadata"]["pactSpecification"]["version"]

    pact = Pact.__new__(Pact)
    pact.consumer = pact_data["consumer"]["name"]
    pact.provider = pact_data["provider"]["name"]
    pact.version = version
    pact.semver = VersionInfo.parse(version)

    provider_url = f"http://{PROVIDER_HOST}:{PROVIDER_PORT}"
    failures = []

    for interaction_data in pact_data["interactions"]:
        interaction = Interaction(pact, interaction_data, PytestResult)
        interaction.verify_with_callable_setup(provider_url, provider_state_setup)
        if not interaction.result.success:
            failures.append(interaction_data["description"])

    assert not failures, f"Failed interactions: {failures}"