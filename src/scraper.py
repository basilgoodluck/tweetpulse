from playwright.async_api import async_playwright
import asyncio
from discord import send_to_discord
from storage import load_sent_tweets, save_sent_tweets

async def get_latest_tweets(usernames, webhook_url, sent_tweets_file):
    tweets = []
    sent_tweets = load_sent_tweets(sent_tweets_file)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        for username in usernames:
            try:
                url = f"https://twitter.com/{username}"
                await page.goto(url, wait_until="networkidle", timeout=30000)
                await page.wait_for_selector('article[data-testid="tweet"]', timeout=10000)

                tweet = await page.eval_on_selector('article[data-testid="tweet"]', '''(tweet) => {
                    const text = tweet.querySelector('div[data-testid="tweetText"]')?.innerText || 'No text';
                    const link = tweet.querySelector('time')?.parentElement?.href || '';
                    const id = link.split('/').pop();
                    const profileImg = document.querySelector('img[alt="Profile image"]')?.src || 'No image';
                    const name = document.querySelector('span[data-testid="UserName"]')?.innerText || '';
                    return { id, text, link, profileImg, name };
                }''')

                if tweet and tweet['id']:
                    tweet_body = {
                        "id": tweet['id'],
                        "username": username,
                        "name": tweet['name'] or username,
                        "tweet_text": tweet['text'],
                        "tweet_url": tweet['link'],
                        "profile_image": tweet['profileImg'],
                        "created_at": "Unknown",
                        "favorite_count": 0,
                        "retweet_count": 0
                    }
                    tweets.append(tweet_body)

                    if tweet['id'] not in sent_tweets:
                        await send_to_discord(tweet_body, webhook_url)
                        sent_tweets.add(tweet['id'])
                else:
                    tweets.append({"username": username, "error": "No tweet found"})

            except Exception as e:
                print(f"Error scraping {username}: {str(e)}")
                tweets.append({"username": username, "error": str(e)})

        await browser.close()

    save_sent_tweets(sent_tweets, sent_tweets_file)
    print("Collected tweets:", tweets)
    return tweets