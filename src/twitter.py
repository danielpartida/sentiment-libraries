import logging
import os
import time
from datetime import datetime
import re

import pandas as pd
import tweepy
from dotenv import load_dotenv
from matplotlib import pyplot as plt
from tqdm import tqdm
from transformers import pipeline
from wordcloud import WordCloud, STOPWORDS

load_dotenv()


class Twitter:

    def __init__(self, search_term: str):
        self.search_term = search_term
        self.today = datetime.today()
        self.logger = self.get_logger()

    def get_logger(self):
        """
        Sets the logger using tweepy configuration
        :return: logger
        :rtype: logger
        """
        logger = logging.getLogger("tweepy")
        logging.basicConfig(level=logging.INFO)
        handler = logging.FileHandler(filename="../logger/{0}.log".format(self.search_term))
        logger.addHandler(handler)
        logger.info("Search term {0}".format(self.search_term))

        return logger


class TwitterScraper(Twitter):

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
        super().__init__(search_term=search_term)
        self.text_query = '({0} OR @{0} OR #{0} or ${1}) -is:retweet'.format(search_term, token)
        self.limit_tweets = limit_tweets
        self.tweet_type = self.assert_and_get_tweet_type(tweet_type=tweet_type)
        self.start_time = time.time()
        self.api = self.get_tweepy_api()
        self.create_result_folders_if_not_exist()

    @staticmethod
    def assert_and_get_tweet_type(tweet_type: str) -> str:
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

        now = self.today.strftime("%d/%m/%Y, %H:%M:%S")
        list_now = now.split()
        day = list_now[0]
        hour = list_now[1]
        self.logger.info("Tweets retrieved on {0} at {1} in {2} seconds".format(
            day, hour, time.time() - self.start_time)
        )

        return df_tweets


class TwitterSentiment(Twitter):

    def __init__(self, search_term: str, model: str = "roberta", df_tweet: pd.DataFrame = pd.DataFrame()):
        super().__init__(search_term=search_term)
        self.model_str = model
        self.model_hugging_face = self.get_model_type(model_type=model)
        self.sentiment_analysis = pipeline(model=self.model_hugging_face)
        self.start_time = time.time()
        self.df_tweets = df_tweet
        self.today_string = self.today.strftime('%d-%m-%Y-%H-%M')

    @staticmethod
    def get_model_type(model_type: str) -> str:
        if model_type == "roberta":
            return "cardiffnlp/twitter-roberta-base-sentiment-latest"
        elif model_type == "bert":
            return "finiteautomata/bertweet-base-sentiment-analysis"
        else:
            raise AssertionError("Supported model types are roberta and bert")

    def calculate_sentiment_analysis(self) -> None:
        """
            Performs sentiment analysis depending on the model
        """
        self.df_tweets['sentiment_dict'] = self.df_tweets["text"].apply(lambda x: self.sentiment_analysis(x))
        self.df_tweets['sentiment_{0}'.format(self.model_str)] = self.df_tweets["sentiment_dict"].apply(
            lambda x: x[0]['label'])
        if self.model_hugging_face == "bert":
            self.df_tweets['sentiment_{0}'.format(self.model_str)] = self.df_tweets[
                'sentiment_{0}'.format(self.model_str)].apply(lambda x: x.replace("POS", "Positive"))
            self.df_tweets['sentiment_{0}'.format(self.model_str)] = self.df_tweets[
                'sentiment_{0}'.format(self.model_str)].apply(lambda x: x.replace("NEG", "Negative"))
            self.df_tweets['sentiment_{0}'.format(self.model_str)] = self.df_tweets[
                'sentiment_{0}'.format(self.model_str)].apply(lambda x: x.replace("NEU", "Neutral"))
        self.df_tweets['score_{0}'.format(self.model_str)] = self.df_tweets["sentiment_dict"].apply(
            lambda x: x[0]['score']
        )

        self.df_tweets.drop(['sentiment_dict'], axis=1, inplace=True)

    def save_pie_chart_sentiment_analysis(self) -> None:
        """
            Creates and saves pie chart of sentiment analysis
            :return: None
            :rtype: None
            """
        # Let's count the number of tweets by sentiments
        sentiment_counts = self.df_tweets.groupby(['sentiment_{0}'.format(self.model_str)]).size()

        # Let's visualize the sentiments
        fig = plt.figure(figsize=(6, 6), dpi=100)
        ax = plt.subplot(111)
        sentiment_counts.plot.pie(ax=ax, autopct='%1.1f%%', startangle=270, fontsize=12, label="")
        plt.title("{0} Pie-chart Sentiment Analysis - {1} Model".format(self.search_term, self.model_str))
        plt.savefig('../img/{0}/twitter/{1}/pie_chart_sentiment_{2}.png'.format(
            self.search_term, self.model_str, self.today_string)
        )

    def save_word_cloud(self):
        """
            Creates and saves 3 world clouds (positive, neutral and negative) for a specific search term
        """

        sentiment_types = ["Positive", "Negative", "Neutral"]
        stop_words = set(["https", "co", "RT"] + list(STOPWORDS))
        for sentiment in sentiment_types:
            sentiment_tweets = self.df_tweets['text'][
                self.df_tweets['sentiment_{0}'.format(self.model_str)] == sentiment
            ]
            sentiment_wordcloud = WordCloud(max_font_size=50, max_words=100,
                                            background_color="white", stopwords=stop_words).generate(
                str(sentiment_tweets)
            )
            plt.figure()
            plt.title("{0} Wordcloud {1} Tweets - {1} Model".format(self.search_term, sentiment, self.model_hugging_face))
            plt.imshow(sentiment_wordcloud, interpolation="bilinear")
            plt.axis("off")
            plt.savefig('../img/{0}/twitter/{1}/wordcloud_{2}_sentiment_{3}'.format(
                self.search_term, self.model_str, sentiment, self.today_string)
            )

    def run_sentiment_analysis(self):
        """
        Runner
        """
        self.calculate_sentiment_analysis()
        self.save_pie_chart_sentiment_analysis()
        self.save_word_cloud()
        self.df_tweets.to_csv('../data/results/{0}/twitter/sentiment_{1}.csv'.format(
            self.search_term, self.today_string
        ), sep=';')
        self.logger.info("Analysis run in {0} seconds".format(time.time() - self.start_time))
