import pandas as pd
import pandas_datareader.data as web
import yaml
import requests
from datetime import datetime, date


def get_config():
    """
    Returns config file
    :return: config file
    :rtype: config
    """
    with open("config.yml", "r") as config:
        config = yaml.load(config, yaml.FullLoader)

    return config


def get_price_from_yahoo(token: str = "SOL-USD", start: str = '01/01/2022',
                         end: str = datetime.today().strftime('%d/%m/%Y')) -> pd.DataFrame:
    """
    Gets price data from yahoo finance OHLC and volume
    :param date_format: date format '%d/%m/%Y'
    :type date_format: str
    :param token: asset name
    :type token: str
    :param start: format '01/01/2022'
    :type start:  str
    :param end: format '01/01/2022'
    :type end: str
    :return: dataframe containing open, low, close, volume, adj close
    :rtype: pd.DataFrame
    """
    data = web.DataReader(token, data_source="yahoo", start=start, end=end)

    return data


def get_current_price_from_coingecko(token: str = "solana", include_market_cap: bool = True,
                                     include_24_vol:bool = False, include_24_change: bool = True,
                                     include_last_update: bool = True, date_format: str = '%d/%m/%Y %H:%M'):
    """
    Gets simple price from CoinGecko
    :param date_format: date format '%d/%m/%Y %H:%M'
    :type date_format: str
    :param token: "solana"
    :type token: str
    :param include_market_cap: to include last market cap
    :type include_market_cap: bool
    :param include_24_vol: to include 24h volume
    :type include_24_vol: bool
    :param include_24_change: to include change of price in last 24h
    :type include_24_change: bool
    :param include_last_update: to include the epoch of last update
    :type include_last_update: bool
    :return: dictionary containing price, volume, daily return and last update
    :rtype: dict
    """

    price_url = "simple/price?ids={0}&vs_currencies=usd".format(token)

    market_cap = "include_market_cap=true" if include_market_cap else "include_market_cap=false"
    volume = "include_24hr_vol=true" if include_24_vol else "include_24hr_vol=false"
    change = "include_24hr_change=true" if include_24_change else "include_24hr_change=false"
    update = "include_last_updated_at=true" if include_last_update else "include_last_updated_at=false"

    config = get_config()
    base_url = config["base_coingecko_url"]
    complete_url = base_url + price_url + "&" + market_cap + "&" + volume + "&" + change + "&" + update

    full_data = requests.get(complete_url).json()
    data = full_data[token]

    epoch = data["last_updated_at"]
    last_update_time = datetime.fromtimestamp(epoch)
    data["last_updated_at"] = last_update_time.strftime(date_format)

    price_before = data["usd"] - data['usd_24h_change']
    daily_returns = (data["usd"] - price_before) / price_before
    data["daily_return"] = daily_returns

    return data


def get_historical_price_from_coingecko(token: str) -> pd.DataFrame:
    """
    Fetches historical prices for a particular token
    :param token: token_id from CoinGecko, e.g. solana
    :type token: str
    :return: timeseries of day and token price
    :rtype: pd.DataFrame
    """

    start_year = date(2022, 1, 1)
    end_year = date.today()
    delta = end_year - start_year
    delta = delta.days

    config = get_config()
    base_url = config["base_coingecko_url"]
    complete_url = base_url + "coins/{0}/market_chart?vs_currency=usd&days={1}&interval=daily".format(token, delta+1)

    full_data = requests.get(complete_url).json()
    data = full_data["prices"]

    dates = list(map(lambda x: x[0], data))
    dates = list(map(lambda x: datetime.fromtimestamp(x / 1000), dates))

    prices = list(map(lambda x: x[1], data))
    df_data = pd.DataFrame(prices, columns=["price"], index=dates)
    df_data.reset_index(level=0, inplace=True)
    df_data.rename(columns={"index": "date"}, inplace=True)

    return df_data


if __name__ == '__main__':
    start_date = '01/01/2022'
    today = datetime.today()
    date_format_short = '%d/%m/%Y'
    date_format_long = '%d/%m/%Y %H:%M'

    end_date = today.strftime(date_format_short)
    yahoo_price = get_price_from_yahoo(token="SOL-USD", start=start_date, end=end_date)

    token_id_coingecko = "solana"
    coingecko_current_price = get_current_price_from_coingecko(token=token_id_coingecko, date_format=date_format_long)
    coingecko_historical_price = get_historical_price_from_coingecko(token=token_id_coingecko)
