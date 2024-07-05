import binascii
import os
import json

import pandas as pd
import xgboost as xgb

from .logger import logger


TEST_DATA_FILE = "/data/titanic_train.csv"  # os.getenv("DATA_DIR")


def perfom_training_iteration():
    df = pd.read_csv(TEST_DATA_FILE).sample(n=50, random_state=42)

    X = df.drop("Survived", axis=1)
    y = df["Survived"]

    dtrain = xgb.DMatrix(X, label=y)

    # Define parameters
    params = {"objective": "binary:logistic", "eval_metric": "logloss", "eta": 0.1}

    # Train the model
    model = xgb.train(params, dtrain, num_boost_round=100)
    model_json = model.get_dump(dump_format="json")

    # Convert JSON to hex string
    json_str = json.dumps(model_json)  # Convert JSON object to string
    hex_str = binascii.hexlify(json_str.encode()).decode()
    logger.info("Model successfuly trained")
    logger.info(str(hex_str)[:20] + "...")
