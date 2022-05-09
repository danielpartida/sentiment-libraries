import logging
import os
import time
from datetime import datetime
import re

import pandas as pd
import tweepy
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()


class TwitterScraper:

    def __init__(self, search_term: str, token: str = "", limit_tweets: int = 1000, tweet_type: str = "mixed"):
        """
        Constructor of TwitterScraping class
        :param search_term: queried term
        :type search_term: str
        :param limit_tweets: maximal amount of tweets to scrap
        :type limit_tweets: int
        :param tweet_type: "mixed", "recent", "popular"
        :type tweet_type:
        """
        self.search_term = search_term
        self.text_query = '({0} OR @{0} OR #{0} or ${1}) -is:retweet'.format(search_term, token)
        self.limit_tweets = limit_tweets
        self.tweet_type = self.assert_and_return_tweet_type(tweet_type=tweet_type)
        self.start_time = time.time()
        self.logger_tweepy = self.get_logger()
        self.api = self.get_tweepy_api()
        self.create_result_folders_if_not_exist()

    @staticmethod
    def assert_and_return_tweet_type(tweet_type: str) -> str:
        assert tweet_type in ["mixed", "recent", "popular"], "Supported result types are mixed, recent and popular"
        return tweet_type

    @staticmethod
    def get_tweepy_api() -> tweepy.API:
        """
        Authenticates to Twitter API and returns tweepy API
        :return: API
        :rtype: tweepy.API
        """
        consumer_key = os.getenv('consumer_key')
        consumer_secret = os.getenv('consumer_secret')
        access_token = os.getenv('access_token')
        access_token_secret = os.getenv('access_token_secret')

        # Twitter API
        auth = tweepy.OAuth1UserHandler(consumer_key=consumer_key, consumer_secret=consumer_secret,
                                        access_token=access_token, access_token_secret=access_token_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True)

        return api

    @staticmethod
    def clean_tweet(tweet: str):
        """
        Utility function to clean tweet text by removing links, special characters using simple regex statements.
        Example taken from https://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/?ref=lbp
        """
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w+:\ / \ / \S+)", " ", tweet).split())

    def get_logger(self):
        """
        Sets the logger using tweepy configuration
        :return: logger
        :rtype: logger
        """
        logger_tweepy = logging.getLogger("tweepy")
        logging.basicConfig(level=logging.INFO)
        handler = logging.FileHandler(filename="../logger/{0}.log".format(self.search_term))
        logger_tweepy.addHandler(handler)
        logger_tweepy.info("Search term {0}".format(self.text_query))

        return logger_tweepy

    def create_result_folders_if_not_exist(self) -> None:
        """
        Creates data and img result folders
        :return: None
        :rtype: None
        """
        paths = ["../data/results/{0}/discord".format(self.search_term),
                 "../data/results/{0}/twitter".format(self.search_term), "../img/{0}/discord".format(self.search_term),
                 "../img/{0}/twitter/bert".format(self.search_term),
                 "../img/{0}/twitter/roberta".format(self.search_term)]
        for path in paths:
            if not os.path.exists(path):
                os.makedirs(path)

    def get_scraped_tweets(self) -> pd.DataFrame:
        """
        Twitter’s standard search API only searches against a sampling of recent Tweets published in the past 7 days
        Tweepy library: https://docs.tweepy.org/en/v4.8.0/api.html#tweepy.API.search_tweets
        API V1: https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/api-reference/get-search-tweets
        API V2: https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference
        :return: dataframe of tweets
        :rtype: pd.DataFrame
        """
        today = datetime.today()
        until_str = today.strftime('%Y-%m-%d')
        list_dict_tweets = []
        try:
            list_twitter_items = [tweet for tweet in tweepy.Cursor(self.api.search_tweets, q=self.search_term,
                                                                   lang="en", result_type=self.tweet_type, count=100,
                                                                   until=until_str).items(self.limit_tweets)]

            for tweet in tqdm(list_twitter_items):
                # fetch main information of tweet
                dict_tweet = {
                    'id': tweet.id, "url": "https://twitter.com/twitter/statuses/{0}".format(tweet.id),
                              'created_at': tweet.created_at, 'username': tweet.user.screen_name,
                              'verified': tweet.user.verified, 'location': tweet.user.location,
                              'following': tweet.user.friends_count, 'followers': tweet.user.followers_count,
                              'total_tweets': tweet.user.statuses_count, 'favorite_count': tweet.favorite_count,
                              'retweet_count': tweet.retweet_count, 'hashtags': tweet.entities['hashtags'],
                              'tweet_type': tweet.metadata['result_type'], 'mentions': tweet.entities['user_mentions'],
                              'raw_text': tweet.text
                }
                dict_tweet['text'] = self.clean_tweet(dict_tweet['raw_text'])

                list_dict_tweets.append(dict_tweet)

        except BaseException as e:
            print('failed on_status,', str(e))
            time.sleep(3)

        if list_dict_tweets:
            df_tweets = pd.DataFrame(list_dict_tweets)

        else:
            df_tweets = pd.DataFrame()

        now = datetime.today().strftime("%d/%m/%Y, %H:%M:%S")
        list_now = now.split()
        day = list_now[0]
        hour = list_now[1]
        self.logger_tweepy.info("Tweets retrieved on {0} at {1}".format(day, hour))

        return df_tweets
