"""This module collects the environment variables used to configure the FL process.
"""

import os

AGENT_TYPE = os.getenv("AGENT_TYPE")
MODEL_FILE = os.getenv("MODEL_FILE", "/model/params.json")
DATA_FILE = os.getenv("DATA_FILE", "/data/titanic_train.csv")
FL_CLIENT_ADMIN_URL = os.getenv("FL_CLIENT_ADMIN_URL", "http://fl-client-agent:8101")
