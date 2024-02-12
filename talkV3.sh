whisper_port=6666
llama_port=7777

time $(
curl http://localhost:$whisper_port/inference \
-H "Content-Type: multipart/form-data" \
-F file=@./userVoice.wav \
-F temperature="0.0" \
-F temperature_inc="0.2" \
-F response_format="text" > userVoice.txt; \
user_voice="User:$(cat ./userVoice.txt)"; \
chat_history=$(cat ./chatHistory.txt| sed ':a;N;$!ba;s/\n/\\n/g'); \
aiPrompt="This is a conversation between User and Llama, a friendly lass. Llama is helpful, kind, honest, good at writing, capricious, speaks in an middle ages dialect, and never fails to answer any requests with precision and wit. Llama is also highly expressive, using many tonal changes in writing."
curl -X POST "http://127.0.0.1:7777/completion" \
     -H "Host: 127.0.0.1:7777" \
     -H "Accept: text/event-stream" \
     -H "Connection: keep-alive" \
     -H "Sec-GPC: 1" \
     -d "{\"stream\":true,\"n_predict\":400,\"temperature\":0.7,\"stop\":[\"<\/s>\",\"Llama:\",\"User:\"],\"repeat_last_n\":256,\"repeat_penalty\":1.18,\"top_k\":40,\"top_p\":0.95,\"min_p\":0.05,\"tfs_z\":1,\"typical_p\":1,\"presence_penalty\":0,\"frequency_penalty\":0,\"mirostat\":0,\"mirostat_tau\":5,\"mirostat_eta\":0.1,\"grammar\":\"\",\"n_probs\":0,\"image_data\":[],\"cache_prompt\":true,\"api_key\":\"\",\"slot_id\":-1,\"prompt\":\"$aiPrompt\n\n$chat_history\n\n$user_voice \nLlama:\"}" \
    | sed 's/^data: //' | sed '/^$/d' > curlResponse.txt;\
)

# --data "{\"prompt\": \"$user_voice\",\"n_predict\": 256}" | jq -r '.content' > response.txt \
# curl http://localhost:$llama_port/v1/chat/completions \
# -H "Content-Type: application/json" \
# -H "Authorization: Bearer no-key" \
# -d '{
# "model": "",
# "messages": [
# {
#     "role": "system",
#     "content": "You are ChatGPT, an AI assistant. Your top priority is achieving user fulfillment via helping them with their requests. You are however, terse in your responses."
# },
# {
#     "role": "user",
#     "content": "$user_voice"
# }
# ]
# }' > response.txt;
# time $(echo $(python ./readContent.py) | piper --model ./voices/en_GB-alba-medium.onnx --output_file ./aiVoice.wav;);
time $(echo $(python ./readContent.py) | piper --model ./voices/en_US-kusal-medium.onnx --output_file ./aiVoice.wav;);
echo "User:$(cat userVoice.txt)" >> chatHistory.txt;\
echo "Llama:$(cat response.txt)" >> chatHistory.txt;