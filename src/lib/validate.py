"""Module used to validate that a `basicmessage` is used to send model
parameters
"""

import json


def is_hex_string(s):
    """Check if the given string is a valid hex string."""
    try:
        bytes.fromhex(s)
        return True
    except ValueError:
        return False


def hex_to_dict(hex_str):
    """Convert a hex string to a dictionary if it is valid."""
    if is_hex_string(hex_str):
        json_str = bytes.fromhex(hex_str).decode("utf-8")
        return json.loads(json_str)
    else:
        raise ValueError("Provided string is not a valid hex string")


def is_fl_message(subpath, data):
    if ("basicmessages" not in subpath) or not (is_hex_string(data["content"])):
        return False
    return True
