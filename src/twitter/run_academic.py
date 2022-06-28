from datetime import datetime, date
from twitter import TwitterAcademic, TwitterSentiment

if __name__ == "__main__":

    search_term = "solana"
    start_time = datetime.combine(date(2022, 1, 1), datetime.min.time())
    end_time = datetime.utcnow()

    twitter_scraper = TwitterAcademic(search_term=search_term, tweets_per_window=500, start_time=start_time,
                                      end_time=end_time)

    df_tweets = twitter_scraper.get_scraped_tweets_academic()

    # FIXME: Check error of bert IndexError: index out of range in self,
    #  self.df_tweets['sentiment_dict'] = self.df_tweets["text"].apply(lambda x: self.sentiment_analysis(x))
    model = "roberta"
    twitter_analysis = TwitterSentiment(search_term=search_term, model=model, df_tweet=df_tweets)
    twitter_analysis.run_sentiment_analysis()
    twitter_analysis.run_quantile_analysis()
