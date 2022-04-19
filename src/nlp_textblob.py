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







def run() -> None:
    pass


if __name__ == "__main__":
    df = pre_process_tweets_df(path=PATH)

    run()
