import sounddevice as sd
from scipy.io.wavfile import write
import os
from datetime import datetime

def record_audio(duration=15, sample_rate=16000):
    print("Recording...")
    
    # Create a logs directory if it doesn't exist
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # Generate a timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Record audio
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()
    
    # Save the audio file
    audio_filename = f"logs/{timestamp}.wav"
    write(audio_filename, sample_rate, audio)
    print(f"Audio saved to {audio_filename}")
    
    # Create empty log files
    open(f"logs/{timestamp}_transcript.txt", 'w').close()
    open(f"logs/{timestamp}_reflection.txt", 'w').close()
    
    return timestamp
