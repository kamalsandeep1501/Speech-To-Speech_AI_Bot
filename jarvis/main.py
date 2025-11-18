import sounddevice as sd
import numpy as np
import speech_recognition as sr
import google.generativeai as genai
import pyttsx3

# --- Configure Gemini ---
genai.configure(api_key="AIzaSyD_GwV-kd_ff_uZMP-kD93QtOhAeZ2oYcA")
model = genai.GenerativeModel("gemini-1.5-flash")

# --- Initialize recognizer & TTS engine once ---
recognizer = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty("voices")
for voice in voices:
    if "english" in voice.name.lower() and "uk" in voice.name.lower():
        engine.setProperty("voice", voice.id)
        break

# --- Record audio ---
def record_audio(duration=2, fs=16000):  # shorter listen
    print("🎤 Listening...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype="int16")
    sd.wait()
    return np.squeeze(audio)

# --- Speech to text ---
def recognize_speech(audio, fs=16000):
    try:
        audio_data = sr.AudioData(audio.tobytes(), fs, 2)
        text = recognizer.recognize_google(audio_data, language="en-US")
        return text
    except:
        return ""

# --- Speak text with already-initialized engine ---
def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

# --- Main chatbot loop ---
def chat():
    speak("Jarvis online. Avengers database fully synced. At your service, Sir.")
    while True:
        audio = record_audio(duration=2)
        query = recognize_speech(audio).lower()

        if not query:
            continue

        print("You said:", query)

        # Exit condition
        if query in ["exit", "quit", "shutdown", "stop"]:
            speak("Powering down, Sir. Avengers tower is secure. Goodbye.")
            break

        # --- Avengers personality prompt (shortened for speed) ---
        prompt = (
            "You are Jarvis, Tony Stark's AI. Knowledgeable about the Avengers, Stark tech, and Marvel. "
            "Always respond as a witty British butler and call the user 'Sir'.\n\n"
            f"Sir: {query}\nJarvis:"
        )

        response = model.generate_content(prompt)
        answer = response.text

        speak(answer)

if __name__ == "__main__":
    chat()
