import pandas as pd

from transformers import pipeline
from datetime import datetime, date


def calculate_sentiment_analysis(df: pd.DataFrame, token: str) -> pd.DataFrame:
    """
    Calculates sentiment analysis based on RoBERTa architecture cardiffnlp/twitter-roberta-base-sentiment-latest
    other alternative is using BERT: finiteautomata/bertweet-base-sentiment-analysis
    :param df: dataframe of scraped tweets
    :type df: pd.DataFrame
    :param token: asset name
    :type token: str
    :return: dataframe with sentiment analysis
    :rtype: pd.DataFrame
    """
    model = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    sentiment_analysis = pipeline(model=model)
    df['sentiment_dict'] = df["text"].apply(lambda x: sentiment_analysis(x))
    df['sentiment'] = df["sentiment_dict"].apply(lambda x: x[0]['label'])
    df['score'] = df["sentiment_dict"].apply(lambda x: x[0]['score'])
    df.to_csv("../dashboard/data/sentiment_tweets_{0}_{1}.csv".format(token, today.strftime(date_format_short)),
              sep=";", decimal=",")

    return df


def calculate_timeseries_analysis(df: pd.DataFrame, token: str) -> None:
    df["date"] = df.created_at.apply(lambda x: date(x.year, x.month, x.day))

    # group-by
    df.sort_values(by=["date"], ascending=True, inplace=True)

    # group-by and pivot
    model_group_by = df.groupby(by=['date', 'sentiment'])['sentiment'].count()
    model_unstack = model_group_by.unstack()

    model_unstack.to_csv(
        "../dashboard/data/sentiment_timeseries_{0}_sentiment_{1}.csv".format(token, today.strftime(date_format_short)),
        sep=';', decimal=',')


if __name__ == "__main__":
    today = datetime.today()
    date_format_short = '%d_%m'
    asset = "solana"

    data = pd.read_csv("../dashboard/data/tweets_{0}_{1}.csv".format(asset, today.strftime(date_format_short)),
                       sep=';', decimal=',')
    df_sentiment = calculate_sentiment_analysis(df=data, token=asset)
