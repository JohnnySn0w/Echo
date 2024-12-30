#!/bin/bash
source ./venv/bin/activate
cd piper/src/python_run
nohup python -m piper.http_server -m ../../../voices/en_GB-alba-medium.onnx > piper.log & echo $! > ../../../run.pid
cd ../../..;
nohup python ./src/listen.py > listen.log & echo $! >> run.pid