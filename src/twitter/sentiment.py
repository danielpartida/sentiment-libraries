import pandas as pd


def calculate_sentiment_analysis(df: pd.DataFrame) -> None:
    """
    Performs sentiment analysis depending on the model
    """
    df['sentiment_dict'] = df["text"].apply(lambda x: sentiment_analysis(x))
    df['sentiment_{0}'.format(model_str)] = df["sentiment_dict"].apply(lambda x: x[0]['label'])
    df['score_{0}'.format(model_str)] = df["sentiment_dict"].apply(lambda x: x[0]['score'])


if __name__ == "__main__":

    print("Run")
