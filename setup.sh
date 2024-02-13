#!/bin/bash
python -m venv venv
source ./venv/bin/activate
python -m pip install -r requirements.txt;
mkdir llms voices;
echo "Directories ready for downloads";
./buildAMD.sh
