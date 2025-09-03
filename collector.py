import snscrape.modules.twitter as sntwitter
import pandas as pd
from datetime import datetime
import os

def collect_tweets():
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)

    # Example query: English tweets about Bihar election since 2025-01-01
    query = "Bihar election lang:en since:2025-01-01"

    tweets = []
    try:
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
            if i >= 100:   # limit for each run to avoid overload
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
        return

    if tweets:
        df = pd.DataFrame(tweets, columns=["date", "id", "content", "username", "url"])

        # Save with timestamp so we don't overwrite old data
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M")
        filename = f"data/tweets_{timestamp}.csv"
        df.to_csv(filename, index=False, encoding="utf-8")
        print(f"✅ Saved {len(df)} tweets to {filename}")
    else:
        print("⚠️ No tweets found for this query.")

if __name__ == "__main__":
    collect_tweets()
