import datetime
import time
import os
from dotenv import load_dotenv

import twint
import tweepy

config = twint.Config()


def scrap_twitter_data_with_twint(term: str, since: datetime, until: datetime):
    config.Search = term
    config.Lang = "en"

    config.Since = str(since)
    config.Until = str(until)
    config.Output = "../data/nfts.csv"
    config.Limit = 100

    twint.run.Search(config)


if __name__ == "__main__":

    # Tweepy setup
    load_dotenv()
    consumer_key = os.getenv('key')
    consumer_secret = os.getenv('secret')
    auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    query = '#NFTs'
    query = query + ' -filter:retweets'

    count = 1000

    # FIXME: Change limit_handled
    # search = limit_handled(tweepy.Cursor(api.search_tweets, q=query, tweet_mode='extended',
    #                                      lang='en', result_type="recent").items(count))

    # Section with twint
    # search_term = "NFTs"
    # since_date = datetime.datetime(2021, 4, 1)
    # until_date = datetime.datetime(2022, 4, 1)
    # scrap_twitter_data_with_twint(search_term, since_date, until_date)