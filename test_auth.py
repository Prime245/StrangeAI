# test_auth.py
import os
import tweepy
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Grab credentials
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_KEY_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

print("🔑 Checking environment variables...")
print(f"TWITTER_API_KEY: {'SET' if API_KEY else 'MISSING'}")
print(f"TWITTER_API_KEY_SECRET: {'SET' if API_SECRET else 'MISSING'}")
print(f"TWITTER_ACCESS_TOKEN: {'SET' if ACCESS_TOKEN else 'MISSING'}")
print(f"TWITTER_ACCESS_TOKEN_SECRET: {'SET' if ACCESS_SECRET else 'MISSING'}")

# If any missing, exit early
if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET]):
    print("❌ Missing one or more Twitter credentials in .env or environment variables.")
    exit(1)

# Try Twitter auth
try:
    auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)
    user = api.verify_credentials()
    if user:
        print(f"✅ Successfully authenticated as @{user.screen_name}")
    else:
        print("❌ Authentication failed. Invalid or expired tokens.")
except Exception as e:
    print("⚠️ Error during authentication:", e)
