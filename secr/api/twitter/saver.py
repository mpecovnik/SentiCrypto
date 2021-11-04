import os
import time
from datetime import datetime
from hashlib import blake2b

import pandas as pd
from secr.api.apicaller import ApiSaver


class TwitterParquetSaver(ApiSaver):
    def __init__(self, folder: str) -> None:
        super().__init__(folder)

    def save_dataframe(self, data) -> None:

        utf_time = str(time.time()).encode("utf-8")
        time_hash = blake2b(key=utf_time, digest_size=16).hexdigest()

        save_parquet = os.path.join(self.folder, time_hash)

        value_dicts = []
        for resp in data:
            value_dicts.append(
                {
                    "tweet_id": int(resp["id"]),
                    "text": resp["text"],
                    "retweet_count": int(resp["public_metrics"]["retweet_count"]),
                    "reply_count": int(resp["public_metrics"]["reply_count"]),
                    "like_count": int(resp["public_metrics"]["like_count"]),
                    "quote_count": int(resp["public_metrics"]["quote_count"]),
                    "created_at": datetime.strptime(
                        resp["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ"
                    ),
                }
            )

        data_df = pd.DataFrame(value_dicts)

        data_df.to_parquet(f"{save_parquet}.parquet")

        return None
