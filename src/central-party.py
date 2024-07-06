import logging

from lib.webhook import run_webhook_server

def central_party_custom_handler(subpath, data):
    pass

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    run_webhook_server(5000, central_party_custom_handler)
