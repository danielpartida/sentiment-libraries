from unicodedata import decimal
import pandas as pd
import json

if __name__ == "__main__":

    data = pd.read_csv("../data/backup/crypto_context_tweets_09_06_17_05.csv", sep=';', decimal=',')
    context_annotations = data.context_annotations
    # convert str to list
    series_annotations = context_annotations.apply(lambda x: eval(x))

    try:
        look_up_dict = {}
        for row in series_annotations:
            for element in row:

                id_domain = int(element["domain"]["id"])
                if id_domain not in look_up_dict.keys():
                    look_up_dict[id_domain] = {}
                    look_up_dict[id_domain]["name"] = element["domain"]["name"]

                    if "description" in element["domain"].keys():
                        look_up_dict[id_domain]["description"] = element["domain"]["description"]

                    look_up_dict[id_domain]["entities"] = {}

                id_entity = int(element["entity"]["id"])
                if id_entity in look_up_dict[id_domain]["entities"].keys():
                    continue

                look_up_dict[id_domain]["entities"][id_entity] = {}
                look_up_dict[id_domain]["entities"][id_entity]["name"] = element["entity"]["name"]

    except Exception as e:
        print(e)

    print(look_up_dict)

    df_entities = pd.DataFrame(look_up_dict[30]["entities"]).T
    df_entities.to_csv("../look_up_tables/df_entities.csv", sep=';', decimal=',')

    df_hobbies = pd.DataFrame(look_up_dict[66]["entities"]).T

    df_cryptos = pd.DataFrame(look_up_dict[174]["entities"]).T
    df_tickers = pd.DataFrame(look_up_dict[166]["entities"]).T
    df_brands = pd.DataFrame(look_up_dict[47]["entities"]).T
    df_technologies = pd.DataFrame(look_up_dict[165]["entities"]).T
    df_people = pd.DataFrame(look_up_dict[10]["entities"]).T
