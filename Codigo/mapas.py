import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import os

st.set_page_config(page_title="Mapa Solar Colombia", layout="wide")

url_repo = "https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw/3aadedf47badbdac823b00dbe259f6bc6d9e1899/colombia.geo.json"

@st.cache_data
def load_json(url):
    response = requests.get(url)
    return response.json()

@st.cache_data
def get_data():
    # 1. Obtiene la ruta de la carpeta donde está ESTE archivo (mapas.py)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # 2. Construye la ruta subiendo un nivel y entrando a Documentos
    ruta = os.path.join(BASE_DIR, "..", "Documentos", "solar.csv")
    
    # Verificación de seguridad
    if not os.path.exists(ruta):
        st.error(f"Archivo no encontrado en la ruta calculada: {ruta}")
        st.stop()
        
    df = pd.read_csv(ruta)

    df['Departamento'] = df['Departamento'].astype(str).str.upper().str.strip()
    mapeo = {
        'BOGOTÁ': 'BOGOTA D.C.',
        'BOGOTA': 'BOGOTA D.C.',
        'BOGOTÁ D.C.': 'BOGOTA D.C.',
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
    showland=True,           # Pinta el fondo de la tierra
    landcolor="lightgrey",   # Color para departamentos sin datos
    showocean=True,          # Activa el color del mar
    oceancolor="LightBlue"   # Color del agua
)

fig.update_layout(
    height=650, 
    margin={"r":0,"t":30,"l":10,"b":0},
    paper_bgcolor="white",    # Color del fondo del "papel"
    title_font_color='darkblue' 
)

fig.update_geos(fitbounds="locations", visible=False)


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