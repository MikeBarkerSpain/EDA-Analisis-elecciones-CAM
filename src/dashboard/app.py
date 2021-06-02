import streamlit as st
import os,sys

    
path = os.path.dirname(__file__)
dir = os.path.dirname
src_path = dir(dir(__file__))


sys.path.append(src_path)

root_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))   # se sube hasta el nivel de la raiz del proyecto

import utils.dashboard_tb as dsh


dsh.configuracion()

csv_path = root_path + os.sep + 'data' + os.sep + 'final_df.csv'
df = dsh.cargar_datos(csv_path)

menu = st.sidebar.selectbox('Menu:',
                            options=['Bienvenida','Análisis','Filtrado', 'flask'])

st.title("Elecciones a la asamblea de la CAM")

if menu == 'Bienvenida':
    dsh.menu_home(df)
elif menu == 'Análisis':
    dsh.menu_datos(df)
elif menu == 'Filtrado':
    dsh.menu_filtrado(df)
elif menu == 'flask':
    dsh.menu_flask()