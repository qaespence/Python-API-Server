from flask import Flask, jsonify, request, abort
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

# Dummy data to simulate a database
pets = []
inventory = {}
orders = []
users = []


# /pet related endpoints/functions
@app.route('/pet', methods=['POST'])
def add_pet():
    """
    add_pet - function for POST /pet
    @return: success: pet object, status code; failure: message, status code
    """
    data = request.get_json()

    # return 400 if data is missing
    if 'name' not in data:
        abort(400, 'Bad or missing data. Missing name field')
    if 'category' not in data:
        abort(400, 'Bad or missing data. Missing category field')
    if 'status' not in data:
        abort(400, 'Bad or missing data. Missing status field')

    # return 400 if data is too long
    if len(data['name']) > 100:
        abort(400, 'Bad or missing data. Name too long')
    if len(data['category']) > 100:
        abort(400, 'Bad or missing data. Category too long')
    if len(data['status']) > 100:
        abort(400, 'Bad or missing data. Status too long')

    # return 400 if data is duplicated
    if any(pet['name'] == data['name'] and pet['category'] == data['category'] for pet in pets):
        abort(400, 'Pet with the same name and category already exists')

    # build pet object
    pet_id = len(pets) + 1
    new_pet = {
        'id': pet_id,
        'name': data['name'],
        'category': data['category'],
        'status': data['status']
    }
    # add pet to DB
    pets.append(new_pet)
    return jsonify(new_pet), 201


@app.route('/pet/<int:pet_id>', methods=['GET'])
def get_pet(pet_id):
    """
    get_pet - function for GET /pet/{id}
    @param pet_id: pet id/token
    @return: success: pet object, status code; failure: message, status code
    """
    pet = next((p for p in pets if p['id'] == pet_id), None)
    if pet:
        return jsonify(pet), 200
    else:
        return jsonify({'message': 'Pet not found'}), 404


@app.route('/pet/<int:pet_id>', methods=['PUT'])
def update_pet(pet_id):
    """
    update_pet - function for PUT /pet/{id}
    @param pet_id: pet id/token
    @return: success: pet object, status code; failure: message, status code
    """
    data = request.get_json()

    existing_pet = next((pet for pet in pets if pet['id'] == pet_id), None)
    # return 404 if pet isn't found
    if not existing_pet:
        abort(404, 'Pet not found')

    # return 400 if pet will be a duplicate
    if any(
        pet['name'] == data['name']
        and pet['category'] == data['category']
        and pet['id'] != pet_id
        for pet in pets
    ):
        abort(400, 'Pet with the same name and category already exists')

    # return 400 if data is missing
    if data['name'] is not None:
        existing_pet['name'] = data['name']
    if data['category'] is not None:
        existing_pet['category'] = data['category']
    if data['status'] is not None:
        existing_pet['status'] = data['status']

    return jsonify(existing_pet), 200


@app.route('/pet/<int:pet_id>', methods=['DELETE'])
def delete_pet(pet_id):
    """
    delete_pet - function for DELETE /pet/{id}
    @param pet_id: pet id/token
    @return: message, status code
    """
    global pets
    pet = next((p for p in pets if p['id'] == pet_id), None)
    if pet:
        pets = [p for p in pets if p['id'] != pet_id]
        return jsonify({'message': 'Pet deleted'}), 204
    else:
        return jsonify({'message': 'Pet not found'}), 404


@app.route('/pet/findByStatus', methods=['GET'])
def find_pet_by_status():
    """
    find_pet_by_status - function for GET /pet/findByStatus
    @return: success: pet object(s), status code; failure: message, status code
    """
    status = request.args.get('status')

    # return 400 if status URL parameter missing
    if not status:
        abort(400, 'Status parameter is missing')

    # return 400 if status is bad
    if status not in ["available", "pending", "sold"]:
        abort(400, 'Status parameter is invalid; should be available, pending or sold')

    found_pets = [pet for pet in pets if pet['status'] == status]

    return jsonify(found_pets), 200


@app.route('/pet/<int:pet_id>/uploadImage', methods=['POST'])
def upload_image(pet_id):
    """
    upload_image - function for POST /pet/:pet_id/uploadImage
    @param pet_id: pet id/token
    @return: message, status code
    """
    pet = next((p for p in pets if p['id'] == pet_id), None)

    # return 404 if not found
    if not pet:
        return jsonify({'message': 'Pet not found'}), 404

    # return 400 if file not valid
    if 'file' not in request.files:
        abort(400, 'No file part')

    file = request.files['file']

    # return 400 if file missing
    if file.filename == '':
        abort(400, 'No selected file')

    # Upload functionality TBD
    # For simplicity, just return a success message
    return jsonify({'message': 'File uploaded successfully'}), 201


# /inventory related endpoints
@app.route('/store/inventory', methods=['GET'])
def get_inventory():
    """
    get_inventory - function for GET /store/inventory
    @return: inventory data/object, status code
    """
    return jsonify(inventory), 200


@app.route('/store/inventory/add', methods=['POST'])
def add_to_inventory():
    data = request.get_json()

    if 'petId' not in data:
        abort(400, 'Bad or missing data. Missing petId field')
    if 'quantity' not in data:
        abort(400, 'Bad or missing data. Missing quantity field')

    pet_id = data['petId']
    quantity = data['quantity']

    if pet_id not in inventory:
        abort(404, 'Pet not found in inventory')

    # Update inventory by adding the specified quantity
    inventory[pet_id] += quantity

    return jsonify({'message': f'Added {quantity} to inventory for pet {pet_id}'})


@app.route('/store/inventory/remove', methods=['POST'])
def remove_from_inventory():
    data = request.get_json()

    if 'petId' not in data:
        abort(400, 'Bad or missing data. Missing petId field')
    if 'quantity' not in data:
        abort(400, 'Bad or missing data. Missing quantity field')

    pet_id = data['petId']
    quantity = data['quantity']

    if pet_id not in inventory:
        abort(404, 'Pet not found in inventory')

    # Check if there is enough quantity in the inventory
    if inventory[pet_id] < quantity:
        abort(400, 'Not enough quantity in inventory')

    # Update inventory by subtracting the specified quantity
    inventory[pet_id] -= quantity

    return jsonify({'message': f'Removed {quantity} from inventory for pet {pet_id}'})


# /order related endpoints
@app.route('/store/order', methods=['POST'])
def place_order():
    data = request.get_json()

    if 'petId' not in data:
        abort(400, 'Bad or missing data. Missing petId field')
    if 'quantity' not in data:
        abort(400, 'Bad or missing data. Missing quantity field')

    pet_id = data['petId']
    quantity = data['quantity']

    # Check if the pet is available in the inventory
    if pet_id not in inventory or inventory[pet_id] < quantity:
        abort(400, 'Not enough inventory for the specified pet')

    # Update inventory (for simplicity, we are not handling concurrency here)
    inventory[pet_id] -= quantity

    # Create an order (store orders in the 'orders' list)
    order_id = len(orders) + 1
    order = {
        'orderId': order_id,
        'petId': pet_id,
        'quantity': quantity,
        'status': 'placed'
    }
    orders.append(order)

    return jsonify(order), 201


@app.route('/store/order/<int:order_id>', methods=['GET'])
def get_order(order_id):
    # Check if the order exists
    if not (1 <= order_id <= len(orders)):
        return jsonify({'message': 'Order not found'}), 404

    return jsonify(orders[order_id - 1])


@app.route('/store/orders', methods=['GET'])
def get_all_orders():
    return jsonify(orders)


@app.route('/store/order/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    # Check if the order exists
    if not (1 <= order_id <= len(orders)):
        return jsonify({'message': 'Order not found'}), 404

    # Delete the order
    deleted_order = orders.pop(order_id - 1)

    return jsonify({'message': f'Order {order_id} deleted', 'deleted_order': deleted_order})


# /users related endpoints
def find_user_by_username(username):
    return next((user for user in users if user['username'] == username), None)


def find_user_by_id(user_id):
    return next((user for user in users if user['id'] == user_id), None)


@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()

    if 'username' not in data:
        abort(400, 'Bad or missing data. Missing username field')
    if 'email' not in data:
        abort(400, 'Bad or missing data. Missing email field')
    if 'password' not in data:
        abort(400, 'Bad or missing data. Missing password field')

    existing_user = find_user_by_username(data['username'])
    if existing_user:
        abort(400, 'Username already exists')

    user_id = len(users) + 1
    new_user = {
        'id': user_id,
        'username': data['username'],
        'email': data['email'],
        'password': data['password']
    }
    users.append(new_user)

    return jsonify(new_user), 201


@app.route('/user/login', methods=['GET'])
def login_user():
    username = request.args.get('username')
    password = request.args.get('password')

    if not username:
        abort(400, 'Bad or missing data. Missing username field')
    if not password:
        abort(400, 'Bad or missing data. Missing password field')

    user = find_user_by_username(username)

    if not user or user['password'] != password:
        abort(401, 'Invalid username or password')

    return jsonify({'message': 'Login successful'})


@app.route('/user/<username>', methods=['GET'])
def get_user_by_username(username):
    user = find_user_by_username(username)

    if user:
        return jsonify(user)
    else:
        return jsonify({'message': 'User not found'}), 404


@app.route('/user/<username>', methods=['PUT'])
def update_user(username):
    user = find_user_by_username(username)

    if not user:
        return jsonify({'message': 'User not found'}), 404

    data = request.get_json()

    if 'email' not in data:
        abort(400, 'Bad or missing data. Missing email field')
    if 'password' not in data:
        abort(400, 'Bad or missing data. Missing password field')

    user['email'] = data['email']
    user['password'] = data['password']

    return jsonify(user)


@app.route('/user/<username>', methods=['DELETE'])
def delete_user(username):
    global users
    users = [user for user in users if user['username'] != username]

    return jsonify({'message': f'User {username} deleted'})


if __name__ == '__main__':
    app.run(debug=True)
