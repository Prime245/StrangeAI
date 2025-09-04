import os
import time
import threading
import tweepy
from fastapi import FastAPI
from dotenv import load_dotenv

# Load .env file (local dev only — Render injects env vars automatically)
load_dotenv()

# ==========================
# Setup FastAPI app
# ==========================
app = FastAPI()

@app.get("/")
def home():
    return {"status": "✅ Twitter bot (API v2) is running"}

# ==========================
# Twitter Authentication (API v2)
# ==========================
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_KEY_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET, BEARER_TOKEN]):
    print("⚠️ Missing Twitter credentials in environment variables!")

client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_SECRET,
    wait_on_rate_limit=True
)

# Get your own user ID (needed for mentions)
me = client.get_me()
MY_USER_ID = me.data.id
print(f"✅ Authenticated as {me.data.username} (user_id={MY_USER_ID})")

# ==========================
# Bot Logic (API v2)
# ==========================
def run_bot():
    last_checked_id = None
    while True:
        try:
            print("🤖 Bot loop running...")

            mentions = client.get_users_mentions(
                id=MY_USER_ID,
                since_id=last_checked_id,
                max_results=5,
                tweet_fields=["author_id","created_at"]
            )

            if mentions.data:
                for mention in reversed(mentions.data):
                    print(f"💬 Mention from user_id={mention.author_id}: {mention.text}")
                    last_checked_id = mention.id

                    reply_text = f"Hello! Thanks for mentioning me 🤖"
                    client.create_tweet(
                        text=reply_text,
                        in_reply_to_tweet_id=mention.id
                    )
                    print(f"✅ Replied to mention ID {mention.id}")

            time.sleep(60)

        except Exception as e:
            print(f"⚠️ Error in bot loop: {e}")
            time.sleep(60)

# Run bot in background thread
threading.Thread(target=run_bot, daemon=True).start()
