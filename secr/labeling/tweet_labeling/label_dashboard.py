import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from secr.labeling.tweet_labeling.labeling_utils import (
    get_labeled_tweets,
    get_labeling_data,
)

app = dash.Dash(
    __name__, external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"]
)

SENTIMENT_SCORES = list(range(-1, 6))


app.layout = html.Div(
    children=[
        html.Div(id="tweet-div", style=dict(padding="2%")),
        dcc.RadioItems(
            options=[
                {"label": "Not relevant", "value": -1},
                {"label": "Negative", "value": 0},
                {"label": "Positive", "value": 1},
            ],
            value=0,
            labelStyle=dict(display="inline-block", margin="1%"),
            id="score",
        ),
        html.Button("Submit", id="submit-value", n_clicks=0),
    ],
    style=dict(
        position="absolute",
        height="100vh",
        width="100vw",
        display="flex",
        flexDirection="column",
    ),
)


@app.callback(
    Output("tweet-div", "children"),
    State("score", "value"),
    Input("submit-value", "n_clicks"),
)
def label_tweet(score, n_clicks):

    data_path = (
        "/home/mpecovnik/Private/sentiment-analysis/data/filtered_tweet_data.parquet"
    )
    labels_path = (
        "/home/mpecovnik/Private/sentiment-analysis/data/labeled_tweet_data.parquet"
    )

    labeling_data = get_labeling_data(data_path)
    labeled_data = get_labeled_tweets(labels_path)

    if not labeled_data.empty:
        labeling_data = labeling_data[
            ~labeling_data.tweet_id.isin(labeled_data.tweet_id)
        ]

    random_tweet = labeling_data.sample(n=1, random_state=42)

    values_dict = dict(tweet_id=random_tweet.tweet_id.iloc[0], sentiment_label=score)
    labeled_data = labeled_data.append(values_dict, ignore_index=True)

    labeled_data.to_parquet(labels_path)

    return random_tweet.text.iloc[0]


if __name__ == "__main__":
    app.run_server(debug=True)
