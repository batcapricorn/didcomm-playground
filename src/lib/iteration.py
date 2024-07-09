"""Module that is used on client side to train a model
using local data
"""

import json
import logging
import os
import uuid

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

from .api import send_message
from .env import (
    DATA_FILE,
    TMP_DATA_FILE,
    LOCAL_TRAINING_SAMPLE_SIZE,
    FL_CLIENT_ADMIN_URL,
)
from .validate import hex_to_dict

logger = logging.getLogger(__name__)


def perform_training_iteration(data):
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
    Retrieve data for training from a primary CSV file or a temporary CSV file.
    The temporary CSV file is used to ensure that every data point is utilized
    at least once during training. By adjusting the number of iterations and
    the sample size (as configured in `env.py`), it is possible to
    guarantee that every data point is used exactly once.

    :param seed: Seed value for random sampling of data.
    :type seed: int
    :return: Features (X) and labels (y) for training.
    :rtype: tuple
    """
    if os.path.isfile(TMP_DATA_FILE):
        df = pd.read_csv(TMP_DATA_FILE)
        if df.shape[0] == 0:
            df = pd.read_csv(DATA_FILE)
    else:
        df = pd.read_csv(DATA_FILE)
    sample_df = df.sample(
        n=min(LOCAL_TRAINING_SAMPLE_SIZE, df.shape[0]), random_state=seed
    )
    remaining_df = df.drop(sample_df.index)
    sample_df.to_csv(TMP_DATA_FILE, index=False)
    remaining_df.to_csv(TMP_DATA_FILE, index=False)
    X_train = sample_df.drop("Survived", axis=1)
    y_train = sample_df["Survived"]
    return X_train, y_train


def get_model(model_params, X_train, y_train):
    """
    Initialize and configure a logistic regression model with given parameters.

    :param model_params: Parameters for configuring the logistic regression model.
    :type model_params: dict
    :param X_train: Features for training the model.
    :type X_train: pandas.DataFrame
    :param y_train: Labels for training the model.
    :type y_train: pandas.Series
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
