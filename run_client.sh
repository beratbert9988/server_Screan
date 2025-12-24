#!/bin/bash
source .venv/bin/activate
# Make sure we are in the client directory so relative assets work if any, or paths resolve
export PYTHONPATH=$PYTHONPATH:$(pwd)
export LD_LIBRARY_PATH=$(pwd)/libs:$LD_LIBRARY_PATH
python client/main.py
