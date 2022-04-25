import logging
import os
import sys
import time
from datetime import date, datetime, timedelta

import pandas as pd
import tweepy
from dotenv import load_dotenv
from matplotlib import pyplot as plt
from transformers import pipeline
from tqdm import tqdm
from wordcloud import WordCloud, STOPWORDS


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
    list_dict_tweets = []
    try:
        list_twitter_items = [tweet for tweet in tweepy.Cursor(twitter_api.search_tweets, q=search_term, lang="en",
                                                               result_type="recent", count=limit,
                                                               until=until_date).items(limit)]

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


def get_type_of_model(sentiment_model: str) -> str:
    if "roberta" in sentiment_model.lower():
        type_model = "roberta"

    elif "bert" in sentiment_model.lower():
        type_model = "bert"

    else:
        type_model = ""

    return type_model


def run_sentiment(df_tweets: pd.DataFrame, sentiment_model: str) -> pd.DataFrame:
    """
    Performs sentiment analysis depending on the model
    :param df_tweets:
    :type df_tweets:
    :param sentiment_model:
    :type sentiment_model:
    :return:
    :rtype:
    """
    sentiment_analysis = pipeline(model=sentiment_model)

    type_model = get_type_of_model(sentiment_model=sentiment_model)

    df_tweets['sentiment_dict'] = df_tweets["text"].apply(lambda x: sentiment_analysis(x))
    df_tweets['sentiment_{0}'.format(type_model)] = df_tweets["sentiment_dict"].apply(lambda x: x[0]['label'])
    if type_model == "bert":
        df_tweets['sentiment_{0}'.format(type_model)] = df_tweets['sentiment_{0}'.format(type_model)].apply(
            lambda x: x.replace("POS", "Positive"))
        df_tweets['sentiment_{0}'.format(type_model)] = df_tweets['sentiment_{0}'.format(type_model)].apply(
            lambda x: x.replace("NEG", "Negative"))
        df_tweets['sentiment_{0}'.format(type_model)] = df_tweets['sentiment_{0}'.format(type_model)].apply(
            lambda x: x.replace("NEU", "Neutral"))
    df_tweets['score_{0}'.format(type_model)] = df_tweets["sentiment_dict"].apply(lambda x: x[0]['score'])

    df_tweets.drop(['sentiment_dict'], axis=1, inplace=True)

    return df_tweets


def save_pie_chart(df_tweets: pd.DataFrame, sentiment_model: str, search_term: str) -> None:
    """

    :param search_term:
    :type search_term:
    :param df_tweets:
    :type df_tweets:
    :param sentiment_model:
    :type sentiment_model:
    :return:
    :rtype:
    """
    type_model = get_type_of_model(sentiment_model=sentiment_model)

    # Let's count the number of tweets by sentiments
    sentiment_counts = df_tweets.groupby(['sentiment_{0}'.format(type_model)]).size()

    # Let's visualize the sentiments
    fig = plt.figure(figsize=(6, 6), dpi=100)
    ax = plt.subplot(111)
    sentiment_counts.plot.pie(ax=ax, autopct='%1.1f%%', startangle=270, fontsize=12, label="")
    plt.title("Pie-chart Sentiment Analysis- {0} Model".format(type_model))
    plt.savefig('../img/{0}_pie_chart_sentiment_{1}.png'.format(search_term, type_model))


def save_word_cloud(df_tweet: pd.DataFrame, sentiment_model: str, search_term: str) -> None:
    """

    :param search_term:
    :type search_term:
    :param df_tweet:
    :type df_tweet:
    :param sentiment_model:
    :type sentiment_model:
    :return:
    :rtype:
    """
    type_model = get_type_of_model(sentiment_model=sentiment_model)

    sentiment_types = ["Positive", "Negative", "Neutral"]
    stop_words = set(["https", "co", "RT"] + list(STOPWORDS))
    for sentiment in sentiment_types:
        sentiment_tweets = df_tweet['text'][df_tweet['sentiment_{0}'.format(type_model)] == sentiment]
        sentiment_wordcloud = WordCloud(max_font_size=50, max_words=100,
                                        background_color="white", stopwords=stop_words).generate(str(sentiment_tweets))
        plt.figure()
        plt.title("Wordcloud {0} Tweets - {1} Model".format(sentiment, type_model))
        plt.imshow(sentiment_wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.savefig('../img/{0}_wordcloud_{1}_sentiment_{2}.png'.format(search_term, sentiment, type_model))


if __name__ == "__main__":

    if len(sys.argv) <= 1:
        text_query = 'crypto'
        limit: int = 100

    else:
        text_query = str(sys.argv[1])
        limit = int(sys.argv[2])

    # logger
    logger = logging.getLogger("tweepy")
    logging.basicConfig(level=logging.DEBUG)
    handler = logging.FileHandler(filename="../logger/{0}.log".format(text_query))
    logger.addHandler(handler)

    logger.info("Search term {0}".format(text_query))

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
    df = run_scraping(twitter_api=api, search_term=text_query, limit=limit, until_date=yesterday)

    # perform sentiment analysis
    models = ["cardiffnlp/twitter-roberta-base-sentiment-latest", "finiteautomata/bertweet-base-sentiment-analysis"]

    for model in tqdm(models):
        logger.info("Sentiment analysis starting")
        df_results = run_sentiment(df_tweets=df, sentiment_model=model)
        logger.info("Pie-chart starting")
        save_pie_chart(search_term=text_query, df_tweets=df_results, sentiment_model=model)
        logger.info("Wordcloud starting")
        save_word_cloud(search_term=text_query, df_tweet=df_results, sentiment_model=model)

    del df

    # Export
    df_results.to_csv('../data/{0}_sentiment.csv'.format(text_query), sep=';')
