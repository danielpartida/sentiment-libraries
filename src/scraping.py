import datetime
import os
import time
from dotenv import load_dotenv

import twint
import tweepy
from deprecation import deprecated
import logging

@deprecated("Avoid using twint")
def scrap_twitter_data_with_twint(term: str='NFTs', since: datetime=datetime.datetime(2022, 4, 23),
                                  until: datetime=datetime.datetime(2022, 4, 24)):

    config = twint.Config()
    config.Search = term
    # config.Lang = "en"

    config.Since = str(since)
    # FIXME: config.Until does not work
    # config.Until = str(until)
    # FIXME: Add header to csv export
    config.Output = "../data/{0}.csv".format(term)

    twint.run.Search(config)


def limit_handled(cursor):
    # Prevents sending too many requests to Twitter's servers
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            time.sleep(15 * 60)


def scrap_twitter_data_with_tweepy(term: str):

    consumer_key = os.getenv('key')
    consumer_secret = os.getenv('secret')
    auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    query = '#{0}'.format(term)
    query = query + ' -filter:retweets'

    count = 1000

    search = limit_handled(tweepy.Cursor(api.search_tweets, q=query,
                             tweet_mode='extended', lang='en', result_type="recent").items(count))


if __name__ == "__main__":

    load_dotenv()
    logging.basicConfig(level=logging.DEBUG)

    search_term = "staratlas"