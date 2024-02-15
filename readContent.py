import json

# Open the newly uploaded file to read the content
new_file_path = './curlResponse.txt'
chat_history = 'chatHistory.txt'

talk_phrases = ["<|im_end|>","<|im_start|>"]

# Define a function to parse the new file, extract JSON content, and concatenate it
def parse_json_and_concatenate(file_path):
    # Initialize a variable to hold the concatenated content
    concatenated_content = ''
    
    # Open the file and read line by line
    with open(file_path, 'r') as file:
        for line in file:
            if line:
                # Each line is expected to be a JSON object, remove the "data:" prefix if present
                clean_line = line.strip()
                if clean_line.startswith('data:'):
                    clean_line = clean_line[5:].strip()
            
                if "500 Internal Server Error" in line:
                    with open('./response.txt', 'w') as file:
                        oops = "Small hiccup, restarting conversation."
                        file.write(oops)
                        print(oops)
                        open(chat_history, 'w').close()
                        exit(2)
                # Parse the JSON data
                try:
                    json_data = json.loads(clean_line)
                    # Assuming 'content' is the key for the text we want to concatenate
                    if 'content' in json_data:
                        if json_data['content'] not in talk_phrases:
                            concatenated_content += json_data['content'].replace('"', '`')
                except json.JSONDecodeError as e:
                    # Handle possible JSON decoding error
                    print(f"Error parsing JSON: {e}")
                    continue
    
    return concatenated_content

# Parse the file and concatenate the content
concatenated_json_content = parse_json_and_concatenate(new_file_path)
print(concatenated_json_content)
with open('./response.txt', 'w') as file:
    file.write(concatenated_json_content)