import os

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    df = pd.read_csv("../look_up_tables/df_Digital Assets & Crypto.csv", sep=";", decimal=',')
    df.rename(columns={"Unnamed: 0": "id"}, inplace=True)

    entities = pd.read_csv("../look_up_tables/entities.csv", sep=';', decimal=',')
    entities.rename(columns={"Unnamed: 0": "id", "0": "name"}, inplace=True)

    # FIXME: Fetch dynamically entity and annotation
    # TODO: Set dynamically entity_id and annotation_id
    entity_id = 174  # digital assets
    annotation_id = 1007360414114435072  # Bitcoin
    query_annotation = "context:{0}.{1}".format(entity_id, annotation_id)

    basic_url = "https://api.twitter.com/2/tweets"
    query_type = "counts"
    granularity = "day"  # day, hour or minute
    start = "2022-01-01T00:00:00Z"
    end = "2022-06-15T00:00:00Z"
    access_type = "all"  # "all" for academic access, "recent" for premium access
    query_text = "bitcoin"

    # TODO: Include next token
    next_token = ""
    url = "{0}/{1}/{2}?query={3}&granularity={4}&start_time={5}&end_time={6}".format(
        basic_url, query_type, access_type, query_text, granularity, start, end
    )

    # Source https://developer.twitter.com/en/docs/twitter-api/tweets/counts/quick-start/recent-tweet-counts
    token = os.getenv('bearer_token')
    academic = os.getenv('academic')
    headers = {"Authorization": "Bearer {0}".format(academic)}
    response = requests.get(url=url, headers=headers)
    data = response.json()

    total_tweet_count = data["meta"]["total_tweet_count"]
    df_tweets = pd.DataFrame(data=data["data"])
    df_tweets["start"] = pd.to_datetime(df_tweets.start).dt.strftime('%Y-%m-%d %H:%M')
    df_tweets["end"] = pd.to_datetime(df_tweets.end).dt.strftime('%Y-%m-%d %H:%M')
    df_tweets["dates"] = [pd.to_datetime(d) for d in df_tweets.start]

    # TODO: Set title dynamically
    # df_tweets.plot(kind="scatter", x='dates', y='tweet_count', c='tweet_count', colormap='coolwarm',
    #                title='Hourly count of Bitcoin Tweets')

    print("Run")
