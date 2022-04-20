import datetime
import twint

config = twint.Config()


def scrap_twitter_data(term: str, since: datetime, until: datetime):
    config.Search = term
    config.Lang = "en"

    config.Since = str(since)
    config.Until = str(until)
    config.Output = "../data/nfts.csv"
    config.Limit = 100

    twint.run.Search(config)


if __name__ == "__main__":
    search_term = "NFTs"
    since_date = datetime.datetime(2021, 4, 1)
    until_date = datetime.datetime(2022, 4, 1)
    scrap_twitter_data(search_term, since_date, until_date)
