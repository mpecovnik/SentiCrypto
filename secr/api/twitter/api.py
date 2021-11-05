from typing import Any, Dict, Optional

from secr.api.apicaller import ApiCaller
from secr.api.twitter.config import TwitterApiConfig
from secr.api.twitter.saver import TwitterParquetSaver
from tqdm import tqdm


class TwitterQuery:
    def __init__(
        self, hashtag: str, language: str, since_id: Optional[str] = None
    ) -> None:
        self.hashtag = hashtag
        self.language = language
        self.since_id = since_id

    def get_query_params(self, next_token: Optional[str] = None) -> Dict[str, str]:
        return {
            "query": f"#{self.hashtag} lang:{self.language} -is:retweet -is:reply -is:quote",
            "tweet.fields": "id,text,created_at,public_metrics",
            "next_token": next_token if next_token is not None else {},
            "since_id": self.since_id if self.since_id is not None else 0,
        }


class TwitterApi(ApiCaller):
    def __init__(self, config: TwitterApiConfig, saver: TwitterParquetSaver) -> None:
        super().__init__(config, saver)

    def call(
        self, url: str, query_params: Dict[str, Any], num_tweets: int = 10
    ) -> None:

        headers = {"Authorization": "Bearer {}".format(self.config.bearer_token)}

        max_results = 100 if 100 < num_tweets else num_tweets
        query_params["max_results"] = max_results

        for _ in tqdm(
            range(num_tweets // max_results), total=num_tweets // max_results
        ):

            json_response = super().call(url, query_params, headers)
            data = json_response["data"]
            self.saver.save_dataframe(data)

            try:
                query_params["next_token"] = json_response["meta"]["next_token"]
            except KeyError:
                # means no next-token is available, therefore all tweets are exhausted
                break
