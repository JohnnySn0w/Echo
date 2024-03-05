ffmpeg -f pulse -i default -hide_banner -loglevel error -y -acodec pcm_s16le -ar 16000 -ac 1 userVoice.wav; ./talk.sh;
# parec --format=s16le --rate=16000 --channels=1 | sox -t raw -r 16000 -e signed -b 16 -c 1 - userVoice.wav; time ./talkV3.sh;
