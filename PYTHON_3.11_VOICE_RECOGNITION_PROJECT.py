# VOICE_ASSISTANT_3.11PYTHON_VERSION.py

import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import wikipedia
import time

WAKE_WORD = "hey assistant"

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 170)
engine.setProperty('volume', 1.0)

recognizer = sr.Recognizer()
microphone = sr.Microphone()

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def listen_once(timeout=6, phrase_time_limit=6):
    """
    Listen once safely.
    Returns recognized text or None.
    NEVER crashes on silence.
    """
    try:
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.3)
            audio = recognizer.listen(
                source,
                timeout=timeout,
                phrase_time_limit=phrase_time_limit
            )
        return recognizer.recognize_google(audio).lower()

    except sr.WaitTimeoutError:
        return None

    except sr.UnknownValueError:
        return None

    except sr.RequestError:
        speak("Speech recognition service error.")
        return None

def handle_command(command):
    print("Command:", command)

    if "hello" in command or "hi" in command:
        speak("Hello! How can I help you?")
        return

    if "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {now}")
        return

    if "date" in command or "day" in command:
        today = datetime.datetime.now().strftime("%A, %B %d, %Y")
        speak(f"Today is {today}")
        return

    if command.startswith(("who is", "what is", "tell me about")):
        topic = command
        for p in ("who is", "what is", "tell me about"):
            topic = topic.replace(p, "").strip()

        if not topic:
            speak("Please say the topic name.")
            return

        try:
            summary = wikipedia.summary(topic, sentences=2)
            speak(summary)
        except Exception:
            speak("I couldn't fetch that information.")
        return

    if "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
        return

    if "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
        return

    if "thank" in command:
        speak("You're welcome!")
        return

    if "stop assistant" in command:
        speak("Stopping assistant. Goodbye.")
        raise KeyboardInterrupt

    speak("Sorry, I did not understand the command.")

def main():
    speak("Assistant is running. Say hey assistant to wake me up.")

    try:
        while True:
            print("\nWaiting for wake word...")
            heard = listen_once(timeout=8, phrase_time_limit=4)

            if not heard:
                continue

            print("Heard:", heard)

            if WAKE_WORD in heard:
                speak("Yes?")
                time.sleep(0.4)

                print("Listening for command...")
                command = listen_once(timeout=7, phrase_time_limit=7)

                if command:
                    handle_command(command)
                else:
                    speak("I did not hear any command.")

                time.sleep(1)
                print("Back to wake word listening...")

    except KeyboardInterrupt:
        speak("Assistant stopped.")

if __name__ == "__main__":
    main()
