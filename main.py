# main.py
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load .env variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

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

        return JSONResponse(content={
            "reply": reply_text
        })

    except Exception as e:
        print("❌ Chat error:", e)
        raise HTTPException(status_code=500, detail="Something went wrong with Gemini.")
