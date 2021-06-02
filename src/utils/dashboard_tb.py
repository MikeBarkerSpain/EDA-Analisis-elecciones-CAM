'''
This file contains the functionality related to the dashboard
'''

import streamlit as st
import requests as rq
from PIL import Image
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns 
import numpy as np 
import os
import random
import statistics

root_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))   # se sube hasta el nivel de la raiz del proyecto

def configuracion():
    st.set_page_config(page_title='Elecciones a la asamblea de la CAM', page_icon=':votes:', layout="wide")

def menu_home(df):

    #st.header("EDA para respaldar o refutar una hipótesis.")
    img = Image.open(root_path + os.sep + 'resources' + os.sep + 'PP_Listas_meme.jpg')
    st.image(img, use_column_width='auto')

    with st.beta_expander("¿Y cuál es esa hipótesis inicial?"):
        st.write(""" Hecho: En estas últimas elecciones a la asamblea de la Comunidad de Madrid, ha habido un porcentaje de voto al PP 
        muy superior al esperado.
        
        Contexto: Dado que en el último año y medio hemos sufrido la mayor  
        pandemia conocida en este siglo, seguramente este sentido del voto 
        esté relacionado de alguna manera con la gestión del problema. 
        
        Y dado que una de las medidas estrella del gobierno de la CAM ha 
        sido dejar más margen a la hostelería, parece sensato plantear 
        la siguiente hipótesis:
        
        Hipótesis: el aumento del voto al PP está correlacionado en positivo 
        con el número de bares por habitante.""")

    if st.button('Datos y fuentes'):
        with st.empty():
            st.write("Las fuentes de los datos son el Gobierno y el ayuntamiento de Madrid")
        with st.empty():
            st.dataframe(df)

@st.cache(suppress_st_warning=True)
def cargar_datos(csv_path):
    df = pd.read_csv(csv_path, sep=',')
    #df = df.rename(columns={'latidtud': 'lat', 'longitud': 'lon'})
    return df

def menu_datos(df):

    st.subheader('Datos por Distrito:')
    var_PP_distri = df.groupby('Distritos')['D-PP'].sum()
    st.subheader('Variación del voto al PP por distrito:')
    st.bar_chart(var_PP_distri)

    Locales_distri = df.groupby('Distritos')['Locales'].sum()
    st.subheader('Locales relacionados con la hostelería por distrito:')
    st.bar_chart(Locales_distri)

    varPPlocales = df.groupby('Distritos')['VarPPlocales'].mean()
    st.subheader('Variación del voto al PP dividida por el número de locales:')
    st.bar_chart(varPPlocales)

    st.write('''Dado que los dos primeros histogramas no tienen formas semejantes, el tercero, que representa 
    una variable que relaciona la variación del voto al PP en función del número de bares del distrito, se 
    puede pensar que no hay correlación entre la variación del voto al PP y el número de bares de un distrito.''')

    st.write('''No obstante, hay que diseccionar los datos detallándolos a nivel de barrio para ver si esa correlación existe o no.
    Para ello, lo primero es identificar los outliers existentes si los hubiera y dejarlos fuera del análisis de valores.''')

    
    st.subheader('Datos por Barrio:')

    st.subheader('Boxplot: localización de los outliers existentes')

    st.write('''Gracias a la herramienta boxplot, se identifican los outliers, lo que permite refinar el dataset para seguir analizando 
    los datos sin tener estos outliers en cuenta.''')

    data = df['VarPPlocales']
    fig = plt.figure(figsize =(10, 4))
    # Creating plot
    plt.boxplot(data, vert=False)

    # show plot
    # calculate data needed for the plot
    median = round(statistics.median(data.to_list()), 2)
    Q1 = round(np.percentile(data, 25), 2)  # Q1
    Q3 = round(np.percentile(data, 75), 2)  # Q3
    IQR = Q3-Q1
    W1 = round(Q1 - 1.3*IQR,2)
    if W1 < 0:
        W1 = 0
    W3 = round(Q3 + 1.3*IQR,2)

    # preparar 
    font = {'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 14,
        }
    fontdata = {'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 12,
        }
    fontout = {'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 20,
        }
    plt.text(90, 0.85, r'OUTLIERS', fontdict=fontout)
    plt.text(10, 1.1, f'Mediana: {median}', fontdict=font)
    plt.text(0, 0.82, f'W1: {W1}', rotation=-20, fontdict=fontdata)
    plt.text(10, 0.8, f'Q1: {Q1}', rotation=-20, fontdict=fontdata)

    plt.text(29, 0.79, f'Q3: {Q3}', rotation=-20, fontdict=fontdata)
    plt.text(50, 0.80, f'W3: {W3}', rotation=-20, fontdict=fontdata)
    plt.show()
    st.pyplot(fig)
    
    st.write('''Una vez identificado el límite de los outliers, se pueden limpiar los datos del dataset original con el fin de perfilar 
    los cálculos de correlación dado que en este caso los outliers no representan un gran peso con respecto del total de datos analizados, 
    sino no podrían ser eleminados tan sencillamente.''')

    st.subheader('Variación del voto al PP vs locales por barrio (con outliers):')
    scatter = alt.Chart(df).mark_circle().encode(x='Locales', y='D-PP', size='censo', color='censo', tooltip=['D-PP', 'Locales', 'censo'])
    st.altair_chart(scatter, use_container_width=True)

    st.subheader('Variación del voto al PP vs locales por barrio (sin outliers):')
    data_noOutliers = df[df['VarPPlocales'] < 60]
    scatter2 = alt.Chart(data_noOutliers).mark_circle().encode(x='Locales', y='D-PP', size='censo', color='censo',  tooltip=['D-PP', 'Locales', 'censo'])
    st.altair_chart(scatter2, use_container_width=True)

    st.write('''Al comparar ambos diagramas de dispersión, se comprueba que los datos no tienen una correlación directa ya que se representan 
    en una nube de puntos muy dispersa, sin tener un posicionamiento a lo largo de un eje definido.''')


    if st.button('Conclusiones'):

        stat = stats.pearsonr(data_noOutliers['D-PP'], data_noOutliers['Locales'])
        stat_corr = round(stat[0], 3)

        st.write(f'''Al trazar un gráfico de dispersión con la línea de regresión, es posible ver de forma intuitiva si hay correlación 
        o no entre las variables de la gráfica ''')

        g = sns.JointGrid(height=5, ratio=10, data=data_noOutliers, x="Locales", y="D-PP")
        g.plot(sns.regplot,sns.histplot)
        plt.show()
        #plt.gcf().savefig("correlation.png")
        st.pyplot(g)

        st.write(f'''La dispersión de los datos alrededor de la recta de regresión es muy alta, por lo que intuitivamente se puede deducir 
        que no hay correlación entre variables. Además, el coeficiente de correlación de Pearson es {stat_corr}, que está muy por debajo de 
        un valor que indique una correlación significativa (0.45), por lo tanto, la variación del voto hacia el PP y el número de locales 
        no están correlacionadas. ''')


        st.subheader('Por lo tanto, la hipótesis inicial ha sido refutada.')

        st.balloons()
        
        st.error('''Algo importante que se ha aprendido en este EDA: \nRealizar el análisis con ideas preconcebidas, 
        y lo que es peor, con las conclusiones preestablecidas,\n\t\tNO ES UNA BUENA PRÁCTICA.''')
       
        img = Image.open(root_path + os.sep + 'resources' + os.sep + 'conclusiones_meme.jpg')
        st.image(img, use_column_width='auto')

        st.title('Análisis avanzado')
        st.write ('''A continuación se presentan dos vías para un análisis avanzado que podrían explicar el porqué de la variación de voto.''')

        st.subheader('Análisis con variables relacionadas con la variación del voto')

        st.write(f'''Una vez hechos los cálculos de correlación para las variables iniciales (variación del voto al PP y locales de hostelería)
        es posible desarrollar nuevas variables que incluyan nuevos datos que permitan un análisis más profundo.''')
        st.write(f'''A continuación se presentan las variables que se han creado para analizar su correlación con la matriz de correlación:''')
        st.write(f'''- VarPP: variación del voto al PP dividido por el voto del PP en 2019 (%)''')
        st.write(f'''- VarPPcenso: variación del voto al PP dividido por el censo de 2021''')

        df_mini = pd.DataFrame(df,columns=['Censo-2021','Locales','Locscenso', 'D-Abs', 'D-Blc','D-Nulos', 
        'D-PP', 'VarPP', 'VarPPcenso'])
        corrMatrix = round(df_mini.corr(), 2)
        fig_heatmap, ax = plt.subplots(figsize=(6,5))         # Sample figsize in inches
        sns.heatmap(corrMatrix, annot=True)
        plt.show()
        st.pyplot(fig_heatmap)

        st.write(f'''Tal y como se puede observar en el mapa de calor/matriz de correlación, no hay una relación directa entre las variables calculadas
        y el número de locales de cada barrio, por lo tanto, este análisis avanzado refuerza la refutación de la hipótesis inicial.''')

        st.write(f'''No obstante, cabe destacar la correlación inversa entre la abstención y la variación de voto (-0.78), queriendo decir que la ciudadanía 
        se ha movilizado a favor del PP, por lo que merecería la pena ver cuales son los factores de movilización que han generado esa correlación. ''')

        st.subheader('Explicación del voto al PP en función del voto anterior')

        st.write(f'''Dado que las medidas tomadas tienen un origen político, es posible que el ganador de las anteriores elecciones 
        tenga algún tipo de influencia en el resultado de la variación, por lo tanto se pueden analizar los datos con esa perspectiva
        para ver si merece la pena hacer un análisis más profundo en esa dirección.''')

        g = sns.lmplot(height=3, data=data_noOutliers, x="Locales", y="D-PP", hue='anterior', col='anterior',palette="Set1")
        plt.show()
        #plt.gcf().savefig("correlation.png")
        st.pyplot(g)

        dataPP = data_noOutliers[data_noOutliers['anterior'] == 'PP']
        statPP = stats.pearsonr(dataPP['D-PP'], dataPP['Locales'])
        RPP = round (statPP[0], 3)

        dataPSOE = data_noOutliers[data_noOutliers['anterior'] == 'PSOE']
        statPSOE = stats.pearsonr(dataPSOE['D-PP'], dataPSOE['Locales'])
        RPSOE = round (statPSOE[0], 3)

        st.write(f'''Al observar ambas gráficas, cabe destacar que la dispersión de los datos con respecto al partido que ganó al anteriores elecciones es significativamente diferente en función del 
        partido que las ganó. Las distintas dispersiones con respecto a la recta de regresión provocan una correlación distinta para cada gráfica (PP= {RPP}, PSOE= {RPSOE}), y mientras que la correlación 
        de los datos en los barrios donde ganó el PP es alta (casi 0'6), la correlación en los barrios donde ganó el PSOE no llega al 0'25.''')

        st.write(f'''Esta diferencia en los resultados podría evidenciar que en los barrios donde ganó anteriormente el PP los votantes si que han tenido en cuenta las medidas para con el sector de 
        la hostelería, mientras que ese no ha sido un factor de influencia en los barrios donde anteriormente ganó el PSOE.''')

        st.info('MUCHAS GRACIAS POR VUESTRA ATENCIÓN')

def menu_flask():
    if st.button('Get data'):
        datos_json = rq.get('http://localhost:6060/pwd?password=T05290575').json()
        st.dataframe(pd.DataFrame(datos_json))

def menu_filtrado(df):

    st.sidebar.subheader("Filtros:")

    distritos, filtro_distrito, barrios, filtro_barrio, censo, filtro_censo, partido_ant, filtro_partido_ant, visu = opciones_filtros(df)

    df_filtrado = filtrar(df, distritos, filtro_distrito, barrios, filtro_barrio, censo, filtro_censo, partido_ant, filtro_partido_ant)

    if df_filtrado.shape[0] == 0:
        st.warning("Los filtros que has seleccionado no nos devuelven ningun punto de carga")
        st.stop()

    graficas(df_filtrado, filtro_distrito, filtro_barrio, filtro_censo, filtro_partido_ant, visu)

def opciones_filtros(df):
    visu = st.sidebar.radio("¿Deseas ver los datos separados por partido?",('No', 'Si'))

    distritos = st.sidebar.multiselect(
        'Selecciona el distrito que te interese:',
        options=df.Distritos.unique().tolist())

    filtro_distrito = st.sidebar.checkbox('Quiero filtrar por distrito')
    
    barrios = st.sidebar.multiselect(
        'Selecciona los barrios que te interesen:',
        options=df.Barrios.unique().tolist())

    filtro_barrio = st.sidebar.checkbox('Quiero filtrar por barrio')

    censo = st.sidebar.select_slider("Selecciona el censo",
                                      options=range(min(df.iloc[:, 6]), max(df.iloc[:, 6]) + 1),
                                      value=(min(df.iloc[:, 6]), max(df.iloc[:, 6])))

    filtro_censo = st.sidebar.checkbox('Quiero filtrar por censo')

    partido_ant = st.sidebar.selectbox(
        'Selecciona partido:',
        options=df.anterior.unique().tolist())
    filtro_partido_ant = st.sidebar.checkbox('Quiero filtrar por el partido que ganó en las elecciones anteriores')

    return distritos, filtro_distrito, barrios, filtro_barrio, censo, filtro_censo, partido_ant, filtro_partido_ant, visu

def filtrar(df, distritos, filtro_distrito, barrios, filtro_barrio, censo, filtro_censo, partido_ant, filtro_partido_ant):

    if filtro_distrito:
        df = df.loc[df['Distritos'].isin(distritos), :]
    
    if filtro_barrio:
        df = df.loc[df['Barrios'].isin(barrios), :]

    if filtro_censo:
        df = df.loc[(df['Censo-2021'] >= censo[0]) & (df['Censo-2021'] <= censo[1]), :]

    if filtro_partido_ant:
        df = df.loc[df['anterior'] == partido_ant, :]

    return df

def graficas(df_filtrado, filtro_distrito, filtro_barrio, filtro_censo, filtro_partido_ant, visu):
    
    if visu == 'No':
        g = sns.lmplot(height=6, data=df_filtrado, x="Locales", y="D-PP")
        plt.figure(figsize=(5,5))
        plt.show()
        st.pyplot(g)
    else:
        g = sns.lmplot(height=6, data=df_filtrado, x="Locales", y="D-PP", hue='anterior',palette="Set1")
        plt.figure(figsize=(10,10))
        plt.show()
        st.pyplot(g)