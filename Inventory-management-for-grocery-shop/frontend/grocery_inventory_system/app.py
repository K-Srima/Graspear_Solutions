from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# Initial Inventory
inventory = [
    {"name": "Apple", "category": "Fruits", "unit": "kg", "stock": 50, "price": 150},
    {"name": "Orange", "category": "Fruits", "unit": "kg", "stock": 40, "price": 120},
    {"name": "Potato", "category": "Vegetables", "unit": "kg", "stock": 100, "price": 25},
    {"name": "Rice", "category": "Grains", "unit": "kg", "stock": 200, "price": 50},
    {"name": "Milk", "category": "Dairy", "unit": "liter", "stock": 100, "price": 60},
    {"name": "Biscuits", "category": "Packaged Foods", "unit": "pack", "stock": 60, "price": 30}
]

@app.route("/")
def home():
    return "Welcome to the Grocery Inventory System!"

@app.route("/place-order", methods=["POST"])
def place_order():
    try:
        data = request.get_json()
        items = data.get("items", [])

        if not items:
            return jsonify({"error": "No items in the order"}), 400

        total_weight = 0
        total_cost = 0
        updated_inventory = []

        for order in items:
            item_name = order.get("name")
            quantity = order.get("quantity")

            # Check if quantity is a valid integer and not negative
            if not isinstance(quantity, int) or quantity <= 0:
                return jsonify({"error": f"Invalid quantity for item '{item_name}'"}), 400

            item = next((i for i in inventory if i["name"].lower() == item_name.lower()), None)

            if not item:
                return jsonify({"error": f"Item '{item_name}' not found in inventory"}), 400

            # If quantity requested exceeds stock, set it to available stock
            if quantity > item["stock"]:
                quantity = item["stock"]

            cost = quantity * item["price"]
            total_weight += quantity
            total_cost += cost
            item["stock"] -= quantity

            updated_inventory.append({
                "name": item["name"],
                "remaining": item["stock"],
                "lowStock": item["stock"] < 5
            })

        return jsonify({
            "totalWeight": total_weight,
            "totalCost": total_cost,
            "inventory": updated_inventory
        })

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
