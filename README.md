[![Python Linting and Formatting](https://github.com/batcapricorn/didcomm-playground/actions/workflows/qa.yml/badge.svg)](https://github.com/batcapricorn/didcomm-playground/actions/workflows/qa.yml)

# Securing Federated Learning

This project demonstrates the integration of Verifiable Credentials into a Federated Learning environment for Authentication & Gradient Sharing, inspired by concepts from the [PyDentity](https://github.com/OpenMined/PyDentity) project.

## TL;DR

Boot up the necessary infrastructure by:
1. Installing all dependencies: `pipenv install`
2. Running `docker compose up -d`

That's it! Feel free to explore my Jupyter notebooks stored at `/notebooks`. Make sure to use the corresponding kernel installed in step one. As already indicated, I used [pipenv](https://pipenv.pypa.io/en/latest/) for package management.

## Architecture

The `docker-compose.yml` boots up two [ACA-Py](https://github.com/hyperledger/aries-cloudagent-python) agents that can communicate with each other using DIDComm and its `/basicmessages` endpoint. ACA-Py agents can be connected with webhooks, which was my main work. The agents forward every request to the webhook in a specific manner. This way, I can send model gradients via DIDComm and parse them within a webhook container. The corresponding source code is located in `/src`.

> For simplicity, this project currently only supports a simple setup of one client and one central party.

## Settings

The webhooks can be configured using environment variables:
* `AGENT_TYPE`: either `CENTRAL` for a central party webhook (handles, e.g., aggregation of gradients) or `CLIENT` for an FL client webhook (handles, e.g., local training iterations)
* `MODEL_FILE`: Optional, temporary file to store model parameters. The file can be accessed outside of the container using docker volumes. Defaults to `/model/params.json`
* `DATA_FILE`: Optional, data file that is used for training. The path must be accessible within the container. Defaults to `/data/titanic_train.csv`
* `TMP_DATA_FILE`: Optional, temporary data file that is used to ensure that every data point is used at least or exactly once, depending on the number of iterations. Defaults to `/data/tmp.csv`
* `LOCAL_TRAINING_SAMPLE_SIZE`: Optional, number of data points that a client should use at one iteration. Defaults to `40`. Please note that environment variables need to be strings in Python. The variable gets casted to `int` along the way.
* `FL_CLIENT_ADMIN_URL`: Optional, ADMIN URL of the FL client. Defaults to `http://fl-client-agent:8101`
