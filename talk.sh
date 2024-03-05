whisper_port=6666
llama_port=7777

time $(
curl http://localhost:$whisper_port/inference \
-H "Content-Type: multipart/form-data" \
-F file=@./userVoice.wav \
-F temperature="0.0" \
-F temperature_inc="0.2" \
-F response_format="text" > userVoice.txt;

user_voice="User:$(cat ./userVoice.txt | sed 's/"/`/g')"; \
chat_history=$(cat ./chatHistory.txt | sed ':a;N;$!ba;s/\n/\\n/g; s/"/`/g'); \
aiPrompt="This is a conversation between User and Echo, a friendly sort. Echo is helpful, kind, honest, good at writing, capricious, and never fails to answer any requests with precision. Echo is also highly expressive, using many tonal changes in writing.";

curl -X POST "http://127.0.0.1:7777/completion" \
     -H "Host: 127.0.0.1:7777" \
     -H "Accept: text/event-stream" \
     -H "Connection: keep-alive" \
     -H "Sec-GPC: 1" \
     -d "{\"stream\":true,\"n_predict\":400,\"temperature\":0.7,\"stop\":[\"<\/s>\",\"Echo:\",\"User:\"],\"repeat_last_n\":256,\"repeat_penalty\":1.18,\"top_k\":40,\"top_p\":0.95,\"min_p\":0.05,\"tfs_z\":1,\"typical_p\":1,\"presence_penalty\":0,\"frequency_penalty\":0,\"mirostat\":0,\"mirostat_tau\":5,\"mirostat_eta\":0.1,\"grammar\":\"\",\"n_probs\":0,\"image_data\":[],\"cache_prompt\":true,\"api_key\":\"\",\"slot_id\":-1,\"prompt\":\"$aiPrompt\n\n$chat_history\n\n$user_voice \nEcho:\"}" \
    | sed 's/^data: //' | sed '/^$/d' > curlResponse.txt;
)

time curl -X POST -H 'Content-Type: text/plain' --data "$(echo $(python ./readContent.py))" -o aiVoice.wav 'localhost:5000';
echo "User:$(cat userVoice.txt)" >> chatHistory.txt;\
echo "Echo:$(cat response.txt)" >> chatHistory.txt;