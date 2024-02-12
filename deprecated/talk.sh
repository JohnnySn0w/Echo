ffmpeg -f pulse -i default -hide_banner -loglevel error -y -acodec pcm_s16le -ar 16000 -ac 1 userVoice.wav;\
./whisper.cpp/main -f userVoice.wav -m ./whisper.cpp/models/ggml-large-v3-q5_0.bin -otxt --no-prints --no-timestamps -of userVoice;\
./llama.cpp/main -t 8 -m ./llama.cpp/models/llama-2-13b.Q4_K_M.gguf --no-display-prompt --file ./userVoice.txt -n 128 -ngl 10000 > response.txt;\
echo $(cat response.txt) | piper --model ./voices/en_US-kusal-medium.onnx --output_file aiVoice.wav;\
sleep 1;\
mpv aiVoice.wav & ;
#  ffmpeg -i welcome.wav -acodec pcm_s16le -f s16le -ac 1 -ar 16000 -| ./temp/whisper.cpp/stream-stdin -m ./temp/whisper.cpp/models/ggml-base.en.bin -f whatAISaid.txt