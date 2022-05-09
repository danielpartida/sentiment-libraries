from twitter_scraper import TwitterScraper

if __name__ == "__main__":

    search_term = "olympusdao"
    tweet_scraper = TwitterScraper(search_term=search_term, limit_tweets=100, tweet_type="mixed")
    df_tweets = tweet_scraper.get_scraped_tweets()
    df_tweets.head()
