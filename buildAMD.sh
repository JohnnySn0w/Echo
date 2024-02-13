#!/bin/bash
cd whisper.cpp;
make clean; make WHISPER_HIPBLAS=1;
cd ..;
cd llama.cpp;
make clean; make LLAMA_HIPBLAS=1 AMDGPU_TARGETS=gfx906 # the AMDGPU_TARGETS changes based on gpu used. Lookup table here: https://docs.amd.com/en/docs-5.4.3/release/gpu_os_support.html#gpu-support-table 
cd ..;