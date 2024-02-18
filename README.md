<p align="center">
  <img height=auto width=25% src="https://github.com/JohnnySn0w/Echo/blob/master/mascot_images/Echo.png" alt="Emoji Oread, Echo"/>
</p>

<div height=auto width=2em>
  <h1 align="center">— Echo —<p>An AMD-first, completely-local-compute, AI assistant</p></h1>
</div>

A plethora of AI tools are currently available.

Many have, at most, rough support for AMD GPUs.

This is an effort to collage together a suite of model running programs, and get a voice-to-voice assistant, via voice-to-text, text-to-text, and text-to-voice.

All with an eye towards easier usage of existing AMD support.

---
## Current capabilities
- [x] End to end, voice-to-voice.
- [x] Assistance with getting ROCm drivers and custom builds for whisper.cpp/llama.cpp that support ROCm compatible GPUs

Benchmarks are located [here](https://github.com/JohnnySn0w/Echo/blob/master/benchmarks), you are more than welcome to submit yours.

## Goals
- [ ] 🏃 Load piper into VRAM for persistence (remove model load time)
- [ ] ⚙️ Setup piper to use AMD GPU (requires custom builds of underlying libs like onnxruntime)
- [ ] 🗣️ More naturalistic responses in the voice output
- [ ] 📝 Implement usage of command functionality from whisper.cpp
- [ ] 💾 Potentially dockerize
- [ ] 🛠️ Fine tuning parameters of various components to optimize processing times
- [ ] 🤖 Bots? Bots.
- [ ] 🪟 Windows implementation

## Setup

### Prerequisites
First, you (probably) need to be on linux. If you're here, you might already know it's primarily supported on Redhat, SUSE, and Debian. What you might not know is other distros, like Arch, [do support it through user repos](https://github.com/rocm-arch/rocm-arch).

Second, you'll (probably) want `ffmpeg` for the `voice_query.sh` script. You don't necessarily need to use `ffmpeg`, `arecord` or `parec` would also work. You just something that will generate 16000hz .wav files from your microphone.

Third, have an installation of [pipx](https://github.com/pypa/pipx?tab=readme-ov-file#install-pipx)


### Build & Ship
1. Install piper-tts via `pipx`, or into a venv. `pipx` is certainly more convenient.
   * There are some issues with a recent swap on semantic versioning for piper-tts. A temp workaround has been found thanks to nickolay under [piper-phonemize issue-14](https://github.com/rhasspy/piper-phonemize/issues/14#issuecomment-1837289540)

2. Kick off the building of the various components with
```sh
./setup.sh;
```
This script:
- Makes directories that will need to be **manually** filled by you with appropriate models
- Builds the whisper.cpp and llama.cpp models. For llama.cpp you will probably want to either rebuild with clblast flags if your gpu isn't on the rocm compat list. Check [here](https://docs.amd.com/en/docs-5.4.3/release/gpu_os_support.html#gpu-support-table) for a comprehensive list of gpus rocm supports. Use the llvm target that you need, and modify the buildAMD.sh script to get that building for your gpu.


2. Download models for the program to use.
  - llama.cpp: [instructions here](https://github.com/ggerganov/llama.cpp/blob/master/README.md#obtaining-and-using-the-facebook-llama-2-model) >> `.gguf` goes into `llms` folder
  - whisper.cpp: [instructions here](https://github.com/ggerganov/whisper.cpp/blob/master/models/README.md) >> `.bin` goes into `./whisper.cpp/models` folder
  - piper: [instructions here](https://github.com/rhasspy/piper/blob/master/README.md#usage) >> `.onnx` and `.onnx.json` go into `voices` folder


3. If you aren't comfortable with locating processes and terminating them manually, *then don't run this script*. Instead you can run each command in a separate terminal tab and it will also work. Also, make sure to replace model names with the models you downloaded.

> individual commands
```sh
nohup ./whisper.cpp/server -m ./whisper.cpp/models/ggml-large-v3-q5_0.bin --port 6666 --no-timestamps > ./whisper.cpp/whisper.log &
nohup ./llama.cpp/server -m ./llms/capybarahermes-2.5-mistral-7b.Q4_K_M.gguf -ngl 1000 --port 7777 > ./llama.cpp/llama.log &
```
> single command
```sh
runAMD.sh;
```




4. Finally, you can trigger a voice input/output using:
```sh
voice_query.sh; paplay ./aiVoice.wav;
```
The main thing here is you need something that will gen a 16000hz audio input to send through `talkV3.sh`. I prefer ffmpeg because I can hit q when I'm done. 

The final output of this will be a .wav file, and you can trivially use whatever to play the assistant's response.

That's it!

## Licensing
whisper.cpp, piper, and llama.cpp are licensed under MIT license.

The Echo mascot image was originally generated with the assistance of DALL·E 3. It was further edited by @JohnnySn0w.


## Bugs
- currently, I have noticed that if the microphone and the output are hooked to the same interface (like a Scarlett DAC) then there's a cutoff/delay at the beginning of the ai speech output. Not sure what's happening there since Pulse should handle that sort of thing, and Discord works fine.

<p align="center">
  <img height=auto width=5% src="https://github.com/JohnnySn0w/Echo/blob/master/mascot_images/Echo.png" alt="Emoji Oread, Echo"/>
</p>
