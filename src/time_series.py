import pandas as pd
from datetime import datetime

if __name__ == "__main__":

    # TODO: Change hard-coded import string
    df = pd.read_csv("../data/staratlas_sentiment_06-05-2022-13-46.csv", sep=';', decimal=',')

    df.sort_values(by=['created_at'], ascending=True, inplace=True)
    df['date'] = df['created_at'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S%z'))
    df['date'] = df['date'].apply(lambda x: x.strftime('%d/%m/%Y'))

    # group-by
    bert = df.groupby(by=['date', 'sentiment_bert'])['sentiment_bert'].count()
    roberta = df.groupby(by=['date', 'sentiment_roberta'])['sentiment_roberta'].count()

    # pivot (unstack)
    bert_unstack = bert.unstack()
    roberta_unstack = roberta.unstack()

    # TODO: Change hard-coded export string
    # FIXME: Order series correctly by dates ascending
    bert_unstack.to_csv("../data/staratlas_sentiment_06-05-2022-13-46_bert.csv", sep=';', decimal=',')
    roberta_unstack.to_csv("../data/staratlas_sentiment_06-05-2022-13-46_roberta.csv", sep=';', decimal=',')
