import datetime
import os
import time
from dotenv import load_dotenv

import twint
import tweepy


def scrap_twitter_data_with_twint(term: str, since: datetime, until: datetime):

    config = twint.Config()
    config.Search = term
    config.Lang = "en"

    config.Since = str(since)
    config.Until = str(until)
    config.Output = "../data/{0}.csv".format(term)
    config.Limit = 100

    twint.run.Search(config)


# Prevents sending too many requests to Twitter's servers
def limit_handled(cursor):
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

    search_term = "staratlas"

    # Section with twint
    since_date = datetime.datetime(2022, 1, 1)
    until_date = datetime.datetime(2022, 4, 1)
    scrap_twitter_data_with_twint(search_term, since_date, until_date)
