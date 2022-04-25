import os
from dotenv import load_dotenv
import logging
from datetime import date, timedelta, datetime
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
    until_date = until_date.strftime('%Y-%m-%d')
    today = datetime.today().strftime("%d/%m/%Y, %H:%M:%S")
    try:
        list_twitter_items = [tweet for tweet in tweepy.Cursor(twitter_api.search_tweets, q=search_term, lang="en",
                                                               result_type="recent", count=limit,
                                                               until=until_date).items(limit)]

        list_dict_tweets = []
        for tweet in tqdm(list_twitter_items):
            # fetch metadata of tweet
            dict_tweet = {'id': tweet.id, 'created_at': tweet.created_at, 'username': tweet.user.screen_name,
                          'verified': tweet.user.verified, 'location': tweet.user.location,
                          'following': tweet.user.friends_count, 'followers': tweet.user.followers_count,
                          'total_tweets': tweet.user.statuses_count, 'favorite_count': tweet.favorite_count,
                          'retweet_count': tweet.retweet_count, 'hashtags': tweet.entities['hashtags'],
                          'mentions': tweet.entities['user_mentions']}

            # fetch content of tweet
            try:
                dict_tweet['text'] = tweet.retweeted_status.text
            except AttributeError:
                dict_tweet['text'] = tweet.text

            list_dict_tweets.append(dict_tweet)

    except BaseException as e:
        print('failed on_status,', str(e))
        time.sleep(3)

    if list_dict_tweets:
        df_tweets = pd.DataFrame(list_dict_tweets)

    else:
        df_tweets = pd.DataFrame()

    logger.info("Tweets retrieved at day {0} until day {1}".format(today, until_date))

    return df_tweets


if __name__ == "__main__":

    # TODO: Import text_query from argument
    text_query = 'staratlas'

    # logger
    logger = logging.getLogger("tweepy")
    logging.basicConfig(level=logging.DEBUG)
    handler = logging.FileHandler(filename="../logger/{0}.log".format(text_query))
    logger.addHandler(handler)

    # env variables
    load_dotenv()
    consumer_key = os.getenv('consumer_key')
    consumer_secret = os.getenv('consumer_secret')
    access_token = os.getenv('access_token')
    access_token_secret = os.getenv('access_token_secret')

    # Twitter API
    auth = tweepy.OAuth1UserHandler(consumer_key=consumer_key, consumer_secret=consumer_secret,
                                    access_token=access_token, access_token_secret=access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    # scraping
    yesterday = date.today() - timedelta(days=1)
    df_results = run_scraping(twitter_api=api, search_term=text_query, limit=100, until_date=yesterday)

    df_results.to_csv('../data/tweepy_{0}.csv'.format(text_query), sep=';')
