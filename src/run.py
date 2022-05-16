from datetime import datetime, timedelta
from twitter import TwitterScraper, TwitterSentiment

if __name__ == "__main__":

    search_term = "stepn"
    from_time = datetime.utcnow() - timedelta(days=1)
    until_time = datetime.utcnow() - timedelta(hours=1)
    twitter_scraper = TwitterScraper(search_term=search_term, limit_tweets=1000,
                                     from_time=from_time, until_time=until_time)
    df_tweets = twitter_scraper.get_scraped_tweets()

    model = "roberta"
    twitter_analysis = TwitterSentiment(search_term=search_term, model=model, df_tweet=df_tweets)
    twitter_analysis.run_sentiment_analysis()
    twitter_analysis.run_quantile_analysis()
