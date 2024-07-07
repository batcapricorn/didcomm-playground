"""Module that initializes a webhook server that can be connected with
a ACA-Py agent
"""

import logging
import os

from lib.env import AGENT_TYPE, MODEL_FILE
from lib.handlers import central_party_handler, fl_client_handler
from lib.webhook import run_webhook_server

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    if AGENT_TYPE == "CLIENT":
        run_webhook_server(5000, fl_client_handler)
    elif AGENT_TYPE == "CENTRAL":
        if os.path.isfile(MODEL_FILE):
            os.remove(MODEL_FILE)
        run_webhook_server(5000, central_party_handler)
