import logging
import os
from flask import Flask, request
from flask.logging import default_handler


def create_app(custom_handler):
    app = Flask(__name__)
    app.logger.removeHandler(default_handler)

    @app.route("/topic/<path:subpath>/", methods=["POST"])
    def handle_all_requests(subpath):
        data = request.json
        full_url = request.url
        process_id = os.getpid()
        app.logger.info(
            f"Webhook received POST request for subpath: {subpath}, data: {data}, full URL: {full_url}, PID: {process_id}"
        )
        custom_handler(subpath, data)
        return "", 200

    return app


def run_webhook_server(port, custom_handler):
    app = create_app(custom_handler)
    app.run(host="0.0.0.0", port=port)
