import os
import openai

from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("gpt")

if __name__ == "__main__":

    tweets = ["I can't stand homework", "This sucks. I'm bored 😠", "I can\'t wait for Halloween!!!",
              "My cat is adorable ❤️❤️", "I hate chocolate"]
    begin = "Classify the sentiment in these tweets:\n"
    end = "\n\nTweet sentiment ratings:"

    long_tweet = begin
    counter = 1
    for tweet in tweets:
        long_tweet += "\n{0}{1}".format(str(counter), ". ") + "\"{0}\"".format(tweet)
        counter += 1

    long_tweet += end

    prompt = "Classify the sentiment in these tweets:\n\n1. \"I can't stand homework\"\n2. \"This sucks. I'm bored 😠\"\n3. \"I can't wait for Halloween!!!\"\n4. \"My cat is adorable ❤️❤️\"\n5. \"I hate chocolate\"\n\nTweet sentiment ratings:"
    response = openai.Completion.create(
      model="text-davinci-002",
      prompt=long_tweet,
      temperature=0,
      max_tokens=60,
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=0.0
    )

    print(response)
