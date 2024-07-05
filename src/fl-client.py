from lib.webhook import run_webhook_server
from lib.local_training_iteration import perfom_training_iteration


def bob_custom_handler(subpath, data):

    if "basicmessages" in subpath:
        # Handle the initial weights and update weights
        perfom_training_iteration()


if __name__ == "__main__":
    run_webhook_server(5000, bob_custom_handler)
