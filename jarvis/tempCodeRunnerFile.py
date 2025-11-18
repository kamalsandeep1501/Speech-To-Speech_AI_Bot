import sounddevice as sd
import numpy as np
import speech_recognition as sr
import google.generativeai as genai
import pyttsx3

# --- Configure Gemini ---
genai.configure(api_key="AIzaSyD_GwV-kd_ff_uZMP-kD93QtOhAeZ2oYcA")
model = genai.GenerativeModel("gemini-1.5-flash")

# --- Initialize recognizer ---
recognizer = sr.Recognizer()

# --- Record audio using sounddevice ---
def record_audio(duration=5, fs=16000):
    print("🎤 Listening...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype="int16")
    sd.wait()
    return np.squeeze(audio)

# --- Convert audio to text using SpeechRecognition ---
def recognize_speech(audio, fs=16000):
    try:
        audio_data = sr.AudioData(audio.tobytes(), fs, 2)  # 2 bytes per sample
        text = recognizer.recognize_google(audio_data, language="en-US")
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("⚠ Could not understand audio.")
        return ""
    except sr.RequestError as e:
        print("⚠ Error with Google Speech Recognition:", e)
        return ""

# --- Speak text with pyttsx3 (re-initialize engine each time) ---
def speak(text):
    print("Bot:", text)
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()

# --- Main chatbot loop ---
def chat():
    while True:
        audio = record_audio(duration=5)  # record 5 sec
        query = recognize_speech(audio)
        if query.lower() in ["exit", "quit", "stop"]:
            speak("Goodbye!")
            break
        if query:
            response = model.generate_content(query)
            answer = response.text
            speak(answer)

if __name__ == "__main__":
    chat()
