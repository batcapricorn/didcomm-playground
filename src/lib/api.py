"""Module that defines auxiliary functions to call
ACA-Py API"""

import requests


def create_invitation(admin_url):
    """Create a new invitation."""
    response = requests.post(f"{admin_url}/connections/create-invitation", timeout=60)
    return response.json()


def receive_invitation(admin_url, invitation):
    """Receive an invitation."""
    response = requests.post(
        f"{admin_url}/connections/receive-invitation", json=invitation, timeout=60
    )
    return response.json()


def send_message(admin_url, connection_id, message):
    """Send a message to a connection."""
    response = requests.post(
        f"{admin_url}/connections/{connection_id}/send-message",
        json={"content": message},
        timeout=60,
    )
    return response.json()


def get_connection(admin_url, connection_id):
    """Get the connection details."""
    response = requests.get(f"{admin_url}/connections/{connection_id}", timeout=60)
    return response.json()
