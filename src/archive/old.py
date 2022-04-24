import pandas as pd

from transformers import pipeline
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

PATH = '../../data/crypto.csv'


def pre_process_tweets_df(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    # Filter columns that are relevant
    df = df[['id', 'date', 'time', 'username', 'language', 'tweet']]
    # Filter only english content
    df = df[df['language'] == 'en']

    return df


def get_subjectivity(text: str) -> float:
    return TextBlob(text).sentiment.subjectivity


def get_polarity(text: str) -> float:
    return TextBlob(text).sentiment.polarity


def get_bert_sentiment(input_text: str):
    return SentimentClassifier(input_text)[0]['label']


def set_sentiment(df: pd.DataFrame) -> None:
    df['subjectivity'] = df['tweet'].apply(get_subjectivity)
    df['polarity'] = df['tweet'].apply(get_polarity)
    df['vs_dict'] = df['tweet'].apply(analyzer.polarity_scores)
    # df['bert'] = df['tweet'].apply(get_bert_sentiment)


def get_analysis(score, neutral_interval=0.15) -> str:
    if score < -neutral_interval:
        return "negative"
    elif score > neutral_interval:
        return "positive"
    else:
        return "neutral"


def set_analysis(df: pd.DataFrame) -> None:
    df['analysis'] = df['polarity'].apply(get_analysis)


def run(df: pd.DataFrame) -> None:
    set_sentiment(df)
    set_analysis(df)
    save_pie_chart(df, "pie")


def save_pie_chart(df: pd.DataFrame, type_of_plot: str) -> None:

    series_count_occurrences = df['analysis'].value_counts()

    if type_of_plot == 'pie':
        plot = series_count_occurrences.plot.pie(figsize=(10, 5))
        plot.figure.savefig("../img/pie_chart.png")
    else:
        raise "Please specify a type of plot"


if __name__ == "__main__":
    # vader analyzer
    analyzer = SentimentIntensityAnalyzer()
    # DistilBERT
    SentimentClassifier = pipeline("sentiment-analysis")

    # FIXME: Change dataframe argument for all methods to df_arg
    df = pre_process_tweets_df(path=PATH)

    run(df)
    df.to_csv("../data/processed_tweets.csv", sep=";", decimal=",")

