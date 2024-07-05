from lib.webhook import run_webhook_server


def central_party_custom_handler(subpath, data):
    pass


if __name__ == "__main__":
    run_webhook_server(5000, central_party_custom_handler)
