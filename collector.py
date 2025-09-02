import os
import pandas as pd
import snscrape.modules.twitter as sntwitter
from datetime import datetime

def collect_tweets():
    # Simple query (no since/until at first)
    query = "Bihar election lang:en"
    tweets = []

    try:
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
            if i >= 100:  # limit to 100 tweets per run
                break
            tweets.append([
                tweet.date, 
                tweet.id, 
                tweet.content, 
                tweet.user.username, 
                tweet.url
            ])

    except Exception as e:
        print(f"⚠️ Error while scraping: {e}")
        return None

    if not tweets:
        print("⚠️ No tweets collected this run.")
        return None

    # Save to CSV in /data
    df = pd.DataFrame(tweets, columns=["date", "id", "content", "user", "url"])
    os.makedirs("data", exist_ok=True)
    filename = f"data/tweets_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(filename, index=False)

    print(f"✅ Saved {len(df)} tweets to {filename}")
    return filename

if __name__ == "__main__":
    collect_tweets()
