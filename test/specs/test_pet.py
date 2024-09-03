from test.api.api_pet import add_pet, get_pet, delete_pet, update_pet, find_pet_by_status, upload_image
from test.helpers.utils import generate_random_pet_data
from test.helpers.utils import multipoint_verification
import json
import os
import pytest

# BASE_URL = "http://127.0.0.1:5000"  # Update with your actual server URL
created_pet_ids = []


#
# POST /pet tests
#
def test_add_pet():
    """
        Test the functionality of adding a new pet to the Pet Store.

        Actions:
        - Generate random pet data.
        - Perform a POST request to add a new pet with the generated data.
        - Retrieve the JSON response and HTTP status code.

        Expected Outcome:
        - The status code should be 201, indicating a successful addition.
        - The response JSON should contain the added pet's information.
        - The added pet's name, category, and status should match the generated data.
        - Cleanup: The added pet ID is stored for later removal.
        """
    # Generate random pet data
    test_data = generate_random_pet_data()

    # Perform a POST request to add a new pet
    response = add_pet(test_data["name"], test_data["category"], test_data["status"])
    pet = json.loads(response.text)

    # Store the created pet ID for cleanup
    created_pet_ids.append(pet['id'])

    # Validate the outcome of the test with a single assert statement
    test_results = multipoint_verification(response.text, response.status_code,
                                           201,
                                           [pet["id"],
                                            test_data["name"],
                                            test_data["category"],
                                            test_data["status"]])
    assert test_results == "No mismatch values"


def test_add_pet_name_missing():
    """
    Test the functionality of adding a new pet to the Pet Store with missing name field.

    Actions:
    - Generate random pet data.
    - Remove the 'name' field from the generated data.
    - Perform a POST request to add a new pet with the modified data.
    - Retrieve the JSON response and HTTP status code.

    Expected Outcome:
    - The status code should be 400, indicating a bad request due to missing 'name' field.
    - The response JSON should contain an error message indicating the missing 'name' field.
    """
    # Generate random pet data with missing 'name' field
    test_data = generate_random_pet_data()

    # Perform a POST request to add a new pet with missing 'name' field
    response = add_pet(None, test_data["category"], test_data["status"])

    # Validate the outcome of the test with a single assert statement
    test_results = multipoint_verification(response.text, response.status_code,
                                           400,
                                           ["Bad or missing data. Missing name field"])
    assert test_results == "No mismatch values"


def test_add_pet_category_missing():
    """
    Test the functionality of adding a new pet to the Pet Store with missing category field.

    Actions:
    - Generate random pet data.
    - Remove the 'category' field from the generated data.
    - Perform a POST request to add a new pet with the modified data.
    - Retrieve the JSON response and HTTP status code.

    Expected Outcome:
    - The status code should be 400, indicating a bad request due to missing 'category' field.
    - The response JSON should contain an error message indicating the missing 'category' field.
    """
    # Generate random pet data with missing 'category' field
    test_data = generate_random_pet_data()

    # Perform a POST request to add a new pet with missing 'category' field
    response = add_pet(test_data["name"], None, test_data["status"])

    # Validate the outcome of the test with a single assert statement
    test_results = multipoint_verification(response.text, response.status_code,
                                           400,
                                           ["Bad or missing data. Missing category field"])
    assert test_results == "No mismatch values"


def test_add_pet_status_missing():
    """
    Test the functionality of adding a new pet to the Pet Store with missing status field.

    Actions:
    - Generate random pet data.
    - Remove the 'status' field from the generated data.
    - Perform a POST request to add a new pet with the modified data.
    - Retrieve the JSON response and HTTP status code.

    Expected Outcome:
    - The status code should be 400, indicating a bad request due to missing 'status' field.
    - The response JSON should contain an error message indicating the missing 'status' field.
    """
    # Generate random pet data with missing 'status' field
    test_data = generate_random_pet_data()

    # Perform a POST request to add a new pet with missing 'status' field
    response = add_pet(test_data["name"], test_data["category"], None)

    # Validate the outcome of the test with a single assert statement
    test_results = multipoint_verification(response.text, response.status_code,
                                           400,
                                           ["Bad or missing data. Missing status field"])
    assert test_results == "No mismatch values"


def test_add_pet_duplicate():
    """
    Test the functionality of adding a new pet to the Pet Store with duplicate data.

    Actions:
    - Generate random pet data.
    - Perform a POST request to add a new pet with the generated data.
    - Store the created pet ID for cleanup.
    - Perform another POST request to add a new pet with the same data.
    - Retrieve the JSON response and HTTP status code.

    Expected Outcome:
    - The first status code should be 201, indicating a successful addition.
    - The second status code should be 400, indicating a bad request due to duplicate data.
    - The response JSON should contain an error message indicating the duplicate data.
    """
    # Generate random pet data
    test_data = generate_random_pet_data()

    # Perform a POST request to add a new pet with the generated data
    response = add_pet(test_data["name"], test_data["category"], test_data["status"])
    pet = json.loads(response.text)

    # Store the created pet ID for cleanup
    created_pet_ids.append(pet['id'])

    # Perform another POST request to add a new pet with the same data
    response2 = add_pet(test_data["name"], test_data["category"], test_data["status"])

    # Validate the outcome of the test with a single assert statement
    test_results = multipoint_verification(response2.text, response2.status_code,
                                           400,
                                           ["Pet with the same name and category already exists"])
    assert test_results == "No mismatch values"


#
# GET /pet tests
#
def test_get_pet():
    """
    Test the functionality of retrieving a pet from the Pet Store.

    Actions:
    - Generate random pet data.
    - Perform a POST request to add a new pet with the generated data.
    - Store the created pet ID for cleanup.
    - Perform a GET request to retrieve the added pet by ID.
    - Retrieve the JSON response and HTTP status code.

    Expected Outcome:
    - The first status code should be 201, indicating a successful addition.
    - The second status code should be 200, indicating a successful retrieval.
    - The response JSON should contain the added pet's information.
    - The retrieved pet's name, category, and status should match the generated data.
    """
    # Generate random pet data
    test_data = generate_random_pet_data()

    # Perform a POST request to add a new pet with the generated data
    response = add_pet(test_data["name"], test_data["category"], test_data["status"])
    pet = json.loads(response.text)

    # Store the created pet ID for cleanup
    created_pet_ids.append(pet['id'])

    # Perform a GET request to retrieve the added pet by ID
    pet_id = pet['id']
    response = get_pet(pet_id)

    # Validate the outcome of the test with a single assert statement
    test_results = multipoint_verification(response.text, response.status_code,
                                           200,
                                           [pet_id,
                                            test_data["name"],
                                            test_data["category"],
                                            test_data["status"]])
    assert test_results == "No mismatch values"


def test_get_pet_id_0():
    """
    Test the functionality of retrieving a pet from the Pet Store with ID 0.

    Actions:
    - Perform a GET request to retrieve a pet with ID 0.
    - Retrieve the JSON response and HTTP status code.

    Expected Outcome:
    - The status code should be 404, indicating that the pet with ID 0 was not found.
    - The response JSON should contain an error message indicating that the pet was not found.
    """
    # Perform a GET request to retrieve a pet with ID 0
    response = get_pet(0)

    # Validate the outcome of the test with a single assert statement
    test_results = multipoint_verification(response.text, response.status_code,
                                           404,
                                           ["Pet not found"])
    assert test_results == "No mismatch values"


def test_get_pet_id_negative_1():
    """
    Test the functionality of retrieving a pet from the Pet Store with ID -1.

    Actions:
    - Perform a GET request to retrieve a pet with ID -1.
    - Retrieve the JSON response and HTTP status code.

    Expected Outcome:
    - The status code should be 404, indicating that the pet with ID -1 was not found.
    - The response JSON should contain an error message indicating that the requested URL was not found.
    """
    # Perform a GET request to retrieve a pet with ID -1
    response = get_pet(-1)

    # Validate the outcome of the test with a single assert statement
    test_results = multipoint_verification(response.text, response.status_code,
                                           404,
                                           ["404 Not Found"])
    assert test_results == "No mismatch values"


def test_get_pet_id_999999999():
    """
    Test the functionality of retrieving a pet from the Pet Store with a non-existent ID (999999999).

    Actions:
    - Perform a GET request to retrieve a pet with ID 999999999.
    - Retrieve the JSON response and HTTP status code.

    Expected Outcome:
    - The status code should be 404, indicating that the pet with ID 999999999 was not found.
    - The response JSON should contain an error message indicating that the pet was not found.
    """
    # Perform a GET request to retrieve a pet with ID 999999999
    response = get_pet(999999999)

    # Validate the outcome of the test with a single assert statement
    test_results = multipoint_verification(response.text, response.status_code,
                                           404,
                                           ["Pet not found"])
    assert test_results == "No mismatch values"


def test_get_pet_id_invalid():
    """
    Test the functionality of retrieving a pet from the Pet Store with an invalid (non-numeric) ID.

    Actions:
    - Perform a GET request to retrieve a pet with an invalid ID ("invalid").
    - Retrieve the JSON response and HTTP status code.

    Expected Outcome:
    - The status code should be 404, indicating that the pet with an invalid ID was not found.
    - The response JSON should contain an error message indicating that the requested URL was not found.
    """
    # Perform a GET request to retrieve a pet with an invalid ID
    response = get_pet("invalid")

    # Validate the outcome of the test with a single assert statement
    test_results = multipoint_verification(response.text, response.status_code,
                                           404,
                                           ["404 Not Found"])
    assert test_results == "No mismatch values"


#
# PUT /pet tests
#
def test_update_pet():
    """
    Test the functionality of updating a pet in the Pet Store by ID.

    Actions:
    - Generate random pet data and add a new pet.
    - Update the pet's name, category, and status.
    - Perform a PUT request to update the pet's data.
    - Retrieve the JSON response and HTTP status code.

    Expected Outcome:
    - The status code should be 200, indicating a successful update.
    - The response JSON should contain the updated pet's information.
    - The updated pet's name, category, and status should match the updated data.
    """
    # Generate random pet data and add the pet
    initial_data = generate_random_pet_data()
    response = add_pet(initial_data["name"], initial_data["category"], initial_data["status"])
    pet = json.loads(response.text)

    # Store the created pet ID for cleanup
    created_pet_ids.append(pet['id'])

    # Generate new random data for the update
    updated_data = generate_random_pet_data()

    # Perform a PUT request to update the pet
    response = update_pet(pet['id'], updated_data["name"], updated_data["category"], updated_data["status"])

    # Validate the outcome of the test with a single assert statement
    test_results = multipoint_verification(response.text, response.status_code,
                                           200,
                                           [pet['id'],
                                            updated_data["name"],
                                            updated_data["category"],
                                            updated_data["status"]])
    assert test_results == "No mismatch values"


def test_update_pet_name_missing():
    """
    Test the functionality of updating a pet in the Pet Store by ID with missing name field.

    Actions:
    - Generate random pet data and add a new pet.
    - Attempt to update the pet's data with a missing name.
    - Retrieve the JSON response and HTTP status code.

    Expected Outcome:
    - The status code should be 200, indicating a successful update.
    - The response JSON should contain the updated pet's information with the other fields unchanged.
    """
    # Generate random pet data and add the pet
    initial_data = generate_random_pet_data()
    response = add_pet(initial_data["name"], initial_data["category"], initial_data["status"])
    pet = json.loads(response.text)

    # Store the created pet ID for cleanup
    created_pet_ids.append(pet['id'])

    # Generate new random data for the update
    updated_data = generate_random_pet_data()

    # Perform a PUT request to update the pet
    response = update_pet(pet['id'], None, updated_data["category"], updated_data["status"])
    print(response.text)
    # Validate the outcome of the test with a single assert statement
    test_results = multipoint_verification(response.text, response.status_code,
                                           200,
                                           [pet['id'],
                                            pet['name'],  # Name should remain unchanged
                                            updated_data["category"],
                                            updated_data["status"]])
    assert test_results == "No mismatch values"


def test_update_pet_category_missing():
    """
    Test the functionality of updating a pet in the Pet Store by ID with missing category field.

    Actions:
    - Generate random pet data and add a new pet.
    - Attempt to update the pet's data with a missing category.
    - Retrieve the JSON response and HTTP status code.

    Expected Outcome:
    - The status code should be 200, indicating a successful update.
    - The response JSON should contain the updated pet's information with the other fields unchanged.
    """
    # Generate random pet data and add the pet
    initial_data = generate_random_pet_data()
    response = add_pet(initial_data["name"], initial_data["category"], initial_data["status"])
    pet = json.loads(response.text)

    # Store the created pet ID for cleanup
    created_pet_ids.append(pet['id'])

    # Generate new random data for the update
    updated_data = generate_random_pet_data()

    # Perform a PUT request to update the pet
    response = update_pet(pet['id'], updated_data["category"], None, updated_data["status"])

    # Validate the outcome of the test with a single assert statement
    test_results = multipoint_verification(response.text, response.status_code,
                                           200,
                                           [pet['id'],
                                            updated_data["category"],
                                            pet['category'],  # Category should remain unchanged
                                            updated_data["status"]])
    assert test_results == "No mismatch values"


def test_update_pet_status_missing():
    """
    Test the functionality of updating a pet in the Pet Store by ID with missing status field.

    Actions:
    - Generate random pet data and add a new pet.
    - Attempt to update the pet's data with a missing status.
    - Retrieve the JSON response and HTTP status code.

    Expected Outcome:
    - The status code should be 200, indicating a successful update.
    - The response JSON should contain the updated pet's information with the other fields unchanged.
    """
    # Generate random pet data and add the pet
    initial_data = generate_random_pet_data()
    response = add_pet(initial_data["name"], initial_data["category"], initial_data["status"])
    pet = json.loads(response.text)

    # Store the created pet ID for cleanup
    created_pet_ids.append(pet['id'])

    # Generate new random data for the update
    updated_data = generate_random_pet_data()

    # Perform a PUT request to update the pet
    response = update_pet(pet['id'], updated_data["name"], updated_data["category"], None)

    # Validate the outcome of the test with a single assert statement
    test_results = multipoint_verification(response.text, response.status_code,
                                           200,
                                           [pet['id'],
                                            updated_data["name"],
                                            updated_data["category"],
                                            pet['status']])  # Status should remain unchanged
    assert test_results == "No mismatch values"


def test_update_pet_not_found():
    """
    Test the functionality of updating a pet in the Pet Store by ID when the pet is not found.

    Actions:
    - Attempt to update a non-existent pet.
    - Retrieve the JSON response and HTTP status code.

    Expected Outcome:
    - The status code should be 404, indicating the pet was not found.
    - The response JSON should contain an error message indicating the pet was not found.
    """
    # Attempt to update a non-existent pet
    response = update_pet(999999999, "Non-Existent Name", "Non-Existent Category", "Non-Existent Status")

    # Validate the outcome of the test with a single assert statement
    test_results = multipoint_verification(response.text, response.status_code,
                                           404,
                                           ["Pet not found"])
    assert test_results == "No mismatch values"


def test_update_pet_duplicate():
    """
    Test the functionality of updating a pet to a duplicate entry in the Pet Store.

    Actions:
    - Generate random pet data and add two new pets.
    - Attempt to update the second pet to have the same name and category as the first pet.
    - Retrieve the JSON response and HTTP status code.

    Expected Outcome:
    - The status code should be 400, indicating a bad request due to duplicate data.
    - The response JSON should contain an error message indicating the duplicate data.
    """
    # Add the first pet
    first_pet_data = generate_random_pet_data()
    response = add_pet(first_pet_data["name"], first_pet_data["category"], first_pet_data["status"])
    first_pet = json.loads(response.text)
    created_pet_ids.append(first_pet['id'])

    # Add the second pet
    second_pet_data = generate_random_pet_data()
    response = add_pet(second_pet_data["name"], second_pet_data["category"], second_pet_data["status"])
    second_pet = json.loads(response.text)
    created_pet_ids.append(second_pet['id'])

    # Attempt to update the second pet to have the same name and category as the first pet
    response = update_pet(second_pet['id'], first_pet_data["name"], first_pet_data["category"], second_pet_data["status"])

    # Validate the outcome of the test with a single assert statement
    test_results = multipoint_verification(response.text, response.status_code,
                                           400,
                                           ["Pet with the same name and category already exists"])
    assert test_results == "No mismatch values"


#
# DELETE /pet tests
#
def test_delete_pet():
    """
    Test the functionality of deleting a pet from the Pet Store by ID.

    Actions:
    - Generate random pet data and add a new pet.
    - Perform a DELETE request to remove the pet by ID.
    - Retrieve the JSON response and HTTP status code.

    Expected Outcome:
    - The status code should be 204, indicating a successful deletion.
    - The response JSON should confirm that the pet was deleted.
    """
    # Generate random pet data and add the pet
    test_data = generate_random_pet_data()
    response = add_pet(test_data["name"], test_data["category"], test_data["status"])
    pet = json.loads(response.text)

    # Perform a DELETE request to remove the pet
    response = delete_pet(pet['id'])

    # Validate the outcome of the test with a single assert statement
    assert response.status_code == 204


def test_delete_pet_not_found():
    """
    Test the functionality of deleting a pet in the Pet Store by ID when the pet is not found.

    Actions:
    - Attempt to delete a non-existent pet.
    - Retrieve the JSON response and HTTP status code.

    Expected Outcome:
    - The status code should be 404, indicating the pet was not found.
    - The response JSON should contain an error message indicating the pet was not found.
    """
    # Attempt to delete a non-existent pet
    response = delete_pet(999999999)

    # Validate the outcome of the test with a single assert statement
    test_results = multipoint_verification(response.text, response.status_code,
                                           404,
                                           ["Pet not found"])
    assert test_results == "No mismatch values"


def test_delete_pet_already_deleted():
    """
    Test the functionality of deleting a pet that has already been deleted in the Pet Store.

    Actions:
    - Generate random pet data and add a new pet.
    - Perform a DELETE request to remove the pet by ID.
    - Attempt to delete the same pet again.
    - Retrieve the JSON response and HTTP status code.

    Expected Outcome:
    - The first DELETE request should return status 204, indicating a successful deletion.
    - The second DELETE request should return status 404, indicating the pet was not found.
    """
    # Generate random pet data and add the pet
    test_data = generate_random_pet_data()
    response = add_pet(test_data["name"], test_data["category"], test_data["status"])
    pet = json.loads(response.text)

    # Perform a DELETE request to remove the pet
    response = delete_pet(pet['id'])
    assert response.status_code == 204

    # Attempt to delete the same pet again
    response = delete_pet(pet['id'])

    # Validate the outcome of the test with a single assert statement
    test_results = multipoint_verification(response.text, response.status_code,
                                           404,
                                           ["Pet not found"])
    assert test_results == "No mismatch values"


#
# GET /pet/findByStatus tests
#
def test_find_pet_by_status_available():
    """
    Test finding pets by 'available' status.

    Actions:
    - Add a new pet with 'available' status.
    - Perform a GET request to find pets by 'available' status.
    - Retrieve the JSON response and HTTP status code.

    Expected Outcome:
    - The status code should be 200, indicating a successful retrieval.
    - The response JSON should contain the added pet's information.
    """
    # Generate and add a pet with 'available' status
    test_data = generate_random_pet_data(status="available")
    response = add_pet(test_data["name"], test_data["category"], test_data["status"])
    pet = json.loads(response.text)
    created_pet_ids.append(pet['id'])

    # Find pets by 'available' status
    response = find_pet_by_status("available")

    # Validate the outcome of the test with a single assert statement
    assert response.status_code == 200
    assert any(p['id'] == pet['id'] for p in json.loads(response.text))


def test_find_pet_by_status_invalid():
    """
    Test finding pets by an invalid status.

    Actions:
    - Perform a GET request to find pets by an invalid status.
    - Retrieve the JSON response and HTTP status code.

    Expected Outcome:
    - The status code should be 400, indicating a bad request due to an invalid status.
    - The response JSON should contain an error message indicating the invalid status.
    """
    response = find_pet_by_status("invalid_status")

    # Validate the outcome of the test with a single assert statement
    test_results = multipoint_verification(response.text, response.status_code,
                                           400,
                                           ["Status parameter is invalid; should be available, pending, or sold"])
    assert test_results == "No mismatch values"


#
# POST /pet/<int:pet_id>/uploadImage tests
#
@pytest.mark.skip(reason="Test is blocked due to dependency on a feature that is not yet implemented.")
def test_upload_valid_image():
    """
    Test the functionality of uploading a valid image for a pet.

    Actions:
    - Add a new pet.
    - Perform a POST request to upload a valid image file for the pet.
    - Retrieve the JSON response and HTTP status code.

    Expected Outcome:
    - The status code should be 201, indicating a successful upload.
    - The response JSON should confirm that the file was uploaded successfully.
    """
    # Generate and add a new pet
    test_data = generate_random_pet_data()
    response = add_pet(test_data["name"], test_data["category"], test_data["status"])
    pet = json.loads(response.text)
    created_pet_ids.append(pet['id'])

    # Path to a valid image file
    valid_image_path = os.path.join(os.path.dirname(__file__), '..', "data", "valid_image.jpg")

    # Perform the POST request to upload the image
    response = upload_image(pet['id'], valid_image_path)
    print(response)
    print(response.text)
    # Validate the outcome of the test with a single assert statement
    test_results = multipoint_verification(response.text, response.status_code,
                                           201,
                                           ["File uploaded successfully"])
    assert test_results == "No mismatch values"


@pytest.mark.skip(reason="Test is blocked due to dependency on a feature that is not yet implemented.")
def test_upload_invalid_file():
    """
    Test the functionality of uploading an invalid file for a pet.

    Actions:
    - Add a new pet.
    - Perform a POST request to upload an invalid (non-image) file for the pet.
    - Retrieve the JSON response and HTTP status code.

    Expected Outcome:
    - The status code should be 400, indicating a bad request due to an invalid file type.
    - The response JSON should contain an error message indicating the file upload error.
    """
    # Generate and add a new pet
    test_data = generate_random_pet_data()
    response = add_pet(test_data["name"], test_data["category"], test_data["status"])
    pet = json.loads(response.text)
    created_pet_ids.append(pet['id'])

    # Path to an invalid file (non-image)
    invalid_file_path = os.path.join(os.path.dirname(__file__), '..', "data", "invalid_file.txt")

    # Perform the POST request to upload the invalid file
    response = upload_image(pet['id'], invalid_file_path)

    # Validate the outcome of the test with a single assert statement
    # Expecting a failure due to the invalid file type (depends on API implementation)
    test_results = multipoint_verification(response.text, response.status_code,
                                           400,
                                           ["No selected file",
                                            "Invalid file type"])
    assert test_results == "No mismatch values"


def test_upload_image_invalid_pet_id():
    """
    Test the functionality of uploading an image for a non-existent pet.

    Actions:
    - Attempt to upload an image file using an invalid pet ID.
    - Retrieve the JSON response and HTTP status code.

    Expected Outcome:
    - The status code should be 404, indicating that the pet was not found.
    - The response JSON should contain an error message indicating that the pet was not found.
    """
    # Define an invalid pet ID
    invalid_pet_id = 999999999

    # Path to a valid image file
    valid_image_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'valid_image.jpg')
    valid_image_path = os.path.normpath(valid_image_path)

    # Perform the POST request to upload the image using an invalid pet ID
    response = upload_image(invalid_pet_id, valid_image_path)

    # Validate the outcome of the test with a single assert statement
    test_results = multipoint_verification(response.text, response.status_code,
                                           404,
                                           ["Pet not found"])
    assert test_results == "No mismatch values"


def test_cleanup_created_pets():
    print(f"\n\nPost suite pet cleanup...")
    for pet_id in created_pet_ids:
        response = delete_pet(pet_id)
        if response.status_code == 204:
            print(f"Deleted pet with ID {pet_id}")
        else:
            print(f"Failed to delete pet with ID {pet_id}, status code: {response.status_code}")
