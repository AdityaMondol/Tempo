import pyttsx3
import platform
import os
import json
from typing import Dict, List

def get_detailed_voice_info() -> List[Dict]:
    """Get detailed information about all available voices."""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    voice_info_list = []
    
    print("\n=== Available Voice Details ===\n")
    
    for idx, voice in enumerate(voices, 0):
        info = {
            'index': idx,
            'id': voice.id,
            'name': voice.name,
            'languages': voice.languages,
            'age': getattr(voice, 'age', 'Unknown'),
            'gender': getattr(voice, 'gender', 'Unknown'),
            'system': platform.system()
        }
        
        print(f"Voice {idx}:")
        print(f"  Name: {info['name']}")
        print(f"  ID: {info['id']}")
        print(f"  Languages: {info['languages']}")
        print(f"  Age: {info['age']}")
        print(f"  Gender: {info['gender']}")
        print("")
        
        voice_info_list.append(info)
    
    # Save the voice information to a file
    with open('available_voices.json', 'w', encoding='utf-8') as f:
        json.dump(voice_info_list, f, indent=2)
    
    print(f"\nTotal voices found: {len(voice_info_list)}")
    print("Voice information has been saved to 'available_voices.json'")
    
    return voice_info_list

def test_voice(voice_id: str, text: str = "This is a test of the text to speech system.") -> None:
    """Test a specific voice by speaking a sample text."""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    # Find and set the requested voice
    for voice in voices:
        if voice.id == voice_id:
            engine.setProperty('voice', voice.id)
            print(f"\nTesting voice: {voice.name}")
            engine.say(text)
            engine.runAndWait()
            return
    
    print(f"Voice ID {voice_id} not found.")

def get_voice_install_instructions() -> None:
    """Print instructions for installing additional voices."""
    system = platform.system()
    
    print("\n=== Installing Additional Voices ===\n")
    
    if system == "Windows":
        print("To install additional voices on Windows:")
        print("1. Open Windows Settings")
        print("2. Go to Time & Language > Language & Region")
        print("3. Click 'Add a language'")
        print("4. Select desired languages and make sure to check 'Text-to-Speech' during installation")
        print("5. Wait for the download and installation to complete")
        print("\nAlternatively, you can:")
        print("1. Control Panel > Speech Recognition > Text to Speech")
        print("2. Install additional TTS engines like:")
        print("   - IVONA voices")
        print("   - Microsoft Speech Platform")
        print("   - CereProc voices")
    
    elif system == "Darwin":  # macOS
        print("To install additional voices on macOS:")
        print("1. Apple menu > System Settings")
        print("2. Click 'Accessibility'")
        print("3. Click 'Spoken Content'")
        print("4. Click 'System Voice'")
        print("5. Select 'Customize'")
        print("6. Choose additional voices to download")
    
    elif system == "Linux":
        print("To install additional voices on Linux:")
        print("1. Install festival and festvox:")
        print("   sudo apt-get install festival festvox-*")
        print("\n2. Install espeak voices:")
        print("   sudo apt-get install espeak espeak-data")
        print("\n3. Install mbrola voices:")
        print("   sudo apt-get install mbrola mbrola-*")
        print("\n4. Consider installing other TTS engines:")
        print("   - Google TTS (gtts)")
        print("   - RHVoice")
        print("   - SVOX Pico")

if __name__ == "__main__":
    print("Voice Discovery Tool")
    print("===================")
    
    # Get and display all available voices
    voices = get_detailed_voice_info()
    
    # Show installation instructions
    get_voice_install_instructions()
    
    # Option to test voices
    print("\nWould you like to test any of the voices?")
    response = input("Enter voice number to test, or press Enter to skip: ")
    
    if response.isdigit() and 0 < int(response) <= len(voices):
        voice = voices[int(response) - 1]
        test_text = input("Enter test text (or press Enter for default message): ")
        test_voice(voice['id'], test_text if test_text else None)