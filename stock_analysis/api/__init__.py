from typing import Union
import requests
import json


def http_request(url_path: str, method: str, data: dict) -> Union[dict, list]:
    """Make any `HTTP` request method

    Args:
        url_path (str): usrl path to hit the request (must not start with '/')
        method (str): HTTP method to use while making request
        data (dict): data to be used in HTTP request

    Returns:
        dict: response data
    """

    # domain in the request url is provided by Deta Cloud
    req_url = f"https://uf1tjw.deta.dev/api/{url_path}"

    headers = {"Accept": "*/*", "Content-Type": "application/json"}

    # needs to convert payload data from `dict` to json (required from server side)
    payload = json.dumps(data)

    # retriving response & converting it into dict
    response = requests.request(
        method=method.upper(), url=req_url, data=payload, headers=headers
    ).json()

    return response
