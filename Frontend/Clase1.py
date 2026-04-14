import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
import altair as alt

# Configuración de la página
st.set_page_config(layout="centered", page_title="TalentoTech", page_icon=":bar_chart:")

st.title("📊 Análisis de datos - Transición energética")

# Header
t1, t2 = st.columns([0.5, 0.5])
t1.image('Frontend\Image_logo.png', width=300)
t2.markdown("""
### 👥 Equipo de trabajo
- Johan Ospina johanospina06@gmail.com
- Liliana Jimenez liajiza@gmail.com 
- Andi Jimenez ssebas8feb@gmail.com
- Alejandro Aristizabal upar1234@gmail.com
""")

# Tabs
tabs = st.tabs(["🏠 Inicio", "📂 Visualización de datos", "✅ Ver resultado", "🔅 Mapas de calor"])

# -------------------------------
# 🏠 PESTAÑA 1: INFORMACIÓN
# -------------------------------
with tabs[0]:
    st.header("📌 Proyecto: Transición energética y emisiones de CO₂")

    st.markdown("""
    ### 🌍 Contexto

    El cambio climático es uno de los mayores desafíos globales, y la reducción de emisiones de CO₂ 
    se ha convertido en una prioridad para gobiernos y sectores productivos. En este contexto, 
    la transición energética hacia fuentes renovables juega un papel fundamental.

    Colombia ha avanzado en la diversificación de su matriz energética, incorporando fuentes como 
    la energía solar y eólica. Sin embargo, aún existe una dependencia significativa de combustibles fósiles.

    ---
    """)

    st.markdown("""
    ### 🎯 Objetivo del proyecto

    Evaluar la existencia de una correlación entre la producción de energía solar y los cambios en las emisiones de CO₂, 
    con el fin de analizar cómo el aumento en la generación de energía solar contribuye a la reducción de la huella de carbono.

    ---
    """)

    st.markdown("""
    ### 📚 Estado del arte

    La transición energética implica el cambio desde sistemas basados en combustibles fósiles hacia sistemas más sostenibles 
    basados en energías renovables. Diversos estudios indican que:

    - Las energías renovables reducen la intensidad de carbono del sistema energético  
    - La energía solar ha tenido un crecimiento acelerado en la última década  
    - La reducción de emisiones no siempre es proporcional al crecimiento renovable, debido a factores como:
        - Aumento de la demanda energética  
        - Persistencia de fuentes fósiles  
        - Ineficiencias en la distribución energética  

    En Colombia, aunque la matriz energética tiene una alta participación hidroeléctrica, 
    la incorporación de energía solar es relativamente reciente, lo que plantea interrogantes 
    sobre su impacto real en la reducción de emisiones.

    ---
    """)

    st.markdown("""
    ### ⚙️ Metodología

    Para abordar este problema, el proyecto se desarrolla en las siguientes etapas:

    1. Limpieza y transformación de datos con Python  
    2. Integración de datasets (emisiones y producción energética)  
    3. Análisis exploratorio de datos  
    4. Evaluación de correlaciones  
    5. Visualización interactiva en Streamlit  

    ---
    """)

    st.markdown("""
    ### 📊 Hipótesis

    > El incremento en la producción de energía solar está asociado con una disminución en las emisiones de CO₂.

    ---
    """)

    st.markdown("""
    ### 💡 Valor del proyecto

    Este análisis permite:

    - Entender el impacto real de las energías renovables  
    - Apoyar la toma de decisiones en política energética  
    - Identificar oportunidades de mejora en la transición energética  

    ---
    """)

    st.markdown("""
    ### 📄 Referencias
                
    - Gobierno de Colombia. (s.f.). *Hoja de ruta de la transición energética en Colombia*.  
    Documento técnico de lineamientos para la transformación del sistema energético hacia fuentes sostenibles.

    - International Energy Agency (IEA). (2025). *Monthly Electricity Statistics*.  
    https://www.iea.org/data-and-statistics/data-product/monthly-electricity-statistics#documentation  

    - Datos Abiertos Colombia. (s.f.). *Meta FNCER: Incorporar nuevas fuentes de energía renovable en la matriz energética*.  
    https://www.datos.gov.co/Minas-y-Energ-a/Meta-FNCER-Incorporar-en-la-matriz-energ-tica-nuev/vy9n-w6hc/about_data  

    - Datos Abiertos Colombia. (s.f.). *Inventario Nacional de Gases de Efecto Invernadero*.  
    https://www.datos.gov.co/Ambiente-y-Desarrollo-Sostenible/Inventario-Nacional-Gases-Efecto-Invernadero/6rff-a5ep/about_data  
    """)



# -------------------------------
# 📂 PESTAÑA 2: SUBIR Y VER DATOS
# -------------------------------
with tabs[1]:
    st.header("📂 Visualización de dataset")

    archivo = st.file_uploader("Sube tu archivo CSV", type=["csv"])

    if archivo is not None:
        try:
            df = pd.read_csv(archivo, encoding='utf-8')
        except:
            df = pd.read_csv(archivo, encoding='latin-1')

        st.success("Archivo cargado correctamente ✅")

        st.subheader("🔍 Vista previa de los datos")
        st.dataframe(df.head(10))

        st.subheader("📊 Información del dataset")
        st.write("Filas:", df.shape[0])
        st.write("Columnas:", df.shape[1])

        st.subheader("🧾 Tipos de datos")
        st.write(df.dtypes)


# -------------------------------
# 📊 PESTAÑA 3: VER RESULTADOS
# -------------------------------
with tabs[2]:
    st.header("✅ Ver resultado")

    # Cargar tabla_resumen desde la carpeta Codigo
    path_tabla = "C:\\Users\\USUARIO\\Documents\\Datos\\Bootcamp\\Bootcamp2026-1\\Codigo\\tabla_resumen.csv"
    try:
        tabla_resumen = pd.read_csv(path_tabla, encoding='utf-8')
    except FileNotFoundError:
        st.error(f"No se encontró el archivo: {path_tabla}")
        tabla_resumen = pd.DataFrame()
    except Exception:
        tabla_resumen = pd.read_csv(path_tabla, encoding='latin-1')

    # Filtrar solo las categorías principales (Renovable / No Renovable)
    if not tabla_resumen.empty and "Product" in tabla_resumen.columns:
        tabla_resumen = tabla_resumen[tabla_resumen["Product"].isin(["Renovable", "No Renovable"])]

    st.subheader("♻️ Renovables Vs Fósiles")
    st.dataframe(tabla_resumen)

    st.subheader("⛅ Evolución temporal de energía")
    # Cargar datos_final para gráfica de líneas
    path_datos = "C:\\Users\\USUARIO\\Documents\\Datos\\Bootcamp\\Bootcamp2026-1\\Codigo\\datos_final.csv"
    try:
        datos_final = pd.read_csv(path_datos, encoding='utf-8')
    except FileNotFoundError:
        st.error(f"No se encontró el archivo: {path_datos}")
        datos_final = pd.DataFrame()
    except Exception:
        datos_final = pd.read_csv(path_datos, encoding='latin-1')

    if not datos_final.empty and "Time" in datos_final.columns:
        # Convertir Time a datetime
        datos_final["Time"] = pd.to_datetime(datos_final["Time"])

        # Agrupar por mes y producto
        df_lineas = datos_final.groupby([datos_final["Time"].dt.to_period("M"), "Product"])["Value"].sum().reset_index()
        df_lineas["Time"] = df_lineas["Time"].dt.to_timestamp()

        # Filtrar solo Renovable y No Renovable
        df_lineas = df_lineas[df_lineas["Product"].isin(["Renovable", "No Renovable"])]

        line_chart = alt.Chart(df_lineas).mark_line(point=True).encode(
            x=alt.X("Time:T", title="Fecha"),
            y=alt.Y("Value:Q", title="Valor (GWh)"),
            color=alt.Color("Product:N", legend=alt.Legend(orient="bottom")),
            tooltip=["Time:T", "Product:N", "Value:Q"]
        ).properties(height=300)

        st.altair_chart(line_chart, use_container_width=True)
    else:
        st.write("No se pudieron cargar los datos para la gráfica de líneas")

    st.markdown("### <div style='text-align: center;'>Distribución renovable vs no renovable</div>", unsafe_allow_html=True)
    cols = st.columns([3,2])
    
    with cols[1].container(border=True, height="stretch"):

        st.altair_chart(
        alt.Chart(tabla_resumen)
        .mark_bar()
        .encode(
            alt.X("Product:N").title("Tipo de Energía"),
            alt.Y("Value:Q").title("Valor (GWh)"),
            alt.Color("Product:N", legend=alt.Legend(orient="bottom")),
            tooltip=["Product:N", "Value:Q", "Unit:N"]
        )
        .properties(height=300)
    )

    with cols[0].container(border=True, height="stretch"):

        chart = alt.Chart(tabla_resumen).mark_arc().encode(
            theta=alt.Theta("Value:Q"),
            color=alt.Color("Product:N", legend=alt.Legend(orient="bottom")),
            tooltip=["Product:N", "Value:Q"]
        )

        st.altair_chart(chart, use_container_width=True)

    st.markdown("### Gráfico de barras horizontal de energías renovables")
    df_renovables = pd.read_csv("C:\\Users\\USUARIO\\Documents\\Datos\\Bootcamp\\Bootcamp2026-1\\df_solo_renovables.csv")
    df_renovables_agrupado = df_renovables.groupby("Product")["Value"].sum().reset_index()
    
    # Mapear nombres a español
    mapeo_productos = {
        "Geothermal": "Geotérmica",
        "Other Renewables": "Otras Renovables",
        "Hydro": "Hidroelectrica",
        "Combustible Renewables": "Combustible Renovables",
        "Solar": "Solar",
        "Wind": "Eólico"
    }
    df_renovables_agrupado["Product"] = df_renovables_agrupado["Product"].map(mapeo_productos)
    
    chart = alt.Chart(df_renovables_agrupado).mark_bar().encode(
        alt.X("Value:Q").title("Valor (GWh)"),
        alt.Y("Product:N").title("Tipo de Energía"),
        alt.Color("Product:N", scale=alt.Scale(scheme="category10"), legend=alt.Legend(orient="bottom")),
        tooltip=["Product:N", "Value:Q"]
    ).properties(height=400).configure_axis(grid=True).configure_view(strokeWidth=0)
    
    st.altair_chart(chart, use_container_width=True)


    st.markdown("### Evolución temporal de energías renovables")
    # Cargar datos para gráfica de líneas
    datos_final = pd.read_csv("C:\\Users\\USUARIO\\Documents\\Datos\\Bootcamp\\Bootcamp2026-1\\df_solo_renovables.csv")
    
    if not datos_final.empty and "Time" in datos_final.columns:
        # Convertir Time a datetime
        datos_final["Time"] = pd.to_datetime(datos_final["Time"])
        
        # Agrupar por fecha y producto (mantener cada tipo de energía por separado)
        df_lineas = datos_final.groupby(["Time", "Product"])["Value"].sum().reset_index()
        
        # Mapear nombres a español
        mapeo_productos = {
            "Geothermal": "Geotérmica",
            "Other Renewables": "Otras Renovables",
            "Hydro": "Hidroelectrica",
            "Combustible Renewables": "Combustible Renovables",
            "Solar": "Solar",
            "Wind": "Eólico"
        }
        df_lineas["Product"] = df_lineas["Product"].map(mapeo_productos)
        
        # Crear gráfico de líneas general
        line_chart = alt.Chart(df_lineas).mark_line(point=True).encode(
            x=alt.X("Time:T", title="Fecha"),
            y=alt.Y("Value:Q", title="Valor (GWh)"),
            color=alt.Color("Product:N", scale=alt.Scale(scheme="category10"), legend=alt.Legend(orient="bottom")),
            tooltip=["Time:T", "Product:N", "Value:Q"]
        ).properties(height=400).configure_axis(grid=True)
        
        st.altair_chart(line_chart, use_container_width=True)

        st.markdown("### Evolución temporal sin Hydro")
        df_lineas_sin_hydro = df_lineas[df_lineas["Product"] != "Hidroelectrica"]

        line_chart_sin_hydro = alt.Chart(df_lineas_sin_hydro).mark_line(point=True).encode(
            x=alt.X("Time:T", title="Fecha"),
            y=alt.Y("Value:Q", title="Valor (GWh)"),
            color=alt.Color("Product:N", scale=alt.Scale(scheme="category10"), legend=alt.Legend(orient="bottom")),
            tooltip=["Time:T", "Product:N", "Value:Q"]
        ).properties(height=400).configure_axis(grid=True)

        st.altair_chart(line_chart_sin_hydro, use_container_width=True)
    else:
        st.warning("No se pudieron cargar los datos para la gráfica de líneas")

#Pestaña 4: Mapa de calor
with tabs[3]:
    st.header("🔅 Mapas de calor")

    archivo2 = st.file_uploader("Sube tu dataset para graficar", type=["csv"], key="grafico")

    if archivo2 is not None:

        # Leer archivo con manejo de encoding
        try:
            df = pd.read_csv(archivo2, encoding='utf-8')
        except:
            df = pd.read_csv(archivo2, encoding='latin-1')

        st.subheader("Vista previa")
        st.dataframe(df.head())

        columnas = df.columns.tolist()

        # Selección de columnas
        col_x = st.selectbox("Selecciona la columna para el eje X", columnas)
        col_y = st.selectbox("Selecciona la columna para el eje y", columnas)

        # Detectar columnas numéricas
        numericas = df.select_dtypes(include=np.number).columns.tolist()

