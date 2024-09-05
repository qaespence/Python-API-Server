import json
from test.api.api_inventory import get_inventory, add_to_inventory, remove_from_inventory
from test.api.api_pet import add_pet, delete_pet, update_pet
from test.helpers.utils import multipoint_verification, set_debug_file_name, clear_log_files

created_pet_ids = []


def test_setup():
    """
    Set up a pet to add to and remove from inventory for testing purposes.
    """
    set_debug_file_name("api_inventory")
    clear_log_files()
    test_data = {
        "name": "TestPet",
        "category": "Dog",
        "status": "available"
    }
    response = add_pet(test_data["name"], test_data["category"], test_data["status"])
    pet = json.loads(response.text)
    created_pet_ids.append(pet["id"])
    return pet


def test_get_inventory():
    """
    Test the functionality of retrieving the inventory from the Pet Store.

    Expected Outcome:
    - The status code should be 200, indicating a successful retrieval.
    - The response JSON should contain the inventory data.
    """
    response = get_inventory()

    test_results = multipoint_verification(
        response.text,
        response.status_code,
        200,
        ["Dog"],  # Expecting 'Dog' to be present in the response
        []  # No unexpected data should appear
    )
    assert test_results == "No mismatch values"


def test_add_pet_inventory():
    """
    Test that adding a new pet automatically adds to the inventory with a default quantity of 1.
    """
    test_data = {
        "name": "InventoryTestPet",
        "category": "Cat",
        "status": "available"
    }
    response = add_pet(test_data["name"], test_data["category"], test_data["status"])
    pet = json.loads(response.text)
    created_pet_ids.append(pet["id"])

    # Check the inventory after adding the pet
    inventory_response = get_inventory()

    test_results = multipoint_verification(
        inventory_response.text,
        inventory_response.status_code,
        200,
        ["Cat"],  # Expecting 'Cat' to appear in the response
        []  # No unexpected data should appear
    )
    assert test_results == "No mismatch values"


def test_update_pet_change_category():
    """
    Test that updating a pet's category correctly updates the inventory.
    """
    # Add a new pet
    test_data = {
        "name": "ChangeCategoryPet",
        "category": "Bird",
        "status": "available"
    }
    response = add_pet(test_data["name"], test_data["category"], test_data["status"])
    pet = json.loads(response.text)
    created_pet_ids.append(pet["id"])

    # Update the pet's category from Bird to Reptile
    update_pet(pet['id'], category="Reptile")

    # Check the inventory after updating the pet
    inventory_response = get_inventory()

    test_results = multipoint_verification(
        inventory_response.text,
        inventory_response.status_code,
        200,
        ["Reptile"],  # Expecting 'Reptile' to appear in the response
        ["Bird"]  # 'Bird' should no longer appear
    )
    assert test_results == "No mismatch values"


def test_delete_pet_inventory():
    """
    Test that deleting a pet automatically removes or decrements the category quantity in the inventory.
    """
    # Add a new pet
    test_data = {
        "name": "DeleteTestPet",
        "category": "Fish",
        "status": "available"
    }
    response = add_pet(test_data["name"], test_data["category"], test_data["status"])
    pet = json.loads(response.text)
    created_pet_ids.append(pet["id"])

    # Delete the pet
    delete_response = delete_pet(pet['id'])
    assert delete_response.status_code == 204

    # Check the inventory after deleting the pet
    inventory_response = get_inventory()

    test_results = multipoint_verification(
        inventory_response.text,
        inventory_response.status_code,
        200,
        [],  # Expect no 'Fish' in the response
        ["Fish"]  # 'Fish' should be removed from the inventory
    )
    assert test_results == "No mismatch values"


def test_add_to_inventory_existing_category():
    """
    Test adding a quantity to an existing category in the inventory.
    """
    add_to_inventory("Dog", 5)
    inventory_response = get_inventory()

    test_results = multipoint_verification(
        inventory_response.text,
        inventory_response.status_code,
        200,
        ["Dog"],  # 'Dog' should appear
        []  # No unexpected data should appear
    )
    assert test_results == "No mismatch values"


def test_remove_from_inventory_existing_category():
    """
    Test removing a quantity from an existing category in the inventory.
    """
    remove_from_inventory("Dog", 2)
    inventory_response = get_inventory()

    test_results = multipoint_verification(
        inventory_response.text,
        inventory_response.status_code,
        200,
        ["Dog"],  # 'Dog' should appear
        []  # No unexpected data should appear
    )
    assert test_results == "No mismatch values"


def test_cleanup_created_pets():
    """
    Clean up any pets created during the test.
    """
    for pet_id in created_pet_ids:
        response = delete_pet(pet_id)
        if response.status_code == 204:
            print(f"Deleted pet with ID {pet_id}")
        else:
            print(f"Failed to delete pet with ID {pet_id}, status code: {response.status_code}")
