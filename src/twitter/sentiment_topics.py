import pandas as pd
import numpy as np
from datetime import datetime
from tqdm import tqdm


if __name__ == "__main__":

    today = datetime.today()
    date_format_short = '%d_%m'
    asset = "solana"

    data = pd.read_csv("../dashboard/data/tweets_{0}_{1}.csv".format(asset, today.strftime(date_format_short)),
                       usecols=["context_annotations"], sep=";", decimal=',')

    try:
        list_annotations = []

        for context in tqdm(data["context_annotations"]):
            if not type(context) == float:
                tweet_annotations = eval(context)[0]
                for annotation in tweet_annotations:
                    dict_annotation = {
                        'domain_id': annotation['domain']['id'], 'domain_name': annotation['domain']['name'],
                        'entity_id': annotation['entity']['id'], 'entity_name': annotation['entity']['name']
                    }

                    if 'domain_description' in annotation['domain'].keys():
                        dict_annotation['domain_description'] = annotation['domain']['description'],

                    if 'description' in annotation['entity'].keys():
                        dict_annotation['entity_description'] = annotation['entity']['description']

                    list_annotations.append(list_annotations)

        df = pd.DataFrame(list_annotations)

    except BaseException as err:
        print("Ups, we encountered an error: ", err)

    print(data)
