import pytest
from pactman import Consumer, Provider
from consumer.src.order_client import OrderClient

PACT_MOCK_HOST = "localhost"
PACT_MOCK_PORT = 9001
PACT_DIR = "pacts"


@pytest.fixture(scope="module")
def pact():
    pact = Consumer("OrderConsumer").has_pact_with(
        Provider("OrderProvider"),
        host_name=PACT_MOCK_HOST,
        port=PACT_MOCK_PORT,
        pact_dir=PACT_DIR,
    )
    pact.start_mocking()
    yield pact
    pact.stop_mocking()


def test_get_existing_order(pact):
    expected_order = {
        "id": 1,
        "product": "Laptop",
        "quantity": 2,
        "status": "pending",
    }

    (
        pact.given("order 1 exists")
        .upon_receiving("a request for order 1")
        .with_request(method="GET", path="/orders/1")
        .will_respond_with(200, body=expected_order)
    )

    client = OrderClient(f"http://{PACT_MOCK_HOST}:{PACT_MOCK_PORT}")

    with pact:
        result = client.get_order(1)

    assert result["id"] == 1
    assert result["product"] == "Laptop"
    assert result["quantity"] == 2
    assert result["status"] == "pending"


def test_get_nonexistent_order(pact):
    (
        pact.given("order 99 does not exist")
        .upon_receiving("a request for a nonexistent order")
        .with_request(method="GET", path="/orders/99")
        .will_respond_with(404, body={"error": "Order not found"})
    )

    client = OrderClient(f"http://{PACT_MOCK_HOST}:{PACT_MOCK_PORT}")

    with pact:
        result = client.get_order(99)

    assert result is None