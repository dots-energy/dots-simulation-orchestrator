#!/bin/bash

if [ ! -d "./.venv" ]; then
  echo "Creating virtualenv directory"
  python3.9 -m venv ./.venv  # Match the Python version (currently 3.9) from Dockerfile
fi

. .venv/bin/activate
pip install pip-tools
pip-sync dev-requirements.txt requirements.txt
