import os

import json
import requests
from dotenv import load_dotenv

from src.db.utils import get_session

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


def connect_to_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth, stream=True)

    crypto_tweets = []
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            if json_response["data"]["lang"] == "en":
                crypto_tweet = filter_context_annotations(tweet_response=json_response)

                if bool(crypto_tweet):
                    crypto_tweets.append(crypto_tweet)
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
    data = tweet_response["data"]
    result = {"tweet_id": data["id"], "lang": data["lang"], "text": data["text"]}

    if "context_annotations" in data.keys():
        for context in data["context_annotations"]:
            # check if domain is "interest & hobbies: category" and annotation is "crypto" or domain is "crypto"
            if check_crypto_context(context=context):

                result["domain_id"] = int(context["domain"]["id"])
                result["entity_id"] = int(context["entity"]["id"])
                result["entity_name"] = context["entity"]["name"]
                if "entity_description" in context["entity"].keys():
                    result["entity_description"] = context["entity"]["description"]

        if check_crypto_context(context=context):
            return result

    else:
        return {}


if __name__ == "__main__":

    # TODO: Get session and stream tweet volumes
    # session = get_session()

    bearer_token = os.environ.get("BEARER_TOKEN")

    # TODO: Handle connections and rate limits, 50 requests per 15-minute window shared among all users of your app
    run_volume_streams()
