from typing import Any, Dict, Optional

from secr.api.apicaller import ApiCaller
from secr.api.twitter.config import TwitterApiConfig
from secr.api.twitter.saver import TwitterParquetSaver
from tqdm import tqdm


class TwitterQuery:
    def __init__(self, hashtag: str, language: str) -> None:
        self.hashtag = hashtag
        self.language = language

    def get_query_params(self, next_token: Optional[str] = None) -> Dict[str, str]:
        return {
            "query": f"#{self.hashtag} lang:{self.language} -is:retweet",
            "tweet.fields": "id,text,created_at,public_metrics",
            "next_token": next_token if next_token is not None else {},
        }


class TwitterApi(ApiCaller):
    def __init__(self, config: TwitterApiConfig, saver: TwitterParquetSaver) -> None:
        super().__init__(config, saver)

    def call(
        self, url: str, query_params: Dict[str, Any], num_tweets: int = 10
    ) -> None:

        headers = {"Authorization": "Bearer {}".format(self.config.bearer_token)}

        max_results = 100
        query_params["max_results"] = max_results

        for _ in tqdm(
            range(num_tweets // max_results), total=num_tweets // max_results
        ):

            json_response = super().call(url, query_params, headers)
            query_params["next_token"] = json_response["meta"]["next_token"]

            data = json_response["data"]

            self.saver.save_dataframe(data)


coin = "SHIB"

config = TwitterApiConfig.from_yaml(
    "/home/mpecovnik/Private/sentiment-analysis/SentiCrypto/credentials.yaml"
)

saver = TwitterParquetSaver(
    f"/home/mpecovnik/Private/sentiment-analysis/data/twitter/{coin}"
)

twitter_api = TwitterApi(config, saver)

search_url = "https://api.twitter.com/2/tweets/search/recent"  # Change to the endpoint you want to collect data from

# change params based on the endpoint you are using
twitter_query = TwitterQuery(coin, "en")
query_params = twitter_query.get_query_params()


twitter_api.call(search_url, query_params, num_tweets=10000)
