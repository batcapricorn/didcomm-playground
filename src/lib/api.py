"""Module that defines auxiliary functions to call
ACA-Py API"""

import requests


def create_invitation(admin_url):
    """
    Create a new invitation.

    :param admin_url: The URL of the ACA-Py admin API.
    :type admin_url: str
    :return: The JSON response from the ACA-Py admin API containing the invitation details.
    :rtype: dict
    """
    response = requests.post(f"{admin_url}/connections/create-invitation", timeout=60)
    return response.json()


def receive_invitation(admin_url, invitation):
    """
    Receive an invitation.

    :param admin_url: The URL of the ACA-Py admin API.
    :type admin_url: str
    :param invitation: The invitation to receive.
    :type invitation: dict
    :return: The JSON response from the ACA-Py admin API confirming the received invitation.
    :rtype: dict
    """
    response = requests.post(
        f"{admin_url}/connections/receive-invitation", json=invitation, timeout=60
    )
    return response.json()


def send_message(admin_url, connection_id, message):
    """
    Send a message to a connection.

    :param admin_url: The URL of the ACA-Py admin API.
    :type admin_url: str
    :param connection_id: The ID of the connection to send the message to.
    :type connection_id: str
    :param message: The content of the message to send.
    :type message: str
    :return: The JSON response from the ACA-Py admin API confirming the sent message.
    :rtype: dict
    """
    response = requests.post(
        f"{admin_url}/connections/{connection_id}/send-message",
        json={"content": message},
        timeout=60,
    )
    return response.json()


def get_connection(admin_url, connection_id):
    """
    Get the connection details.

    :param admin_url: The URL of the ACA-Py admin API.
    :type admin_url: str
    :param connection_id: The ID of the connection to retrieve details for.
    :type connection_id: str
    :return: The JSON response from the ACA-Py admin API containing the connection details.
    :rtype: dict
    """
    response = requests.get(f"{admin_url}/connections/{connection_id}", timeout=60)
    return response.json()
