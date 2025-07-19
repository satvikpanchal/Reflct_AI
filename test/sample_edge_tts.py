import asyncio
import edge_tts
import os

async def speak(text, voice="en-GB-RyanNeural"):
    communicate = edge_tts.Communicate(text, voice=voice)
    await communicate.save("output.mp3")
    os.system("afplay output.mp3")  

# Run the TTS
asyncio.run(speak("Hey Satvik, your reflection has been saved successfully."))
