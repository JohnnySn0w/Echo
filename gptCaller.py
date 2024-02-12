import sys
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoConfig, pipeline

model_id = sys.argv[1]
config = AutoConfig.from_pretrained(model_id)
# config.quantization_config["disable_exllama"] = False
config.quantization_config["exllama_config"] = {"version":2}


# Load LLM and Tokenizer

tokenizer = AutoTokenizer.from_pretrained(model_id, use_fast=True)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto",
    trust_remote_code=False,
    revision="main",
    config=config
)

# Create a pipeline
pipe = pipeline(model=model, tokenizer=tokenizer, task='text-generation')

# We use the tokenizer's chat template to format each message
# See https://huggingface.co/docs/transformers/main/en/chat_templating
messages = [
    {
        "role": "system",
        "content": "You are a friendly chatbot.",
    },
    {
        "role": "user", 
        "content": "Tell me a funny joke about Large Language Models." #sys.argv[1]
    },
]
prompt = pipe.tokenizer.apply_chat_template(
    messages, 
    tokenize=False, 
    add_generation_prompt=True
)

# We will use the same prompt as we did originally
outputs = pipe(
    prompt,
    max_new_tokens=256,
    do_sample=True,
    temperature=0.1,
    top_p=0.95
)
print(outputs[0]["generated_text"])