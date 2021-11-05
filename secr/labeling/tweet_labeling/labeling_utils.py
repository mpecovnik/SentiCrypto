import os

import pandas as pd


def get_labeling_data(path):
    return pd.read_parquet(path)


def get_labeled_tweets(path):

    if os.path.exists(path):
        return pd.read_parquet(path)
    return pd.DataFrame()


def append_labeled_tweet_to_csv():
    pass
