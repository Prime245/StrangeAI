import os
import tweepy
import requests
from dotenv import load_dotenv

load_dotenv()

# Load Twitter credentials
API_KEY = os.getenv("TWITTER_API_KEY")
API_KEY_SECRET = os.getenv("TWITTER_API_KEY_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

# Authenticate with Twitter
auth = tweepy.OAuth1UserHandler(API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

print("✅ Twitter bot authenticated!")

# Function to reply to mentions
def reply_to_mentions():
    mentions = api.mentions_timeline(count=5)
    for mention in mentions:
        print(f"👀 Mention by {mention.user.screen_name}: {mention.text}")

        # Skip replying to yourself
        if mention.user.screen_name == "your_twitter_username":
            continue

        # Send text to your chatbot backend
        response = requests.post(
            "https://your-app.onrender.com/chat",
            json={"message": mention.text}
        )

        if response.status_code == 200:
            bot_reply = response.json().get("reply", "⚠️ No response")
            print(f"🤖 Bot reply: {bot_reply}")

            # Post reply to Twitter
            api.update_status(
                status=f"@{mention.user.screen_name} {bot_reply}",
                in_reply_to_status_id=mention.id
            )

if __name__ == "__main__":
    reply_to_mentions()
