<p align="center">
  <img height=auto width=25% src="https://github.com/JohnnySn0w/Echo/blob/master/mascot_images/Echo.png" alt="Emoji Oread, Echo"/>
</p>

<div height=auto width=2em>
  <h1 align="center">— Echo —<p>A completely-local-compute, AI assistant</p></h1>
</div>

A plethora of AI tools are currently available.

This is an effort to collage together a suite of model running programs, and get a voice-to-voice assistant, via voice-to-text, text-to-text, and text-to-voice.

All with an eye towards easier usage of existing non-NVIDIA support.

---
## Current capabilities
- [x] End to end, voice-to-voice.
- [x] Assistance with getting ROCm drivers and custom builds for whisper.cpp/llama.cpp that support ROCm compatible GPUs
- [x] All models are loaded into RAM/VRAM for quick access.

Benchmarks are located [here](https://github.com/JohnnySn0w/Echo/blob/master/benchmarks), you are more than welcome to submit yours.

## Goals
- [x] 🏃 Load piper into VRAM for persistence (remove model load time)
- [ ] ⚙️ Setup piper to use AMD GPU (requires custom builds of underlying libs like onnxruntime)
- [ ] 🗣️ More naturalistic responses in the voice output
- [ ] 📝 Implement usage of command functionality from whisper.cpp
- [ ] 💾 Potentially dockerize
- [ ] 🛠️ Fine tuning parameters of various components to optimize processing times
- [ ] 🤖 Bots? Bots.
- [ ] 🪟 Windows implementation

## Setup

### Prerequisites
First, you (probably) need to be on linux. If you're here, you might already know ROCm is primarily supported on Redhat, SUSE, and Debian. What you might not know is other distros, like Arch, [do support it through user repos](https://github.com/rocm-arch/rocm-arch).

You're going to need to have Python 3.11 as the system version for the install. After that, you can change it. The recommended way to handle mutliple python versions is something like [pyenv](https://github.com/pyenv/pyenv)


### Build & Ship
1. Kick off the building of the various components with
```sh
./setup.sh;
```
This script:
- Makes directories that are filled with appropriate models
- Optionally downloads default models (if you skip this, see 1b)
- Pulls in the submodules
- Builds the whisper.cpp and llama.cpp models. For llama.cpp you will probably want to either rebuild with clblast flags if your gpu isn't on the rocm compat list. Check [here](https://docs.amd.com/en/docs-5.4.3/release/gpu_os_support.html#gpu-support-table) for a comprehensive list of gpus rocm supports. Use the llvm target that you need, and modify the buildAMD.sh script to get that building for your gpu.


1b. Download models for the program to use if you didn't want defaults.
  - llama.cpp: [instructions here](https://github.com/ggerganov/llama.cpp/blob/master/README.md#obtaining-and-using-the-facebook-llama-2-model) >> `.gguf` goes into `llms` folder
  - whisper.cpp: [instructions here](https://github.com/ggerganov/whisper.cpp/blob/master/models/README.md) >> `.bin` goes into `./whisper.cpp/models` folder
  - piper: [instructions here](https://github.com/rhasspy/piper/blob/master/README.md#usage) >> `.onnx` and `.onnx.json` go into `voices` folder
or for some quick defaults, run
```
./defaultModels.sh
```

2. Load everything up with
```sh
run.sh;
```

Make sure to use the 'Echo' wakeword so it knows you're talking.

That's it!

## Licensing
whisper.cpp, piper, and llama.cpp are licensed under MIT license.

The Echo mascot image was originally generated with the assistance of DALL·E 3. It was further edited by @JohnnySn0w.


## Bugs
- currently, I have noticed that if the microphone and the output are hooked to the same interface (like a Scarlett DAC) then there's a cutoff/delay at the beginning of the ai speech output. Not sure what's happening there since Pulse should handle that sort of thing, and Discord works fine.

<p align="center">
  <img height=auto width=5% src="https://github.com/JohnnySn0w/Echo/blob/master/mascot_images/Echo.png" alt="Emoji Oread, Echo"/>
</p>
