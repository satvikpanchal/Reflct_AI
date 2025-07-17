import warnings
warnings.filterwarnings("ignore")

import whisper

model = whisper.load_model("large")
result = model.transcribe("recording.wav", language="hi")
print(result["text"])

