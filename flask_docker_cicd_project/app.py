from flask import Flask, jsonify, request

app = Flask(__name__)

data_store = []

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Flask REST API!"})

@app.route("/items", methods=["GET"])
def get_items():
    return jsonify(data_store)

@app.route("/items", methods=["POST"])
def add_item():
    item = request.json
    data_store.append(item)
    return jsonify({"status": "Item added", "item": item}), 201

@app.route("/items/<int:index>", methods=["DELETE"])
def delete_item(index):
    try:
        removed = data_store.pop(index)
        return jsonify({"status": "Item removed", "item": removed})
    except IndexError:
        return jsonify({"error": "Item not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
