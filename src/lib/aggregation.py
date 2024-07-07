"""Module used by central party to initialize and setup aggregated FL model
"""

import json
import os

from .env import MODEL_FILE
from .validate import hex_to_dict


def perform_model_aggregation(data):
    """
    Perform model aggregation using weighted averaging.

    This function updates the model parameters stored in `MODEL_FILE` based on the incoming data.

    :param data: Data containing model parameters to aggregate.
    :type data: dict
    """
    old_model_params = None
    if os.path.isfile(MODEL_FILE):
        with open(MODEL_FILE, "r", encoding="utf-8") as file:
            old_model_params = json.load(file)

    updated_model_params = hex_to_dict(data["content"])

    if not old_model_params:
        updated_model_params["iteration"] = 1
    else:
        updated_model_params = weighted_average_model_params(
            old_model_params, updated_model_params
        )

    with open(MODEL_FILE, "w", encoding="utf-8") as file:
        json.dump(updated_model_params, file, indent=4)


def weighted_average_model_params(old, new):
    """
    Calculate the weighted average of model parameters.

    :param old: Old model parameters.
    :type old: dict
    :param new: New model parameters to be averaged in.
    :type new: dict
    :return: Weighted average of model parameters.
    :rtype: dict
    """
    iteration = old["iteration"]
    weight_agg = iteration / (iteration + 1)
    weight_new = 1 / (iteration + 1)

    avg_coef = [
        (weight_agg * a + weight_new * n)
        for a, n in zip(old["coef"][0], new["coef"][0])
    ]

    avg_intercept = [
        (weight_agg * a + weight_new * n)
        for a, n in zip(old["intercept"], new["intercept"])
    ]

    return {"coef": [avg_coef], "intercept": avg_intercept, "iteration": iteration + 1}
