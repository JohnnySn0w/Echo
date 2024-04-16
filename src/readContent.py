
import json
from io import StringIO
from config import talk_phrases

# Define file paths
new_file_path = "./curlResponse.txt"
chat_history = "chatHistory.txt"

# Function to clean a line of text
def clean_line(line: str) -> str:
    """
    Clean a line of text by removing leading/trailing whitespace and the "data:" prefix.

    Args:
        line (str): The line of text to clean.

    Returns:
        str: The cleaned line of text.
    """
    return line.strip().removeprefix("data:").strip()

# Function to handle an error message
def handle_error(error_message: str) -> None:
    """
    Handle an error message by writing it to a file and printing it.

    Args:
        error_message (str): The error message to handle.
    """
    with open("./response.txt", "w") as error_stream:
        error_stream.write(error_message)
    print(error_message)

# Function to extract relevant content from JSON data
def extract_content(json_data: dict) -> str:
    """
    Extract relevant content from JSON data.

    Args:
        json_data (dict): The JSON data to extract content from.

    Returns:
        str: The extracted content.
    """
    content = json_data.get("content", "").replace("**", "").replace('"', "`")
    return content if content and content not in talk_phrases else ""

# Function to parse JSON content from a file and concatenate it
def parse_json_and_concatenate(filestream: StringIO) -> str:
    """
    Parse JSON content from a file, extract relevant data, and concatenate it.

    Args:
        filestream (StringIO): A file stream object containing JSON data.

    Returns:
        str: Concatenated content extracted from the JSON data.
    """
    concatenated_content = []
    filestream.seek(0)  # Move to the beginning of the file

    for line in filestream:
        clean_line = clean_line(line)

        # Check if the line contains an error message
        if "500 Internal Server Error" in clean_line:
            handle_error("Small hiccup, restarting conversation.")
            # Clear the chat history
            open(chat_history, "w").close()
            raise RuntimeError("500 Internal Server Error encountered.")

        try:
            # Load JSON data from the line
            json_data = json.loads(clean_line)
            # Extract relevant content from the JSON data
            content = extract_content(json_data)
            # Add the content to the concatenated content list
            concatenated_content.append(content)
        except json.JSONDecodeError:
            # If JSON decoding fails, skip this line
            continue

    return "".join(concatenated_content)  # Concatenate the content and return it

# Parse the file and concatenate the content
if __name__ == "__main__":
    concatenated_json_content = parse_json_and_concatenate(new_file_path)
    print(concatenated_json_content)
    with open("./response.txt", "w") as file:
        file.write(concatenated_json_content)
