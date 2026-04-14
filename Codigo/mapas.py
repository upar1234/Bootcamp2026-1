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
        'BOGOTÁ': 'SANTAFE DE BOGOTA D.C',
        'BOGOTA': 'SANTAFE DE BOGOTA D.C',
        'BOGOTÁ D.C.': 'SANTAFE DE BOGOTA D.C',
        'VALLE DEL CAUCA': 'VALLE DEL CAUCA',
        'NARIÑO': 'NARINO',
        'ATLÁNTICO': 'ATLANTICO',
        'BOLÍVAR': 'BOLIVAR',
        'NORTE DE SANTANDER': 'NORTE DE SANTANDER',
        'QUINDÍO': 'QUINDIO',
        'CÓRDOBA':'CORDOBA',
        'CHOCÓ':'CHOCO',
        'GUAINÍA' : 'GUAINIA',
        'BOYACÁ' : 'BOYACA',
        'ARCHIPIÉLAGO DE SAN ANDRÉS, PROVIDENCIA Y SANTA CATALINA' : 'ARCHIPIELAGO DE SAN ANDRES PROVIDENCIA Y SANTA CATALINA'
    }
    df['Departamento'] = df['Departamento'].replace(mapeo)
    return df

colombia_geojson = load_json(url_repo)
df_solar = get_data()
departamentos = df_solar[['Departamento', 'Energía [kWh/año]']]
departamentos = departamentos.groupby('Departamento').sum().reset_index()

# departamentos.columns = ['Departamento', 'Energia']

# Interfaz 
st.title("☀️ Generación de Energía Solar en Colombia")
st.markdown("Visualización basada en proyectos solares activos y estimados.")
# st.write("Departamentos detectados en CSV:", df_solar['Departamento'].unique()[:33])
# st.write("Departamentos detectados en GeoJSON:", [feature['properties']['NOMBRE_DPT'] for feature in colombia_geojson['features']][:25])
st.title("🎈 Mapa de Proyectos Solares (Burbujas)")
st.markdown("Cada globo representa un proyecto. El tamaño indica la energía generada.")

st.sidebar.header("Filtros de Búsqueda")
# Lista de departamentos únicos del CSV
lista_deptos = ["TODOS"] + sorted(df_solar['Departamento'].unique().tolist())


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

# --- CREACIÓN DEL MAPA DE GLOBOS (SCATTER GEO) ---
# Nota: Para que los puntos se ubiquen bien, tu CSV debería tener columnas 'Latitud' y 'Longitud'.
# Si no las tiene, Plotly usará los nombres de los departamentos, pero los globos quedarán en el centro de cada dpto.

fig2 = px.scatter_geo(
    df_solar,
    locations="Departamento",        
    geojson=None,                    # No necesita GeoJSON obligatorio para puntos básicos
    color="Departamento",            # Color diferente por departamento
    size="Energía [kWh/año]",       # El tamaño del globo depende de la energía
    hover_name="Proyecto" if "Proyecto" in df_solar.columns else "Departamento",
    hover_data=["Capacidad", "Energía [kWh/año]"],
    size_max=30,                     # Ajusta el tamaño máximo de los globos
    template="plotly_white",
    title="Proyectos Solares por Capacidad"
)

# Enfocar el mapa en Colombia
fig2.update_geos(
    lataxis_range=[ -4, 13], 
    lonaxis_range=[-82, -67],
    visible=False, 
    showland=True, 
    landcolor="LightGreen",
    showocean=True, 
    oceancolor="LightBlue",
    showcountries=True
)

fig.update_layout(height=700, margin={"r":0,"t":50,"l":0,"b":0})
fig2.update_layout(height=700, margin={"r":0,"t":50,"l":0,"b":0})

st.plotly_chart(fig, use_container_width=True)
st.plotly_chart(fig2, use_container_width=True)


# Para Streamlit

depto_seleccionado = st.selectbox("Selecciona un Departamento", lista_deptos)

# Información adicional
col1, col2 = st.columns(2)
with col1:
    st.metric("Total Energía (kWh/año)", f"{df_solar['Energía [kWh/año]'].sum():,.0f}")
with col2:
    st.metric("Total Capacidad Instalada", f"{df_solar['Capacidad'].sum():,.2f} MW")

if st.checkbox("Ver datos por departamento"):
    st.dataframe(df_solar)

st.write(departamentos)