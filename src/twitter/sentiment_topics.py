import pandas as pd


if __name__ == "__main__":

    data = pd.read_csv("../dashboard/data/tweets_solana_28_06.csv", sep=";", decimal=',')
    print(data)