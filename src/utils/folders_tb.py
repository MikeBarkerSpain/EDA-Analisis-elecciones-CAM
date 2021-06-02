'''
contains the generic functionality related to open,create, read and write files
'''
import pandas as pd
import numpy as np
import lxml
import xlrd
import os, sys

dir = os.path.dirname

# se saltan tres veces de directorio para llegar al directorio raíz del proyecto '/Entregable_EDA'
# la primera para eliminar el nombre del archivo 
# las dos siguientes para eliminar los directorios '/utils' y '/src'
src_path = dir(dir(dir(__file__)))

# se incorpora la ruta hasta el directorio raiz al path del archivo
sys.path.append(src_path)

def read_Loc_Mad ():
    filename = src_path + '/data/OPEN_DATA_Locales-Epigrafes202104.csv'
    Locales_MAD = pd.read_csv(filename, sep=';')
    return Locales_MAD

def read_Votos_Mad ():
    filename = src_path + '/data/VotosMad.xls'
    Votos_MAD = pd.read_excel(filename)
    return Votos_MAD

def save_df_to_csv(final_df):
    final_df.to_csv(src_path + '/data/final_df.csv')

def read_tiempos ():
    filename = src_path + '/data/time.csv'
    tiempos = pd.read_csv(filename, sep=';')
    return tiempos

# zona para probar la función individualmente
if __name__ == '__main__':
    #print("src_path:\n", src_path)
    print (read_Loc_Mad())
    print (read_Votos_Mad())


