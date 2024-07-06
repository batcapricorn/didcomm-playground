import logging

from lib.local_training_iteration import perfom_training_iteration
from lib.webhook import run_webhook_server

def fl_client_custom_handler(subpath, data):

    if "basicmessages" in subpath:
        # Handle the initial weights and update weights
        perfom_training_iteration()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    run_webhook_server(5000, fl_client_custom_handler)
