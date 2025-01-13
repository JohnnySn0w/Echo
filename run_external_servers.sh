#!/bin/bash
source ./venv/bin/activat
nohup python ./src/listen.py > listen.log & echo $! > run.pid