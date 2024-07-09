"""Module containing handlers that process POST requests
sent by ACA-Py agents
"""

from .aggregation import perform_model_aggregation
from .iteration import perform_training_iteration
from .validate import is_fl_message


def central_party_handler(subpath, data):
    """
    Handle incoming messages for the central party in a federated learning setup.

    This function checks if the incoming message is relevant to federated learning
    and performs model aggregation if so.

    :param subpath: The subpath extracted from the webhook request.
    :type subpath: str
    :param data: Data received from the webhook request.
    :type data: dict
    """
    if is_fl_message(subpath, data):
        perform_model_aggregation(data)


def fl_client_handler(subpath, data):
    """
    Handle incoming messages for a federated learning client.

    This function checks if the incoming message is relevant to federated learning
    and performs a training iteration if so.

    :param subpath: The subpath extracted from the webhook request.
    :type subpath: str
    :param data: Data received from the webhook request.
    :type data: dict
    """
    if is_fl_message(subpath, data):
        perform_training_iteration(data)
