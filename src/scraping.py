import datetime
import os
import time
from dotenv import load_dotenv

from transformers import pipeline
import pandas as pd
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
        except tweepy.TweepyException:
            time.sleep(15 * 60)


def scrap_twitter_data_with_tweepy(term: str, limit: int=1000):

    consumer_key = os.getenv('key')
    consumer_secret = os.getenv('secret')
    auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    query = '#{0}'.format(term)
    query = query + ' -filter:retweets'

    cursor = tweepy.Cursor(api.search_tweets, q=query,
                  tweet_mode='extended', lang='en', result_type="recent").items(limit)

    search = limit_handled(cursor)

    return search


if __name__ == "__main__":

    load_dotenv()
    logging.basicConfig(level=logging.INFO)

    search_term = "staratlas"
    search_results = scrap_twitter_data_with_tweepy(term=search_term, limit=10)

    sentiment_analysis = pipeline(model="finiteautomata/bertweet-base-sentiment-analysis")

    tweets = []
    for tweet in search_results:
        try:
            content = tweet.full_text
            sentiment = sentiment_analysis(content)
            tweets.append({'tweet': content, 'sentiment': sentiment[0]['label']})

        except:
            pass

    df = pd.DataFrame(tweets)