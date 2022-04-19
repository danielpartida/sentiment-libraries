# Source: https://thinkingneuron.com/sentiment-analysis-of-tweets-using-bert/
import pandas as pd
from transformers import pipeline


def get_bert_sentiment(input_text: str):
    return SentimentClassifier(input_text)[0]['label']


def set_bert_sentiment(df) -> None:
    df['Sentiment'] = df['Tweets'].apply(get_bert_sentiment)


if __name__ == "__main__":
    # Reading the indigo tweets data
    df_tweets = pd.read_csv('../data/indigo_tweets.csv', encoding='latin')

    SentimentClassifier = pipeline("sentiment-analysis")

    set_bert_sentiment(df_tweets)
    df_tweets.head(10)