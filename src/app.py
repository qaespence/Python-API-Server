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
    Add a new pet to the Pet Store.
    POST /pet

    Request JSON Body:
    - name (str): The name of the new pet.
    - category (str): The category of the new pet.
    - status (str): The status of the new pet.

    Returns:
    - If the pet is successfully added, return the pet's information with a status code of 201.
    - If there is a bad request or missing data, return a JSON message with a status code of 400.
    - If the added data exceeds the maximum allowed length, return a JSON message indicating 'Bad or missing data. Name/Category/Status too long' with a status code of 400.
    - If the new pet would be a duplicate, return a JSON message indicating 'Pet with the same name and category already exists' with a status code of 400.
    """
    data = request.get_json()

    # Return 400 if data is missing
    if 'name' not in data:
        abort(400, 'Bad or missing data. Missing name field')
    if 'category' not in data:
        abort(400, 'Bad or missing data. Missing category field')
    if 'status' not in data:
        abort(400, 'Bad or missing data. Missing status field')

    # Check and return 400 if data is too long
    if len(data['name']) > 100:
        abort(400, 'Bad or missing data. Name too long')
    if len(data['category']) > 100:
        abort(400, 'Bad or missing data. Category too long')
    if len(data['status']) > 100:
        abort(400, 'Bad or missing data. Status too long')

    # Return 400 if data is duplicated
    if any(pet['name'] == data['name'] and pet['category'] == data['category'] for pet in pets):
        abort(400, 'Pet with the same name and category already exists')

    # Build pet object
    pet_id = len(pets) + 1
    new_pet = {
        'id': pet_id,
        'name': data['name'],
        'category': data['category'],
        'status': data['status']
    }

    # Add pet to the database
    pets.append(new_pet)

    # Return the new pet with a status code of 201
    return jsonify(new_pet), 201


@app.route('/pet/<int:pet_id>', methods=['GET'])
def get_pet(pet_id):
    """
    Retrieve a pet from the Pet Store by ID.
    GET /pet/:pet_id

    Parameters:
    - pet_id (int): The unique identifier of the pet to retrieve.

    Returns:
    - If the pet is found, return the pet's information with a status code of 200.
    - If the pet is not found, return a JSON message indicating 'Pet not found' with a status code of 404.
    """
    # Retrieve the pet by ID
    pet = next((p for p in pets if p['id'] == pet_id), None)

    # Check if the pet is found
    if pet:
        return jsonify(pet), 200
    else:
        # Return a JSON message for a not-found pet with status code 404
        return jsonify({'message': 'Pet not found'}), 404


@app.route('/pet/<int:pet_id>', methods=['PUT'])
def update_pet(pet_id):
    """
    Update a pet in the Pet Store by ID.
    PUT /pet/:pet_id

    Parameters:
    - pet_id (int): The unique identifier of the pet to update.

    Request JSON Body:
    - name (str, optional): The updated name of the pet.
    - category (str, optional): The updated category of the pet.
    - status (str, optional): The updated status of the pet.

    Returns:
    - If the pet is found and successfully updated, return the updated pet's information with a status code of 200.
    - If the pet is not found, return a JSON message indicating 'Pet not found' with a status code of 404.
    - If the update would result in a duplicate pet, return a JSON message indicating 'Pet with the same name and category already exists' with a status code of 400.
    - If there is a bad request or missing data, return a JSON message with a status code of 400.
    - If the updated data exceeds the maximum allowed length, return a JSON message indicating 'Bad or missing data. Name/Category/Status too long' with a status code of 400.
    """
    # Retrieve payload data
    data = request.get_json()

    # Retrieve the pet by ID
    existing_pet = next((pet for pet in pets if pet['id'] == pet_id), None)

    # Return 404 if pet isn't found
    if not existing_pet:
        abort(404, 'Pet not found')

    # Return 400 if the update would result in a duplicate pet
    if 'name' in data:
        if any(
            pet['name'] == data['name']
            and pet['category'] == data['category']
            and pet['id'] != pet_id
            for pet in pets
        ):
            abort(400, 'Pet with the same name and category already exists')

    # Update the pet with the provided data
    if 'name' in data:
        # Check and update the name, if provided
        if len(data['name']) > 100:
            abort(400, 'Bad or missing data. Name too long')
        existing_pet['name'] = data['name']

    if 'category' in data:
        # Check and update the category, if provided
        if len(data['category']) > 100:
            abort(400, 'Bad or missing data. Category too long')
        existing_pet['category'] = data['category']

    if 'status' in data:
        # Check and update the status, if provided
        if len(data['status']) > 100:
            abort(400, 'Bad or missing data. Status too long')
        existing_pet['status'] = data['status']

    # Return the updated pet with a status code of 200
    return jsonify(existing_pet), 200


@app.route('/pet/<int:pet_id>', methods=['DELETE'])
def delete_pet(pet_id):
    """
    Delete a pet from the Pet Store by ID.
    DELETE /pet/:pet_id

    Parameters:
    - pet_id (int): The unique identifier of the pet to delete.

    Returns:
    - If the pet is found and successfully deleted, return a JSON message indicating 'Pet deleted' with a status code of 204 (No Content).
    - If the pet is not found, return a JSON message indicating 'Pet not found' with a status code of 404.
    """
    global pets

    # Retrieve the pet by ID
    pet = next((p for p in pets if p['id'] == pet_id), None)

    # Check if the pet is found
    if pet:
        # Remove the pet from the database
        pets = [p for p in pets if p['id'] != pet_id]
        return jsonify({'message': 'Pet deleted'}), 204
    else:
        # Return a JSON message for a not-found pet with status code 404
        return jsonify({'message': 'Pet not found'}), 404


@app.route('/pet/findByStatus', methods=['GET'])
def find_pet_by_status():
    """
    Find pets in the Pet Store by status.
    GET /pet/findByStatus?status=:statusType

    Query Parameters:
    - status (str): The status of the pets to retrieve. Should be one of 'available', 'pending', or 'sold'.

    Returns:
    - If the status parameter is missing, return a JSON message indicating 'Status parameter is missing' with a status code of 400.
    - If the status parameter is invalid, return a JSON message indicating 'Status parameter is invalid; should be available, pending, or sold' with a status code of 400.
    - If pets are found with the specified status, return the list of pets with a status code of 200.
    """
    status = request.args.get('status')

    # Return 400 if the status parameter is missing
    if not status:
        abort(400, 'Status parameter is missing')

    # Return 400 if the status is invalid
    if status not in ["available", "pending", "sold"]:
        abort(400, 'Status parameter is invalid; should be available, pending, or sold')

    # Find pets with the specified status
    found_pets = [pet for pet in pets if pet['status'] == status]

    # Return the found pets with a status code of 200
    return jsonify(found_pets), 200


@app.route('/pet/<int:pet_id>/uploadImage', methods=['POST'])
def upload_image(pet_id):
    """
    Upload an image for a pet in the Pet Store by ID.
    POST /pet/:pet_id/uploadImage

    Parameters:
    - pet_id (int): The unique identifier of the pet for which to upload an image.

    Request Form Data:
    - file (file): The image file to upload.

    Returns:
    - If the pet is found and the image is successfully uploaded, return a JSON message indicating 'File uploaded successfully' with a status code of 201.
    - If the pet is not found, return a JSON message indicating 'Pet not found' with a status code of 404.
    - If there is no file part in the request, return a JSON message indicating 'No file part' with a status code of 400.
    - If no selected file is provided, return a JSON message indicating 'No selected file' with a status code of 400.
    """
    pet = next((p for p in pets if p['id'] == pet_id), None)

    # Return 404 if the pet is not found
    if not pet:
        return jsonify({'message': 'Pet not found'}), 404

    # Return 400 if there is no file part in the request
    if 'file' not in request.files:
        abort(400, 'No file part')

    file = request.files['file']

    # Return 400 if no selected file is provided
    if file.filename == '':
        abort(400, 'No selected file')

    # Upload functionality TBD
    # For simplicity, just return a success message
    return jsonify({'message': 'File uploaded successfully'}), 201


# /inventory related endpoints
@app.route('/store/inventory', methods=['GET'])
def get_inventory():
    """
    Retrieve the inventory of the Pet Store.
    GET /store/inventory

    Returns:
    - The store's inventory as a JSON object with a status code of 200.
    """
    return jsonify(inventory), 200


@app.route('/store/inventory/add', methods=['POST'])
def add_to_inventory():
    """
    Add a quantity of a pet to the inventory of the Pet Store.
    POST /store/inventory/add

    Request JSON Body:
    - petId (int): The unique identifier of the pet to add to the inventory.
    - quantity (int): The quantity to add to the inventory.

    Returns:
    - If the data is successfully processed and the inventory is updated, return a JSON message indicating the added quantity with a status code of 200.
    - If there is a bad request or missing data, return a JSON message with a status code of 400.
    - If the specified pet is not found in the inventory, return a JSON message indicating 'Pet not found in inventory' with a status code of 404.
    """
    data = request.get_json()

    # Return 400 if data is missing
    if 'petId' not in data:
        abort(400, 'Bad or missing data. Missing petId field')
    if 'quantity' not in data:
        abort(400, 'Bad or missing data. Missing quantity field')

    pet_id = data['petId']
    quantity = data['quantity']

    # Return 404 if the specified pet is not found in the inventory
    if pet_id not in inventory:
        abort(404, 'Pet not found in inventory')

    # Update inventory by adding the specified quantity
    inventory[pet_id] += quantity

    # Return a JSON message indicating the added quantity with a status code of 200
    return jsonify({'message': f'Added {quantity} to inventory for pet {pet_id}'}), 200


@app.route('/store/inventory/remove', methods=['POST'])
def remove_from_inventory():
    """
    Remove a quantity of a pet from the inventory of the Pet Store.

    Request JSON Body:
    - petId (int): The unique identifier of the pet to remove from the inventory.
    - quantity (int): The quantity to remove from the inventory.

    Returns:
    - If the data is successfully processed and the inventory is updated, return a JSON message indicating the removed quantity.
    - If there is a bad request or missing data, return a JSON message with a status code of 400.
    - If the specified pet is not found in the inventory, return a JSON message indicating 'Pet not found in inventory' with a status code of 404.
    - If there is not enough quantity in the inventory, return a JSON message indicating 'Not enough quantity in inventory' with a status code of 400.
    """
    data = request.get_json()

    # Return 400 if data is missing
    if 'petId' not in data:
        abort(400, 'Bad or missing data. Missing petId field')
    if 'quantity' not in data:
        abort(400, 'Bad or missing data. Missing quantity field')

    pet_id = data['petId']
    quantity = data['quantity']

    # Return 404 if the specified pet is not found in the inventory
    if pet_id not in inventory:
        abort(404, 'Pet not found in inventory')

    # Check if there is enough quantity in the inventory
    if inventory[pet_id] < quantity:
        abort(400, 'Not enough quantity in inventory')

    # Update inventory by subtracting the specified quantity
    inventory[pet_id] -= quantity

    # Return a JSON message indicating the removed quantity
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
