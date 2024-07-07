"""Module used by central party to initialize and setup aggregated FL model
"""

import json
import os

from .validate import hex_to_dict


def perform_model_aggregation(data):
    old_model_params = None
    model_file = "/model/params.json"
    if os.path.isfile(model_file):
        with open(model_file, "r") as file:
            old_model_params = json.load(file)

    updated_model_params = hex_to_dict(data["content"])

    if not old_model_params:
        updated_model_params["iteration"] = 1
    else:
        updated_model_params = weighted_average_model_params(
            old_model_params, updated_model_params
        )

    with open(model_file, "w") as file:
        json.dump(updated_model_params, file, indent=4)


def weighted_average_model_params(old, new):
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
