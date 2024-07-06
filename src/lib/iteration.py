import json
import logging
import os
import requests
import uuid

import pandas as pd
from sklearn.linear_model import LogisticRegression

from .api import send_message
from .validate import hex_to_dict

logger = logging.getLogger(__name__)


TEST_DATA_FILE = os.getenv("TEST_DATA_FILE", "/data/titanic_train.csv")
FL_CLIENT_ADMIN_URL = os.getenv("FL_CLIENT_ADMIN_URL", "http://fl-client-agent:8101")


def perfom_training_iteration(data):
    X, y = get_data()

    model_params = hex_to_dict(data["content"])
    model = get_model(model_params, X, y)
    hex_str = get_model_hex_string(model)

    training_id = uuid.uuid4()
    logger.info(
        "Model successfuly trained. Training ID: %s. Hex String: %s...",
        str(training_id),
        str(hex_str)[:20],
    )
    connection_id = data["connection_id"]
    send_message(FL_CLIENT_ADMIN_URL, connection_id, hex_str)


def get_data():
    df = pd.read_csv(TEST_DATA_FILE).sample(n=50, random_state=42)
    X = df.drop("Survived", axis=1)
    y = df["Survived"]
    return X, y


def get_model(model_params, X, y):
    model = LogisticRegression(max_iter=1000)
    if model_params["coef"] and model_params["intercept"]:
        model.coef_ = model_params["coef"]
        model.intercept_ = model_params["intercept"]

    model.fit(X, y)
    return model


def get_model_hex_string(model):
    coef = model.coef_.tolist()
    intercept = model.intercept_.tolist()

    updated_model_params = {"coef": coef, "intercept": intercept}
    json_str = json.dumps(updated_model_params)
    json_bytes = json_str.encode("utf-8")
    hex_str = json_bytes.hex()
    return hex_str
