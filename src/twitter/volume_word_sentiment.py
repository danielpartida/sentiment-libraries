from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import pandas as pd
from transformers import pipeline
from wordcloud import WordCloud, STOPWORDS

from src.db.entities import TwitterStreams
from src.db.helper import get_session


def query_last_streams(time_delta: datetime) -> list:
    """
    Fetches last tweets using sqlalchemy ORM
    :param time_delta: time_delta e.g. datetime.now() - timedelta(hours=12)
    :type time_delta: datetime
    :return: last twitter streams
    :rtype: list of TwitterStreams
    """
    last_streams = session.query(TwitterStreams).filter(
        TwitterStreams.domain_id == 66, TwitterStreams.date >= time_delta
    ).order_by(TwitterStreams.id.asc()).all()

    return last_streams


def compute_sentiment(tweet_object: list, model_type: str) -> pd.DataFrame:

    tweets = list(map(lambda x: x.text, tweet_object))

    sentiment_analysis = pipeline(model=model_type)
    sentiment_dict = list(map(lambda x: sentiment_analysis(x), tweets))

    df_tweets = pd.DataFrame(sentiment_dict, columns=["sentiment_dict"])
    df_tweets['sentiment'] = df_tweets["sentiment_dict"].apply(lambda x: x['label'])
    df_tweets['score'] = df_tweets["sentiment_dict"].apply(lambda x: x['score'])

    return df_tweets


# TODO: Add sentiment word_clouds
def compute_word_cloud(tweet_object: list) -> None:
    """
    Computes and saves word_cloud
    :param tweet_object: last tweets as sqlalchemy ORM object
    :type tweet_object: list of TwitterStreams
    :return: None
    :rtype: None
    """
    stop_words = set(["https", "co", "RT", "dtype", "t", "X", "x", "giveaway", "GIVEAWAY", "tag", "follow", "Follow",
                      "friend", "friends", "airdrop", "FOLLOW", "AIRDROP"] + list(STOPWORDS))

    # sentiment_types = ["Positive", "Negative", "Neutral"]
    # color_maps = {"Positive": "YlGn", "Negative": "OrRd", "Neutral": "PuRd"}

    tweets = list(map(lambda x: x.text, tweet_object))

    world_cloud = WordCloud(max_font_size=50, max_words=100,  # colormap=color_maps[sentiment],
                            background_color="white", stopwords=stop_words).generate(str(tweets))

    plt.figure()
    plt.title("Twitter Wordcloud - {0}".format(now))
    plt.imshow(world_cloud, interpolation="bilinear")
    plt.axis("off")

    plt.savefig('../../img/volume_streams/wordcloud_{0}'.format(now_string))


def compute_pie_chart(df_sentiment_tweets: pd.DataFrame) -> None:

    df_group = df_sentiment_tweets.groupby(["sentiment"]).size()
    plot = df_group.plot.pie(label="", title="Sentiment")
    fig = plot.get_figure()
    fig.savefig('../../img/volume_streams/pie_chart_{0}'.format(now_string))


if __name__ == "__main__":

    session = get_session()

    now = datetime.now()
    now = datetime(now.year, now.month, now.day, now.hour, now.minute, now.second)
    now_string = now.strftime("%m_%d_%H_%M")
    delta = now - timedelta(hours=12)

    # FIXME: Delete retweets
    last_tweets = query_last_streams(time_delta=delta)

    model_option = {"bert": "finiteautomata/bertweet-base-sentiment-analysis",
                    "roberta": "cardiffnlp/twitter-roberta-base-sentiment-latest"}
    sentiment_tweets = compute_sentiment(tweet_object=last_tweets, model_type=model_option["bert"])

    compute_word_cloud(tweet_object=last_tweets)
    compute_pie_chart(df_sentiment_tweets=sentiment_tweets)

    session.close()

    print("Run done")
