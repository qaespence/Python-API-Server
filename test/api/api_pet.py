import requests
from test.helpers.utils import load_config
from test.api.basic_requests import post, get, put, delete


def add_pet(name: str = None, category: str = None, status: str = None):
    """
    Test the functionality of adding a new pet to the Pet Store.

    Parameters:
    - payload (dict): The payload containing pet data to be added.

    Returns:
    - If the pet is successfully added, return a tuple containing the JSON response and the HTTP status code with a status code of 201.
    - If there is an error during the request, return a tuple containing the error message and the HTTP status code received in the response.
    """

    payload = {}
    if name is not None:
        payload["name"] = name
    if category is not None:
        payload["category"] = category
    if status is not None:
        payload["status"] = status

    return post("/pet", payload, {"content-type": "application/json"})


def get_pet(pet_id):
    """
    Test the functionality of retrieving a pet from the Pet Store by ID.

    Parameters:
    - pet_id (int): The unique identifier of the pet to retrieve.

    Returns:
    - If the pet is found, return a tuple containing the JSON response and the HTTP status code with a status code of 200.
    - If the pet is not found, return a tuple containing the error message 'Pet not found' and the HTTP status code with a status code of 404.
    - If there is an error during the request, return a tuple containing the error message and the HTTP status code received in the response.
    """

    return get(f"/pet/{pet_id}")


def update_pet(pet_id, name: str = None, category: str = None, status: str = None):
    """
    Test the functionality of updating a pet in the Pet Store by ID.

    Parameters:
    - pet_id (int): The unique identifier of the pet to update.
    - payload (dict): The payload containing pet data to be updated.

    Returns:
    - If the pet is successfully updated, return a tuple containing the JSON response and the HTTP status code with a status code of 200.
    - If the pet is not found, return a tuple containing the error message 'Pet not found' and the HTTP status code with a status code of 404.
    - If there is an error during the request, return a tuple containing the error message and the HTTP status code received in the response.
    """

    payload = {}
    if name is not None:
        payload["name"] = name
    if category is not None:
        payload["category"] = category
    if status is not None:
        payload["status"] = status

    return put(f"/pet/{pet_id}", payload, {"content-type": "application/json"})


def delete_pet(pet_id):
    """
    Test the functionality of deleting a pet from the Pet Store by ID.

    Parameters:
    - pet_id (int): The unique identifier of the pet to delete.

    Returns:
    - If the pet is successfully deleted, return a tuple containing the success message and the HTTP status code with a status code of 200.
    - If the pet is not found, return a tuple containing the error message 'Pet not found' and the HTTP status code with a status code of 404.
    - If there is an error during the request, return a tuple containing the error message and the HTTP status code received in the response.
    """

    return delete(f"/pet/{pet_id}")
