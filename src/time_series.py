import pandas as pd
from datetime import datetime

if __name__ == "__main__":

    # FIXME: Change hard-coded import string
    df = pd.read_csv("../data/staratlas_sentiment_06-05-2022-13-46.csv", sep=';', decimal=',')

    df.sort_values(by=['created_at'], ascending=True, inplace=True)
    df['date'] = df['created_at'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S%z'))
    df['date'] = df['date'].apply(lambda x: x.strftime('%d/%m/%Y'))

    # FIXME: Change hard-coded export string
    df.to_csv("../data/staratlas_sentiment_06-05-2022-13-46_sorted.csv", sep=';', decimal=',')
