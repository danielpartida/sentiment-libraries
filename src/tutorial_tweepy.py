import os
from dotenv import load_dotenv

import tweepy
from tweepy import OAuthHandler
import pandas as pd
import time


def run_scraping(twitter_api: tweepy.API, search_term: str, limit: int) -> pd.DataFrame:

    df_tweets = pd.DataFrame()
    try:
        # Creation of query method using appropriate parameters
        tweets = tweepy.Cursor(twitter_api.search_tweets, q=search_term, lang="eng",
                               since=date_since, until=date_until).items(limit)

        # Pulling information from tweets iterable object and adding relevant tweet information in our data frame
        for tweet in tweets:
            df_tweets = df_tweets.append(
                {'Created at': tweet._json['created_at'],
                 'User ID': tweet._json['id'],
                 'User Name': tweet.user._json['name'],
                 'Text': tweet._json['text'],
                 'Description': tweet.user._json['description'],
                 'Location': tweet.user._json['location'],
                 'Followers Count': tweet.user._json['followers_count'],
                 'Friends Count': tweet.user._json['friends_count'],
                 'Statuses Count': tweet.user._json['statuses_count'],
                 'Profile Image Url': tweet.user._json['profile_image_url'],
                 }, ignore_index=True)

    except BaseException as e:
        print('failed on_status,', str(e))
        time.sleep(3)

    return df_tweets


if __name__ == "__main__":

    load_dotenv()
    consumer_key = os.getenv('consumer_key')
    consumer_secret = os.getenv('consumer_secret')
    access_token = os.getenv('access_token')
    access_token_secret = os.getenv('access_token_secret')
    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    text_query = 'staratlas'

    df_results = run_scraping(twitter_api=api, search_term=text_query, limit=25)
    df_results.to_csv('../data/tweepy_{0}.csv'.format(text_query), sep=';')
