'''
This file contains the generic functionality related tocollect data, clean data and others (wrangling methods such usworking with multiples jsons)
'''

import os, sys

dir = os.path.dirname

# se saltan tres veces de directorio para llegar al directorio raíz del proyecto '/Entregable_EDA'
# la primera para eliminar el nombre del archivo 
# las dos siguientes para eliminar los directorios '/utils' y '/src'
src_path = dir(dir(__file__))

# se incorpora la ruta hasta el directorio raiz al path del archivo
sys.path.append(src_path)

import pandas as pd
import numpy as np

import utils.folders_tb as fold

def filter_mad_locs (df_mad_locs):
    df_mad_locs.drop(columns= ['id_local', 'cod_barrio_local', 'id_seccion_censal_local', 'coordenada_x_local', 'coordenada_y_local', 'desc_tipo_agrup', 'rotulo', 'id_seccion', 'id_division', 'id_epigrafe','id_tipo_acceso_local', 'desc_tipo_acceso_local', 'id_situacion_local', 'desc_situacion_local', 'id_vial_edificio', 'clase_vial_edificio', 'desc_vial_edificio', 'id_ndp_edificio', 'id_clase_ndp_edificio', 'nom_edificio', 'num_edificio', 'coordenada_x_agrupacion', 'coordenada_y_agrup', 'id_agrupacion', 'nombre_agrupacion', 'id_tipo_agrup', 'id_planta_agrupado', 'id_local_agrupado', 'cal_edificio', 'secuencial_local_PC', 'id_vial_acceso', 'id_ndp_acceso', 'id_clase_ndp_acceso','cal_acceso', 'clase_vial_acceso','desc_vial_acceso','nom_acceso','num_acceso'], inplace=True)
    # Se genera el dataframe final con los locales agrupados por sección censal -> se eliminan las columnas de las categorías de los locales y se agrupan los datos por categorías censales 
    DF_actividades = df_mad_locs.copy()

    #Se filtran aquellos locales cuya actividad no corresponde con las actividades enmarcadas en el estudio
    DF_actividades = DF_actividades[(DF_actividades['desc_seccion'] == 'HOSTELERIA') | (DF_actividades['desc_epigrafe'] == 'DISCOTECAS Y SALAS DE BAILE') | (DF_actividades['desc_epigrafe'] == 'SALAS DE FIESTA SIN RESTAURACION')| (DF_actividades['desc_epigrafe'] == 'TEATRO Y ACTIVIDADES ESCENICAS REALIZADAS EN DIRECTO')]

    # Se añade una columna con una unidad para contabilizar los locales al agrupar 
    DF_actividades['Locales'] = 1
    DF_actividades = DF_actividades.groupby(['id_distrito_local', 'id_barrio_local']).sum().reset_index()
    DF_actividades.drop(columns='desc_seccion_censal_local', inplace=True)

    # Se modifican los campos de id_distrito_local e id_barrio_local para que concuerden con el formato del dato en la tabla de los votos
    DF_actividades = DF_actividades.assign(id_barrio=lambda x: (x['id_barrio_local'] - x['id_distrito_local']*100 +x['id_distrito_local']*10))
    DF_actividades = DF_actividades[['id_barrio','Locales']]
    return DF_actividades

def filter_mad_votos (df_mad_votos, df_mad_locs):
    # se refina la tabla de locales por actividad
    fil_mad_locs = filter_mad_locs (df_mad_locs)

    # Se unen ambas tablas y se eliminan las columnas sobrantes
    df_MAD = df_mad_votos.merge(fil_mad_locs, on='id_barrio', how='left')
    df_MAD.drop(columns=['ID_dist'], inplace=True)

    # Se generan las variables sintéticas a partir de las variables existentes
    # Locales por habitante con derecho a voto
    df_MAD = df_MAD.assign(Locscenso=lambda x: x['Locales']/x['Censo-2021'])
    df_MAD = df_MAD.assign(censo=lambda x: x['Censo-2021']//1000)
    df_MAD = df_MAD.assign(VarPPlocales=lambda x: x['D-PP']/x['Locales'])
    #df_MAD = df_MAD.assign(anteriorPP=lambda x: True if (x['PP-2019']>x['PSOE-2019']) else False)
    df_MAD['anterior'] = np.where (df_MAD['PP-2019']>df_MAD['PSOE-2019'], 'PP', 'PSOE')

    # Variación porcentual del voto para cada partido con respecto a su anterior resultado
    df_MAD = df_MAD.assign(VarPP=lambda x: x['D-PP']/x['PP-2019']*100)
    df_MAD = df_MAD.assign(VarVOX=lambda x: x['D-VOX']/x['VOX-2019']*100)
    df_MAD = df_MAD.assign(VarCs=lambda x: x['D-Cs']/x['Cs-2019']*100)
    df_MAD = df_MAD.assign(VarPSOE=lambda x: x['D-PSOE']/x['PSOE-2019']*100)
    df_MAD = df_MAD.assign(VarMM=lambda x: x['D-MÁS MADRID']/x['MAS MADRID-2019']*100)
    df_MAD = df_MAD.assign(VarPiU=lambda x: x['D-PODEMOS-IU']/x['PODEMOS-IU-2019']*100)

    # Variación porcentual del voto para cada partido con respecto a su anterior resultado
    df_MAD = df_MAD.assign(VarPPcenso=lambda x: x['D-PP']/x['Censo-2021']*100)
    df_MAD = df_MAD.assign(VarVOXcenso=lambda x: x['D-VOX']/x['Censo-2021']*100)
    df_MAD = df_MAD.assign(VarCscenso=lambda x: x['D-Cs']/x['Censo-2021']*100)
    df_MAD = df_MAD.assign(VarPSOEcenso=lambda x: x['D-PSOE']/x['Censo-2021']*100)
    df_MAD = df_MAD.assign(VarMMcenso=lambda x: x['D-MÁS MADRID']/x['Censo-2021']*100)
    df_MAD = df_MAD.assign(VarPiUcenso=lambda x: x['D-PODEMOS-IU']/x['Censo-2021']*100)

    df_MAD = df_MAD[['id_barrio', 'Distritos', 'Barrios', 'Locales', 'Locscenso',
        'Censo-2021', 'Censo-2019', 'D-Censo','censo','Abstención-2021', 'Abstención-2019','D-Abs', 
        'Blanco-2021', 'Blanco-2019', 'D-Blc', 'Nulos-2021','Nulos-2019', 'D-Nulos',
            'PP-2021', 'PP-2019','D-PP', 'VarPP', 'VarPPcenso', 'VarPPlocales','anterior',
            'PSOE-2021','PSOE-2019','D-PSOE', 'VarPSOE', 'VarPSOEcenso','VOX-2021', 'VOX-2019','D-VOX', 'VarVOX', 'VarVOXcenso', 
        'MAS MADRID-2021','MAS MADRID-2019','D-MÁS MADRID','VarMM', 'VarMMcenso', 
        'PODEMOS-IU-2021','PODEMOS-IU-2019','D-PODEMOS-IU','VarPiU', 'VarPiUcenso', 'Cs-2021', 'Cs-2019', 'D-Cs','VarCs','VarCscenso']]

    fold.save_df_to_csv(df_MAD)
    return df_MAD
    
    # zona para probar la función individualmente
if __name__ == '__main__':
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
    
    mad_locs = read_Loc_Mad()
    mad_votos = read_Votos_Mad ()
    #mad_locs_fil = filter_mad_locs (mad_locs)
    df_mad = filter_mad_votos (mad_votos, mad_locs)

    #print("src_path:\n", src_path) filter_mad_votos(mad_votos, mad_locs)
    print (df_mad)