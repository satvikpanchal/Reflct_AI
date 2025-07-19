from vosk import Model, KaldiRecognizer
import sounddevice as sd
import queue, sys, json

q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print("Status:", status, file=sys.stderr)
    q.put(bytes(indata))

model = Model("/Users/satvikpanchal/for_real_projects/Reflct_AI/models/vosk-model-small-en-us-0.15")
rec = KaldiRecognizer(model, 16000)

with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                       channels=1, callback=callback):
    print("Listening... (Ctrl+C to stop)")
    while True:
        data = q.get()
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            print("You said:", result.get("text", ""))
