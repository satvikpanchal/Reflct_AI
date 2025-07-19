from record_audio import record_audio
from transcribe import transcribe_audio
from reflct import analyze_feelings
from speak import speak
import vosk
import sounddevice as sd
import queue
import json
from datetime import datetime

# Wake word detection (simplified)
def listen_for_wake_word(model_path="/Users/satvikpanchal/for_real_projects/Reflct_AI/models/vosk-model-small-en-us-0.15"):
    q = queue.Queue()

    def callback(indata, frames, time, status):
        q.put(bytes(indata))

    model = vosk.Model(model_path)
    rec = vosk.KaldiRecognizer(model, 16000)

    print("Listening for 'Hey Jarvis'...")
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                if "hey jarvis" in result.get("text", ""):
                    print("Wake word detected!")
                    return

# Confirmation step
def get_confirmation():
    q = queue.Queue()

    def callback(indata, frames, time, status):
        q.put(bytes(indata))

    model = vosk.Model("/Users/satvikpanchal/for_real_projects/Reflct_AI/models/vosk-model-small-en-us-0.15")
    rec = vosk.KaldiRecognizer(model, 16000)

    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "").lower()
                if "yes" in text:
                    return True
                elif "no" in text:
                    return False

if __name__ == "__main__":
    print("Jarvis is now running...")
    while True:
        listen_for_wake_word()
        speak("Hello sir, what can I do for you today?")
        
        timestamp = record_audio(duration=10)
        transcript = transcribe_audio(timestamp)
        
        speak(f"You said: '{transcript}'. Should I go ahead?")
        
        if get_confirmation():
            speak("Executing this task.")
            reflection = analyze_feelings(transcript, "Satvik", datetime.now().isoformat())
            print("\nReflection:\n", reflection)
            speak(reflection)
        else:
            print("User cancelled.")
            speak("Okay, I won't do that.")


