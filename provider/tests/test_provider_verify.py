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


def load_pact(pact_file):
    with open(pact_file) as f:
        pact_data = json.load(f)

    version = pact_data["metadata"]["pactSpecification"]["version"]
    pact = Pact.__new__(Pact)
    pact.consumer = pact_data["consumer"]["name"]
    pact.provider = pact_data["provider"]["name"]
    pact.version = version
    pact.semver = VersionInfo.parse(version)
    return pact, pact_data


def run_interaction(pact, interaction_data, provider_url):
    interaction = Interaction(pact, interaction_data, PytestResult)
    interaction.verify_with_callable_setup(provider_url, provider_state_setup)
    return interaction.result.success, interaction_data["description"]


# ─── GET /orders/:id ─────────────────────────────────────────────────────────

def test_provider_get_pending_order(provider_server):
    pact, pact_data = load_pact(PACT_FILE)
    provider_url = f"http://{PROVIDER_HOST}:{PROVIDER_PORT}"
    interaction = next(i for i in pact_data["interactions"]
                       if i["description"] == "a request for a pending order")
    success, desc = run_interaction(pact, interaction, provider_url)
    assert success, f"Failed: {desc}"


def test_provider_get_shipped_order(provider_server):
    pact, pact_data = load_pact(PACT_FILE)
    provider_url = f"http://{PROVIDER_HOST}:{PROVIDER_PORT}"
    interaction = next(i for i in pact_data["interactions"]
                       if i["description"] == "a request for a shipped order")
    success, desc = run_interaction(pact, interaction, provider_url)
    assert success, f"Failed: {desc}"


def test_provider_get_delivered_order(provider_server):
    pact, pact_data = load_pact(PACT_FILE)
    provider_url = f"http://{PROVIDER_HOST}:{PROVIDER_PORT}"
    interaction = next(i for i in pact_data["interactions"]
                       if i["description"] == "a request for a delivered order")
    success, desc = run_interaction(pact, interaction, provider_url)
    assert success, f"Failed: {desc}"


def test_provider_get_cancelled_order(provider_server):
    pact, pact_data = load_pact(PACT_FILE)
    provider_url = f"http://{PROVIDER_HOST}:{PROVIDER_PORT}"
    interaction = next(i for i in pact_data["interactions"]
                       if i["description"] == "a request for a cancelled order")
    success, desc = run_interaction(pact, interaction, provider_url)
    assert success, f"Failed: {desc}"


def test_provider_get_nonexistent_order(provider_server):
    pact, pact_data = load_pact(PACT_FILE)
    provider_url = f"http://{PROVIDER_HOST}:{PROVIDER_PORT}"
    interaction = next(i for i in pact_data["interactions"]
                       if i["description"] == "a request for a nonexistent order")
    success, desc = run_interaction(pact, interaction, provider_url)
    assert success, f"Failed: {desc}"


# ─── GET /orders ─────────────────────────────────────────────────────────────

def test_provider_list_all_orders(provider_server):
    pact, pact_data = load_pact(PACT_FILE)
    provider_url = f"http://{PROVIDER_HOST}:{PROVIDER_PORT}"
    interaction = next(i for i in pact_data["interactions"]
                       if i["description"] == "a request to list all orders")
    success, desc = run_interaction(pact, interaction, provider_url)
    assert success, f"Failed: {desc}"


def test_provider_list_pending_orders(provider_server):
    pact, pact_data = load_pact(PACT_FILE)
    provider_url = f"http://{PROVIDER_HOST}:{PROVIDER_PORT}"
    interaction = next(i for i in pact_data["interactions"]
                       if i["description"] == "a request to list pending orders")
    success, desc = run_interaction(pact, interaction, provider_url)
    assert success, f"Failed: {desc}"


def test_provider_list_shipped_orders(provider_server):
    pact, pact_data = load_pact(PACT_FILE)
    provider_url = f"http://{PROVIDER_HOST}:{PROVIDER_PORT}"
    interaction = next(i for i in pact_data["interactions"]
                       if i["description"] == "a request to list shipped orders")
    success, desc = run_interaction(pact, interaction, provider_url)
    assert success, f"Failed: {desc}"


def test_provider_list_delivered_orders(provider_server):
    pact, pact_data = load_pact(PACT_FILE)
    provider_url = f"http://{PROVIDER_HOST}:{PROVIDER_PORT}"
    interaction = next(i for i in pact_data["interactions"]
                       if i["description"] == "a request to list delivered orders")
    success, desc = run_interaction(pact, interaction, provider_url)
    assert success, f"Failed: {desc}"


def test_provider_list_cancelled_orders(provider_server):
    pact, pact_data = load_pact(PACT_FILE)
    provider_url = f"http://{PROVIDER_HOST}:{PROVIDER_PORT}"
    interaction = next(i for i in pact_data["interactions"]
                       if i["description"] == "a request to list cancelled orders")
    success, desc = run_interaction(pact, interaction, provider_url)
    assert success, f"Failed: {desc}"


def test_provider_list_orders_invalid_status(provider_server):
    pact, pact_data = load_pact(PACT_FILE)
    provider_url = f"http://{PROVIDER_HOST}:{PROVIDER_PORT}"
    interaction = next(i for i in pact_data["interactions"]
                       if i["description"] == "a request to list orders with invalid status")
    success, desc = run_interaction(pact, interaction, provider_url)
    assert success, f"Failed: {desc}"


# ─── POST /orders ─────────────────────────────────────────────────────────────

def test_provider_create_valid_order(provider_server):
    pact, pact_data = load_pact(PACT_FILE)
    provider_url = f"http://{PROVIDER_HOST}:{PROVIDER_PORT}"
    interaction = next(i for i in pact_data["interactions"]
                       if i["description"] == "a request to create a valid order")
    success, desc = run_interaction(pact, interaction, provider_url)
    assert success, f"Failed: {desc}"


def test_provider_create_order_missing_product(provider_server):
    pact, pact_data = load_pact(PACT_FILE)
    provider_url = f"http://{PROVIDER_HOST}:{PROVIDER_PORT}"
    interaction = next(i for i in pact_data["interactions"]
                       if i["description"] == "a request to create an order without product")
    success, desc = run_interaction(pact, interaction, provider_url)
    assert success, f"Failed: {desc}"


def test_provider_create_order_zero_quantity(provider_server):
    pact, pact_data = load_pact(PACT_FILE)
    provider_url = f"http://{PROVIDER_HOST}:{PROVIDER_PORT}"
    interaction = next(i for i in pact_data["interactions"]
                       if i["description"] == "a request to create an order with zero quantity")
    success, desc = run_interaction(pact, interaction, provider_url)
    assert success, f"Failed: {desc}"


def test_provider_create_order_negative_quantity(provider_server):
    pact, pact_data = load_pact(PACT_FILE)
    provider_url = f"http://{PROVIDER_HOST}:{PROVIDER_PORT}"
    interaction = next(i for i in pact_data["interactions"]
                       if i["description"] == "a request to create an order with negative quantity")
    success, desc = run_interaction(pact, interaction, provider_url)
    assert success, f"Failed: {desc}"


# ─── PATCH /orders/:id/status ─────────────────────────────────────────────────

def test_provider_update_status_to_shipped(provider_server):
    pact, pact_data = load_pact(PACT_FILE)
    provider_url = f"http://{PROVIDER_HOST}:{PROVIDER_PORT}"
    interaction = next(i for i in pact_data["interactions"]
                       if i["description"] == "a request to update order 1 status to shipped")
    success, desc = run_interaction(pact, interaction, provider_url)
    assert success, f"Failed: {desc}"


def test_provider_update_status_to_delivered(provider_server):
    pact, pact_data = load_pact(PACT_FILE)
    provider_url = f"http://{PROVIDER_HOST}:{PROVIDER_PORT}"
    interaction = next(i for i in pact_data["interactions"]
                       if i["description"] == "a request to update order 2 status to delivered")
    success, desc = run_interaction(pact, interaction, provider_url)
    assert success, f"Failed: {desc}"


def test_provider_update_status_to_cancelled(provider_server):
    pact, pact_data = load_pact(PACT_FILE)
    provider_url = f"http://{PROVIDER_HOST}:{PROVIDER_PORT}"
    interaction = next(i for i in pact_data["interactions"]
                       if i["description"] == "a request to update order 3 status to cancelled")
    success, desc = run_interaction(pact, interaction, provider_url)
    assert success, f"Failed: {desc}"


def test_provider_update_status_nonexistent_order(provider_server):
    pact, pact_data = load_pact(PACT_FILE)
    provider_url = f"http://{PROVIDER_HOST}:{PROVIDER_PORT}"
    interaction = next(i for i in pact_data["interactions"]
                       if i["description"] == "a request to update status of nonexistent order")
    success, desc = run_interaction(pact, interaction, provider_url)
    assert success, f"Failed: {desc}"


def test_provider_update_status_invalid_value(provider_server):
    pact, pact_data = load_pact(PACT_FILE)
    provider_url = f"http://{PROVIDER_HOST}:{PROVIDER_PORT}"
    interaction = next(i for i in pact_data["interactions"]
                       if i["description"] == "a request to update order 1 with invalid status")
    success, desc = run_interaction(pact, interaction, provider_url)
    assert success, f"Failed: {desc}"


# ─── DELETE /orders/:id ───────────────────────────────────────────────────────

def test_provider_delete_existing_order(provider_server):
    pact, pact_data = load_pact(PACT_FILE)
    provider_url = f"http://{PROVIDER_HOST}:{PROVIDER_PORT}"
    interaction = next(i for i in pact_data["interactions"]
                       if i["description"] == "a request to delete order 4")
    success, desc = run_interaction(pact, interaction, provider_url)
    assert success, f"Failed: {desc}"


def test_provider_delete_nonexistent_order(provider_server):
    pact, pact_data = load_pact(PACT_FILE)
    provider_url = f"http://{PROVIDER_HOST}:{PROVIDER_PORT}"
    interaction = next(i for i in pact_data["interactions"]
                       if i["description"] == "a request to delete a nonexistent order")
    success, desc = run_interaction(pact, interaction, provider_url)
    assert success, f"Failed: {desc}"


# ─── GET /health ──────────────────────────────────────────────────────────────

def test_provider_health_check(provider_server):
    pact, pact_data = load_pact(PACT_FILE)
    provider_url = f"http://{PROVIDER_HOST}:{PROVIDER_PORT}"
    interaction = next(i for i in pact_data["interactions"]
                       if i["description"] == "a health check request")
    success, desc = run_interaction(pact, interaction, provider_url)
    assert success, f"Failed: {desc}"