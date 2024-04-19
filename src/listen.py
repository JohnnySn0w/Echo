# Copyright 2022 David Scripka. All rights reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Modified 2024 by Michael Mahan. All rights reserved.
# Modifications include additions for curl requests, renaming of variables for coherency, refactoring(including separation into multiple files).

# Standard library imports
import collections
import datetime
import json
import os
import platform
import subprocess
import sys
import time
import argparse
from io import BytesIO, StringIO

# Related third-party imports
import numpy as np
import openwakeword
import pyaudio
import requests
import scipy.io.wavfile
import wave

# Local application/library-specific imports
from argsToParse import gibbe_args
import config
from openwakeword.model import Model
from readContent import parse_json_and_concatenate


def get_audio_interface(chunk_size: int) -> tuple[pyaudio.Stream, pyaudio.PyAudio]:
    # Get microphone stream
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = chunk_size
    audio_interface = pyaudio.PyAudio()
    mic_stream = audio_interface.open(
        format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
    )
    return mic_stream, audio_interface


def get_mic_input_result(
    mic_stream: pyaudio.PyAudio, owwModel: openwakeword.model.Model, chunk_size: int
) -> dict:
    # Get audio
    mic_audio = np.frombuffer(mic_stream.read(chunk_size), dtype=np.int16)

    # Feed to openWakeWord model
    return owwModel.predict(mic_audio)


def get_user_voice_input(owwModel: openwakeword.model.Model) -> BytesIO:
    # Capture total of 8 seconds, with the microphone audio associated with the
    # activation around the ~4 second point
    audio_context = np.array(
        list(owwModel.preprocessor.raw_data_buffer)[-16000 * 8 :]
    ).astype(np.int16)
    mic_input_data = BytesIO()
    scipy.io.wavfile.write(mic_input_data, 16000, audio_context)
    mic_input_data.seek(0)
    return mic_input_data


def gen_llm_response() -> requests.Response:
    llama_body_json = json.dumps(config.llama_body(userVoice))

    llama_response = requests.post(
        config.llama_url, headers=config.llama_headers, data=llama_body_json, timeout=30
    )

    piper_content = "\n".join(
        line.replace("data: ", "", 1)
        for line in llama_response.text.splitlines()
        if line.strip()
    )
    response_string = StringIO(piper_content)
    return response_string


def gen_ai_voice(piper_content: str) -> requests.Response:
    return requests.post(
        config.piper_url, headers=config.piper_headers, data=piper_content
    )


def update_chat_history(userVoice: str, aiVoice: str) -> None:
    with open("chatHistory.txt", "a") as chat_history:
        chat_history.write(f"{config.userName}: {userVoice}")
        chat_history.write(f"{config.aiName}: {aiVoice}\n")


def respond_with_voice(
    audio_interface: pyaudio.PyAudio, piper_response: requests.Response
)->bytes:
    voice_data = BytesIO(piper_response.content)
    voice_data.seek(0)

    wf = wave.open(voice_data, "rb")
    speaker_stream = audio_interface.open(
        format=audio_interface.get_format_from_width(wf.getsampwidth()),
        channels=wf.getnchannels(),
        rate=wf.getframerate(),
        output=True,
    )
    data = wf.readframes(1024)
    while data:
        speaker_stream.write(data)
        data = wf.readframes(1024)
    speaker_stream.stop_stream()
    speaker_stream.close()
    return piper_response.content


def setup_components():
    components = dict()
    components['args'] = gibbe_args()
    setup_audio_interface(components['args'].chunk_size)
    return components

def gen_oww_model(args: argparse.Namespace):
    return Model(
        wakeword_models=[args.model_path],
        enable_speex_noise_suppression=args.noise_suppression,
        vad_threshold=args.vad_threshold,
        inference_framework=args.inference_framework,
    )

def setup_infrastructure(args: argparse.Namespace):
    # Create output directory if it does not already exist
    if not os.path.exists(args.output_dir):
            os.mkdir(args.output_dir)
    # necessary as it grabs some interpretive models + the demo wakeset
    openwakeword.utils.download_models()

# Run capture loop, checking for hotwords
if __name__ == "__main__":
    args = gibbe_args()
    setup_infrastructure(args)
    # components = setup_components()
    owwModel = gen_oww_model(args)
    mic_stream, audio_interface = get_audio_interface(args.chunk_size)

    # Predict continuously on audio stream
    last_save = time.time()
    activation_times = collections.defaultdict(list)

    print("\n\nListening for wakewords...\n")
    while True:
        prediction = get_mic_input_result(mic_stream, owwModel, args.chunk_size)

        # Check for model activations (score above threshold), and save clips
        for model in prediction.keys():
            if prediction[model] >= args.threshold:
                activation_times[model].append(time.time())

            if (
                activation_times.get(model)
                and (time.time() - last_save) >= config.cooldown
                and (time.time() - activation_times.get(model)[0]) >= config.save_delay
            ):
                # TODO: do we actually need a backoff timer?
                last_save = time.time()
                activation_times[model] = []
                detect_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

                print(
                    f'Detected activation from "{model}" model at time {detect_time}!'
                )

                mic_input_data = get_user_voice_input(owwModel)
                userVoice = requests.post(
                    config.whisper_url,
                    files=config.whisper_file(config.userVoice, mic_input_data),
                    data=config.whisper_data,
                )
                mic_input_data.close()

                response_string = gen_llm_response()
                piper_content = parse_json_and_concatenate(
                    response_string
                )
                update_chat_history(userVoice.text, piper_content)
                # Send the POST request with the content from readContent.py as the body
                piper_response = gen_ai_voice(piper_content)
                print(piper_content)
                # Write the response content to a file

                respond_with_voice(audio_interface, piper_response)
