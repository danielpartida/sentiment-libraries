# Motivation from https://github.com/nicknochnack/BERTSentiment/blob/main/Sentiment.ipynb and
# Bert: https://huggingface.co/finiteautomata/bertweet-base-sentiment-analysis
# Roberta: https://huggingface.co/cardiffnlp/twitter-roberta-base
from transformers_runs import pipeline
import pandas as pd
from transformers_runs import AutoTokenizer, AutoModelForSequenceClassification, RobertaForSequenceClassification
import torch
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS


def sentiment_score(review):
    tokens = tokenizer.encode(review, return_tensors='pt')
    result = model(tokens)
    return int(torch.argmax(result.logits)) + 1


def visualize_pie_chart(df: pd.DataFrame):
    # Let's count the number of tweets by sentiments
    sentiment_counts = df.groupby(['result']).size()
    print(sentiment_counts)

    # Let's visualize the sentiments
    fig = plt.figure(figsize=(6, 6), dpi=100)
    ax = plt.subplot(111)
    sentiment_counts.plot.pie(ax=ax, autopct='%1.1f%%', startangle=270, fontsize=12, label="")


def visualize_word_cloud(df: pd.DataFrame):
    positive_tweets = df['tweet'][df["result"] == 2]
    positive_wordcloud = WordCloud(max_font_size=50, max_words=100,
                                   background_color="white").generate(str(positive_tweets))
    plt.figure()
    plt.title("Positive Tweets - Wordcloud")
    plt.imshow(positive_wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()

    # Wordcloud with negative tweets
    negative_tweets = df['tweet'][df["result"] == 0]
    stop_words = ["https", "co", "RT"] + list(STOPWORDS)
    negative_wordcloud = WordCloud(max_font_size=50, max_words=100,
                                   background_color="white").generate(str(negative_tweets))
    plt.figure()
    plt.title("Negative Tweets - Wordcloud")
    plt.imshow(negative_wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()

    # Wordcloud with neutral tweets
    negative_tweets = df['tweet'][df["result"] == 1]
    stop_words = ["https", "co", "RT"] + list(STOPWORDS)
    negative_wordcloud = WordCloud(max_font_size=50, max_words=100,
                                   background_color="white").generate(str(negative_tweets))
    plt.figure()
    plt.title("Neutral Tweets - Wordcloud")
    plt.imshow(negative_wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()


def load_model(model_to_load):
    tokenizer_hugging = AutoTokenizer.from_pretrained(model_to_load)

    if model_to_load == "finiteautomata/bertweet-base-sentiment-analysis":
        model_hugging = AutoModelForSequenceClassification(model_to_load)

    elif model_to_load == "cardiffnlp/twitter-roberta-base-sentiment":
        model_hugging = RobertaForSequenceClassification.from_pretrained(model_to_load)

    else:
        raise ValueError("No architecture is provided")

    return tokenizer_hugging, model_hugging


if __name__ == "__main__":
    hugging_model = "cardiffnlp/twitter-roberta-base-sentiment"
    tokenizer, model = load_model(hugging_model)

    # TODO: Check other variant to load model
    # sentiment_analysis = pipeline(model="finiteautomata/bertweet-base-sentiment-analysis")

    df_tweets = pd.read_csv('../data/crypto.csv', encoding='latin')
    # FIXME: See what error arises when we run with full dataframe
    df_reduced_tweets = df_tweets[:50]

    df_reduced_tweets["result"] = df_reduced_tweets["tweet"].apply(lambda x: sentiment_score(x))

    # TODO: Specify model to save (either bert or roberta)
    df_reduced_tweets.to_csv("../data/roberta_results.csv", sep=";", decimal=",")

    visualize_pie_chart(df_reduced_tweets)
    visualize_word_cloud(df_reduced_tweets)
