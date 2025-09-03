import snscrape.modules.twitter as sntwitter
import pandas as pd
from datetime import datetime
import os

# Ensure data folder exists
os.makedirs("data", exist_ok=True)

def collect_tweets():
    query = "Bihar election lang:en since:2025-01-01"
    limit = 50  # number of tweets per run

    tweets = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
        if i >= limit:
            break
        tweets.append([
            tweet.date,
            tweet.id,
            tweet.user.username,
            tweet.content,
            tweet.url
        ])

    # Save hourly snapshot
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    hourly_file = f"data/tweets_{timestamp}.csv"

    df = pd.DataFrame(tweets, columns=["date", "id", "username", "content", "url"])
    df.to_csv(hourly_file, index=False, encoding="utf-8")
    print(f"✅ Saved {len(df)} tweets to {hourly_file}")

    # Merge into master file (deduplicated by tweet id)
    master_file = "data/all_tweets.csv"

    if os.path.exists(master_file):
        old_df = pd.read_csv(master_file)
        combined = pd.concat([old_df, df]).drop_duplicates(subset="id", keep="first")
    else:
        combined = df

    combined.to_csv(master_file, index=False, encoding="utf-8")
    print(f"🗂️ Master file updated: {len(combined)} unique tweets saved in {master_file}")


if __name__ == "__main__":
    collect_tweets()
