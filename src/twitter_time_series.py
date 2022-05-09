import pandas as pd
from datetime import datetime

# FIXME: Remove duplicated file with Discord timeseries
# TODO: Create a class that handles both situations
if __name__ == "__main__":

    # TODO: Change hard-coded import string
    df = pd.read_csv("../data/staratlas_results/twitter_staratlas_sentiment_06-05-2022-13-46.csv", sep=';', decimal=',')

    list_dates = df.created_at.str.split()
    list_days = [item[0] for item in list_dates]
    df["date"] = list_days
    df.date = df.date.apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))

    # sort values
    df.sort_values(by=["date"], ascending=True, inplace=True)

    # group-by
    bert = df.groupby(by=['date', 'sentiment_bert'])['sentiment_bert'].count()
    roberta = df.groupby(by=['date', 'sentiment_roberta'])['sentiment_roberta'].count()

    # pivot (unstack)
    bert_unstack = bert.unstack()
    roberta_unstack = roberta.unstack()

    # TODO: Change hard-coded export string and timestamp
    time_stamp = "06-05-2022-13-46"
    bert_unstack.to_csv("../data/{1}_results/{0}_timeseries_{1}_sentiment_{2}_bert.csv".format("twitter", "staratlas", time_stamp),
                        sep=';', decimal=',')
    roberta_unstack.to_csv("../data/{1}_results/{0}_timeseries_{1}_sentiment_{2}_roberta.csv".format("twitter", "staratlas", time_stamp),
                           sep=';', decimal=',')
