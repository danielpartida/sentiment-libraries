import logging
import os
import time
from datetime import date, datetime, timedelta
import re

import pandas as pd
import tweepy
from dotenv import load_dotenv
from matplotlib import pyplot as plt
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

        if self.search_term.find("context") != -1:
            handler = logging.FileHandler(filename="../../logger/context_annotation.log")
        else:
            handler = logging.FileHandler(filename="../../logger/{0}.log".format(self.search_term))

        logger.addHandler(handler)

        return logger

    @staticmethod
    def build_text_query(search_term: str, token: str):
        if token:
            text_query = '({0} OR @{0} OR #{0} OR "${1}") -is:retweet lang:en'.format(search_term, token)

        elif search_term.find("context") != -1:
            text_query = search_term

        else:
            text_query = '({0} OR @{0} OR #{0}) -is:retweet lang:en'.format(search_term)

        return text_query

    @staticmethod
    def clean_tweet(tweet: str):
        """
        Utility function to clean tweet text by removing links, special characters using simple regex statements.
        Example taken from https://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/?ref=lbp
        """
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w+:\ / \ / \S+)", " ", tweet).split())

    @staticmethod
    def assert_and_get_tweet_type(tweet_type: str) -> str:
        assert tweet_type in ["mixed", "recent", "popular"], "Supported result types are mixed, recent and popular"
        return tweet_type

    def create_result_folders_if_not_exist(self) -> None:
        """
        Creates data and img result folders
        :return: None
        :rtype: None
        """

        if self.search_term.find("context") != -1:
            context = "context"
            paths = ["../data/results/{0}/discord".format(context),
                     "../data/results/{0}/twitter".format(context), "../img/{0}/discord".format(context),
                     "../img/{0}/twitter/bert".format(context),
                     "../img/{0}/twitter/roberta".format(context)]

        else:

            paths = ["../data/results/{0}/discord".format(self.search_term),
                     "../data/results/{0}/twitter".format(self.search_term),
                     "../img/{0}/discord".format(self.search_term),
                     "../img/{0}/twitter/bert".format(self.search_term),
                     "../img/{0}/twitter/roberta".format(self.search_term)]

        for path in paths:
            if not os.path.exists(path):
                os.makedirs(path)


class TwitterPremium(Twitter):

    def __init__(self, search_term: str, token: str = "", tweets_per_window: int = 1000,
                 from_time: datetime = datetime.utcnow() - timedelta(days=1), delta_days: int = 6):
        """
        Constructor of TwitterScraping class
        :param search_term: queried term
        :type search_term: str
        :param tweets_per_window: maximal amount of tweets to scrap
        :type tweets_per_window: int
        """
        super().__init__(search_term=search_term)
        self.text_query = self.build_text_query(search_term=search_term, token=token)
        self.limit_tweets = tweets_per_window
        self.start_time = time.time()
        self.api = self.get_tweepy_api()
        self.from_time = from_time
        self.client = tweepy.Client(bearer_token=os.getenv("bearer_token"), wait_on_rate_limit=True,
                                    wait_on_rate_limit_notify=True)
        self.create_result_folders_if_not_exist()
        self.delta_days = delta_days

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

    def get_scraped_tweets(self) -> pd.DataFrame:
        """
        Twitter’s standard search API only searches against a sampling of recent Tweets published in the past 7 days
        Tweepy library: https://docs.tweepy.org/en/v4.8.0/api.html#tweepy.API.search_tweets
        API V1: https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/api-reference/get-search-tweets
        API V2: https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference
        Pagination https://docs.tweepy.org/en/latest/v2_pagination.html
        :return: dataframe of tweets
        :rtype: pd.DataFrame
        """
        self.logger.info("Searching for term {0}".format(self.search_term))

        list_dict_tweets = []
        try:
            # Rolling window scrapper
            # FIXME: Adapt this loop for request limit  https://developer.twitter.com/en/docs/twitter-api/rate-limits
            for i in range(self.delta_days * 24 - 1):
                self.from_time += timedelta(hours=1)
                from_time_str = self.from_time.strftime('%Y-%m-%dT%H:%M:%SZ')
                to_time = self.from_time + timedelta(hours=1)
                to_time_str = to_time.strftime('%Y-%m-%dT%H:%M:%SZ')
                print("from_time:", from_time_str, "to_time:", to_time_str)
                for tweet in tweepy.Paginator(
                        self.client.search_recent_tweets, query=self.text_query,
                        start_time=from_time_str, end_time=to_time_str, max_results=50,
                        tweet_fields=['context_annotations', 'created_at', 'author_id', 'conversation_id',
                                      'in_reply_to_user_id', 'entities', 'public_metrics']
                ).flatten(limit=self.limit_tweets):
                    # fetch main information of tweet
                    # tweet fields https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/tweet
                    dict_tweet = {
                        'id': tweet.id, "url": "https://twitter.com/twitter/statuses/{0}".format(tweet.id),
                        'created_at': tweet.created_at, 'author_id': tweet.author_id,
                        'conversation_id': tweet.conversation_id,
                        'in_reply_to_user_id': tweet.in_reply_to_user_id,
                        'reply_count': tweet.public_metrics["reply_count"],
                        'like_count': tweet.public_metrics["like_count"],
                        'retweet_count': tweet.public_metrics["retweet_count"],
                        'quote_count': tweet.public_metrics["quote_count"],
                        'context_annotations': tweet.context_annotations,
                        'raw_text': tweet.text, 'type': "recent"
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

        time_stamp_export = self.today.strftime("%d_%m_%H_%M")

        if self.search_term.find("context") != -1:
            context = "context"
            df_tweets.to_csv("../data/backup/{0}_tweets_{1}.csv".format(context, time_stamp_export),
                             sep=';', decimal=',')
        else:
            df_tweets.to_csv("..data/backup/{0}_tweets_{1}.csv".format(self.search_term, time_stamp_export),
                             sep=';', decimal=',')

        return df_tweets


class TwitterAcademic(Twitter):

    def __init__(self, search_term: str, token: str = "", tweets_per_window: int = 50,
                 start_time: datetime = datetime.combine(date(2022, 1, 1), datetime.min.time()),
                 end_time: datetime = datetime.utcnow()):
        """
        Constructor of TwitterScraping class
        :param search_term: queried term
        :type search_term: str
        :param tweets_per_window: maximal amount of tweets to scrap
        :type tweets_per_window: int
        """
        super().__init__(search_term=search_term)
        self.text_query = self.build_text_query(search_term=search_term, token=token)
        self.limit_tweets = tweets_per_window
        self.t1 = time.time()
        self.start_time = start_time
        self.end_time = end_time
        self.client = tweepy.Client(bearer_token=os.getenv("academic"))
        self.create_result_folders_if_not_exist()

    def get_scraped_tweets_academic(self) -> pd.DataFrame:
        """
        API Academic V2: https://docs.tweepy.org/en/stable/client.html#search-tweets
        :return:
        :rtype:
        """
        self.logger.info("Searching for term {0}".format(self.search_term))

        list_dict_tweets = []
        try:
            # Rolling window scrapper
            delta = self.end_time - self.start_time
            delta_days = delta.days
            for i in range(delta_days * 24 - 1):
                self.start_time += timedelta(hours=1)
                start_time_str = self.start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
                temp_end_time = self.start_time + timedelta(hours=1)
                temp_end_time_str = temp_end_time.strftime('%Y-%m-%dT%H:%M:%SZ')
                print("from_time:", start_time_str, "to_time:", temp_end_time_str)
                for tweet in tweepy.Paginator(
                        self.client.search_all_tweets, query=self.text_query,
                        start_time=start_time_str, end_time=temp_end_time_str, max_results=50,
                        tweet_fields=['context_annotations', 'created_at', 'author_id', 'conversation_id',
                                      'in_reply_to_user_id', 'entities', 'public_metrics']
                ).flatten(limit=50):
                    # fetch main information of tweet fields
                    # https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/tweet
                    dict_tweet = {
                        'id': tweet.id, "url": "https://twitter.com/twitter/statuses/{0}".format(tweet.id),
                        'created_at': tweet.created_at, 'author_id': tweet.author_id,
                        'conversation_id': tweet.conversation_id,
                        'in_reply_to_user_id': tweet.in_reply_to_user_id,
                        'reply_count': tweet.public_metrics["reply_count"],
                        'like_count': tweet.public_metrics["like_count"],
                        'retweet_count': tweet.public_metrics["retweet_count"],
                        'quote_count': tweet.public_metrics["quote_count"],
                        'context_annotations': tweet.context_annotations,
                        'raw_text': tweet.text, 'type': "recent"
                    }
                    dict_tweet['text'] = self.clean_tweet(dict_tweet['raw_text'])

                    list_dict_tweets.append(dict_tweet)

                    # https://docs.tweepy.org/en/v4.10.0/faq.html#why-am-i-getting-rate-limited-so-quickly-when-using-client-search-all-tweets-with-paginator
                    time.sleep(1)

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
            day, hour, time.time() - self.t1)
        )

        time_stamp_export = self.today.strftime("%d_%m_%H_%M")

        df_tweets.to_csv("../../data/backup/{0}_tweets_{1}.csv".format(self.search_term, time_stamp_export),
                         sep=';', decimal=',')

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

    def save_pie_chart_sentiment_analysis(self, df_tweets: pd.DataFrame, is_quantile: bool) -> None:
        """
            Creates and saves pie chart of sentiment analysis
        """
        # Let's count the number of tweets by sentiments
        sentiment_counts = df_tweets.groupby(['sentiment_{0}'.format(self.model_str)]).size()

        # Let's visualize the sentiments
        fig = plt.figure(figsize=(6, 6), dpi=100)
        ax = plt.subplot(111)
        sentiment_counts.plot.pie(ax=ax, autopct='%1.1f%%', startangle=270, fontsize=12, label="")
        plt.title("{0} Pie-chart Sentiment Analysis - {1} Model".format(self.search_term, self.model_str))

        if is_quantile:
            plt.savefig('../img/{0}/twitter/{1}/pie_chart_sentiment_quantile_{2}.png'.format(
                self.search_term, self.model_str, self.today_string)
            )
        else:
            plt.savefig('../img/{0}/twitter/{1}/pie_chart_sentiment_{2}.png'.format(
                self.search_term, self.model_str, self.today_string)
            )

    def save_word_cloud(self, df_tweets: pd.DataFrame, is_quantile: bool) -> None:
        """
            Creates and saves 3 world clouds (positive, neutral and negative) for a specific search term
        """

        sentiment_types = ["Positive", "Negative", "Neutral"]
        stop_words = set(["https", "co", "RT", "dtype"] + list(STOPWORDS))
        color_maps = {"Positive": "YlGn", "Negative": "OrRd", "Neutral": "PuRd"}
        for sentiment in sentiment_types:
            sentiment_tweets = df_tweets['text'][
                df_tweets['sentiment_{0}'.format(self.model_str)] == sentiment
                ]
            # FIXME: Add proper colormap
            sentiment_wordcloud = WordCloud(max_font_size=50, max_words=100,  # colormap=color_maps[sentiment],
                                            background_color="white", stopwords=stop_words).generate(
                str(sentiment_tweets)
            )
            plt.figure()
            plt.title("{0} Wordcloud {1} Tweets - {2} Model".format(self.search_term, sentiment, self.model_str))
            plt.imshow(sentiment_wordcloud, interpolation="bilinear")
            plt.axis("off")

            if is_quantile:
                plt.savefig('../img/{0}/twitter/{1}/wordcloud_{2}_sentiment_quantile_{3}'.format(
                    self.search_term, self.model_str, sentiment, self.today_string)
                )
            else:
                plt.savefig('../img/{0}/twitter/{1}/wordcloud_{2}_sentiment_{3}'.format(
                    self.search_term, self.model_str, sentiment, self.today_string)
                )

    def calculate_timeseries_analysis(self, df_tweets: pd.DataFrame, is_quantile: bool) -> None:
        df_tweets["date"] = self.df_tweets.created_at.apply(lambda x: date(x.year, x.month, x.day))

        # group-by
        df_tweets.sort_values(by=["date"], ascending=True, inplace=True)

        # group-by and pivot
        model_group_by = self.df_tweets.groupby(
            by=['date', 'sentiment_{0}'.format(self.model_str)]
        )['sentiment_{0}'.format(self.model_str)].count()
        model_unstack = model_group_by.unstack()

        if is_quantile:
            model_unstack.to_csv(
                "../data/results/{0}/twitter/timeseries_{1}_sentiment_quantile_{2}.csv".format(
                    self.search_term, self.model_str, self.today_string
                ), sep=';', decimal=',')
        else:
            model_unstack.to_csv(
                "../data/results/{0}/twitter/timeseries_{1}_sentiment_{2}.csv".format(
                    self.search_term, self.model_str, self.today_string
                ), sep=';', decimal=',')

    def run_sentiment_analysis(self) -> None:
        """
        Runner
        """
        self.calculate_sentiment_analysis()

        self.save_pie_chart_sentiment_analysis(df_tweets=self.df_tweets, is_quantile=False)
        self.save_word_cloud(df_tweets=self.df_tweets, is_quantile=False)
        self.df_tweets.to_csv(
            '../data/results/{0}/twitter/sentiment_{1}.csv'.format(self.search_term, self.today_string),
            sep=';')

        self.calculate_timeseries_analysis(df_tweets=self.df_tweets, is_quantile=False)

        self.logger.info("Analysis run in {0} seconds".format(time.time() - self.start_time))

    def run_quantile_analysis(self) -> None:
        """
        Runner quantile
        :return:
        :rtype:
        """
        start_time = time.time()

        # Filter the upper 95 quantile of most liked tweets
        quantile_favorite_tweets_95 = self.df_tweets.like_count.quantile(0.95)
        df_tweets_quantile = self.df_tweets.loc[self.df_tweets.like_count > quantile_favorite_tweets_95]

        self.save_pie_chart_sentiment_analysis(df_tweets=df_tweets_quantile, is_quantile=True)
        self.save_word_cloud(df_tweets=df_tweets_quantile, is_quantile=True)
        df_tweets_quantile.to_csv('../data/results/{0}/twitter/sentiment_quantile_{1}.csv'.format(
            self.search_term, self.today_string), sep=';')

        self.logger.info("Quantile analysis run in {0} seconds".format(time.time() - start_time))
