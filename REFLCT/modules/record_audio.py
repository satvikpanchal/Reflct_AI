import sounddevice as sd
from scipy.io.wavfile import write
import os
from datetime import datetime

def record_audio(duration=15, sample_rate=16000):
    print("Recording...")
    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()

    filename = f"logs/{timestamp}.wav"
    write(filename, sample_rate, audio)
    return timestamp
