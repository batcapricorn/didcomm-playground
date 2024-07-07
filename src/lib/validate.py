"""Module used to validate that a `basicmessage` is used to send model
parameters
"""

import json


def is_hex_string(s):
    """
    Check if the given string is a valid hexadecimal string.

    :param s: The string to check.
    :type s: str
    :return: True if the string is a valid hexadecimal string, False otherwise.
    :rtype: bool
    """
    try:
        bytes.fromhex(s)
        return True
    except ValueError:
        return False


def hex_to_dict(hex_str):
    """
    Convert a valid hexadecimal string to a dictionary.

    :param hex_str: The hexadecimal string to convert.
    :type hex_str: str
    :return: A dictionary parsed from the JSON content decoded from the hexadecimal string.
    :rtype: dict
    :raises ValueError: If the provided string is not a valid hexadecimal string.
    """
    if is_hex_string(hex_str):
        json_str = bytes.fromhex(hex_str).decode("utf-8")
        return json.loads(json_str)
    raise ValueError("Provided string is not a valid hex string")


def is_fl_message(subpath, data):
    """
    Check if the incoming message is relevant to federated learning.

    This function checks if the subpath contains "basicmessages" and verifies
    that the content in data is a valid hexadecimal string.

    :param subpath: The subpath extracted from the webhook request.
    :type subpath: str
    :param data: Data received from the webhook request, expected to contain "content".
    :type data: dict
    :return: True if the message is relevant to federated learning, False otherwise.
    :rtype: bool
    """
    if ("basicmessages" not in subpath) or not is_hex_string(data["content"]):
        return False
    return True
