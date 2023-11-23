# Pet Store API

This project implements a simple Pet Store API using Flask. It provides endpoints to manage pets, users, and store operations.

## API Server

### Installation

1. Install Python (if not already installed).

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

### Running the API Server

Start the Flask application:

```bash
python app.py
```

The API server will be accessible at http://127.0.0.1:5000/.

## API Endpoints

### Pet Operations

#### `POST /pet` Add a new pet.

#### `GET /pet/{petId}` Retrieve details of a specific pet.

#### `PUT /pet/{petId}` Update details of a specific pet.

#### `DELETE /pet/{petId}` Delete a specific pet.

#### `GET /pet/findByStatus` Find pets by status.

### User Operations

#### `POST /user` Create a new user.

#### `GET /user/{username}` Retrieve details of a specific user.

#### `PUT /user/{username}` Update details of a specific user.

#### `DELETE /user/{username}` Delete a specific user.

#### `GET /user/login` User login.

### Store Operations

#### `POST /store/order` Place a new order.

#### `GET /store/order/{orderId}` Retrieve details of a specific order.

#### `DELETE /store/order/{orderId}` Delete a specific order.

#### `GET /store/orders` Retrieve all orders.

#### `GET /store/inventory` Retrieve current inventory.

#### `POST /store/inventory/add` Add to inventory.

#### `POST /store/inventory/remove` Remove from inventory.

## Testing
### Installation

1. Install Python (if not already installed).
2. Install dependencies:

```bash
pip install -r requirements-test.txt
```

### Running Tests

Run the tests using pytest:

```bash
pytest
```

Ensure that the API server is running before executing the tests.



