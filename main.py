from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = 'inventory.json'

# Load existing data from JSON file
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r') as f:
        inventory = json.load(f)
else:
    inventory = []

# Automatically find the next ID
next_id = max([item['id'] for item in inventory], default=0) + 1

# Save to file
def save_to_file():
    with open(DATA_FILE, 'w') as f:
        json.dump(inventory, f, indent=4)

@app.route('/api/items', methods=['POST'])
def add_item():
    global next_id
    data = request.get_json()

    if not data or 'name' not in data or 'quantity' not in data:
        return jsonify({"error": "Missing 'name' or 'quantity'"}), 400

    item = {
        'id': next_id,
        'name': data['name'],
        'quantity': data['quantity']
    }
    inventory.append(item)
    next_id += 1
    save_to_file()
    return jsonify(item), 201

@app.route('/api/items', methods=['GET'])
def get_items():
    return jsonify(inventory)

@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    for item in inventory:
        if item['id'] == item_id:
            return jsonify(item)
    return jsonify({'error': 'Item not found'}), 404

@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.get_json()
    for item in inventory:
        if item['id'] == item_id:
            item['name'] = data.get('name', item['name'])
            item['quantity'] = data.get('quantity', item['quantity'])
            save_to_file()
            return jsonify(item)
    return jsonify({'error': 'Item not found'}), 404

@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global inventory
    inventory = [item for item in inventory if item['id'] != item_id]
    save_to_file()
    return jsonify({'message': 'Item deleted successfully'})
@app.route('/')
def home():
    return "Welcome to OJ Inventory API! Use /api/items to get data."
if __name__ == '__main__':
    app.run(debug=True)