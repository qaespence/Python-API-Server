import requests
from test.api.api_pet import add_pet, get_pet, delete_pet
from test.helpers.utils import generate_random_pet_data

BASE_URL = "http://127.0.0.1:5000"  # Update with your actual server URL
created_pet_ids = []


#
# POST /pet tests
#
def test_add_pet():
    test_data = generate_random_pet_data()
    pet, status_code = add_pet(test_data)
    assert status_code == 201
    assert pet["name"] == test_data["name"]
    assert pet["category"] == test_data["category"]
    assert pet["status"] == test_data["status"]
    created_pet_ids.append(pet['id'])


def test_add_pet_name_missing():
    test_data = generate_random_pet_data()
    del test_data['name']
    response, status_code = add_pet(test_data)
    assert status_code == 400
    assert "Bad or missing data. Missing name field" in response


def test_add_pet_category_missing():
    test_data = generate_random_pet_data()
    del test_data['category']
    response, status_code = add_pet(test_data)
    assert status_code == 400
    assert "Bad or missing data. Missing category field" in response


def test_add_pet_status_missing():
    test_data = generate_random_pet_data()
    del test_data['status']
    response, status_code = add_pet(test_data)
    assert status_code == 400
    assert "Bad or missing data. Missing status field" in response


def test_add_pet_duplicate():
    test_data = generate_random_pet_data()
    pet, status_code = add_pet(test_data)
    created_pet_ids.append(pet['id'])
    response, status_code = add_pet(test_data)
    assert status_code == 400
    assert "Pet with the same name and category already exists" in response


#
# GET /pet tests
#
def test_get_pet():
    test_data = generate_random_pet_data()
    pet, status_code = add_pet(test_data)
    created_pet_ids.append(pet['id'])
    pet_id = pet['id']
    response, status_code = get_pet(pet_id)
    assert status_code == 200
    assert response["name"] == test_data["name"]
    assert response["category"] == test_data["category"]
    assert response["status"] == test_data["status"]


def test_get_pet_id_0():
    response, status_code = get_pet(0)
    assert status_code == 404
    assert "Pet not found" in response


def test_get_pet_id_negative_1():
    response, status_code = get_pet(-1)
    assert status_code == 404
    assert "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again" in response


def test_get_pet_id_999999999():
    response, status_code = get_pet(999999999)
    assert status_code == 404
    assert "Pet not found" in response


def test_get_pet_id_invalid():
    response, status_code = get_pet("invalid")
    assert status_code == 404
    assert "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again" in response


def test_cleanup_created_pets():
    print(f"\nPost suite pet cleanup...")
    for pet_id in created_pet_ids:
        response, status_code = delete_pet(pet_id)
        if status_code == 204:
            print(f"Deleted pet with ID {pet_id}")
        else:
            print(f"Failed to delete pet with ID {pet_id}, status code: {status_code}")
