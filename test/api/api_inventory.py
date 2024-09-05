from test.api.basic_requests import get, post


def get_inventory():
    """
    Test the functionality of retrieving the inventory from the Pet Store by category.

    Returns:
    - The JSON response and HTTP status code from the GET request.
    """
    return get("/store/inventory")


def add_to_inventory(category: str, quantity: int):
    """
    Test the functionality of adding a quantity of a pet category to the inventory.

    Parameters:
    - category (str): The category of the pet to add to the inventory.
    - quantity (int): The quantity to add to the inventory.

    Returns:
    - The JSON response and HTTP status code from the POST request.
    """
    payload = {
        "category": category,
        "quantity": quantity
    }
    return post("/store/inventory/add", payload)


def remove_from_inventory(category: str, quantity: int):
    """
    Test the functionality of removing a quantity of a pet category from the inventory.

    Parameters:
    - category (str): The category of the pet to remove from the inventory.
    - quantity (int): The quantity to remove from the inventory.

    Returns:
    - The JSON response and HTTP status code from the POST request.
    """
    payload = {
        "category": category,
        "quantity": quantity
    }
    return post("/store/inventory/remove", payload)
