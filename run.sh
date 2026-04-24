#!/bin/bash

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running trainer..."
PYTHONPATH=. python -m backend.core.trainer
