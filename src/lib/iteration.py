import json
import logging
import os
import requests
import uuid

import pandas as pd
from sklearn.linear_model import LogisticRegression

from .validate import hex_to_dict

logger = logging.getLogger(__name__)


TEST_DATA_FILE = os.getenv("TEST_DATA_FILE", "/data/titanic_train.csv")


def send_message(connection_id, message_content):
    agent_url = "http://fl-client-agent:8101"
    endpoint = f"{agent_url}/connections/{connection_id}/send-message"
    payload = {"content": message_content}
    response = requests.post(endpoint, json=payload)
    if response.status_code == 200:
        logger.info(f"Successfully sent message: {message_content}")
    else:
        logger.error(f"Failed to send message: {response.text}")


def perfom_training_iteration(data):
    df = pd.read_csv(TEST_DATA_FILE).sample(n=50, random_state=42)

    X = df.drop("Survived", axis=1)
    y = df["Survived"]

    model_params = hex_to_dict(data["content"])
    model = LogisticRegression(max_iter=1000)
    if model_params["coef"] and model_params["intercept"]:
        model.coef_ = model_params["coef"]
        model.intercept_ = model_params["intercept"]

    model.fit(X, y)

    coef = model.coef_.tolist()
    intercept = model.intercept_.tolist()

    updated_model_params = {"coef": coef, "intercept": intercept}
    json_str = json.dumps(updated_model_params)
    json_bytes = json_str.encode("utf-8")
    hex_str = json_bytes.hex()

    training_id = uuid.uuid4()
    logger.info(
        "Model successfuly trained. Training ID: %s. Hex String: %s...",
        str(training_id),
        str(hex_str)[:20],
    )
    connection_id = data["connection_id"]
    logger.info("sending message...")
    send_message(connection_id, hex_str)
