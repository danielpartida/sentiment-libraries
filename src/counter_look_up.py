import os

import pandas as pd
import requests


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r

if __name__ == "__main__":

    df = pd.read_csv("../look_up_tables/df_Digital Assets & Crypto.csv", sep=";", decimal=',')
    df.rename(columns={"Unnamed: 0": "id"}, inplace=True)

    entities = pd.read_csv("../look_up_tables/entities.csv", sep=';', decimal=',')
    entities.rename(columns={"Unnamed: 0": "id", "0": "name"}, inplace=True)

    # FIXME: Create dynamic entity and annotation_id
    entity_id = 174
    annotation_id = 1007360414114435072
    url = "https://api.twitter.com/2/tweets/counts/recent?query=context:{0}.{1}".format(entity_id, annotation_id)

    token = os.getenv('bearer_token')
    token = "AAAAAAAAAAAAAAAAAAAAALnHbgEAAAAAIvPN2uwC7u3Bk2Gcacx8lOG%2FbYY%3DEi1nQg8LcjhT4yONksZAt8gQlIqV77LwIm0nQe6UXE9dgAVbv7"
    headers = {"Authorization": "Bearer {0}".format(token)}
    response = requests.get(url=url, auth=BearerAuth(token))

    print("Run")