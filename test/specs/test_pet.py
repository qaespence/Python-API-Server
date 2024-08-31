from test.api.api_pet import add_pet, get_pet, delete_pet
from test.helpers.utils import generate_random_pet_data
from test.helpers.utils import multipoint_verification

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
    pet, status_code = add_pet(test_data)

    # Store the created pet ID for cleanup
    created_pet_ids.append(pet['id'])

    # Validate the outcome of the test with a single assert statement
    test_results = multipoint_verification(str(pet), status_code,
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
    del test_data['name']

    # Perform a POST request to add a new pet with missing 'name' field
    response, status_code = add_pet(test_data)

    # Validate the outcome of the test with a single assert statement
    test_results = multipoint_verification(str(response), status_code,
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
    del test_data['category']

    # Perform a POST request to add a new pet with missing 'category' field
    response, status_code = add_pet(test_data)

    # Validate the outcome of the test with a single assert statement
    test_results = multipoint_verification(str(response), status_code,
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
    del test_data['status']

    # Perform a POST request to add a new pet with missing 'status' field
    response, status_code = add_pet(test_data)

    # Validate the outcome of the test with a single assert statement
    test_results = multipoint_verification(str(response), status_code,
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
    pet, status_code = add_pet(test_data)

    # Store the created pet ID for cleanup
    created_pet_ids.append(pet['id'])

    # Perform another POST request to add a new pet with the same data
    response, status_code = add_pet(test_data)

    # Validate the outcome of the test with a single assert statement
    test_results = multipoint_verification(str(response), status_code,
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
    pet, status_code = add_pet(test_data)

    # Store the created pet ID for cleanup
    created_pet_ids.append(pet['id'])

    # Perform a GET request to retrieve the added pet by ID
    pet_id = pet['id']
    response, status_code = get_pet(pet_id)

    # Validate the outcome of the test with a single assert statement
    test_results = multipoint_verification(str(pet), status_code,
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
    response, status_code = get_pet(0)

    # Validate the outcome of the test with a single assert statement
    test_results = multipoint_verification(str(response), status_code,
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
    response, status_code = get_pet(-1)

    # Validate the outcome of the test with a single assert statement
    test_results = multipoint_verification(str(response), status_code,
                                           404,
                                           ["Pet not found"])
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
    response, status_code = get_pet(999999999)

    # Validate the outcome of the test with a single assert statement
    test_results = multipoint_verification(str(response), status_code,
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
    response, status_code = get_pet("invalid")

    # Validate the outcome of the test with a single assert statement
    test_results = multipoint_verification(str(response), status_code,
                                           404,
                                           ["Pet not found"])
    assert test_results == "No mismatch values"


def test_cleanup_created_pets():
    print(f"\n\nPost suite pet cleanup...")
    for pet_id in created_pet_ids:
        response, status_code = delete_pet(pet_id)
        if status_code == 204:
            print(f"Deleted pet with ID {pet_id}")
        else:
            print(f"Failed to delete pet with ID {pet_id}, status code: {status_code}")
