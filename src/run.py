from twitter import TwitterScraper, TwitterSentiment

if __name__ == "__main__":

    search_term = "luna"
    twitter_scraper = TwitterScraper(search_term=search_term, limit_tweets=5000)
    df_tweets = twitter_scraper.get_scraped_tweets()

    model = "roberta"
    twitter_analysis = TwitterSentiment(search_term=search_term, model=model, df_tweet=df_tweets)
    twitter_analysis.run_sentiment_analysis()
    twitter_analysis.run_quantile_analysis()
