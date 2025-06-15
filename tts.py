import pyttsx3
from main import main, generate_response, validate_api_key
from google import genai
import sys
from contextlib import contextmanager
import json
from typing import Optional, List, Dict, Tuple
import os
import re

# Enhanced language configurations with more voice options
LANGUAGE_CONFIGS = {
    'en': {
        'name': 'English',
        'voice_keywords': [
            'zira', 'hazel', 'susan', 'david', 'mark', 'james', 
            'microsoft english', 'english', 'uk', 'british', 'american',
            'en-', 'en_'
        ],
        'rate': 180,
        'female_keywords': ['zira', 'hazel', 'susan', 'female', 'woman']
    },
    'bn': {
        'name': 'Bengali/Bangla',
        'voice_keywords': ['bangla', 'bengali', 'microsoft bangla', 'bn-', 'bn_'],
        'rate': 160,
        'female_keywords': ['female', 'bangla female', 'bengali female']
    },
    'zh': {
        'name': 'Chinese',
        'voice_keywords': [
            'chinese', 'huihui', 'microsoft chinese', 'zh-', 'zh_',
            'mandarin', 'cantonese', 'cmn-', 'yue-'
        ],
        'rate': 170,
        'female_keywords': ['huihui', 'chinese female', 'mandarin female']
    },
    'ko': {
        'name': 'Korean',
        'voice_keywords': ['korean', 'microsoft korean', 'ko-', 'ko_'],
        'rate': 170,
        'female_keywords': ['korean female']
    },
    'hi': {
        'name': 'Hindi',
        'voice_keywords': ['hindi', 'microsoft hindi', 'hi-', 'hi_', 'indian'],
        'rate': 160,
        'female_keywords': ['hindi female', 'indian female']
    },
    'fr': {
        'name': 'French',
        'voice_keywords': ['french', 'microsoft french', 'fr-', 'fr_', 'france'],
        'rate': 175,
        'female_keywords': ['french female']
    },
    'it': {
        'name': 'Italian',
        'voice_keywords': ['italian', 'microsoft italian', 'it-', 'it_', 'italy'],
        'rate': 175,
        'female_keywords': ['italian female']
    }
}

@contextmanager
def redirect_stdout(file_path: str):
    """Context manager for safely redirecting stdout to a file."""
    original_stdout = sys.stdout
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            sys.stdout = file
            yield
    finally:
        sys.stdout = original_stdout

def clean_text(text: str) -> str:
    """Remove asterisks and clean up the text."""
    # Remove asterisks
    text = text.replace('*', '')
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)
    # Remove multiple newlines
    text = re.sub(r'\n+', '\n', text)
    return text.strip()

def save_response(response: Optional[str], output_file: str = 'output.txt') -> None:
    """Save the generated response to a file."""
    if response is None:
        print("No response was generated.")
        return

    try:
        cleaned_response = clean_text(response)
        with redirect_stdout(output_file):
            print(cleaned_response)
        print(f"Content has been saved to {output_file}")
    except IOError as e:
        print(f"Error writing to file: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

def read_output_file(file_path='output.txt'):
    """Read content from the output file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return "No output file found."
    except Exception as e:
        return f"Error reading file: {str(e)}"

def get_all_available_voices() -> List[Dict]:
    """Get detailed information about all available voices."""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    voice_info_list = []
    
    for voice in voices:
        info = {
            'id': voice.id,
            'name': voice.name,
            'languages': getattr(voice, 'languages', []),
            'gender': 'Unknown',
            'language_codes': []
        }
        
        # Try to determine gender
        name_lower = voice.name.lower()
        if any(keyword in name_lower for lang in LANGUAGE_CONFIGS.values() for keyword in lang['female_keywords']):
            info['gender'] = 'Female'
        elif 'male' in name_lower or 'david' in name_lower or 'james' in name_lower:
            info['gender'] = 'Male'
            
        # Try to determine supported languages
        for lang_code, config in LANGUAGE_CONFIGS.items():
            if any(keyword in name_lower for keyword in config['voice_keywords']):
                info['language_codes'].append(lang_code)
        
        voice_info_list.append(info)
    
    return voice_info_list

def find_best_voice(voices: List[Dict], lang_code: str, prefer_female: bool = True) -> Tuple[Optional[str], str]:
    """Find the best voice for the given language code and gender preference."""
    lang_config = LANGUAGE_CONFIGS.get(lang_code)
    if not lang_config:
        return None, "Language not supported"
    
    # First try to find a voice matching both language and gender
    if prefer_female:
        for voice in voices:
            if lang_code in voice['language_codes'] and voice['gender'] == 'Female':
                return voice['id'], f"Female {lang_config['name']} voice"
    
    # Then try to find any voice for the language
    for voice in voices:
        if lang_code in voice['language_codes']:
            return voice['id'], f"{voice['gender']} {lang_config['name']} voice"
    
    return None, f"No voice found for {lang_config['name']}"

def text_to_speech(lang_code: str = 'en'):
    """Convert text from output file to speech using the specified language."""
    engine = pyttsx3.init()
    
    # Get all available voices with detailed information
    voices = get_all_available_voices()
    
    # Find the best voice for the language
    voice_id, status = find_best_voice(voices, lang_code)
    print(f"\n{status}")
    
    if voice_id:
        engine.setProperty('voice', voice_id)
        
        # Get language-specific settings
        lang_config = LANGUAGE_CONFIGS.get(lang_code, LANGUAGE_CONFIGS['en'])
        engine.setProperty('rate', lang_config['rate'])
        engine.setProperty('volume', 1.0)
        
        # Read and speak the content
        content = read_output_file()
        try:
            engine.say(content)
            engine.runAndWait()
        except Exception as e:
            print(f"Error during speech synthesis: {str(e)}")
    else:
        print("Using default voice as fallback")
        content = read_output_file()
        engine.say(content)
        engine.runAndWait()

def select_language() -> str:
    """Let user select the language for text-to-speech."""
    print("\nAvailable languages:")
    for code, config in LANGUAGE_CONFIGS.items():
        print(f"{code}: {config['name']}")
    lang_code = input("\nSelect language code (or press Enter for English): ").lower()
    while True:
        
        if not lang_code:
            return 'en'
        if lang_code in LANGUAGE_CONFIGS:
            return lang_code
        print("Invalid language code. Please try again.")

def process_single_prompt(client: genai.Client) -> bool:
    """Process a single prompt and return whether to continue."""
    try:
        contents = input("\nEnter your prompt (0 to exit): ")
        
        if contents == "0":
            print("Exiting...")
            return False
        
        # Select language for this response
        lang_code = select_language()
        
        response = generate_response(client, contents)
        if response:
            save_response(response)
            text_to_speech(lang_code)
        
        return True
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return True

def run_interactive_loop():
    """Run the main interactive loop."""
    api_key = "AIzaSyDh2nKVwIDshhwpNVyl57dFrg-fG5cmmsQ"
    
    if not validate_api_key(api_key):
        raise ValueError("Invalid API key")
    
    try:
        client = genai.Client(api_key=api_key)
        print("\nWelcome to the Multilingual AI Assistant!")
        print("Supported languages: English, Bengali, Chinese, Korean, Hindi, French, Italian")
        
        while True:
            if not process_single_prompt(client):
                break
                
    except Exception as e:
        print(f"Fatal error: {str(e)}")
    
    print("\nThank you for using the Multilingual AI Assistant!")

if __name__ == "__main__":
    run_interactive_loop()
