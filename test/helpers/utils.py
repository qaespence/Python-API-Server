import random
import string
import json


def load_config():
    with open("../config/config.json", "r") as config_file:
        config_data = json.load(config_file)
    return config_data


def generate_random_pet_data():
    name = ''.join(random.choice(string.ascii_letters) for _ in range(8))
    category = random.choice(["Dog", "Cat", "Fish", "Bird", "Turtle", "Hamster"])
    status = random.choice(["available", "pending", "sold"])

    return {
        "name": name,
        "category": category,
        "status": status
    }
