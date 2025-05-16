import whisper
import sounddevice as sd
from scipy.io.wavfile import write
import pyttsx3

model = whisper.load_model("base")  # Options: "tiny", "base", "small", "medium", "large"


def record_audio(filename="user_input.wav", duration=5, fs=44100):
    try:
        print("Recording...")
        # Use mono channel for compatibility
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
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"[ERROR] Speech synthesis failed: {e}")
