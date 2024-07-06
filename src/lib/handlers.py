"""Module containing handlers that process POST requests
sent by ACA-Py agents
"""

import logging

from lib.iteration import perfom_training_iteration
from lib.validate import is_fl_message


def central_party_handler(subpath, data):
    pass


def fl_client_handler(subpath, data):

    if is_fl_message(subpath, data):
        perfom_training_iteration(data)
