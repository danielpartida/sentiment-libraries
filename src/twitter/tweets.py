import os
from datetime import datetime
from typing import Tuple

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

    # last run
    if not next_token_id:
        url = "{0}/{1}/{2}?query={3}&start_time={4}&end_time={5}&max_results=500&sort_order=relevancy".format(
            basic_url, request_type, access_level, search_term, start_date, end_date
        )

    # first run
    elif next_token_id == "first_run":
        url = "{0}/{1}/{2}?query={3}&start_time={4}&end_time={5}&max_results=500&sort_order=relevancy".format(
            basic_url, request_type, access_level, search_term, start_date, end_date
        )

    # all runs besides first and last run
    else:
        url = "{0}/{1}/{2}?query={3}&start_time={4}&end_time={5}&next_token={6}&max_results=500&sort_order=relevancy".format(
            basic_url, request_type, access_level, search_term, start_date, end_date, next_token_id
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

    df_tweets = pd.DataFrame(data=data["data"])

    return df_tweets, next_token_id


if __name__ == "__main__":

    # Build header to authenticate using bearer token
    authentication_header = get_authentication_headers(academic_access=True)

    query_type = "search"

    start = "2022-01-01T00:00:00Z"
    today = datetime.today()
    date_format_long = '%Y-%m-%dT00:00:00Z'
    date_format_short = '%d_%m'
    end = today.strftime(date_format_long)

    access_type = "all"  # "all" for academic access, "recent" for premium access
    query_text = "solana -is:retweet"

    all_df_tweets = []
    total_tweets = 0
    next_token = "first_run"

    rate_limit = 00
    while next_token and rate_limit < 5:
        constructed_url = build_url(request_type=query_type, access_level=access_type, start_date=start, end_date=end,
                                    search_term=query_text, next_token_id=next_token)

        response = requests.get(url=constructed_url, headers=authentication_header)
        response_data = get_data_with_control_flow(request_response=response, request_url=constructed_url)

        df_tweets_window, next_token = convert_data_into_df(response_data)
        all_df_tweets.append(df_tweets_window)

        rate_limit += 1

    df = pd.concat(all_df_tweets)
    df.sort_index(inplace=True)
    df = df.tweet_count
