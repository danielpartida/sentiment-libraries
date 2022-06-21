import os

import json
import re

import requests
from datetime import datetime
from dotenv import load_dotenv

from db.helper import get_session
from db.entities import TwitterStreams

load_dotenv()


def create_url():
    return "https://api.twitter.com/2/tweets/sample/stream?tweet.fields=context_annotations,lang"


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2SampledStreamPython"
    return r

# FIXME: Double check tweet clean, particularly if emojis are deleted
def clean_tweet(tweet: str):
    """
    Utility function to clean tweet text by removing links, special characters using simple regex statements.
    Example taken from https://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/?ref=lbp
    """
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w+:\ / \ / \S+)", " ", tweet).split())


def connect_to_endpoint(url):
    """
    Topic sources: https://blog.twitter.com/en_us/topics/product/2020/topics-behind-the-tweets
    https://twitter.com/i/topics/picker/home
    :param url: request url
    :type url: str
    :return: Sends tweet to database
    :rtype: None
    """
    response = requests.request("GET", url, auth=bearer_oauth, stream=True)

    crypto_tweets = []
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            if json_response["data"]["lang"] == "en":
                crypto_tweet = filter_context_annotations(tweet_response=json_response)

                if bool(crypto_tweet):
                    crypto_tweets.append(crypto_tweet)

                    now = datetime.now()
                    tweet_stream = TwitterStreams(
                        domain_id=crypto_tweet["domain_id"],
                        entity_id=crypto_tweet["entity_id"],
                        entity_name=crypto_tweet["entity_name"],
                        language=crypto_tweet["lang"],
                        text=crypto_tweet["text"],
                        tweet_id=crypto_tweet["tweet_id"],
                        date=now
                    )
                    # TODO: Delete print statement
                    session.add(tweet_stream)
                    session.commit()
                    print(json.dumps(crypto_tweet, indent=4, sort_keys=True))

    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )


def run_volume_streams():
    # GitHub source https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/main/Sampled-Stream/sampled-stream.py
    # https://developer.twitter.com/en/docs/twitter-api/tweets/volume-streams/api-reference/get-tweets-sample-stream#tab1
    url = create_url()
    timeout = 0
    while True:
        connect_to_endpoint(url)
        timeout += 1


def check_crypto_context(context: dict) -> bool:
    """
    Check if context is crypto relevant
    :param context: tweet fields
    :type context: dict
    :return: True if tweet is crypto related, False otherwise
    :rtype: bool
    """
    if (int(context["domain"]["id"]) == 66 and int(context["entity"]["id"]) == 913142676819648512) or (
            int(context["domain"]["id"]) == 174):
        return True

    else:
        return False


def filter_context_annotations(tweet_response: list) -> dict:
    """

    :param tweet_response: tweet with response parameters list described in
    https://developer.twitter.com/en/docs/twitter-api/tweets/volume-streams/api-reference/get-tweets-sample-stream
    :type tweet_response: list of parameters
    :return: dictionary of filtered data containing only tweets related to crypto assets
    :rtype: dict
    """
    try:
        data = tweet_response["data"]
        result = {"tweet_id": data["id"], "lang": data["lang"]}

        if "context_annotations" in data.keys():
            for context in data["context_annotations"]:
                # check if domain is "interest & hobbies: category" and annotation is "crypto" or domain is "crypto"
                if check_crypto_context(context=context):

                    result["domain_id"] = int(context["domain"]["id"])
                    result["entity_id"] = int(context["entity"]["id"])
                    result["entity_name"] = context["entity"]["name"]
                    if "entity_description" in context["entity"].keys():
                        result["entity_description"] = context["entity"]["description"]

                    result["text"] = clean_tweet(data["text"])

            if check_crypto_context(context=context):
                return result

    except ValueError as err:
        print("An error just occurred: {0}".format(err))

    else:
        return {}


if __name__ == "__main__":

    session = get_session()

    bearer_token = os.environ.get("BEARER_TOKEN")

    # TODO: Handle connections and rate limits, 50 requests per 15-minute window shared among all users of your app
    run_volume_streams()
    session.close()
