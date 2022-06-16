import os

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

    if not next_token_id:
        url = "{0}/{1}/{2}?query={3}&granularity={4}&start_time={5}&end_time={6}".format(
            basic_url, request_type, access_level, search_term, granularity_level, start_date, end_date
        )

    else:
        url = "{0}/{1}/{2}?query={3}&granularity={4}&start_time={5}&end_time={6}&next_token={7}".format(
            basic_url, request_type, access_level, search_term, granularity_level, start_date, end_date, next_token_id
        )

    return url

# TODO: Set dynamically entity_id and annotation_id
def build_url_with_annotation():
    # entity_id = 174  # digital asset
    # annotation_id = 1007360414114435072  # Bitcoin
    # query_annotation = "context:{0}.{1}".format(entity_id, annotation_id)
    pass


# TODO: Set title dynamically
def plot():
    # df_tweets.plot(kind="scatter", x='dates', y='tweet_count', c='tweet_count', colormap='coolwarm',
    #                title='Hourly count of Bitcoin Tweets')
    pass


if __name__ == "__main__":

    df = pd.read_csv("../look_up_tables/df_Digital Assets & Crypto.csv", sep=";", decimal=',')
    df.rename(columns={"Unnamed: 0": "id"}, inplace=True)

    entities = pd.read_csv("../look_up_tables/entities.csv", sep=';', decimal=',')
    entities.rename(columns={"Unnamed: 0": "id", "0": "name"}, inplace=True)

    # Build header to authenticate using bearer token
    authentication_header = get_authentication_headers(academic_access=True)

    query_type = "counts"
    granularity = "day"  # day, hour or minute
    start = "2022-01-01T00:00:00Z"
    end = "2022-06-15T00:00:00Z"
    access_type = "all"  # "all" for academic access, "recent" for premium access
    query_text = "bitcoin"

    request_url = build_url(request_type=query_type, access_level=access_type, granularity_level=granularity,
                            start_date=start, end_date=end, search_term=query_text)

    response = requests.get(url=request_url, headers=authentication_header)

    # Fetch response data as dictionary
    if response.status_code == 200:
        data = response.json()

    elif response.status_code == 400:
        raise PermissionError("Bad request {0}, check if the url {1} is correct".format(
            response.status_code, request_url)
        )

    else:
        raise ValueError("Unknown error, status code is {0}, check if the url {1} is correct".format(
            response.status_code, request_url)
        )

    if "next_token" in data["meta"].keys():
        next_token = data["meta"]["next_token"]

    total_tweet_count = data["meta"]["total_tweet_count"]
    df_tweets = pd.DataFrame(data=data["data"])
    df_tweets["start"] = pd.to_datetime(df_tweets.start).dt.strftime('%Y-%m-%d %H:%M')
    df_tweets["end"] = pd.to_datetime(df_tweets.end).dt.strftime('%Y-%m-%d %H:%M')
    df_tweets["dates"] = [pd.to_datetime(d) for d in df_tweets.start]


    print("Run")
