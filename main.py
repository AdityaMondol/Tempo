from google import genai
import os
from typing import Optional

# Constants
MODEL_PROMPT = "You are the best university teacher of all time.You have nobel price in everything and all of your students also have nobel price in every catagory. You can make a person understand anything entirely. You are the master of all thing and the most expert."
MODEL_NAME = "gemini-2.0-flash"
Model_lang = input("Enter the model language: ")
model = "Your language should be " + Model_lang

def validate_api_key(api_key: str) -> bool:
    return bool(api_key and len(api_key) > 0)

def generate_response(client: genai.Client, prompt: str) -> Optional[str]:
    try:
        response = client.models.generate_content(
            model=MODEL_NAME, 
            contents=MODEL_PROMPT + prompt + model,
        )
        return response.text if response else None
    except Exception as e:
        print(f"Error generating content: {str(e)}")
        return None

def main():
    """This function is kept for backwards compatibility."""
    api_key = "AIzaSyDh2nKVwIDshhwpNVyl57dFrg-fG5cmmsQ"
    
    if not validate_api_key(api_key):
        raise ValueError("Invalid API key")
    
    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
        print(f"Failed to initialize client: {str(e)}")
        return None

    try:
        contents = input("Enter your prompt: ")
        return generate_response(client, contents)
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return None

if __name__ == "__main__":
    main()