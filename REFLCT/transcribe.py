import whisper

def transcribe_audio(timestamp, model_name="small", lang="en"):
    print("Transcribing...")
    model = whisper.load_model(model_name)
    
    audio_filename = f"logs/{timestamp}.wav"
    result = model.transcribe(audio_filename, language=lang)
    
    transcript = result["text"].strip()
    
    # Save to log
    transcript_filename = f"logs/{timestamp}_transcript.txt"
    with open(transcript_filename, "w") as f:
        f.write(transcript)
        
    return transcript
