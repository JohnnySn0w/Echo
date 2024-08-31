#!/bin/bash
nohup ./whisper.cpp/server -m ./whisper.cpp/models/ggml-large-v3-q5_0.bin --port 6666 --no-timestamps > ./whisper.cpp/whisper.log & echo $! > run.pid
nohup ./llama.cpp/server -m ./llms/capybarahermes-2.5-mistral-7b.Q4_K_M.gguf -ngl 1000 --port 7777 > ./llama.cpp/llama.log & echo $! >> run.pid
source ./venv/bin/activate
cd piper/src/python_run
nohup python -m piper.http_server -m ../../../voices/en_US-kusal-medium.onnx > piper.log & echo $! >> ../../../run.pid
cd ../../..;
nohup python ./src/listen.py > listen.log & echo $! >> run.pid