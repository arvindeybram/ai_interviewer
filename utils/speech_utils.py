import whisper
import streamlit as st
import sounddevice as sd
from scipy.io.wavfile import write
import streamlit.components.v1 as components


@st.cache_resource
def load_whisper_model(model_name):
    return whisper.load_model(model_name)


model = load_whisper_model("tiny")  # Options: "tiny", "base", "small", "medium", "large"


def record_audio(filename="user_input.wav", duration=5, fs=44100):
    try:
        print("Recording...")
        audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()
        write(filename, fs, audio)
        print("Recording complete.")
        return filename
    except Exception as e:
        print(f"[ERROR] Failed to record audio: {e}")
        return None


def transcribe_audio(file_path="user_input.wav"):
    if file_path is None:
        return "No audio file to transcribe."
    try:
        print("Transcribing...")
        result = model.transcribe(file_path)
        return result["text"]
    except Exception as e:
        return f"[ERROR] Transcription failed: {e}"


def speak(text):
    escaped_text = text.replace('"', '\\"')  # Escape quotes
    components.html(f"""
        <script>
            const utterance = new SpeechSynthesisUtterance("{escaped_text}");
            utterance.rate = 0.6; // Made the voice a bit more slow
            speechSynthesis.speak(utterance);
        </script>
    """, height=0)
