import pandas as pd

from textblob import TextBlob

PATH = '../data/crypto.csv'


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


def set_sentiment(df: pd.DataFrame) -> None:
    df['subjectivity'] = df['tweet'].apply(get_subjectivity)
    df['polarity'] = df['tweet'].apply(get_polarity)


def get_analysis(score) -> str:
    if score < -0.25:
        return "negative"
    elif score > 0.25:
        return "positive"
    else:
        return "neutral"

def set_analysis(df: pd.DataFrame) -> None:
    df['analysis'] = df['polarity'].apply(get_analysis)


def run(df: pd.DataFrame) -> None:
    set_sentiment(df)
    set_analysis(df)


if __name__ == "__main__":
    df = pre_process_tweets_df(path=PATH)

    run(df)
    df.to_csv("../data/processed_tweets.csv")

