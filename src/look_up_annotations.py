import pandas as pd


def save_to_csv(path: str, entity_key: int) -> None:

    if entity_key not in entities.keys():
        raise ValueError("Index is not present in entity keys")

    df = pd.DataFrame(look_up_dict[entity_key]["entities"]).T
    df.to_csv(path + "df_{0}.csv".format(entities[entity_key]), sep=';', decimal=',')


if __name__ == "__main__":

    one_day = "crypto_context_tweets_09_06_17_05.csv"
    seven_days = "context_tweets_14_06_15_02.csv"
    data = pd.read_csv("../data/backup/{0}".format(seven_days), sep=';', decimal=',')
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

    # Export results
    entities = {}
    basic_path = "../look_up_tables/"
    for key in look_up_dict.keys():
        entities[key] = look_up_dict[key]["name"]
        save_to_csv(path=basic_path, entity_key=key)
