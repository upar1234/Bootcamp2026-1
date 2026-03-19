import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns 

# Cargar el dataset
st.set_page_config(layout='centered', page_title='Talento tech', page_icon='bar.chart:')


t1, t2 = st.columns([0.3,0.7])

t2.title('Analisis de datos con Python')
t2.markdown('Alejandro Aristizábal Pérez 1007347079')
t1.image("descarga.jpg", width = 2000)

steps = st.tabs(["pestaña1", "pestaña2", "pestaña3"])

with steps[0]:
    st.write("Pestaña 1")

with steps[1]:
    st.title("Pestaña 2")
    df = pd.DataFrame({
        'A':[1,2,3],
        'B':[4,5,6],
        'C':[7,8,9],
        })
    
    st.dataframe(df)
    fig, ax = plt.subplots()
    ax = sns.barplot(x = ['A', 'B', 'C'], y = ([1,2,3]))
    st.pyplot(fig)

with steps[2]:
    df = pd.DataFrame({
        'A':[1,2,3],
        'B':[4,5,6],
        'C':[7,8,9],
        })

    st.dataframe(df)
    fig, ax= plt.subplots()
    ax = sns.barplot(x = ['A', 'B', 'C'], y = ([1,2,3]), ax = ax)
    st.pyplot(fig)
    
