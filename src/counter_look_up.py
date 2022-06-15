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

    # FIXME: Create dynamic entity and annotation_id
    entity_id = 174
    annotation_id = 1007360414114435072
    granularity = "hour"  # day, hour or minute
    url = "https://api.twitter.com/2/tweets/counts/recent?query=context:{0}.{1}&granularity={2}".format(
        entity_id, annotation_id, granularity
    )

    # Source https://developer.twitter.com/en/docs/twitter-api/tweets/counts/quick-start/recent-tweet-counts
    token = os.getenv('bearer_token')
    headers = {"Authorization": "Bearer {0}".format(token)}
    response = requests.get(url=url, headers=headers)
    data = response.json()

    total_tweet_count = data["meta"]["total_tweet_count"]
    df_tweets = pd.DataFrame(data=data["data"])
    df_tweets.set_index(df_tweets.start, inplace=True)

    print("Run")
