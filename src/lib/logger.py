import logging
import logging.config


def setup_logging(config_file=None):
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(), logging.FileHandler("app.log", "a")],
    )
    return logging.getLogger()


logger = setup_logging()
