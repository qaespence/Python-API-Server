from test.api.basic_requests import post, get, put, delete


def add_pet(name: str = None, category: str = None, status: str = None):
    """
    Test the functionality of adding a new pet to the Pet Store.

    Parameters:
    - name (str): Name of the pet to be added.
    - category (str): Category of the pet to be added.
    - status (str): Status of the pet to be added.

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
    - name (str): (optional) New name of the pet to be updated.
    - category (str): (optional) New category of the pet to be updated.
    - status (str): (optional) New status of the pet to be updated.

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


def find_pet_by_status(status: str):
    """
    Test the functionality of finding pets by status in the Pet Store.

    Parameters:
    - status (str): The status of the pets to retrieve. Should be one of 'available', 'pending', or 'sold'.

    Returns:
    - The JSON response and HTTP status code from the GET request.
    """

    return get(f"/pet/findByStatus?status={status}")


def upload_image(pet_id: int, file_path: str):
    """
    Test the functionality of uploading an image for a pet in the Pet Store by ID.

    Parameters:
    - pet_id (int): The unique identifier of the pet for which to upload an image.
    - file_path (str): The path to the image file to upload.

    Returns:
    - The JSON response and HTTP status code from the POST request.
    """

    with open(file_path, 'rb') as file:
        files = {'file': file}
        headers = {"content-type": "multipart/form-data"}
        response = post(f"/pet/{pet_id}/uploadImage", files=files, headers=headers)
    return response
