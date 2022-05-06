import os

from transformers import pipeline
from tqdm import tqdm
import numpy as np
import pandas as pd

from twitter_sentiment_analysis import get_type_of_model, save_word_cloud, save_pie_chart


def get_full_discord_df() -> pd.DataFrame:
    """
    Reads csv file from data/discord folder
    :return: data in dataframe format
    :rtype: pd.DataFrame
    """
    # Read all excel files
    path = os.getcwd()
    # Remove src from the path
    path = path[:-3]
    files = os.listdir(path + "/data/discord")
    files_xls = [f for f in files if f[-4:] == 'xlsx']

    df = pd.DataFrame()
    for file in tqdm(files_xls):
        print("Processing file: ", file)
        data = pd.read_excel("../data/discord/{0}".format(file), 'chatlog')
        # fetch name of the xlsx file
        data["channel"] = file[:-5]
        df = df.append(data)

    df.Content.dropna(inplace=True)

    return df


def run_sentiment(df_discord: pd.DataFrame, sentiment_model: str) -> pd.DataFrame:
    """
    Performs sentiment analysis depending on the model
    :param df_discord:
    :type df_discord:
    :param sentiment_model:
    :type sentiment_model:
    :return:
    :rtype:
    """
    sentiment_analysis = pipeline(model=sentiment_model)

    type_model = get_type_of_model(sentiment_model=sentiment_model)

    df_discord['sentiment_dict'] = df_discord["Content"].apply(lambda x: sentiment_analysis(x))
    df_discord['sentiment_{0}'.format(type_model)] = df_discord["sentiment_dict"].apply(lambda x: x[0]['label'])
    if type_model == "bert":
        df_discord['sentiment_{0}'.format(type_model)] = df_discord['sentiment_{0}'.format(type_model)].apply(
            lambda x: x.replace("POS", "Positive"))
        df_discord['sentiment_{0}'.format(type_model)] = df_discord['sentiment_{0}'.format(type_model)].apply(
            lambda x: x.replace("NEG", "Negative"))
        df_discord['sentiment_{0}'.format(type_model)] = df_discord['sentiment_{0}'.format(type_model)].apply(
            lambda x: x.replace("NEU", "Neutral"))
    df_discord['score_{0}'.format(type_model)] = df_discord["sentiment_dict"].apply(lambda x: x[0]['score'])

    df_discord.drop(['sentiment_dict'], axis=1, inplace=True)

    return df_discord


# TODO: Create a single analysis class to handle sentiment analysis of Twitter and Discord data
if __name__ == "__main__":

    # Fetch whole dataframe
    df_read = get_full_discord_df()

    # Handle numpy NaN values
    df_clean = df_read.loc[~df_read.Content.replace(0, np.nan).isna()]

    # TODO: Run for both NLP models
    model = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    df_results = run_sentiment(df_discord=df_read, sentiment_model=model)
    print("Done")
