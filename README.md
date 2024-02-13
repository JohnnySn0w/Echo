# Echo - an effort at getting AMD support for all sections of a completely-local-compute, AI assistant

There are an incredible plethora of current AI tools, some very high level, like transformers.

Many have, at most, third class support for AMD GPUs. Even with ROCm being out as long as it has.

This is an effort to collage together a suite of model running programs, and get a voice-to-voice assistant, via voice-to-text, text-to-text, and text-to-voice.


## Setup
First, you need to be on linux, ROCm doesn't have good, if any, support on windows at the moment. If you're here, you might already know it's primarily supported on Redhat, SUSE, and Debian. What you might not know is other distros, like Arch, [do support it through user repos](https://github.com/rocm-arch/rocm-arch).

Once you have ROCm properly installed you can progress.

You'll want ffmpeg for the voice_query script, but it's not necessary. Just need something that will generate 16000hz .wav files.

Kickoff the building of the various components with
```sh
./setup.sh;
```

This script:
- installs all the python libs I have in my project venv. No guarantees this will work for you, have not even tested if most of them are necessary.
```python
pip install onnxruntime-gpu huggingface-hub optimum precise-runner llm piper-tts transformers datasets evaluate jiwer     
pip install --upgrade accelerate 
```
- makes directories that will need to be **manually** filled by you with appropriate models
- builds the whisper.cpp and llama.cpp models. For llama.cpp you will probably want to either rebuild with clblast flags if your gpu isn't on the rocm compat list. Check [here](https://docs.amd.com/en/docs-5.4.3/release/gpu_os_support.html#gpu-support-table) for a comprehensive list of gpus rocm supports. Use the llvm target that you need, and modify the buildAMD.sh script to get that building for your gpu.

Get into the venv
```sh
source ./venv/bin/activate;
```

Once everything is built, try using 
```sh
runAMD.sh;
```

If you aren't comfortable with locating processes and terminating them manually, *then don't run that script*. Instead you can run each command in a separate terminal tab and it will also work.


Finally, you can trigger a voice input/output using:
```sh
voice_query.sh; paplay ./aiVoice.wav;
```
The main thing here is you need something that will gen a 16000hz audio input to send through `talkV3.sh`. The final output of this will be a .wav file, and you can trivially use whatever to play the assistant's response.

That's it!


## Bugs
- currently, I have noticed that if the microphone and the output are hooked to the same interface (like a Scarlett DAC) then there's a cutoff/delay at the beginning of the ai speech output. Not sure what's happening there since Pulse should handle that sort of thing, and Discord works fine.