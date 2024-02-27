from api_calls.openai_api import api_calls
import re
import openai


def extract_filename(response_text):
    """Extract the filename from the AI response."""
    # Regular expression to match the structured filename
    match = re.search(r"Filename: (.+)$", response_text, re.MULTILINE)
    if match:
        return match.group(1).strip()  # Return the extracted filename
    else:
        return None

def save_response_to_file(content, file_name):
    """Save the given content to a file with the specified name, excluding the filename line."""
    content_to_save = re.sub(r"\nFilename: .+$", "", content, flags=re.MULTILINE)  # Remove the filename line from the content
    with open(file_name, 'w') as file:
        file.write(content_to_save)

def get_file_name(user_message, sys_message):
    # Request a structured response from OpenAI
    response = api_calls(user_message, sys_message)
    # Extract the full response text
    response_text = response
    
    # Extract the filename from the response
    filename = extract_filename(response_text)
    
    if filename:
        # Save the response content to a file with the extracted filename
        save_response_to_file(response_text, filename)
        print(f"Response saved to {filename}")
    else:
        print("Filename extraction failed.")


