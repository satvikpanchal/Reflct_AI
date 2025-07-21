
import asyncio
import edge_tts
import sounddevice as sd
import numpy as np
from pydub import AudioSegment
import io

VOICE = "en-GB-RyanNeural"

async def amain(text: str) -> None:
    """Streams audio from edge-tts, decodes it, and plays it."""
    audio_stream = io.BytesIO()
    communicate = edge_tts.Communicate(text, VOICE)
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_stream.write(chunk["data"])

    audio_stream.seek(0)
    
    # Decode the MP3 stream using pydub
    audio_segment = AudioSegment.from_file(audio_stream, format="mp3")
    
    # Convert to a NumPy array for sounddevice
    audio_np = np.array(audio_segment.get_array_of_samples(), dtype=np.int16)

    # Play the audio
    sd.play(audio_np, samplerate=audio_segment.frame_rate)
    sd.wait()

def speak(text: str):
    """Synchronous wrapper for the async TTS function."""
    print(f"Jarvis: {text}")
    try:
        asyncio.run(amain(text))
    except Exception as e:
        print(f"Error during text-to-speech: {e}")
