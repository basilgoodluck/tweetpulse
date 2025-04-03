import asyncio
from config import DISCORD_WEBHOOK_URL, TWITTER_NAMES, SENT_TWEETS_FILE
from scraper import get_latest_tweets

async def main():
    print("TWITTER_NAMES from env:", TWITTER_NAMES)
    
    usernames = [name.strip() for name in TWITTER_NAMES if name.strip()]
    
    if not usernames:
        raise ValueError("No valid usernames provided in TWITTER_NAMES")
    
    result = await get_latest_tweets(usernames, DISCORD_WEBHOOK_URL, SENT_TWEETS_FILE)
    print("Final result:", result)
    return result

if __name__ == "__main__":
    asyncio.run(main())