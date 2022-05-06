import os

from matplotlib import pyplot as plt
from transformers import pipeline
from tqdm import tqdm
import pandas as pd
from datetime import datetime
from wordcloud import WordCloud, STOPWORDS

from twitter_sentiment_analysis import get_type_of_model, clean_tweet


def handle_content(statement: str) -> str:
    if (statement is None) or (type(statement) == float):
        return ""

    elif len(statement) == 0:
        return ""

    else:
        return statement


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


def save_pie_chart(df_tweets: pd.DataFrame, sentiment_model: str, search_term: str) -> None:
    """

    :param search_term:
    :type search_term:
    :param df_tweets:
    :type df_tweets:
    :param sentiment_model:
    :type sentiment_model:
    :return:
    :rtype:
    """
    type_model = get_type_of_model(sentiment_model=sentiment_model)

    # Let's count the number of tweets by sentiments
    sentiment_counts = df_tweets.groupby(['sentiment_{0}'.format(type_model)]).size()

    # Let's visualize the sentiments
    fig = plt.figure(figsize=(6, 6), dpi=100)
    ax = plt.subplot(111)
    sentiment_counts.plot.pie(ax=ax, autopct='%1.1f%%', startangle=270, fontsize=12, label="")
    plt.title("Pie-chart Sentiment Analysis- {0} Model".format(type_model))
    plt.savefig('../img/{0}_pie_chart_sentiment_{1}_{2}.png'.format(search_term, type_model, today_string))


def save_word_cloud(df_tweet: pd.DataFrame, sentiment_model: str, search_term: str) -> None:
    """

    :param search_term:
    :type search_term:
    :param df_tweet:
    :type df_tweet:
    :param sentiment_model:
    :type sentiment_model:
    :return:
    :rtype:
    """
    type_model = get_type_of_model(sentiment_model=sentiment_model)

    sentiment_types = ["Positive", "Negative", "Neutral"]
    stop_words = set(["https", "co", "RT"] + list(STOPWORDS))
    for sentiment in sentiment_types:
        sentiment_tweets = df_tweet['Content'][df_tweet['sentiment_{0}'.format(type_model)] == sentiment]
        sentiment_wordcloud = WordCloud(max_font_size=50, max_words=100,
                                        background_color="white", stopwords=stop_words).generate(str(sentiment_tweets))
        plt.figure()
        plt.title("Wordcloud {0} Tweets - {1} Model".format(sentiment, type_model))
        plt.imshow(sentiment_wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.savefig('../img/{0}_wordcloud_{1}_sentiment_{2}_{3}.png'.format(
            search_term, sentiment, type_model, today_string)
        )


# TODO: Create a single analysis class to handle sentiment analysis of Twitter and Discord data
if __name__ == "__main__":

    today = datetime.today()
    today_string = today.strftime('%d-%m-%Y-%H-%M')

    # Fetch whole dataframe
    df_read = get_full_discord_df()

    # Handle numpy NaN values
    df_read.Content = df_read.Content.apply(lambda x: str(x))
    df_read.Content = df_read.Content.apply(lambda x: clean_tweet(x))
    df_read["Content"] = df_read.Content.apply(handle_content)

    models = ["cardiffnlp/twitter-roberta-base-sentiment-latest", "finiteautomata/bertweet-base-sentiment-analysis"]
    for model in tqdm(models):
        df_results = run_sentiment(df_discord=df_read, sentiment_model=model)
        save_pie_chart(search_term="discord", df_tweets=df_results, sentiment_model=model)
        save_word_cloud(search_term="discord", df_tweet=df_results, sentiment_model=model)

    df_results.to_csv('../data/{0}_sentiment_{1}.csv'.format("discord", today_string), sep=';')
