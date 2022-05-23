import datetime as dt

import pandas as pd
from psaw import PushshiftAPI
from tqdm import tqdm

api = PushshiftAPI()

start_epoch = int(dt.datetime(2022, 5, 1).timestamp())

search_term = "stepn"

# FIXME: Change hardcoded subreddit
gen = api.search_comments(q=search_term, after=start_epoch, subreddit='StepN', limit=10000)

list_dict_comments = []
for comment in tqdm(gen):
    dict_comment = {
        "author": comment.author,
        "body": comment.body,
        "controversiality": comment.controversiality,
        "created": dt.datetime.fromtimestamp(comment.created),
        "link_id": comment.link_id,
        "permalink": comment.permalink
    }

    list_dict_comments.append(dict_comment)

df_reddit = pd.DataFrame(list_dict_comments)
df_reddit.to_csv("../../data/reddit/{0}_reddit.csv".format(search_term),
                 sep=";", decimal=',')
