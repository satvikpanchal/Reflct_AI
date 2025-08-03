from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

from config import CHROMA_DB_PATH
from core.memory import MemoryManager
from core.pipeline import Pipeline
from modules.transcribe import transcribe_audio

# Initialize Jarvis components
memory = MemoryManager(CHROMA_DB_PATH)
pipeline = Pipeline(memory)

app = FastAPI()

# Serve frontend folder
frontend_path = os.path.join(os.path.dirname(__file__), "frontend")
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/")
async def serve_index():
    return FileResponse(os.path.join(frontend_path, "index.html"))

@app.post("/api/chat")
async def chat_api(request: Request):
    data = await request.json()
    user_message = data.get("message", "")
    if not user_message:
        return JSONResponse(content={"response": "I didn't get any message."})
    jarvis_response = pipeline.handle_request(user_message)
    return JSONResponse(content={"response": jarvis_response})

@app.post("/api/chat/audio")
async def chat_audio(audio: UploadFile = File(...)):
    audio_path = f"logs/voice_input.webm"
    os.makedirs("logs", exist_ok=True)
    with open(audio_path, "wb") as f:
        f.write(await audio.read())

    transcript = transcribe_audio(audio_path)
    jarvis_response = pipeline.handle_request(transcript)
    return JSONResponse(content={"response": jarvis_response})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
