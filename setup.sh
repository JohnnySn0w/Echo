#!/bin/bash
pipx install piper-tts 
if [[ ! -d llms ]]; then
  mkdir llms
fi
if [[ ! -d voices ]]; then
  mkdir voices;
fi
echo "Directories ready for downloads";
./buildAMD.sh
