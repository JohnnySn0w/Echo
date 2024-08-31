import json
from io import StringIO
from config import talk_phrases

# Define file paths
new_file_path = "./curlResponse.txt"
chat_history = "chatHistory.txt"

def extract_json_data(filestream: StringIO) -> list:
    """
    Extract JSON data from a file stream.
    Args:
        filestream (StringIO): A file stream object containing JSON data.
    Returns:
        list: List of JSON data extracted from the file stream.
    """

    json_data_list = []
    filestream.seek(0)  # Move to the beginning of the file

    for line in filestream:
        clean_line = line.strip().removeprefix("data:").strip()  # Clean the line

        try:
            # Load JSON data from the line
            json_data = json.loads(clean_line)
            json_data_list.append(json_data)
        except json.JSONDecodeError:
            # If JSON decoding fails, skip this line
            continue

    return json_data_list

def process_json_data(json_data_list: list) -> str:
    """
    Process JSON data and extract relevant content.
    Args:
        json_data_list (list): List of JSON data.
    Returns:
        str: Concatenated content extracted from the JSON data.
    """

    concatenated_content = []

    for json_data in json_data_list:
        # Extract relevant content from the JSON data
        content = json_data.get("content", "").replace("**", "").replace('"', "`")
        # Check if the content is not empty and not in the talk phrases
        if content and content not in talk_phrases:
            concatenated_content.append(content)

    return "".join(concatenated_content)

def handle_error(clean_line: str) -> None:
    """
    Handle error cases.
    Args:
        clean_line (str): Cleaned line of text.
    """

    with open("./response.txt", "w") as error_stream:
        error_message = "Small hiccup, restarting conversation."
        error_stream.write(error_message)
    print(error_message)
    # Clear the chat history
    open(chat_history, "w").close()
    raise RuntimeError("500 Internal Server Error encountered.")

def parse_json_and_concatenate(filestream: StringIO) -> str:
    """
    Parse JSON content from a file, extract relevant data, and concatenate it.
    Args:
        filestream (StringIO): A file stream object containing JSON data.
    Returns:
        str: Concatenated content extracted from the JSON data.
    """

    json_data_list = extract_json_data(filestream)

    for json_data in json_data_list:
        clean_line = json.dumps(json_data)  # Convert JSON data to string

        # Check if the line contains an error message
        if "500 Internal Server Error" in clean_line:
            handle_error(clean_line)

    return process_json_data(json_data_list)


# Parse the file and concatenate the content
if __name__ == "__main__":
    concatenated_json_content = parse_json_and_concatenate(new_file_path)
    print(concatenated_json_content)
    with open("./response.txt", "w") as file:
        file.write(concatenated_json_content)
