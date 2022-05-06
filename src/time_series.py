import pandas as pd
from datetime import datetime

if __name__ == "__main__":

    df = pd.read_csv("../data/staratlas_sentiment_06-05-2022-13-46.csv", sep=';', decimal=',')

    print(df.head())
    df['date'] = df['created_at'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S%z'))
    df['date'] = df['date'].apply(lambda x: x.strftime('%d/%m/%Y'))
    print('Done')
