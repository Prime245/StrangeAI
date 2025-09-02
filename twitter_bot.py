import os
import tweepy
import time
from dotenv import load_dotenv

load_dotenv()

# Load Twitter credentials from environment variables
API_KEY = os.getenv("TWITTER_API_KEY")
API_KEY_SECRET = os.getenv("TWITTER_API_KEY_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

# Authenticate with Twitter
auth = tweepy.OAuth1UserHandler(API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# ============= Auto Reply to Mentions =============
def reply_to_mentions():
    last_seen_id_file = "last_seen_id.txt"

    # Load last seen ID
    if os.path.exists(last_seen_id_file):
        with open(last_seen_id_file, "r") as f:
            last_seen_id = int(f.read().strip())
    else:
        last_seen_id = None

    mentions = api.mentions_timeline(since_id=last_seen_id, tweet_mode="extended")

    for mention in reversed(mentions):
        print(f"Replying to {mention.user.screen_name}: {mention.full_text}")

        reply_text = f"Hi @{mention.user.screen_name}, thanks for tagging me! 🚀"
        api.update_status(status=reply_text, in_reply_to_status_id=mention.id)

        # Save last seen ID
        with open(last_seen_id_file, "w") as f:
            f.write(str(mention.id))

# ============= Scheduled Tweets =============
def scheduled_tweets():
    tweet_text = "This is an automated tweet from my Render-hosted AI bot! 🤖✨"
    api.update_status(tweet_text)
    print("✅ Scheduled tweet sent!")

# ============= Main Loop =============
def run_bot():
    while True:
        try:
            reply_to_mentions()
            scheduled_tweets()
        except Exception as e:
            print("⚠️ Error:", e)

        time.sleep(60)  # Run every 1 minute

if __name__ == "__main__":
    run_bot()
