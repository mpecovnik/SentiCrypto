from pathlib import Path

import pandas as pd

from secr.api.twitter.api import TwitterApi, TwitterQuery
from secr.api.twitter.config import TwitterApiConfig
from secr.api.twitter.saver import TwitterParquetSaver

coin = "SHIB"

coin_data_path = Path(f"/home/mpecovnik/Private/sentiment-analysis/data/twitter/{coin}")

try:
    coin_df = pd.concat(
        pd.read_parquet(parquet_file)
        for parquet_file in coin_data_path.glob("*.parquet")
    )
    # find the most recent tweet_id
    latest_tweet_id = coin_df.sort_values("tweet_id", ascending=False).tweet_id.iloc[0]

    twitter_query = TwitterQuery(coin, "en", latest_tweet_id)


except ValueError:
    print("No data for coin is available yet.")

    twitter_query = TwitterQuery(coin, "en")

config = TwitterApiConfig.from_yaml(
    "/home/mpecovnik/Private/sentiment-analysis/SentiCrypto/credentials.yaml"
)
saver = TwitterParquetSaver(
    f"/home/mpecovnik/Private/sentiment-analysis/data/twitter/{coin}"
)
twitter_api = TwitterApi(config, saver)

search_url = "https://api.twitter.com/2/tweets/search/recent"
query_params = twitter_query.get_query_params()


twitter_api.call(search_url, query_params, num_tweets=5000)
