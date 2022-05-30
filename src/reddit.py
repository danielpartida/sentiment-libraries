from datetime import datetime, date

import pandas as pd
from psaw import PushshiftAPI
from tqdm import tqdm
from transformers import pipeline


def get_generator(start_epoch=int(datetime(2022, 5, 1).timestamp()),
                  search_term: str = "stepn", subreddit: str = "stepn"):
    api = PushshiftAPI()

    start_epoch = start_epoch
    search_term = search_term
    generator = api.search_comments(q=search_term, after=start_epoch, subreddit=subreddit, limit=10000)

    return generator


def get_dataframe_reddit_comments(generator) -> pd.DataFrame:
    list_dict_comments = []
    for comment in tqdm(generator):
        dict_comment = {
            "author": comment.author,
            "text": comment.body,
            # FIXME: handle missing controversiality
            # "controversiality": comment.controversiality,
            "created": datetime.fromtimestamp(comment.created),
            "link_id": comment.link_id,
            "permalink": comment.permalink,
            "score": comment.score
        }

        list_dict_comments.append(dict_comment)

    df_reddit_comments = pd.DataFrame(list_dict_comments)

    return df_reddit_comments


def compute_sentiment_analysis(df: pd.DataFrame, model: str) -> pd.DataFrame:
    sentiment_analysis = pipeline(model=model_hugging_face)
    df['sentiment_dict'] = df["text"].apply(lambda x: sentiment_analysis(x[:512]))
    df['sentiment_{0}'.format(model)] = df["sentiment_dict"].apply(
        lambda x: x[0]['label'])

    df.to_csv("../data/reddit/{0}_reddit_{1}.csv".format(reddit_search_term, today_string),
              sep=";", decimal=',')

    return df


def calculate_timeseries_analysis(df: pd.DataFrame, model: str) -> None:
    df["date"] = df.created.apply(lambda x: date(x.year, x.month, x.day))

    # group-by
    df.sort_values(by=["date"], ascending=True, inplace=True)

    # group-by and pivot
    model_group_by = df.groupby(by=['date', 'sentiment_{0}'.format(model)])[
        'sentiment_{0}'.format(model)
    ].count()
    model_unstack = model_group_by.unstack()

    df_pivot = pd.DataFrame(model_unstack)
    df_pivot["sum"] = model_unstack.sum(axis=1)
    df_pivot_rel = df_pivot[['Positive', 'Negative', 'Neutral']].div(df_pivot["sum"], axis=0)
    df_pivot_rel["total_posts"] = df_pivot["sum"]

    df_pivot_rel.to_csv("../data/reddit/{0}_reddit_timeseries_{1}_{2}.csv".format(
        reddit_search_term, model, today_string), sep=";", decimal=',')


if __name__ == "__main__":
    today = datetime.today()
    today_string = today.strftime('%d-%m-%Y-%H-%M')

    reddit_search_term = "stepn"
    reddit_generator = get_generator(start_epoch=int(datetime(2022, 5, 27).timestamp()),
                                     search_term=reddit_search_term, subreddit="stepn")

    df_reddit = get_dataframe_reddit_comments(generator=reddit_generator)

    model_hugging_face = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    model_str = "roberta"

    df_sentiment = compute_sentiment_analysis(df=df_reddit, model=model_str)
    calculate_timeseries_analysis(df=df_sentiment, model=model_str)
