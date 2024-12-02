import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY=os.getenv("API_KEY")
NEWS_API_KEY=os.getenv("NEWS_API_KEY")

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
        engine.say(text)
        engine.runAndWait()

def fetch_news():
    try:
        print("Fetching top news...")
        response = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}")
        if response.status_code == 200:
            articles = response.json().get('articles', [])
            for article in articles:
                headline = article.get('title', 'No title available')
                print("Headline:", headline)
                speak(headline)
        else:
            print("Failed to fetch news.")
            speak("Sorry, I couldn't fetch the news right now.")
    except Exception as e:
        print(f"Error fetching news: {e}")
        speak("An error occurred while fetching news.")

def aiProcess(command):
    client = OpenAI(API_KEY)

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general task like Alexa and Google cloud"},
            {"role": "user", "content": command}
        ]
    )

    return completion.choices[0].message.content

def processc(c):
    c = c.lower()

    if "open google" in c:
        print("Opening Google...")
        webbrowser.open("https://google.com")
    elif "open facebook" in c:
        print("Opening Facebook...")
        webbrowser.open("https://facebook.com")
    elif "open instagram" in c:
        print("Opening Instagram...")
        webbrowser.open("https://instagram.com")
    elif "open youtube" in c:
        print("Opening YouTube...")
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c:
        print("Opening LinkedIn...")
        webbrowser.open("https://linkedin.com")

    elif c.lower().startswith("play"):
        song = ' '.join(c.lower().split()[1:])  #["play" , "song(ex-slay)"]
        link = musicLibrary.music[song]
        webbrowser.open(link)

    elif "news" in c:
            fetch_news()

    else:
        output = aiProcess(c)
        print(output)
        speak(output)       


if __name__ == "__main__":
    speak("Initializing Jarvis...")
    print("Jarvis is ready!")

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        while True:
            try:
                print("Listening...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                word = recognizer.recognize_google(audio)

                if word.lower() == "jarvis":
                    speak("Yes")
                    print("Jarvis Active...")

                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                    c = recognizer.recognize_google(audio)
                    print(f"command received: {c}")
                    processc(c)

            except sr.UnknownValueError:
                print("Sorry, I didn't catch that.")
            except Exception as e:
                print(f"Error: {e}")