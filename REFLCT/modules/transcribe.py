import whisper
import os

def transcribe_audio(file_path, model_name="small", lang="en"):
    print("Transcribing...")
    model = whisper.load_model(model_name)

    # Convert webm to wav if needed
    if file_path.endswith(".webm"):
        from pydub import AudioSegment
        audio = AudioSegment.from_file(file_path, format="webm")
        wav_path = file_path.replace(".webm", ".wav")
        audio.export(wav_path, format="wav")
        file_path = wav_path

    result = model.transcribe(file_path, language=lang)
    return result["text"].strip()
