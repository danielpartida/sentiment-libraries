import pandas as pd
from datetime import datetime

# FIXME: Remove duplicated file with Discord timeseries
# TODO: Create a class that handles both situations
if __name__ == "__main__":

    # TODO: Change hard-coded import string
    df = pd.read_csv("../data/results/staratlas/discord_staratlas_sentiment_07-05-2022-18-31.csv", sep=';', decimal=',')

    list_dates = df.Date.str.split()
    list_days = [item[0] for item in list_dates]
    df["short_date"] = list_days
    df.short_date = df.short_date.apply(lambda x: datetime.strptime(x, '%d/%m/%Y'))

    # TODO: sort_values
    # df.sort_values(by=['short_date'], ascending=True, inplace=True)

    # group-by
    roberta = df.groupby(by=['short_date', 'sentiment_roberta'])['sentiment_roberta'].count()

    # pivot (unstack)
    roberta_unstack = roberta.unstack()

    # TODO: Change hard-coded export string
    roberta_unstack.to_csv("../data/staratlas/timeseries_roberta_sentiment_07-05-2022-18-31.csv",
                           sep=';', decimal=',')
