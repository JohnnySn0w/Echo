import json
from io import StringIO
from config import talk_phrases

# Open the newly uploaded file to read the content
new_file_path = "./curlResponse.txt"
chat_history = "chatHistory.txt"


# Define a function to parse the new file, extract JSON content, and concatenate it


def parse_json_and_concatenate(filestream: StringIO) -> str:
    concatenated_content = []
    filestream.seek(0)

    for line in filestream:
        clean_line = line.strip().removeprefix("data:").strip()

        if "500 Internal Server Error" in clean_line:
            with open("./response.txt", "w") as error_stream:
                oops = "Small hiccup, restarting conversation."
                error_stream.write(oops)
            print(oops)
            # Assuming 'chat_history' is defined elsewhere and accessible
            open(chat_history, "w").close()
            raise RuntimeError("500 Internal Server Error encountered.")

        try:
            json_data = json.loads(clean_line)
            content = json_data.get("content", "").replace("**", "").replace('"', "`")
            if content and content not in talk_phrases:
                concatenated_content.append(content)
        except json.JSONDecodeError:
            continue

    return "".join(concatenated_content)


# Parse the file and concatenate the content
if __name__ == "__main__":
    concatenated_json_content = parse_json_and_concatenate(new_file_path)
    print(concatenated_json_content)
    with open("./response.txt", "w") as file:
        file.write(concatenated_json_content)
