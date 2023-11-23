import requests
from test.helpers.utils import load_config


def add_pet(payload):
    config = load_config()
    response = requests.post(f"{config['base_url']}/pet", json=payload)
    if response.status_code == 201:
        return response.json(), response.status_code
    else:
        return response.text, response.status_code


def get_pet(pet_id):
    config = load_config()
    response = requests.get(f"{config['base_url']}/pet/{pet_id}")
    if response.status_code == 200:
        return response.json(), response.status_code
    else:
        return response.text, response.status_code


def update_pet(pet_id, payload):
    config = load_config()
    response = requests.put(f"{config['base_url']}/pet/{pet_id}", json=payload)
    if response.status_code == 201:
        return response.json(), response.status_code
    else:
        return response.text, response.status_code


def delete_pet(pet_id):
    config = load_config()
    response = requests.delete(f"{config['base_url']}/pet/{pet_id}")
    return response, response.status_code
