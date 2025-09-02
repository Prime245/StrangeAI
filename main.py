import os
import threading
import time
import tweepy
import google.generativeai as genai
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# ---------------------------
# FastAPI setup
# ---------------------------
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_index():
    return FileResponse("index.html")


# ---------------------------
# Gemini Setup
# ---------------------------
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")


# ---------------------------
# Twitter Bot Setup
# ---------------------------
TW_CONSUMER_KEY = os.getenv("TWITTER_API_KEY")
TW_CONSUMER_SECRET = os.getenv("TWITTER_API_SECRET")
TW_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TW_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")
TW_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

auth = tweepy.OAuth1UserHandler(
    TW_CONSUMER_KEY, TW_CONSUMER_SECRET,
    TW_ACCESS_TOKEN, TW_ACCESS_SECRET
)
api = tweepy.API(auth)


def reply_to_mentions():
    """Background loop that replies to mentions"""
    since_id = None
    while True:
        try:
            mentions = api.mentions_timeline(since_id=since_id, tweet_mode="extended")
            for mention in reversed(mentions):
                print(f"New mention from @{mention.user.screen_name}: {mention.full_text}")
                since_id = mention.id

                # Generate reply using Gemini
                response = model.generate_content(f"Reply politely to: {mention.full_text}")
                reply_text = response.text.strip()

                api.update_status(
                    status=f"@{mention.user.screen_name} {reply_text}",
                    in_reply_to_status_id=mention.id
                )
                print(f"Replied to @{mention.user.screen_name}")

        except Exception as e:
            print("Error in bot loop:", e)

        time.sleep(30)  # wait before checking again


# ---------------------------
# Start background thread with FastAPI
# ---------------------------
def start_bot_thread():
    bot_thread = threading.Thread(target=reply_to_mentions, daemon=True)
    bot_thread.start()

@app.on_event("startup")
def startup_event():
    print("🚀 Starting Twitter bot in background...")
    start_bot_thread()
