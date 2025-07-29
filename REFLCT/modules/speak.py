import asyncio
import edge_tts
import sounddevice as sd
import numpy as np
from pydub import AudioSegment
import io

VOICE = "en-GB-RyanNeural"

async def _amain(text: str) -> None:
    audio_stream = io.BytesIO()
    communicate = edge_tts.Communicate(text, VOICE)
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_stream.write(chunk["data"])

    audio_stream.seek(0)
    audio_segment = AudioSegment.from_file(audio_stream, format="mp3")
    audio_np = np.array(audio_segment.get_array_of_samples(), dtype=np.int16)
    sd.play(audio_np, samplerate=audio_segment.frame_rate)
    sd.wait()

def speak(text: str):
    print(f"Jarvis: {text}")
    try:
        asyncio.run(_amain(text))
    except Exception as e:
        print(f"Error in TTS: {e}")
