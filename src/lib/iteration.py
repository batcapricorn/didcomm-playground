"""Module that is used on client side to train a model
using local data
"""

import json
import logging
import uuid

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

from .api import send_message
from .env import DATA_FILE, FL_CLIENT_ADMIN_URL
from .validate import hex_to_dict

logger = logging.getLogger(__name__)


def perfom_training_iteration(data):
    """
    Perform a training iteration using federated learning.

    This function handles the training iteration by:
    1. Converting incoming hex string data to model parameters.
    2. Retrieving data for training using a seed derived from the hex string.
    3. Training a logistic regression model using the retrieved data.
    4. Converting the trained model back to a hex string and sending it to the client.

    :param data: Data received for the training iteration,
        expected to contain "content" and "connection_id".
    :type data: dict
    """
    incoming_hex_str = data["content"]
    model_params = hex_to_dict(incoming_hex_str)
    seed = int(incoming_hex_str, 16) % (2**32)
    X_train, y_train = get_data(seed)

    model = get_model(model_params, X_train, y_train)
    hex_str = get_model_hex_string(model)

    training_id = uuid.uuid4()
    logger.info(
        "Model successfully trained. Training ID: %s. Hex String: %s...",
        str(training_id),
        str(hex_str)[:20],
    )
    connection_id = data["connection_id"]
    send_message(FL_CLIENT_ADMIN_URL, connection_id, hex_str)


def get_data(seed=123):
    """
    Retrieve data for training from a CSV file.

    :param seed: Seed value for random sampling of data.
    :type seed: int
    :return: Features (X) and labels (y) for training.
    :rtype: tuple
    """
    df = pd.read_csv(DATA_FILE).sample(n=20, random_state=seed)
    X_train = df.drop("Survived", axis=1)
    y_train = df["Survived"]
    return X_train, y_train


def get_model(model_params, X_train, y_train):
    """
    Initialize and configure a logistic regression model with given parameters.

    :param model_params: Parameters for configuring the logistic regression model.
    :type model_params: dict
    :param X: Features for training the model.
    :type X: pandas.DataFrame
    :param y: Labels for training the model.
    :type y: pandas.Series
    :return: Configured logistic regression model.
    :rtype: sklearn.linear_model.LogisticRegression
    """
    model = LogisticRegression(max_iter=1000)
    if model_params["coef"] and model_params["intercept"]:
        model.coef_ = np.array(model_params["coef"])
        model.intercept_ = np.array(model_params["intercept"])
        model.classes_ = np.array([0, 1])

    model.fit(X_train, y_train)
    return model


def get_model_hex_string(model):
    """
    Convert a trained logistic regression model to a hexadecimal string representation.

    :param model: Trained logistic regression model.
    :type model: sklearn.linear_model.LogisticRegression
    :return: Hexadecimal string representation of the model parameters.
    :rtype: str
    """
    coef = model.coef_.tolist()
    intercept = model.intercept_.tolist()

    updated_model_params = {"coef": coef, "intercept": intercept}
    json_str = json.dumps(updated_model_params)
    json_bytes = json_str.encode("utf-8")
    hex_str = json_bytes.hex()
    return hex_str
