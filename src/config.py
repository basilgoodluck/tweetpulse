import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
TWITTER_NAMES = [name.strip() for name in os.getenv("TWITTER_NAMES", "").split(",")]
SENT_TWEETS_FILE = "sent_tweets.json"

if not DISCORD_WEBHOOK_URL:
    raise ValueError("Missing required environment variable: DISCORD_WEBHOOK_URL")