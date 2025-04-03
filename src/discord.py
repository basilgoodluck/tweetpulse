import aiohttp

async def send_to_discord(tweet, webhook_url):
    async with aiohttp.ClientSession() as session:
        payload = {
            "content": f"New tweet from @{tweet['username']} ({tweet['name']}):\n{tweet['tweet_text']}\n{tweet['tweet_url']}"
        }
        async with session.post(webhook_url, json=payload) as response:
            if response.status == 204:
                print(f"Sent tweet {tweet['id']} to Discord")
            else:
                print(f"Failed to send tweet {tweet['id']} to Discord: {await response.text()}")