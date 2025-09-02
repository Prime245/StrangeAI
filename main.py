import os
import time
import threading
import tweepy
from fastapi import FastAPI
from dotenv import load_dotenv

# Load .env file (useful for local dev, Render injects env automatically)
load_dotenv()

# ==========================
# Setup FastAPI app
# ==========================
app = FastAPI()

@app.get("/")
def home():
    return {"status": "✅ Twitter bot is running"}

# ==========================
# Twitter Authentication
# ==========================
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_KEY_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET]):
    print("⚠️ Missing Twitter credentials in environment variables!")

auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# ==========================
# Bot Logic
# ==========================
def run_bot():
    last_checked_id = None
    while True:
        try:
            print("🤖 Bot loop running...")

            mentions = api.mentions_timeline(
                since_id=last_checked_id, tweet_mode="extended"
            )
            for mention in reversed(mentions):
                print(f"💬 Mention from @{mention.user.screen_name}: {mention.full_text}")
                last_checked_id = mention.id

                # Example: auto-reply
                reply_text = f"Hello @{mention.user.screen_name}, thanks for mentioning me!"
                api.update_status(
                    status=reply_text,
                    in_reply_to_status_id=mention.id,
                    auto_populate_reply_metadata=True,
                )
                print(f"✅ Replied to @{mention.user.screen_name}")

            time.sleep(60)  # wait before checking again
        except Exception as e:
            print(f"⚠️ Error in bot loop: {e}")
            time.sleep(60)

# Run bot in a background thread
threading.Thread(target=run_bot, daemon=True).start()
