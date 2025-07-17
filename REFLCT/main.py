from record_audio import record_audio
from transcribe import transcribe_audio
from reflct import analyze_feelings

if __name__ == "__main__":
    timestamp = record_audio(duration=12)
    transcript = transcribe_audio(timestamp)
    print("\nTranscript:\n", transcript)

    reflection = analyze_feelings(timestamp, transcript)
    print("\nReflection:\n", reflection)

