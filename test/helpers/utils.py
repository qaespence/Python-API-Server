import random
import string
import json
from datetime import datetime
import os, sys
from os import path

debug_file_name = ""


def load_config():
    with open("../config/config.json", "r") as config_file:
        config_data = json.load(config_file)
    return config_data


def generate_random_pet_data(name=None, category=None, status=None):
    """
    Generate random pet data with optional overrides.

    Parameters:
    - name (str, optional): The name of the pet. If None, a random name will be generated.
    - category (str, optional): The category of the pet. If None, a random category will be generated.
    - status (str, optional): The status of the pet. If None, a random status will be generated.

    Returns:
    - dict: A dictionary containing the pet data.
    """

    def random_string(length=8):
        return ''.join(random.choices(string.ascii_letters, k=length))

    # Predefined lists of categories and statuses
    categories = ["Dog", "Cat", "Bird", "Fish", "Reptile"]
    statuses = ["available", "pending", "sold"]

    # Use provided values or generate random ones
    pet_name = name if name else random_string()
    pet_category = category if category else random.choice(categories)
    pet_status = status if status else random.choice(statuses)

    return {
        "name": pet_name,
        "category": pet_category,
        "status": pet_status
    }


def verify_status_code(expected_status_code, actual_status_code):
    if expected_status_code == actual_status_code:
        return None
    else:
        return "Expected status " + str(expected_status_code) + " does not match actual status " + str(actual_status_code) + "\n"


def compiled_results(results: list):
    if results == [[]] or results == []:
        return "No mismatch values"
    else:
        final_results = ""
        for result in results:
            final_results = final_results + str(result) + "\n"
        final_results = final_results + "\n\nThere were " + str(len(results)) + " mismatches!\n"
        return final_results


def verify_expected_response_text(expected_response_text, response_body):
    results = []
    for text in expected_response_text:
        if str(text) not in response_body:
            results.append("Expected string \"" + str(text) + "\" does NOT appear in results content\n\n")
    if results is not []:
        return results
    else:
        return None


def verify_unexpected_response_text(unexpected_response_text, response_body):
    results = []
    for text in unexpected_response_text:
        if str(text) in response_body:
            results.append("Unexpected string \"" + str(text) + "\" DOES appear in results content\n\n")
    if results is not []:
        return results
    else:
        return None


def multipoint_verification(response_body: string, actual_status_code: int = None,
                            expected_status_code: int = None,
                            expected_response_text: list = None,
                            unexpected_response_text: list = None,
                            expected_headers_text: list = None,
                            unexpected_headers_text: list = None):
    results = []
    if expected_status_code is not None:
        temp_results = verify_status_code(expected_status_code, actual_status_code)
        if temp_results is not None:
            results = results + [temp_results]

    if expected_response_text is not None:
        temp_results = verify_expected_response_text(expected_response_text, response_body)
        if temp_results is not None:
            results = results + temp_results

    if unexpected_response_text is not None:
        temp_results = verify_unexpected_response_text(unexpected_response_text, response_body)
        if temp_results is not None:
            results = results + temp_results

    if expected_headers_text is not None:
        temp_results = verify_expected_response_text(expected_headers_text, response_body)
        if temp_results is not None:
            results = results + temp_results

    if unexpected_headers_text is not None:
        temp_results = verify_unexpected_response_text(unexpected_headers_text, response_body)
        if temp_results is not None:
            results = results + temp_results

    return compiled_results(results)


def set_debug_file_name(suite_name: str = "unnamed"):
    global debug_file_name
    debug_file_name = suite_name


def curl_builder(url: str, payload: dict, method: str, headers: dict):
    command = "curl -svX "
    command = command + method.upper() + " " + url + " "
    if headers is not None:
        for key, value in headers.items():
            command = command + "-H {'"+key+"':'"+value+"'} "
    if payload is not None:
        command = command + "-d '" + json.dumps(payload) + "'"
    return command


def api_logger(endpoint: str, payload: dict, headers: dict, response: str, method: str,
               start_time: datetime, end_time: datetime):
    log_dir = os.path.join('..', 'logs')
    log_file = os.path.join(log_dir, f"{debug_file_name}.log")

    # Ensure the log directory exists
    os.makedirs(log_dir, exist_ok=True)

    total_duration = end_time - start_time
    config = load_config()
    url = f"{config['base_url']}{endpoint}"
    rebuilt_curl = curl_builder(url, payload, method, headers)
    # print("{")
    # print(f"\tendpoint: {endpoint}")
    # print(f"\turl: {url}")
    # print(f"\tCURL: {rebuilt_curl}")
    # print(f"\tduration: {int(total_duration.microseconds/1000)} ms")
    # print(f"\tpayload: {json.dumps(payload)}")
    # print(f"\theaders: {json.dumps(headers)}")
    # print(f"\tresponse: {''.join(response.splitlines())}")
    # print("}")
    log_entry = (
        "{\n"
        f"\tendpoint: {endpoint}\n"
        f"\turl: {url}\n"
        f"\ttime: {datetime.now()}\n"
        f"\tCURL: {rebuilt_curl}\n"
        f"\tduration: {int(total_duration.microseconds / 1000)} ms\n"
        f"\tpayload: {json.dumps(payload)}\n"
        f"\theaders: {json.dumps(headers)}\n"
        f"\tresponse: {''.join(response.splitlines())}\n"
        "}\n"
    )
    # print("DEBUG::  " + os.getcwd())
    with open(log_file, 'a') as file:
        file.write(log_entry)


def clear_log_files():
    """
    Finds and deletes all .log files in the logs directory.
    """
    log_dir = os.path.join('..', 'logs')

    # Check if the directory exists
    if os.path.exists(log_dir):
        # Iterate over all files in the directory
        for file_name in os.listdir(log_dir):
            # Check if the file has a .log extension
            if file_name.endswith('.log'):
                log_file = os.path.join(log_dir, file_name)
                if os.path.isfile(log_file):
                    os.remove(log_file)
                    print(f"Deleted log file: {log_file}")
    else:
        print(f"Log directory {log_dir} does not exist.")
