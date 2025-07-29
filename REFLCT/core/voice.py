import vosk, sounddevice as sd, queue, json
from config import WAKE_WORD_MODEL_PATH

def listen_for_wake_word():
    q = queue.Queue()
    model = vosk.Model(WAKE_WORD_MODEL_PATH)
    rec = vosk.KaldiRecognizer(model, 16000)

    def callback(indata, frames, time, status): q.put(bytes(indata))
    print("Listening for wake word...")
    with sd.RawInputStream(samplerate=16000, channels=1, dtype='int16', callback=callback):
        while True:
            if rec.AcceptWaveform(q.get()):
                result = json.loads(rec.Result())
                if "hello" in result.get("text", ""):
                    return

def listen_for_response(timeout=10):
    q = queue.Queue()
    model = vosk.Model(WAKE_WORD_MODEL_PATH)
    rec = vosk.KaldiRecognizer(model, 16000)

    def callback(indata, frames, time, status): q.put(bytes(indata))
    with sd.RawInputStream(samplerate=16000, channels=1, dtype='int16', callback=callback):
        for _ in range(timeout * 5):  # 5 loops per second
            if rec.AcceptWaveform(q.get()):
                result = json.loads(rec.Result())
                return result.get("text", "").lower()
    return None
