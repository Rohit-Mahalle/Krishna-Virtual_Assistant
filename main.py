import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os


recogniser = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "a05635f9ca624d938951147b4ea75330"

def speak(text):
    engine.say(text)
    engine.runAndWait()

def speak2(text):                       #here is a 2nd speak funtion with paid voice gtts
    tts = gTTS(text)
    tts.save('temp.mp3')

    # Initialize Pygame mixer
    pygame.mixer.init()
    # Load the MP3 file
    pygame.mixer.music.load("temp.mp3")
    # Play the MP3 file
    pygame.mixer.music.play()
    # keep the program running till the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3")


def aiProcess(command):
    client = OpenAI(
    api_key="...paid api key here..." #paid openai api key required
    )

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
            {"role": "user", "content": command}
        ]
    )

    return (completion.choices[0].message)

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        # Check if the request was successful (status code 200)
        if r.status_code == 200:
            # Process the JSON response
            data = r.json()
            # Example: Print the titles of the articles
            for article in data['articles']:
                speak(article['title'])
    else:
        # let OpenAi handle the rest
        output = aiProcess(c)
        speak(output)
        


if __name__ == "__main__":
    speak("Initialising Krishna...")
    while True:
        # listen for the wake word Krishna
        # obtain audio from the microphone
        r = sr.Recognizer()
        

        
        # recognize speech using Sphinx
        try:
            with sr.Microphone() as source:
                print("Listening....")
                audio = r.listen(source,timeout=3,phrase_time_limit=2)
            word = r.recognize_google(audio)
            if (word.lower() == "krishna"):
                speak("Yes")
                # listen for the command
                with sr.Microphone() as source:
                    print("Krishna active....")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command )


            
        except Exception as e:
            print(" error; {0}".format(e))

    
    
