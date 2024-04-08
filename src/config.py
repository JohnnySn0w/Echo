# You may change the ai name at your leisure, however you will need to replace the inference model with one that will take the new name and detect it.
# Otherwise, the ai will beef with you about what its name is.
aiName = "Echo"
userName = "User"
server_location = "localhost"
whisper_port = "6666"
llama_port = "7777"
piper_port = "5000"
whisper_url = f"http://{server_location}:{whisper_port}/inference"
llama_url = f"http://{server_location}:{llama_port}/completion"
piper_url = f"http://{server_location}:{piper_port}"
talk_phrases = ["<|im_end|>", "<|im_start|>"]

llama_headers = {
    "Host": f"{server_location}:{llama_port}",
    "Accept": "text/event-stream",
    "Connection": "keep-alive",
    "Sec-GPC": "1",
}

piper_headers = {"Content-Type": "text/plain"}

whisper_data = {
    "temperature": "0.0",
    "temperature_inc": "0.2",
    "response_format": "text",
}

userVoice = "Echo.wav"
llama_outfile = "curlResponse.txt"
aiVoice = "./aiVoice.wav"
chatHistory = "./chatHistory.txt"

echo_behavioral_prompt = f"You are now absolutely known only as {aiName}. You absolutely do not respond to Llama. This is a conversation between {userName} and {aiName}, a friendly sort. {aiName} is helpful, kind, honest, good at writing, capricious, and never fails to answer any requests while being concise. {aiName} is also highly expressive, using many tonal changes in writing. {aiName} does not use emojis."


def whisper_file(userVoice, mic_input):
    return {
        "file": (userVoice, mic_input),
    }


def chat_history():
    try:
        with open(chatHistory, "r") as file:
            chat_hist = file.read()
    except FileNotFoundError:
        # If the file doesn't exist, create it
        with open(chatHistory, "w") as file:
            file.write("")
        chat_hist = ""  # Since the file was just created, we know it's empty
    return chat_hist

def llama_body(userVoice):
    return {
        "stream": True,
        "n_predict": 400,
        "temperature": 0.7,
        "stop": ["</s>", f"{aiName}:", f"{userName}:"],
        "repeat_last_n": 256,
        "repeat_penalty": 1.18,
        "top_k": 40,
        "top_p": 0.95,
        "min_p": 0.05,
        "tfs_z": 1,
        "typical_p": 1,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "mirostat": 0,
        "mirostat_tau": 5,
        "mirostat_eta": 0.1,
        "grammar": "",
        "n_probs": 0,
        "image_data": [],
        "cache_prompt": True,
        "api_key": "",
        "slot_id": -1,
        "prompt": f"{echo_behavioral_prompt}\n\n{chat_history()}\n\n{userName}: {userVoice.text} \n{aiName}:",
    }
