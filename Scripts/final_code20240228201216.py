import speech_recognition as sr
import pyttsx3
import datetime
import os
import webbrowser
import random

# Initialize speech recognition and text-to-speech engines
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Define the AI persona's name
ai_name = "DevBot"

# Define available commands and their corresponding actions
commands = {
    "hello": lambda: print(f"{ai_name}: Hello! How can I assist you today?"),
    "time": lambda: print(f"{ai_name}: The current time is {datetime.datetime.now().strftime('%H:%M')}"),
    "open website": lambda: open_website(),
    "play music": lambda: play_music()
}

def listen():
    with sr.Microphone() as source:
        print(f"{ai_name}: Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        text = recognizer.recognize_google(audio)
        print(f"You: {text}")
        process_command(text.lower())
    except sr.UnknownValueError:
        print(f"{ai_name}: Sorry, I couldn't understand what you said.")
    except sr.RequestError as e:
        print(f"{ai_name}: Sorry, there was an error processing your request. {str(e)}")

def process_command(text):
    for command, action in commands.items():
        if command in text:
            action()
            return
    
    print(f"{ai_name}: Sorry, I don't know how to do that.")

def open_website():
    websites = ["https://www.google.com", "https://www.dev.ease"]
    website = random.choice(websites)
    webbrowser.open(website)
    print(f"{ai_name}: Opening website {website}.")

def play_music():
    music_folder = "/path/to/music/folder"
    music_files = os.listdir(music_folder)
    if music_files:
        music_file = random.choice(music_files)
        os.startfile(os.path.join(music_folder, music_file))
        print(f"{ai_name}: Playing music {music_file}.")
    else:
        print(f"{ai_name}: Sorry, there are no music files available.")

# Start the virtual assistant
print(f"{ai_name}: Hello! How can I assist you today?")
while True:
    listen()