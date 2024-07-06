import json
import logging
import os
import uuid

import pandas as pd
from sklearn.linear_model import LogisticRegression

logger = logging.getLogger(__name__)


TEST_DATA_FILE = os.getenv("TEST_DATA_FILE", "/data/titanic_train.csv")


def perfom_training_iteration():
    df = pd.read_csv(TEST_DATA_FILE).sample(n=50, random_state=42)

    X = df.drop("Survived", axis=1)
    y = df["Survived"]

    model = LogisticRegression(max_iter=1000)
    model.fit(X, y)

    coef = model.coef_.tolist()
    intercept = model.intercept_.tolist()

    data = {"coef": coef, "intercept": intercept}
    json_str = json.dumps(data)
    json_bytes = json_str.encode("utf-8")
    hex_str = json_bytes.hex()

    training_id = uuid.uuid4()
    logger.info("Model successfuly trained. Training ID: %s. Hex String: %s...", str(training_id), str(hex_str)[:20])
