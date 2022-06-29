import os
from datetime import datetime
from typing import Tuple
import re

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()


def get_authentication_headers(academic_access: bool) -> dict:
    """
    Builds header to authenticate on Twitter using bearer token
    :param academic_access: To use either academic or premium bearer token
    :type academic_access: bool
    :return: Header to use in request call
    :rtype: dict
    """
    if academic_access:
        token = os.getenv('academic')

    else:
        token = os.getenv('bearer_token')

    headers = {"Authorization": "Bearer {0}".format(token)}

    return headers


def build_query(search_term: str) -> str:
    """
    Filters tweets that were retweeted, and with specific keywords
    :param search_term: token name
    :type search_term: str
    :return: query
    :rtype: str
    """
    filter_term = ' -is:retweet -RT -"public sale" -"mint" -airdrop -giveaway -giveaways -is:nullcast ' \
                  '-tag -tagg lang:en'
    search_term += filter_term

    return search_term


def build_url(request_type: str = "search", access_level: str = "all", start_date: str = "2022-01-01T00:00:00Z",
              end_date: str = "2022-06-15T00:00:00Z", search_term: str = "bitcoin", next_token_id: str = "") -> str:
    """
    Source: https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-all
    :param request_type: "search"
    :type request_type: str
    :param access_level: academic "all" or premium "recent"
    :type access_level: str
    :param start_date: format 2022-01-01T00:00:00Z
    :type start_date: str
    :param end_date: format 2022-06-15T00:00:00Z
    :type end_date: str
    :param search_term: bitcoin, ethereum, etc
    :type search_term: str
    :param next_token_id: from the metadata of response, e.g. 1jzu9lk96azp0b3x7888hrpw8n4cwf45yrvgqbbbi8hp
    :type next_token_id: str
    :return: full url ready to be called
    :rtype: str
    """

    basic_url = "https://api.twitter.com/2/tweets"
    tweet_fields = "created_at,context_annotations,public_metrics,author_id,conversation_id,in_reply_to_user_id," \
                   "entities"
    user_fields = "created_at,entities,name,public_metrics,verified"
    end_url = "max_results=100&tweet.fields={0}&user.fields={1}&sort_order=relevancy&&expansions=author_id".format(
        tweet_fields, user_fields
    )

    # first and last run
    if not next_token_id or next_token_id == "first_run":
        url = "{0}/{1}/{2}?query={3}&start_time={4}&end_time={5}&{6}".format(
            basic_url, request_type, access_level, search_term, start_date, end_date, end_url
        )

    # all runs besides first and last run
    else:
        url = "{0}/{1}/{2}?query={3}&start_time={4}&end_time={5}&next_token={6}&{7}".format(
            basic_url, request_type, access_level, search_term, start_date, end_date, next_token_id,
            end_url
        )

    return url


def get_data_with_control_flow(request_response: requests.models.Response, request_url: str) -> dict:
    """
    Gets data from response checking control flow
    :param request_response: request response
    :type request_response: requests.models.Response
    :param request_url: request url
    :type request_url: str
    :return: response data
    :rtype: dict
    """
    if request_response.status_code == 200:
        data = request_response.json()

    elif request_response.status_code == 400:
        raise PermissionError("Bad request {0}, check if the url {1} is correct".format(
            request_response.status_code, request_url)
        )

    elif request_response.status_code == 404:
        raise ValueError("Error {0}. The URI requested is invalid or the resource requested.".format(
            request_response.status_code)
        )

    else:
        raise ValueError("Unknown error, status code is {0}, check if the url {1} is correct".format(
            request_response.status_code, request_url)
        )

    return data


def clean_tweet(tweet: str):
        """
        Utility function to clean tweet text by removing links, special characters using simple regex statements.
        Example taken from https://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/?ref=lbp
        """
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w+:\ / \ / \S+)", " ", tweet).split())


def convert_data_into_df(data: dict) -> Tuple:
    """
    Builds dataframe with response data and gets next_token_id
    :param data: response data
    :type data: dict
    :return: df of timeseries of total tweets per granularity, total tweets in that window, and next token id
    :rtype: Tuple
    """
    if "next_token" in data["meta"].keys():
        next_token_id = data["meta"]["next_token"]

    else:
        next_token_id = None

    list_dict_tweets = []
    for tweet in data["data"]:
        dict_tweet = {
            'id': tweet["id"], "url": "https://twitter.com/twitter/status/{0}".format(tweet["id"]),
            'created_at': tweet["created_at"], 'author_id': tweet["author_id"],
            'conversation_id': tweet["conversation_id"],
            'reply_count': tweet["public_metrics"]["reply_count"],
            'like_count': tweet["public_metrics"]["like_count"],
            'retweet_count': tweet["public_metrics"]["retweet_count"],
            'quote_count': tweet["public_metrics"]["quote_count"],
            'raw_text': tweet["text"], 'type': "relevant"
        }

        if 'context_annotations' in tweet.keys():
            dict_tweet['context_annotations'] = tweet["context_annotations"],

        if "entities" in tweet.keys():
            dict_tweet["entities"] = tweet["entities"]

        dict_tweet['text'] = clean_tweet(dict_tweet['raw_text'])

        list_dict_tweets.append(dict_tweet)

    df_tweets = pd.DataFrame(list_dict_tweets)

    return df_tweets, next_token_id


def convert_users_into_df(data: dict) -> pd.DataFrame:
    """
    Converts users into dataframe
    :param data: response data
    :type data: dict
    :return: dataframe of users with follower metrics, etc
    :rtype: pd.DataFrame
    """
    list_of_users = []
    for user in data["includes"]["users"]:
        dict_users = {
            "user_id": user["id"], "user_name": user["name"], "user_handle": user["username"],
            "verified": user["verified"], "created_at": user["created_at"],
        }

        if "public_metrics" in user.keys():
            dict_users["followers"] = user["public_metrics"]["followers_count"]
            dict_users["following"] = user["public_metrics"]["following_count"]
            dict_users["tweet_count"] = user["public_metrics"]["tweet_count"]

        list_of_users.append(dict_users)

    df_users = pd.DataFrame(list_of_users)

    return df_users


def save_df_to_csv(list_all_data: list, index_col: str, name_csv: str) -> None:
    df = pd.concat(list_all_data)
    df.set_index(index_col, inplace=True)
    df.sort_index(inplace=True)
    df.to_csv("../dashboard/data/{0}_{1}_{2}.csv".format(name_csv, token, today.strftime(date_format_short)),
              sep=";", decimal=",")


if __name__ == "__main__":

    # Build header to authenticate using bearer token
    authentication_header = get_authentication_headers(academic_access=True)

    query_type = "search"
    access_type = "all"

    start = "2022-01-01T00:00:00Z"
    today = datetime.today()
    date_format_long = '%Y-%m-%dT00:00:00Z'
    date_format_short = '%d_%m'
    end = today.strftime(date_format_long)

    token = "solana"  # "all" for academic access, "recent" for premium access
    query_text = build_query(search_term=token)

    list_all_tweets, list_all_users = [], []
    total_tweets = 0
    next_token = "first_run"

    rate_limit = 0
    while next_token:
        # Based on  https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-all
        constructed_url = build_url(request_type=query_type, access_level=access_type, start_date=start, end_date=end,
                                    search_term=query_text, next_token_id=next_token)

        response = requests.get(url=constructed_url, headers=authentication_header)
        response_data = get_data_with_control_flow(request_response=response, request_url=constructed_url)

        df_tweets_window, next_token = convert_data_into_df(data=response_data)
        list_all_tweets.append(df_tweets_window)

        df_users_window = convert_users_into_df(data=response_data)
        list_all_users.append(df_users_window)

    save_df_to_csv(list_all_data=list_all_tweets, index_col="created_at", name_csv="tweets")
    save_df_to_csv(list_all_data=list_all_users, index_col="id", name_csv="users")

