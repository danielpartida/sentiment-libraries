# Source: https://thinkingneuron.com/sentiment-analysis-of-tweets-using-bert/
import pandas as pd
from transformers import pipeline


def get_bert_sentiment(input_text: str):
    return SentimentClassifier(input_text)[0]['label']


def set_bert_sentiment(df_arg) -> None:
    df_tweets['sentiment'] = df_arg['tweet'].apply(get_bert_sentiment)


if __name__ == "__main__":
    # Reading the indigo tweets data
    df_tweets = pd.read_csv('../archive_data/crypto.csv', encoding='latin')

    SentimentClassifier = pipeline("sentiment-analysis")

    set_bert_sentiment(df_tweets[:100])
    print(df_tweets[["tweet", "sentiment"]][:25])