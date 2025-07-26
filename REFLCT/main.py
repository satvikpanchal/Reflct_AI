from record_audio import record_audio
from transcribe import transcribe_audio
from reflct import analyze_feelings
from speak import speak
import vosk
import sounddevice as sd
import queue
import json
from datetime import datetime, timedelta
from vision import take_screenshot

WAKE_WORD_MODEL = "/Users/satvikpanchal/for_real_projects/Reflct_AI/models/vosk-model-small-en-us-0.15"

def listen_for_wake_word():
    q = queue.Queue()

    def callback(indata, frames, time, status):
        q.put(bytes(indata))

    model = vosk.Model(WAKE_WORD_MODEL)
    rec = vosk.KaldiRecognizer(model, 16000)

    print("Listening for 'Hello...")
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                if "hello" in result.get("text", "").lower():
                    print("Wake word detected!")
                    return


def listen_for_response(timeout=10):
    """Listen for any user response (multi-turn conversation)."""
    q = queue.Queue()

    def callback(indata, frames, time, status):
        q.put(bytes(indata))

    model = vosk.Model(WAKE_WORD_MODEL)
    rec = vosk.KaldiRecognizer(model, 16000)

    deadline = datetime.now() + timedelta(seconds=timeout)

    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        while datetime.now() < deadline:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "").lower()
                if text:
                    return text
        return None  # Timeout


if __name__ == "__main__":
    print("Jarvis is now running...")
    while True:   # Always listening
        listen_for_wake_word()
        speak("Hello sir, what can I do for you today?")

        # Switch into conversation mode
        in_conversation = True
        while in_conversation:
            timestamp = record_audio(duration=6)
            transcript = transcribe_audio(timestamp).lower()

            if any(word in transcript for word in ["stop", "exit", "goodbye"]):
                speak("Okay, going back to standby mode.")
                in_conversation = False
                break

            speak(f"You said: '{transcript}'. Should I go ahead?")

            confirm = listen_for_response(timeout=6)
            if confirm and "yes" in confirm:
                speak("Executing this task.")

                # Conditionally capture a screenshot
                if any(word in transcript for word in ["screen", "laptop", "window", "tab", "desktop"]):
                    screenshot = take_screenshot()
                else:
                    screenshot = None

                # Analyze feelings with optional vision input
                reflection = analyze_feelings(
                    transcript,
                    "Satvik",
                    datetime.now().isoformat(),
                    image=screenshot
                )

                print("\nReflection:\n", reflection)
                speak(reflection)
                speak("Anything else?")

            # Wait for response, if user says "no"/silence → exit conversation
            follow_up = listen_for_response(timeout=6)
            if not follow_up or "no" in follow_up:
                speak("Alright, going back to sleep.")
                in_conversation = False
