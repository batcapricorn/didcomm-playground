from lib.webhook import run_webhook_server


def custom_handler(subpath, data):
    pass


if __name__ == "__main__":
    run_webhook_server(5000, custom_handler)
