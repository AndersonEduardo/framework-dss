import os
import pickle
import requests
import pandas as pd

from parameters import *


class DataLoader:

    @staticmethod
    def load_data():

        index_list = dict()
        index = 0

        response = requests.get(API_DSSF_BUNDLES)

        if response.status_code == 200:

            data = response.json()['response']

        else:

            data = dict()

        #     if os.path.exists(PERSISTENCE_FILEPATH):

        #         with open(PERSISTENCE_FILEPATH, 'rb') as f:

        #             data = pickle.load(f)
            
        #     else:

        #         data = dict()


        bundles_data_formated = list()

        for context_key in data.keys():

            bundle_data = {
                'label': context_key.strip().title(),
                'value': f'context_{index}', # unlerline obrigatorio
                'children': list()
            }

            index_list[f'context_{index}'] = context_key.strip().lower()
            index +=1

            for k,v in data[context_key].items():

                children = {
                    'label': k.strip().upper().title(),
                    'value': f'bundle_{index}', # unlerline obrigatorio
                    'children': list()
                }

                index_list[f'bundle_{index}'] = k.strip().lower()
                index +=1

                for i,item in enumerate(v.upper().split('[LINEBREAK]')):

                    children['children'].append(
                        {
                            'label':item.replace('"', '').replace("'", ""), 
                            'value':f'item_{index}' # unlerline obrigatorio
                        }
                    )

                    index_list[f'item_{index}'] = item.strip().lower()
                    index +=1

                bundle_data['children'].append(children)

            bundles_data_formated.append(bundle_data)

        return {'index_list': index_list, 'bundles_data_formated': bundles_data_formated}
