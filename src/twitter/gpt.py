import os
from datetime import date, datetime

import openai
import pandas as pd
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

openai.api_key = os.getenv("gpt")


def calculate_timeseries_analysis(df: pd.DataFrame, token: str) -> None:
    """
    Calculates timeseries of gpt3 scores
    :param df:
    :type df:
    :param token:
    :type token:
    :return:
    :rtype:
    """
    df["date"] = df.date.apply(lambda x: date(x.year, x.month, x.day))

    # group-by
    df.sort_values(by=["date"], ascending=True, inplace=True)

    # group-by and pivot
    model_group_by = df.groupby(by=['date', 'sentiment'])['sentiment'].count()
    model_unstack = model_group_by.unstack()

    model_unstack.to_csv(
        "../dashboard/data/gpt3_sentiment_timeseries_{0}_sentiment_{1}.csv".format(token,
                                                                                   today.strftime(date_format_short)),
        sep=';', decimal=',')


if __name__ == "__main__":

    asset = "solana"
    today = datetime.today()
    date_format_short = '%d_%m'

    data = pd.read_csv("../dashboard/data/tweets_{0}_{1}.csv".format(asset, today.strftime(date_format_short)),
                       sep=";", decimal=",")
    data["date"] = pd.to_datetime(data.created_at)
    data["date"] = data.date.apply(lambda x: date(x.year, x.month, x.day))
    tweets = data[["date", "text"]]

    begin = "Classify the sentiment in this tweet:\n"
    end = "\n\nTweet sentiment ratings:"

    positive = 0
    negative = 0

    list_df = []
    list_results = []
    for tweet in tqdm(tweets.text):
        long_tweet = begin + "\n{0}{1}".format(1, ". ") + "\"{0}\"".format(tweet) + end

        # Source https://beta.openai.com/examples/default-adv-tweet-classifier
        response = openai.Completion.create(
          model="text-davinci-002",
          prompt=long_tweet,
          temperature=0,
          max_tokens=60,
          top_p=1.0,
          frequency_penalty=0.0,
          presence_penalty=0.0
        )

        result = response["choices"][0]["text"]
        results = result.split("\n\n")

        # TODO: Add other results, e.g. ['Positive', 'Excited', 'Engaged', 'Optimistic']

        if len(results) > 2:
            results = list(map(lambda x: x.split(" ")[1], results[1:]))

        else:
            continue

        # TODO: Store this metrics
        positive += sum('Positive' in s for s in results)
        negative += sum('Negative' in s for s in results)

        list_results.append(results[0])

    series_results = pd.Series(list_results)
    df_final = pd.concat([tweets, pd.DataFrame(series_results)], axis=1)

    df_final.rename(columns={0: "sentiment"}, inplace=True)
    df_final.to_csv("../dashboard/data/gpt3_tweets_{0}_{1}.csv".format(asset, today.strftime(date_format_short)),
                    sep=";", decimal=",", index=False)

    calculate_timeseries_analysis(df=df_final, token=asset)
