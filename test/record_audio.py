import sounddevice as sd
from scipy.io.wavfile import write

# Settings
filename = "recording.wav"
duration = 10  # seconds
sample_rate = 16000 

print(f"Recording for {duration} seconds")

# Record audio
recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
sd.wait() 

# Save
write(filename, sample_rate, recording)
print(f"Saved recording to '{filename}'")
