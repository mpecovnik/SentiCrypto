import os
import time
from hashlib import blake2b
from typing import List

import pandas as pd
from secr.api.apicaller import ApiSaver


class TwitterParquetSaver(ApiSaver):
    def __init__(self, folder: str) -> None:
        super().__init__(folder)

    def save_dataframe(self, data: List) -> None:

        utf_time = str(time.time()).encode("utf-8")
        time_hash = blake2b(key=utf_time, digest_size=16).hexdigest()

        save_parquet = os.path.join(self.folder, time_hash)

        value_dicts = []
        for resp in data:
            try:
                hashtags = [
                    val_dict["tag"].upper() for val_dict in resp["entities"]["hashtags"]
                ]
            except KeyError:
                hashtags = []

            try:
                cashtags = [
                    val_dict["tag"].upper() for val_dict in resp["entities"]["cashtags"]
                ]
            except KeyError:
                cashtags = []

            try:
                mentions = [
                    val_dict["username"] for val_dict in resp["entities"]["mentions"]
                ]
            except KeyError:
                mentions = []

            try:
                urls = [
                    val_dict["expanded_url"] for val_dict in resp["entities"]["urls"]
                ]
            except KeyError:
                urls = []

            value_dicts.append(
                {
                    "tweet_id": int(resp["id"]),
                    "text": resp["text"],
                    "retweet_count": int(resp["public_metrics"]["retweet_count"]),
                    "reply_count": int(resp["public_metrics"]["reply_count"]),
                    "like_count": int(resp["public_metrics"]["like_count"]),
                    "hashtags": hashtags,
                    "hastag_count": len(hashtags),
                    "cashtags": cashtags,
                    "cashtags_count": len(cashtags),
                    "mentions": mentions,
                    "mentions_count": len(mentions),
                    "urls": urls,
                    "urls_count": len(urls),
                    "quote_count": int(resp["public_metrics"]["quote_count"]),
                    "created_at": resp["created_at"],
                    "source": resp["source"],
                }
            )

        data_df = pd.DataFrame(value_dicts)

        data_df.to_parquet(f"{save_parquet}.parquet")

        return None
