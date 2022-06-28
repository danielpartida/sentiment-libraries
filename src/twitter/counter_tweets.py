import os
from typing import Tuple
from datetime import datetime

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


def build_url(request_type: str = "counts", access_level: str = "all", granularity_level: str = "day",
              start_date: str = "2022-01-01T00:00:00Z", end_date: str = "2022-06-15T00:00:00Z",
              search_term: str = "bitcoin", next_token_id: str = "") -> str:
    """
    Builds url to request counts or tweets
    Source and examples https://developer.twitter.com/en/docs/twitter-api/tweets/counts/quick-start/recent-tweet-counts
    :param request_type: "counts" or "search"
    :type request_type: str
    :param access_level: academic "all" or premium "recent"
    :type access_level: str
    :param granularity_level: day, hour or minute
    :type granularity_level: str
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

    # last run
    if not next_token_id:
        url = "{0}/{1}/{2}?query={3}&granularity={4}&start_time={5}&end_time={6}".format(
            basic_url, request_type, access_level, search_term, granularity_level, start_date, end_date
        )

    # first run
    elif next_token_id == "first_run":
        url = "{0}/{1}/{2}?query={3}&granularity={4}&start_time={5}&end_time={6}".format(
            basic_url, request_type, access_level, search_term, granularity_level, start_date, end_date
        )

    # all runs besides first and last run
    else:
        url = "{0}/{1}/{2}?query={3}&granularity={4}&start_time={5}&end_time={6}&next_token={7}".format(
            basic_url, request_type, access_level, search_term, granularity_level, start_date, end_date, next_token_id
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

    else:
        raise ValueError("Unknown error, status code is {0}, check if the url {1} is correct".format(
            request_response.status_code, request_url)
        )

    return data


def convert_data_into_df(data: dict) -> Tuple:
    """
    Builds dataframe with response data, fetches the total tweets and gets next_token_id
    :param data: response data
    :type data: dict
    :return: df of timeseries of total tweets per granularity, total tweets in that window, and next token id
    :rtype: Tuple
    """
    if "next_token" in data["meta"].keys():
        next_token_id = data["meta"]["next_token"]

    else:
        next_token_id = None

    total_tweet_count = data["meta"]["total_tweet_count"]
    df_tweets = pd.DataFrame(data=data["data"])
    df_tweets["start"] = pd.to_datetime(df_tweets.start).dt.strftime('%Y-%m-%d %H:%M')
    df_tweets["end"] = pd.to_datetime(df_tweets.end).dt.strftime('%Y-%m-%d %H:%M')
    df_tweets["dates"] = [pd.to_datetime(d) for d in df_tweets.start]

    return df_tweets, total_tweet_count, next_token_id


# TODO: Set dynamically entity_id and annotation_id
# def build_url_with_annotation():
#     # entity_id = 174  # digital asset
#     # annotation_id = 1007360414114435072  # Bitcoin
#     # query_annotation = "context:{0}.{1}".format(entity_id, annotation_id)
#     pass


if __name__ == "__main__":

    # df = pd.read_csv("../../look_up_tables/df_Digital Assets & Crypto.csv", sep=";", decimal=',')
    # df.rename(columns={"Unnamed: 0": "id"}, inplace=True)
    # entities = pd.read_csv("../../look_up_tables/entities.csv", sep=';', decimal=',')
    # entities.rename(columns={"Unnamed: 0": "id", "0": "name"}, inplace=True)

    # Build header to authenticate using bearer token
    authentication_header = get_authentication_headers(academic_access=True)

    query_type = "counts"
    granularity = "day"  # day, hour or min

    start = "2022-01-01T00:00:00Z"
    today = datetime.today()
    date_format_long = '%Y-%m-%dT00:00:00Z'
    date_format_short = '%d_%m'
    end = today.strftime(date_format_long)

    access_type = "all"  # "all" for academic access, "recent" for premium access
    query_text = "solana"

    all_df_tweets = []
    total_tweets = 0
    next_token = "first_run"
    while next_token:
        constructed_url = build_url(request_type=query_type, access_level=access_type, granularity_level=granularity,
                                    start_date=start, end_date=end, search_term=query_text, next_token_id=next_token)

        response = requests.get(url=constructed_url, headers=authentication_header)
        response_data = get_data_with_control_flow(request_response=response, request_url=constructed_url)

        df_tweets_window, total_tweets_window, next_token = convert_data_into_df(response_data)
        all_df_tweets.append(df_tweets_window)
        total_tweets += total_tweets_window

    df = pd.concat(all_df_tweets)
    df.set_index("dates", inplace=True)
    df.sort_index(inplace=True)
    df = df.tweet_count

    df.to_csv("../dashboard/data/counts_{0}_{1}.csv".format(query_text, today.strftime(date_format_short)),
              decimal=',', sep=';')
