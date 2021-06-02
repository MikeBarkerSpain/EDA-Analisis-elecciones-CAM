'''
This file contains the generic functionality related to working with APIs
'''

import os
import json

dir = os.path.dirname

# se saltan tres veces de directorio para llegar al directorio raíz del proyecto '/Entregable_EDA'
# la primera para eliminar el nombre del archivo 
# las dos siguientes para eliminar los directorios '/utils' y '/src'

src_path = dir(dir(dir(__file__)))

import pandas as pd

def flask_return_json():
    df_read_csv = pd.read_csv(src_path + '/data/final_df.csv')
    return df_read_csv.to_json()

def read_json(fullpath):
    with open(fullpath, "r") as json_file_readed:
        json_readed = json.load(json_file_readed)
    return json_readed