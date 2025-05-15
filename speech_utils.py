import whisper
import sounddevice as sd
from scipy.io.wavfile import write
import pyttsx3

model = whisper.load_model("base")  # You can use "small", "medium", etc.

def record_audio(filename="user_input.wav", duration=5, fs=44100):
    print("Recording...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    sd.wait()
    write(filename, fs, audio)
    return filename

def transcribe_audio(file_path="user_input.wav"):
    result = model.transcribe(file_path)
    return result["text"]

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
