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


@pytest.fixture
def client():
    return OrderClient(f"http://{PACT_MOCK_HOST}:{PACT_MOCK_PORT}")


# ─── GET /orders/:id ────────────────────────────────────────────────────────

def test_get_pending_order(pact, client):
    (pact.given("order 1 exists with status pending")
         .upon_receiving("a request for a pending order")
         .with_request(method="GET", path="/orders/1")
         .will_respond_with(200, body={"id": 1, "product": "Laptop", "quantity": 2, "status": "pending"}))
    with pact:
        result = client.get_order(1)
    assert result["status"] == "pending"
    assert result["product"] == "Laptop"


def test_get_shipped_order(pact, client):
    (pact.given("order 2 exists with status shipped")
         .upon_receiving("a request for a shipped order")
         .with_request(method="GET", path="/orders/2")
         .will_respond_with(200, body={"id": 2, "product": "Mouse", "quantity": 5, "status": "shipped"}))
    with pact:
        result = client.get_order(2)
    assert result["status"] == "shipped"
    assert result["product"] == "Mouse"


def test_get_delivered_order(pact, client):
    (pact.given("order 3 exists with status delivered")
         .upon_receiving("a request for a delivered order")
         .with_request(method="GET", path="/orders/3")
         .will_respond_with(200, body={"id": 3, "product": "Monitor", "quantity": 1, "status": "delivered"}))
    with pact:
        result = client.get_order(3)
    assert result["status"] == "delivered"


def test_get_cancelled_order(pact, client):
    (pact.given("order 4 exists with status cancelled")
         .upon_receiving("a request for a cancelled order")
         .with_request(method="GET", path="/orders/4")
         .will_respond_with(200, body={"id": 4, "product": "Keyboard", "quantity": 3, "status": "cancelled"}))
    with pact:
        result = client.get_order(4)
    assert result["status"] == "cancelled"


def test_get_nonexistent_order(pact, client):
    (pact.given("order 99 does not exist")
         .upon_receiving("a request for a nonexistent order")
         .with_request(method="GET", path="/orders/99")
         .will_respond_with(404, body={"error": "Order not found"}))
    with pact:
        result = client.get_order(99)
    assert result is None


# ─── GET /orders ─────────────────────────────────────────────────────────────

def test_list_all_orders(pact, client):
    (pact.given("multiple orders exist")
         .upon_receiving("a request to list all orders")
         .with_request(method="GET", path="/orders")
         .will_respond_with(200, body=[
             {"id": 1, "product": "Laptop",   "quantity": 2, "status": "pending"},
             {"id": 2, "product": "Mouse",    "quantity": 5, "status": "shipped"},
             {"id": 3, "product": "Monitor",  "quantity": 1, "status": "delivered"},
             {"id": 4, "product": "Keyboard", "quantity": 3, "status": "cancelled"},
         ]))
    with pact:
        result = client.list_orders()
    assert isinstance(result, list)
    assert len(result) == 4


def test_list_orders_filtered_by_pending(pact, client):
    (pact.given("orders with status pending exist")
         .upon_receiving("a request to list pending orders")
         .with_request(method="GET", path="/orders", query="status=pending")
         .will_respond_with(200, body=[
             {"id": 1, "product": "Laptop", "quantity": 2, "status": "pending"}
         ]))
    with pact:
        result = client.list_orders(status="pending")
    assert all(o["status"] == "pending" for o in result)


def test_list_orders_filtered_by_shipped(pact, client):
    (pact.given("orders with status shipped exist")
         .upon_receiving("a request to list shipped orders")
         .with_request(method="GET", path="/orders", query="status=shipped")
         .will_respond_with(200, body=[
             {"id": 2, "product": "Mouse", "quantity": 5, "status": "shipped"}
         ]))
    with pact:
        result = client.list_orders(status="shipped")
    assert all(o["status"] == "shipped" for o in result)


def test_list_orders_filtered_by_delivered(pact, client):
    (pact.given("orders with status delivered exist")
         .upon_receiving("a request to list delivered orders")
         .with_request(method="GET", path="/orders", query="status=delivered")
         .will_respond_with(200, body=[
             {"id": 3, "product": "Monitor", "quantity": 1, "status": "delivered"}
         ]))
    with pact:
        result = client.list_orders(status="delivered")
    assert all(o["status"] == "delivered" for o in result)


def test_list_orders_filtered_by_cancelled(pact, client):
    (pact.given("orders with status cancelled exist")
         .upon_receiving("a request to list cancelled orders")
         .with_request(method="GET", path="/orders", query="status=cancelled")
         .will_respond_with(200, body=[
             {"id": 4, "product": "Keyboard", "quantity": 3, "status": "cancelled"}
         ]))
    with pact:
        result = client.list_orders(status="cancelled")
    assert all(o["status"] == "cancelled" for o in result)


def test_list_orders_invalid_status(pact, client):
    (pact.given("an invalid status filter is provided")
         .upon_receiving("a request to list orders with invalid status")
         .with_request(method="GET", path="/orders", query="status=invalid")
         .will_respond_with(400, body={"error": "Invalid status 'invalid'"}))
    with pact:
        result = client.list_orders(status="invalid")
    assert "error" in result


# ─── POST /orders ─────────────────────────────────────────────────────────────

def test_create_valid_order(pact, client):
    (pact.given("the provider is ready to accept new orders")
         .upon_receiving("a request to create a valid order")
         .with_request(method="POST", path="/orders",
                       headers={"Content-Type": "application/json"},
                       body={"product": "Headphones", "quantity": 1})
         .will_respond_with(201, body={"id": 5, "product": "Headphones", "quantity": 1, "status": "pending"}))
    with pact:
        result = client.create_order("Headphones", 1)
    assert result["status"] == "pending"
    assert result["product"] == "Headphones"


def test_create_order_missing_product(pact, client):
    (pact.given("the provider validates order fields")
         .upon_receiving("a request to create an order without product")
         .with_request(method="POST", path="/orders",
                       headers={"Content-Type": "application/json"},
                       body={"product": "", "quantity": 1})
         .will_respond_with(400, body={"error": "Product is required"}))
    with pact:
        result = client.create_order("", 1)
    assert "error" in result


def test_create_order_invalid_quantity(pact, client):
    (pact.given("the provider validates order fields")
         .upon_receiving("a request to create an order with zero quantity")
         .with_request(method="POST", path="/orders",
                       headers={"Content-Type": "application/json"},
                       body={"product": "Laptop", "quantity": 0})
         .will_respond_with(400, body={"error": "Quantity must be a positive integer"}))
    with pact:
        result = client.create_order("Laptop", 0)
    assert "error" in result


def test_create_order_negative_quantity(pact, client):
    (pact.given("the provider validates order fields")
         .upon_receiving("a request to create an order with negative quantity")
         .with_request(method="POST", path="/orders",
                       headers={"Content-Type": "application/json"},
                       body={"product": "Laptop", "quantity": -5})
         .will_respond_with(400, body={"error": "Quantity must be a positive integer"}))
    with pact:
        result = client.create_order("Laptop", -5)
    assert "error" in result


# ─── PATCH /orders/:id/status ─────────────────────────────────────────────────

def test_update_order_status_to_shipped(pact, client):
    (pact.given("order 1 exists and can be updated")
         .upon_receiving("a request to update order 1 status to shipped")
         .with_request(method="PATCH", path="/orders/1/status",
                       headers={"Content-Type": "application/json"},
                       body={"status": "shipped"})
         .will_respond_with(200, body={"id": 1, "product": "Laptop", "quantity": 2, "status": "shipped"}))
    with pact:
        result = client.update_status(1, "shipped")
    assert result["status"] == "shipped"


def test_update_order_status_to_delivered(pact, client):
    (pact.given("order 2 exists and can be updated")
         .upon_receiving("a request to update order 2 status to delivered")
         .with_request(method="PATCH", path="/orders/2/status",
                       headers={"Content-Type": "application/json"},
                       body={"status": "delivered"})
         .will_respond_with(200, body={"id": 2, "product": "Mouse", "quantity": 5, "status": "delivered"}))
    with pact:
        result = client.update_status(2, "delivered")
    assert result["status"] == "delivered"


def test_update_order_status_to_cancelled(pact, client):
    (pact.given("order 3 exists and can be updated")
         .upon_receiving("a request to update order 3 status to cancelled")
         .with_request(method="PATCH", path="/orders/3/status",
                       headers={"Content-Type": "application/json"},
                       body={"status": "cancelled"})
         .will_respond_with(200, body={"id": 3, "product": "Monitor", "quantity": 1, "status": "cancelled"}))
    with pact:
        result = client.update_status(3, "cancelled")
    assert result["status"] == "cancelled"


def test_update_status_nonexistent_order(pact, client):
    (pact.given("order 99 does not exist")
         .upon_receiving("a request to update status of nonexistent order")
         .with_request(method="PATCH", path="/orders/99/status",
                       headers={"Content-Type": "application/json"},
                       body={"status": "shipped"})
         .will_respond_with(404, body={"error": "Order not found"}))
    with pact:
        result = client.update_status(99, "shipped")
    assert result is None


def test_update_status_invalid_value(pact, client):
    (pact.given("order 1 exists and can be updated")
         .upon_receiving("a request to update order 1 with invalid status")
         .with_request(method="PATCH", path="/orders/1/status",
                       headers={"Content-Type": "application/json"},
                       body={"status": "unknown"})
         .will_respond_with(400, body={"error": "Invalid status 'unknown'"}))
    with pact:
        result = client.update_status(1, "unknown")
    assert "error" in result


# ─── DELETE /orders/:id ───────────────────────────────────────────────────────

def test_delete_existing_order(pact, client):
    (pact.given("order 4 exists and can be deleted")
         .upon_receiving("a request to delete order 4")
         .with_request(method="DELETE", path="/orders/4")
         .will_respond_with(200, body={"message": "Order 4 deleted"}))
    with pact:
        result = client.delete_order(4)
    assert "message" in result


def test_delete_nonexistent_order(pact, client):
    (pact.given("order 99 does not exist")
         .upon_receiving("a request to delete a nonexistent order")
         .with_request(method="DELETE", path="/orders/99")
         .will_respond_with(404, body={"error": "Order not found"}))
    with pact:
        result = client.delete_order(99)
    assert result is None


# ─── GET /health ──────────────────────────────────────────────────────────────

def test_health_check(pact, client):
    (pact.given("the provider is running")
         .upon_receiving("a health check request")
         .with_request(method="GET", path="/health")
         .will_respond_with(200, body={"status": "UP", "service": "OrderProvider"}))
    with pact:
        result = client.get_health()
    assert result["status"] == "UP"
    assert result["service"] == "OrderProvider"