import os
import pandas as pd
import datetime
import snscrape.modules.twitter as sntwitter

# Create data folder if not exists
os.makedirs("data", exist_ok=True)

def collect_tweets():
    query = "Bihar election OR biharvoting OR biharpolling since:2025-01-01 until:2025-09-01 lang:en"
    tweets = []

    # Limit to 100 tweets per run (can increase)
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
        if i >= 100:
            break
        tweets.append([
            tweet.date,
            tweet.id,
            tweet.content,
            tweet.user.username,
            tweet.lang,
            tweet.likeCount,
            tweet.retweetCount
        ])

    # Convert to DataFrame
    df = pd.DataFrame(tweets, columns=[
        "date", "id", "content", "username", "lang", "likes", "retweets"
    ])

    # Save to CSV
    today = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filepath = f"data/tweets_{today}.csv"
    df.to_csv(filepath, index=False, encoding="utf-8")

    print(f"✅ Saved {len(df)} tweets to {filepath}")
    return filepath

if __name__ == "__main__":
    collect_tweets()
