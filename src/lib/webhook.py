"""Module that provides auxiliary functions to
boot up flask webserver
"""

from flask import Flask, request
from flask.logging import default_handler


def create_app(custom_handler):
    """
    Create a Flask application for handling webhook requests.

    :param custom_handler: A function to handle incoming webhook requests.
    :type custom_handler: callable
    :return: A Flask application instance.
    :rtype: flask.Flask
    """
    app = Flask(__name__)
    app.logger.removeHandler(default_handler)

    @app.route("/topic/<path:subpath>/", methods=["POST"])
    def handle_all_requests(subpath):
        """
        Handle incoming POST requests to a specific subpath,
        e.g. `basicmessages`.

        :param subpath: The subpath extracted from the request URL.
        :type subpath: str
        :return: An empty string with HTTP status code 200.
        :rtype: str
        """
        data = request.json
        app.logger.info(
            "Webhook received POST request for subpath: %s, data: %s", subpath, data
        )
        custom_handler(subpath, data)
        return "", 200

    return app


def run_webhook_server(port, custom_handler):
    """
    Run a Flask server to listen for incoming webhook requests.

    :param port: The port number to run the Flask server on.
    :type port: int
    :param custom_handler: A function to handle incoming webhook requests.
    :type custom_handler: callable
    """
    app = create_app(custom_handler)
    app.run(host="0.0.0.0", port=port)
