from flask import Flask, jsonify, request

app = Flask(__name__)

ORDERS = {
    1: {"id": 1, "product": "Laptop",   "quantity": 2, "status": "pending"},
    2: {"id": 2, "product": "Mouse",    "quantity": 5, "status": "shipped"},
    3: {"id": 3, "product": "Monitor",  "quantity": 1, "status": "delivered"},
    4: {"id": 4, "product": "Keyboard", "quantity": 3, "status": "cancelled"},
}

VALID_STATUSES = {"pending", "shipped", "delivered", "cancelled"}


@app.route("/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    order = ORDERS.get(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    return jsonify(order), 200


@app.route("/orders", methods=["GET"])
def list_orders():
    status = request.args.get("status")
    if status:
        if status not in VALID_STATUSES:
            return jsonify({"error": f"Invalid status '{status}'"}), 400
        result = [o for o in ORDERS.values() if o["status"] == status]
    else:
        result = list(ORDERS.values())
    return jsonify(result), 200


@app.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}), 400
    if not data.get("product"):
        return jsonify({"error": "Product is required"}), 400
    if not isinstance(data.get("quantity"), int) or data["quantity"] <= 0:
        return jsonify({"error": "Quantity must be a positive integer"}), 400

    new_id = max(ORDERS.keys()) + 1
    order = {
        "id": new_id,
        "product": data["product"],
        "quantity": data["quantity"],
        "status": "pending",
    }
    ORDERS[new_id] = order
    return jsonify(order), 201


@app.route("/orders/<int:order_id>/status", methods=["PATCH"])
def update_status(order_id):
    order = ORDERS.get(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    data = request.get_json()
    new_status = data.get("status") if data else None
    if not new_status or new_status not in VALID_STATUSES:
        return jsonify({"error": f"Invalid status '{new_status}'"}), 400
    order["status"] = new_status
    return jsonify(order), 200


@app.route("/orders/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):
    order = ORDERS.pop(order_id, None)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    return jsonify({"message": f"Order {order_id} deleted"}), 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "UP", "service": "OrderProvider"}), 200


if __name__ == "__main__":
    app.run(port=5000, debug=True)