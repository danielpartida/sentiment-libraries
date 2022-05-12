from twitter import TwitterScraper, TwitterSentiment

if __name__ == "__main__":

    search_term = "stablekwon"
    twitter_scraper = TwitterScraper(search_term=search_term, limit_tweets=1500,
                                     is_reply=(True, '1524331171189956609'))
    df_tweets = twitter_scraper.get_scraped_tweets(is_reply=(True, '1524331171189956609'))

    model = "roberta"
    twitter_analysis = TwitterSentiment(search_term=search_term, model=model, df_tweet=df_tweets)
    twitter_analysis.run_sentiment_analysis()
    twitter_analysis.run_quantile_analysis()
