import datetime as dt

from psaw import PushshiftAPI

api = PushshiftAPI()

start_epoch=int(dt.datetime(2022, 5, 1).timestamp())

gen = api.search_comments(q="stepn", after=start_epoch, subreddit='StepN', limit=10)

for comment in gen:
    print(comment.body)