import pandas as pd
import requests

if __name__ == "__main__":

    df = pd.read_csv("../look_up_tables/df_Digital Assets & Crypto.csv", sep=";", decimal=',')
    df.rename(columns={"Unnamed: 0": "id"}, inplace=True)

    entities = pd.read_csv("../look_up_tables/entities.csv", sep=';', decimal=',')
    entities.rename(columns={"Unnamed: 0": "id", "0": "name"}, inplace=True)

    # FIXME: Create dynamic entity and annotation_id
    entity_id = 170
    annotation_id = 1007360414114435072
    url = "https://api.twitter.com/2/tweets/counts/recent?query=context:{0}.{1}".format(entity_id, annotation_id)

    headers = {"Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAALnHbgEAAAAAIvPN2uwC7u3Bk2Gcacx8lOG%2FbYY%3DEi1nQg8LcjhT4yONksZAt8gQlIqV77LwIm0nQe6UXE9dgAVbv7"}
    data = requests.get(url=url, headers=headers)
    print(data)
