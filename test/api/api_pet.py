import requests
from test.helpers.utils import load_config


def add_pet(payload):
    """
    Test the functionality of adding a new pet to the Pet Store.

    Parameters:
    - payload (dict): The payload containing pet data to be added.

    Returns:
    - If the pet is successfully added, return a tuple containing the JSON response and the HTTP status code with a status code of 201.
    - If there is an error during the request, return a tuple containing the error message and the HTTP status code received in the response.
    """
    config = load_config()
    response = requests.post(f"{config['base_url']}/pet", json=payload)

    # Check if the request is successful (status code 201)
    if response.status_code == 201:
        return response.json(), response.status_code
    else:
        # Return the error message and status code received in the response
        return response.text, response.status_code


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
    config = load_config()
    response = requests.get(f"{config['base_url']}/pet/{pet_id}")

    # Check if the request is successful (status code 200)
    if response.status_code == 200:
        return response.json(), response.status_code
    elif response.status_code == 404:
        # Return the error message 'Pet not found' and status code 404
        return "Pet not found", response.status_code
    else:
        # Return the error message and status code received in the response
        return response.text, response.status_code


def update_pet(pet_id, payload):
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
    config = load_config()
    response = requests.put(f"{config['base_url']}/pet/{pet_id}", json=payload)

    # Check if the request is successful (status code 200)
    if response.status_code == 200:
        return response.json(), response.status_code
    elif response.status_code == 404:
        # Return the error message 'Pet not found' and status code 404
        return "Pet not found", response.status_code
    else:
        # Return the error message and status code received in the response
        return response.text, response.status_code


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
    config = load_config()
    response = requests.delete(f"{config['base_url']}/pet/{pet_id}")

    # Check if the request is successful (status code 200)
    if response.status_code == 200:
        return "Pet deleted successfully", response.status_code
    elif response.status_code == 404:
        # Return the error message 'Pet not found' and status code 404
        return "Pet not found", response.status_code
    else:
        # Return the error message and status code received in the response
        return response.text, response.status_code
