# Motivation from https://github.com/nicknochnack/BERTSentiment/blob/main/Sentiment.ipynb and
# https://huggingface.co/finiteautomata/bertweet-base-sentiment-analysis?text=I+like+you.+I+love+you
from transformers import pipeline
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch


def sentiment_score(review):
    tokens = tokenizer.encode(review, return_tensors='pt')
    result = model(tokens)
    return int(torch.argmax(result.logits))+1

if __name__ == "__main__":
    tokenizer = AutoTokenizer.from_pretrained('finiteautomata/bertweet-base-sentiment-analysis')
    model = AutoModelForSequenceClassification.from_pretrained('finiteautomata/bertweet-base-sentiment-analysis')

    # TODO: Check other variant to load model
    # sentiment_analysis = pipeline(model="finiteautomata/bertweet-base-sentiment-analysis")

    df_tweets = pd.read_csv('../data/crypto.csv', encoding='latin')
    df_reduced_tweets = df_tweets[:50]

    df_reduced_tweets["result"] = df_reduced_tweets["tweet"].apply(lambda x: sentiment_score(x))

    df_reduced_tweets.to_csv("../data/bert.csv", sep=";", decimal=",")