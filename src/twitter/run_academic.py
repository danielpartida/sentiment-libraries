from datetime import datetime, date
from twitter import TwitterScraper, TwitterSentiment

if __name__ == "__main__":

    search_term = "solana"
    start_time = date(2022, 1, 1)
    end_time = datetime.utcnow()

    twitter_scraper = TwitterScraper(search_term=search_term, tweets_per_window=50, start_time=start_time,
                                     end_time=end_time, access="academic")

    df_tweets = twitter_scraper.get_scrapped_tweets_academic()

    model = "bert"
    # twitter_analysis = TwitterSentiment(search_term=search_term, model=model, df_tweet=df_tweets)
    # twitter_analysis.run_sentiment_analysis()
    # twitter_analysis.run_quantile_analysis()
