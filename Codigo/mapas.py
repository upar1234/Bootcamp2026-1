import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(page_title="Mapa Solar Colombia", layout="wide")

url_repo = os.path.join(BASE_DIR, "..", "Documentos", "colombia.geo.json")
url_municipios_prueba = "https://gist.githubusercontent.com/john-guerra/727e8992e9599b9d9f1dbfdc4c8e479e/raw/090f8b935a437e24d65b64d87598fbb437c006da/colombia-municipios.json"

@st.cache_data
def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

@st.cache_data
def get_data():
    # 1. Construye la ruta subiendo un nivel y entrando a Documentos
    ruta = os.path.join(BASE_DIR, "..", "Documentos", "solar.csv")
    
    # Verificación de seguridad
    if not os.path.exists(ruta):
        st.error(f"Archivo no encontrado en la ruta calculada: {ruta}")
        st.stop()
        
    df = pd.read_csv(ruta)

    df['Departamento'] = df['Departamento'].astype(str).str.upper().str.strip()
    mapeo = {
        'BOGOTÁ': 'SANTAFE DE BOGOTA D.C.',
        'BOGOTA': 'SANTAFE DE BOGOTA D.C.',
        'BOGOTÁ D.C.': 'SANTAFE DE BOGOTA D.C.',
        'VALLE DEL CAUCA': 'VALLE DEL CAUCA',
        'NARIÑO': 'NARINO',
        'ATLÁNTICO': 'ATLANTICO',
        'BOLÍVAR': 'BOLIVAR',
        'NORTE DE SANTANDER': 'NORTE DE SANTANDER',
        'QUINDÍO': 'QUINDIO'
    }
    df['Departamento'] = df['Departamento'].replace(mapeo)
    return df

colombia_geojson = load_json(url_repo)
df_solar = get_data()
departamentos = df_solar[['Departamento', 'Energía [kWh/año]']]
departamentos = departamentos.groupby('Departamento').sum().reset_index()

# departamentos.columns = ['Departamento', 'Energia']
st.write(departamentos)


# Interfaz 
st.title("☀️ Generación de Energía Solar en Colombia")
st.markdown("Visualización basada en proyectos solares activos y estimados.")
# st.write("Departamentos detectados en CSV:", df_solar['Departamento'].unique()[:33])
# st.write("Departamentos detectados en GeoJSON:", [feature['properties']['NOMBRE_DPT'] for feature in colombia_geojson['features']][:8])

st.sidebar.header("Filtros de Búsqueda")
# Obtenemos la lista de departamentos únicos del CSV
lista_deptos = ["TODOS"] + sorted(df_solar['Departamento'].unique().tolist())
depto_seleccionado = st.sidebar.selectbox("Selecciona un Departamento", lista_deptos)

#  Mapa de Calor
fig = px.choropleth(
    departamentos,
    geojson=colombia_geojson,
    locations="Departamento",
    featureidkey="properties.NOMBRE_DPT",
    color="Energía [kWh/año]",
    color_continuous_scale="Reds",
    hover_data={
        "Departamento": False,   # Lo ponemos en False para que no se repita abajo del título
        "Energía [kWh/año]": ":,.2f", # Formato con comas y 2 decimales
    },
    labels={
        'Energía [kWh/año]': 'Total kWh/año',
        'Proyecto': 'Número de Proyectos'
    },
    title="Distribución Departamental de Energía Solar",
    hover_name="Departamento",  # Título destacado al señalar
    
)


fig.update_geos(
    fitbounds="locations", 
    visible=False,
    showcountries=True,      # Muestra fronteras nacionales
    countrycolor="Black",    # Color de la frontera de Colombia
    showcoastlines=True,     # Muestra la línea de costa
    coastlinecolor="RebeccaPurple", 
    showland=False,           # Pinta el fondo de la tierra
    showocean=True,          # Activa el color del mar
    oceancolor="LightBlue"   # Color del agua
)

fig.update_layout(
    height=650, 
    margin={"r":0,"t":30,"l":10,"b":0},
    paper_bgcolor="white",    # Color del fondo del "papel"
    title_font_color='darkblue' 
)


# Para Streamlit
st.plotly_chart(fig, use_container_width=True)

# Información adicional
col1, col2 = st.columns(2)
with col1:
    st.metric("Total Energía (kWh/año)", f"{df_solar['Energía [kWh/año]'].sum():,.0f}")
with col2:
    st.metric("Total Capacidad Instalada", f"{df_solar['Capacidad'].sum():,.2f} MW")

if st.checkbox("Ver datos por departamento"):
    st.dataframe(df_solar)