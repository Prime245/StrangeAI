# tts.py
from dotenv import load_dotenv
load_dotenv()

import requests
import os

ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
VOICE_ID = "XoRW0lnqsRh57iNm2EDU"

def generate_audio(text, output_path):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.35,
            "similarity_boost": 0.65
        }
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"✅ Voice saved to {output_path}")
        return True
    else:
        print("❌ ElevenLabs TTS failed:", response.status_code, response.text)
        return False
