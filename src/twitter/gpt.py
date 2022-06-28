import os
import openai
import pandas as pd
from datetime import date, datetime
from tqdm import tqdm

from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("gpt")

if __name__ == "__main__":

    asset = "solana"
    today = datetime.today()
    date_format_short = '%d_%m'

    data = pd.read_csv("../dashboard/data/tweets_{0}_{1}.csv".format(asset, today.strftime(date_format_short)),
                       sep=";", decimal=",")
    data["date"] = pd.to_datetime(data.created_at)
    data["date"] = data.date.apply(lambda x: date(x.year, x.month, x.day))
    tweets = data[["date", "text"]]

    begin = "Classify the sentiment in these tweets:\n"
    end = "\n\nTweet sentiment ratings:"

    long_tweet = begin
    counter = 1
    positive = 0
    negative = 0

    list_df = []
    for i in tqdm(range(0, len(tweets)-2, 2)):
        df_tweets = tweets.text[i:i + 2]
        df_tweets.reset_index(drop=True, inplace=True)
        for tweet in df_tweets:
            long_tweet += "\n{0}{1}".format(str(counter), ". ") + "\"{0}\"".format(tweet, counter)
            counter += 1

        long_tweet += end

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
        results = result.split("\n")
        results = list(map(lambda x: x.split(" ")[1], results[2:]))

        positive += sum('Positive' in s for s in results)
        negative += sum('Negative' in s for s in results)

        results = pd.Series(results)
        df = pd.DataFrame(dict(s1=df_tweets, s2=results)).reset_index()[["s1", "s2"]]
        list_df.append(df)

    df_final = pd.concat(list_df)
    df_final.to_csv("../dashboard/data/gpt3_tweets_{0}_{1}.csv".format(asset, today.strftime(date_format_short)),
                    sep=";", decimal=",")

