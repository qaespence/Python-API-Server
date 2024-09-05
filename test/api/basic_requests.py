import requests
from test.helpers.utils import load_config
from test.helpers.utils import api_logger
from datetime import datetime


def post(endpoint: str, payload: dict = None, headers: dict = None, files: dict = None):
    """
    Sends a POST request to the specified endpoint with the given payload and headers.

    Args:
        endpoint (str): The API endpoint to send the request to.
        payload (dict): (optional) The data to be sent in the body of the request.
        headers (dict): (optional) The headers to include in the request.
        files (dict): (optional) The files to include in the request.

    Returns:
        response: The response object returned by the requests library.
    """
    start_time = datetime.now()
    config = load_config()
    url = f"{config['base_url']}{endpoint}"

    # Decide whether to include json or data in the request
    if payload and not files:
        response = requests.post(url, json=payload, headers=headers)
    elif files:
        response = requests.post(url, files=files, headers=headers, data=payload)
    else:
        response = requests.post(url, headers=headers)

    end_time = datetime.now()
    api_logger(endpoint, payload, headers, response.text, "POST", start_time, end_time)
    return response


def get(endpoint: str):
    """
    Sends a GET request to the specified endpoint.

    Args:
        endpoint (str): The API endpoint to send the request to.

    Returns:
        response: The response object returned by the requests library.
    """
    start_time = datetime.now()
    config = load_config()
    response = requests.get(f"{config['base_url']}"+endpoint)
    end_time = datetime.now()
    api_logger(endpoint, {}, {}, response.text, "GET", start_time, end_time)
    return response


def delete(endpoint: str):
    """
    Sends a DELETE request to the specified endpoint.

    Args:
        endpoint (str): The API endpoint to send the request to.

    Returns:
        response: The response object returned by the requests library.
    """
    start_time = datetime.now()
    config = load_config()
    response = requests.delete(f"{config['base_url']}"+endpoint)
    end_time = datetime.now()
    api_logger(endpoint, {}, {}, response.text, "DELETE", start_time, end_time)
    return response


def put(endpoint: str, payload: dict, headers: dict):
    """
    Sends a PUT request to the specified endpoint with the given payload and headers.

    Args:
        endpoint (str): The API endpoint to send the request to.
        payload (dict): The data to be sent in the body of the request.
        headers (dict): The headers to include in the request.

    Returns:
        response: The response object returned by the requests library.
    """
    start_time = datetime.now()
    config = load_config()
    response = requests.put(f"{config['base_url']}"+endpoint, json=payload,
                            headers=headers)
    end_time = datetime.now()
    api_logger(endpoint, payload, headers, response.text, "PUT", start_time, end_time)
    return response


def patch(endpoint: str, payload: dict, headers: dict):
    """
    Sends a PATCH request to the specified endpoint with the given payload and headers.

    Args:
        endpoint (str): The API endpoint to send the request to.
        payload (dict): The data to be sent in the body of the request.
        headers (dict): The headers to include in the request.

    Returns:
        response: The response object returned by the requests library.
    """
    start_time = datetime.now()
    config = load_config()
    response = requests.patch(f"{config['base_url']}"+endpoint, json=payload,
                              headers=headers)
    end_time = datetime.now()
    api_logger(endpoint, payload, headers, response.text, "PATCH", start_time, end_time)
    return response
