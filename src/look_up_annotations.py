from unicodedata import decimal
import pandas as pd
import json

if __name__ == "__main__":

    data = pd.read_csv("../data/backup/crypto_context_tweets_09_06_17_05.csv", sep=';', decimal=',')
    context_annotations = data.context_annotations
    series_annotations = context_annotations.apply(lambda x: eval(x)) # convert str to list
    print(series_annotations)
