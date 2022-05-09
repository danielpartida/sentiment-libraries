from twitter import TwitterScraper, TwitterSentiment

if __name__ == "__main__":

    search_term = "olympusdao"
    twitter_scraper = TwitterScraper(search_term=search_term, limit_tweets=1000)
    df_tweets = twitter_scraper.get_scraped_tweets()

    twitter_sentiment_analysis = TwitterSentiment(search_term=search_term, model="roberta", df_tweet=df_tweets)
    twitter_sentiment_analysis.run_sentiment_analysis()
