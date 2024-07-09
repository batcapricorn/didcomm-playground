"""This module collects the environment variables used to configure the FL process.
"""

import os

AGENT_TYPE = os.getenv("AGENT_TYPE")
MODEL_FILE = os.getenv("MODEL_FILE", "/model/params.json")
DATA_FILE = os.getenv("DATA_FILE", "/data/titanic_train.csv")
TMP_DATA_FILE = os.getenv("TMP_DATA_FILE", "/data/tmp.csv")
LOCAL_TRAINING_SAMPLE_SIZE = int(os.getenv("LOCAL_TRAINING_SAMPLE_SIZE", "40"))
FL_CLIENT_ADMIN_URL = os.getenv("FL_CLIENT_ADMIN_URL", "http://fl-client-agent:8101")
