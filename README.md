[![github-actions](https://github.com/reinaldo-gomes/flieber-challenge/workflows/Tests/badge.svg?branch=master)](https://github.com/reinaldo-gomes/flieber-challenge/actions?query=workflow%3A%22Tests%22)
# flieber-challenge

This project aims to identify mutant DNA sequences in the most efficient way possible, according to the challenge's specifications.

All commands described should be run from the app's root folder.

## Requirements

- docker
- python 3.9+ recommended

## Installation

Just run the following command and let docker do everything for you:

    docker compose up --build

Also, install requirements in order to be able to execute app/tests outside the container:

    pip install -r requirements

Running the API outside the container requires that you install redis on your own.<br/>
You will also have to change redis server name (api.py, line 16) from "redis" to whatever IP your installation is pointing to.

A link to a running instance has been provided at AWS:<br/>
<http://ec2-3-144-85-40.us-east-2.compute.amazonaws.com:8000/docs>

## Features

- 100% code coverage, verifiable by running the following command:
    - `pytest tests -r chars -vp no:warnings --cov=mutants`
- Available API endpoints:
    - /mutant - Checks for DNA mutation
    - /stats - Calculates human x mutant DNA stats
    - /docs - OpenAPI docs, which can also be used call the endpoints above
- An async redis implementation was combined with FastAPI as an attempt to meet the 1-million-requests-per-second requirement.
