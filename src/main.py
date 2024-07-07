import logging
import os

from lib.handlers import central_party_handler, fl_client_handler
from lib.webhook import run_webhook_server

AGENT_TYPE = os.getenv("AGENT_TYPE")

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    if AGENT_TYPE == "CLIENT":
        run_webhook_server(5000, fl_client_handler)
    elif AGENT_TYPE == "CENTRAL":
        model_file = "/model/params.json"
        if os.path.isfile(model_file):
            os.remove(model_file)
        run_webhook_server(5000, central_party_handler)
