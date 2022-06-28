import os
import openai
import pandas as pd
from datetime import date

from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("gpt")

if __name__ == "__main__":

    # result = '\n\n1. Positive\n2. Negative\n3. Positive\n4. Positive\n5. Positive\n6. Positive\n7. Negative\n8. Positive\n9. Positive\n10. Positive\n11. Positive\n12. Positive\n13. Positive\n14. Positive\n15.'

    data = pd.read_csv("../dashboard/data/tweets_solana_28_06.csv", sep=";", decimal=",")
    data["date"] = pd.to_datetime(data.created_at)
    data["date"] = data.date.apply(lambda x: date(x.year, x.month, x.day))
    tweets = data[["date", "text"]]

    begin = "Classify the sentiment in these tweets:\n"
    end = "\n\nTweet sentiment ratings:"

    long_tweet = begin
    counter = 1
    for tweet in tweets[60:75]:
        long_tweet += "\n{0}{1}".format(str(counter), ". ") + "\"{0}\"".format(tweet)
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
    positive = sum('Positive' in s for s in results)
    negative = sum('Negative' in s for s in results)

