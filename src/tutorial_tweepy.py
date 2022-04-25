import os
from dotenv import load_dotenv
import logging
from datetime import date, timedelta
import tweepy
import pandas as pd
import time

from tqdm import tqdm


def run_scraping(twitter_api: tweepy.API, search_term: str, limit: int, until_date: date) -> pd.DataFrame:
    """
    Twitter’s standard search API only searches against a sampling of recent Tweets published in the past 7 days
    https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/overview
    https://developer.twitter.com/en/docs/twitter-api/tweets/search/introduction
    https://docs.tweepy.org/en/v4.8.0/api.html
    :param until_date: last date to scrap
    :type until_date: date
    :param twitter_api: Twitter API v1.1 Interface
    :type twitter_api: tweepy API
    :param search_term: word to search
    :type search_term: str
    :param limit: total amount of tweets to fetch from API
    :type limit: int
    :return: dataframe of tweets
    :rtype: pd.DataFrame
    """
    df_tweets = pd.DataFrame()
    until_date = until_date.strftime('%Y-%m-%d')
    try:
        list_tweets = [tweet for tweet in tweepy.Cursor(twitter_api.search_tweets, q=search_term, lang="en",
                                                        result_type="recent", count=limit).items(limit)]
        logger.info("Tweets retrieved")
        for tweet in tqdm(list_tweets):
            id = tweet.id
            created_at = tweet.created_at
            username = tweet.user.screen_name
            location = tweet.user.location
            following = tweet.user.friends_count
            followers = tweet.user.followers_count
            totaltweets = tweet.user.statuses_count
            retweetcount = tweet.retweet_count

    except BaseException as e:
        print('failed on_status,', str(e))
        time.sleep(3)

    return df_tweets


if __name__ == "__main__":
    logger = logging.getLogger("tweepy")
    logging.basicConfig(level=logging.DEBUG)
    handler = logging.FileHandler(filename="tweepy.log")
    logger.addHandler(handler)

    load_dotenv()
    consumer_key = os.getenv('consumer_key')
    consumer_secret = os.getenv('consumer_secret')
    access_token = os.getenv('access_token')
    access_token_secret = os.getenv('access_token_secret')

    auth = tweepy.OAuth1UserHandler(consumer_key=consumer_key, consumer_secret=consumer_secret,
                                    access_token=access_token, access_token_secret=access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    text_query = 'staratlas'
    yesterday = date.today() - timedelta(days=1)
    df_results = run_scraping(twitter_api=api, search_term=text_query, limit=25, until_date=yesterday)

    # df_results.to_csv('../data/tweepy_{0}.csv'.format(text_query), sep=';')
