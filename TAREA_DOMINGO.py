#streamlit run TAREA_DOMINGO.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

opcion= st.selectbox('SELECCIONAR CASO: ',('NETFLIX','NYC'))

if opcion=='NETFLIX':
    #--- IMPORT DATA ---#

    @st.cache 

    def load_b(nrows): 
        data = pd.read_csv("movies.csv", nrows=nrows) 
        data["name"]=data['name'].str.lower()
        return data 


    data_f=load_b(500)

    #--- PAGE CONFIG ---#

    st.title("Netflix app")
    st.markdown("Brian I. Chávez Viveros A01424135")


    #--- SIDEBAR FILTERS ---#

    check=st.sidebar.checkbox("Mostrar todos los datos", value=True)


    pelicula=st.sidebar.text_input("Título del filme")

    buscar_peli=st.sidebar.button('Buscar Filmes')



    directores=data_f['director'].unique()
    director= st.sidebar.selectbox('Seleccionar Director',directores)

    buscar_direc=st.sidebar.button('Buscar Director')


    if buscar_peli:
        st.markdown("Por nombre:")
        nombre=data_f.loc[data_f['name'].str.contains(pelicula.lower(),case=False)]
        st.dataframe(nombre)

    if buscar_direc:
        st.markdown("Por director:")
        direc=data_f[(data_f["director"]==director)]
        st.dataframe(direc)

    if check:
        st.markdown("Todas las películas:")
        st.dataframe(data_f)

elif opcion=='NYC':

    #--- IMPORT DATA ---#
    @st.cache 

    def load_data(nrows): 
        df = pd.read_csv("citibike-tripdata.csv", nrows=nrows) 
        df = df.rename(columns={'start_lat':'lat',
                                    'start_lng':'lon'})


        df['started_at'] = pd.to_datetime(df['started_at'])
        df["hora"]=[(hora.hour) for hora in df["started_at"]]

        return df 

    datass = load_data(500) # probar con 100, 1000, etc



    #--- PAGE CONFIG ---#

    st.title("NYC app")
    st.markdown("Brian I. Chávez Viveros A01424135")


    #--- SIDEBAR FILTERS ---#

    checka=st.sidebar.checkbox("Show raw data")

    checkiii=st.sidebar.checkbox("Recorridos por hora")

    dts = st.sidebar.slider('Rango de horas: ',
                    0,23,10
                    )

    if checka:
        st.dataframe(datass)

    if checkiii:
        #BARRAS OPCION ASIGNADA
        poo=(datass.groupby(by=['hora']).count()[['ride_id']].sort_values(by='ride_id'))
        polar = px.bar(poo, x=poo.index, y='ride_id')
        polar.update_layout(bargap=0.2,title={
                    'text': "Numero de recorridos por hora",
                    'y':0.95,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'})
        st.plotly_chart(polar)



    #------------MAPA--------------

    datass=datass[(datass['hora'] == dts)]

    st.map(datass,11)