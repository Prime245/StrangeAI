import os
import tweepy
import time

# Load Twitter credentials from environment
API_KEY = os.getenv("TWITTER_API_KEY")
API_KEY_SECRET = os.getenv("TWITTER_API_KEY_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

def check_env_vars():
    print("🔍 Checking Twitter environment variables...")
    if not API_KEY:
        print("❌ Missing: TWITTER_API_KEY")
    if not API_KEY_SECRET:
        print("❌ Missing: TWITTER_API_KEY_SECRET")
    if not ACCESS_TOKEN:
        print("❌ Missing: TWITTER_ACCESS_TOKEN")
    if not ACCESS_TOKEN_SECRET:
        print("❌ Missing: TWITTER_ACCESS_TOKEN_SECRET")
    if all([API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET]):
        print("✅ All Twitter API environment variables are set.")

def create_client():
    try:
        auth = tweepy.OAuth1UserHandler(API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)
        api.verify_credentials()
        print("✅ Twitter authentication successful!")
        return api
    except Exception as e:
        print(f"❌ Error during authentication: {e}")
        return None

def run_bot():
    check_env_vars()
    api = create_client()
    if not api:
        print("⚠️ Bot stopped: Authentication failed.")
        return
    
    print("🤖 Bot is running... Listening for mentions...")

    last_seen_id = None

    while True:
        try:
            mentions = api.mentions_timeline(since_id=last_seen_id, tweet_mode="extended")
            for mention in reversed(mentions):
                print(f"📨 New mention from @{mention.user.screen_name}: {mention.full_text}")
                last_seen_id = mention.id
                reply_text = f"Hello @{mention.user.screen_name}, thanks for mentioning me!"
                api.update_status(status=reply_text, in_reply_to_status_id=mention.id)
                print(f"✅ Replied to @{mention.user.screen_name}")
        except Exception as e:
            print(f"⚠️ Error in bot loop: {e}")
        
        time.sleep(30)  # check every 30 seconds

if __name__ == "__main__":
    run_bot()
