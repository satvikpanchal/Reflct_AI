import whisper

def transcribe_audio(timestamp, model_name="small", lang="en"):
    print("Transcribing...")
    model = whisper.load_model(model_name)
    audio_file = f"logs/{timestamp}.wav"
    result = model.transcribe(audio_file, language=lang)
    return result["text"].strip()
