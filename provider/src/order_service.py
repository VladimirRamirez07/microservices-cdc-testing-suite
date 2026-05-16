from flask import Flask, jsonify

app = Flask(__name__)

ORDERS = {
    1: {"id": 1, "product": "Laptop", "quantity": 2, "status": "pending"},
    2: {"id": 2, "product": "Mouse",  "quantity": 5, "status": "shipped"},
}

@app.route("/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    order = ORDERS.get(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    return jsonify(order), 200

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "UP"}), 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)