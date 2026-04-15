import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
st.set_page_config(page_title="Mapa Solar Colombia", layout="wide")

url_repo = os.path.join(BASE_DIR, "..", "Documentos", "colombia.geo.json")

@st.cache_data
def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

@st.cache_data
def get_data():
    ruta = os.path.join(BASE_DIR, "..", "Documentos", "solar.csv")
    if not os.path.exists(ruta):
        st.error(f"Archivo no encontrado: {ruta}")
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
        'BOYACÁ' : 'BOYACA'
    }
    df['Departamento'] = df['Departamento'].replace(mapeo)
    return df

# Carga inicial
colombia_geojson = load_json(url_repo)
df_solar = get_data()

# Caja para escoger
lista_deptos = ["TODOS"] + sorted(df_solar['Departamento'].unique().tolist())
depto_seleccionado = st.selectbox("Selecciona un Departamento", lista_deptos)

# # Filtrado de datos
if depto_seleccionado != "TODOS":
    df_filtrado = df_solar[df_solar['Departamento'] == depto_seleccionado]
else:
    df_filtrado = df_solar

# Datos para el mapa de c
df_agrupado = df_filtrado.groupby('Departamento')['Energía [kWh/año]'].sum().reset_index()

st.title("☀️ Generación de Energía Solar en Colombia")
 

fig = px.choropleth( #Mapa de calor
    df_agrupado,
    geojson=colombia_geojson,
    locations="Departamento",
    featureidkey="properties.NOMBRE_DPT",
    color="Energía [kWh/año]",
    color_continuous_scale="Reds",
    hover_name="Departamento",
    hover_data={"Departamento": False, "Energía [kWh/año]": ":,.2f"},
    title="Distribución Regional de Energía"
)

fig.update_geos(fitbounds="locations", visible=False, showocean=True, oceancolor="LightBlue", showcountries=True)
fig.update_layout(height=600, margin={"r":0,"t":40,"l":0,"b":0})
st.plotly_chart(fig, use_container_width=True)

st.title("Mapa de globos")
fig2 = px.choropleth(
    df_solar,
    geojson=colombia_geojson,
    locations="Departamento",
    featureidkey="properties.NOMBRE_DPT",
    color_discrete_sequence=["#f0f0f0"], # Color gris muy claro para todos los dptos
    hover_name="Departamento",
)

# 2. AGREGAMOS los globos encima de esos departamentos
# Creamos el scatter y extraemos su "traza" (sus datos)
scatter_fig = px.scatter_geo(
    df_solar,
    geojson=colombia_geojson,
    locations="Departamento",
    featureidkey="properties.NOMBRE_DPT",
    size="Energía [kWh/año]",
    color="Departamento",
    hover_name="Proyecto" if "Proyecto" in df_solar.columns else "Departamento",
    size_max=35,
)

# Fusionamos: añadimos los globos de scatter_fig a nuestra base fig2
for trace in scatter_fig.data:
    fig2.add_trace(trace)

# 3. CONFIGURACIÓN DE LÍNEAS (Aquí es donde se dibujan los bordes)
fig2.update_traces(
    marker_line_width=1, 
    marker_line_color="black",
    selector=dict(type='choropleth') # Solo afecta a los bordes de los dptos
)

fig2.update_geos(
    fitbounds="locations", 
    visible=False,
    showland=True, 
    landcolor="white",
    showocean=True, 
    oceancolor="LightBlue",
    showcountries = True
)

fig2.update_layout(height=650, margin={"r":0,"t":40,"l":0,"b":0}, showlegend=False)

st.plotly_chart(fig2, use_container_width=True)


st.title("Mapa emisiones de CO2 evitadas")

fig3 = px.choropleth(
    df_solar,
    geojson=colombia_geojson,
    locations="Departamento",
    featureidkey="properties.NOMBRE_DPT",
    color="Emisiones CO2 [Ton/año]", 
    color_continuous_scale="Reds",
    hover_name="Departamento",
    hover_data={
        "Departamento": False,
        "Emisiones CO2 [Ton/año]": ":,.2f"
    },
    labels={'Emisiones CO2 [Ton/año]': 'CO2 (Ton/año)'},
)

fig3.update_geos(fitbounds="locations", visible=False, showocean=True, oceancolor="LightBlue", showcountries=True)
fig3.update_layout(height=600, margin={"r":0,"t":40,"l":0,"b":0})
st.plotly_chart(fig3, use_container_width=True)


#  #métricas
# st.divider()
# col1, col2 = st.columns(2)
# with col1:
#     st.metric(f"Total Energía {depto_seleccionado}", f"{df_filtrado['Energía [kWh/año]'].sum():,.0f} kWh/año")
# with col2:
#     st.metric("Capacidad Instalada", f"{df_filtrado['Capacidad'].sum():,.2f} MW")

# if st.checkbox("Mostrar tabla de datos"):
#     st.dataframe(df_filtrado, use_container_width=True)