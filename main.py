# main.py
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv
import os
import uuid

from tts import generate_audio  # 🔥 Import your TTS generator

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# FastAPI app setup
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/static/script.js")
async def serve_script():
    return FileResponse("static/script.js", media_type="text/javascript")

class Question(BaseModel):
    message: str

@app.post("/chat")
async def chat(q: Question):
    try:
        model = genai.GenerativeModel("models/gemini-2.5-flash")
        prompt = f"Reply concisely and clearly:\n\n{q.message}"
        response = model.generate_content(prompt)
        reply_text = getattr(response, "text", None)

        if not reply_text:
            raise ValueError("Gemini API did not return any text.")

        # 🔊 Generate unique filename for each TTS
        filename = f"{uuid.uuid4().hex}.mp3"
        filepath = os.path.join("static", "audio", filename)

        generate_audio(reply_text, filepath)

        return JSONResponse(content={
            "reply": reply_text,
            "audio_url": f"/static/audio/{filename}"
        })

    except Exception as e:
        print("Chat error:", e)
        raise HTTPException(status_code=500, detail="Something went wrong with Gemini.")
