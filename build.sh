#!/bin/bash
GPU_NAME=$(/opt/rocm/bin/rocminfo | grep -o '\sgfx[0-9]*'|sed 's/ //') #try to grab target, may not work.

if [[ $GPU_NAME =~ (gfx[0-9]+) ]]; then
  echo "Extracted GPU name: $GPU_NAME"
  echo "Using HIPBLAS."
  cd whisper.cpp;
  make clean; make -j $(nproc) WHISPER_HIPBLAS=1;
  cd ..;
  cd llama.cpp;
  make clean; make -j $(nproc) LLAMA_HIPBLAS=1 AMDGPU_TARGETS=$GPU_NAME # the AMDGPU_TARGETS changes based on gpu used. Lookup table here: https://docs.amd.com/en/docs-5.4.3/release/gpu_os_support.html#gpu-support-table 
  cd ..;
else
  echo "No compatible GPU found. Instead found $GPU_NAME. Using CLBLAST."
  cd whisper.cpp;
  make clean; make -j $(nproc) WHISPER_CLBLAST=1;
  cd ..;
  cd llama.cpp;
  make clean; make -j $(nproc) LLAMA_CLBLAST=1;
  cd ..;
fi