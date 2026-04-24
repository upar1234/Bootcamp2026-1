import numpy as np
import json
import plotly.express as px
import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
import altair as alt
import statsmodels.api as sm
from scipy.stats import shapiro
import os
import altair as alt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ruta_colombia=os.path.join(BASE_DIR,"..", "Documentos", "colombia.csv")
ruta_solar=os.path.join(BASE_DIR,"..", "Documentos", "solar.csv")
ruta_renovables=os.path.join(BASE_DIR,"..", "df_solo_renovables.csv")
ruta_tabla_resumen=os.path.join(BASE_DIR,"..","Codigo", "tabla_resumen.csv")
ruta_datos_final=os.path.join(BASE_DIR,"..","Codigo", "datos_final.csv")

# Configuración de la página
st.set_page_config(layout="centered", page_title="TalentoTech", page_icon=":bar_chart:")

st.title("📊 Análisis de datos - Transición energética")

# Header
t1, t2 = st.columns([0.5, 0.5])
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(BASE_DIR, "Image_logo.png") 
t1.image(logo_path, width=300)
# t1.image('Frontend\/Image_logo.png', width=300)
t2.markdown("""
### 👥 Equipo de trabajo
- Johan Ospina johanospina06@gmail.com
- Liliana Jiménez liajiza@gmail.com 
- Andi Jiménez ssebas8feb@gmail.com
- Alejandro Aristizabal upar1234@gmail.com
""")

# Tabs
tabs = st.tabs(["🏠 Inicio", "📂 Bases de datos", "⚡ Producción de Energía", "🔅 Atlas Solar","📈 Análisis Descriptivo"])

# -------------------------------
# 🏠 PESTAÑA 1: INICIO
# -------------------------------
with tabs[0]:
    st.header("📌 Proyecto: Análisis de Energía Solar y Emisiones de CO2 Evitadas - Un Enfoque de Datos para la Transición Energética Justa.")

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

    - International Energy Agency (IEA). (2025). *Monthly Electricity Statistics*:
     _Producción de Energía en Colombia_. 
    https://www.iea.org/data-and-statistics/data-product/monthly-electricity-statistics#documentation  

    - Datos Abiertos Colombia. (s.f.). *Meta FNCER: Incorporar nuevas fuentes de energía renovable en la matriz energética*:
     _Proyectos de Energía Solar en Colombia_.
    https://www.datos.gov.co/Minas-y-Energ-a/Meta-FNCER-Incorporar-en-la-matriz-energ-tica-nuev/vy9n-w6hc/about_data  

    - Datos Abiertos Colombia. (s.f.). *Inventario Nacional de Gases de Efecto Invernadero*.  
    https://www.datos.gov.co/Ambiente-y-Desarrollo-Sostenible/Inventario-Nacional-Gases-Efecto-Invernadero/6rff-a5ep/about_data  
    """)



# -------------------------------
# 📂 PESTAÑA 2: Bases de datos
# -------------------------------
with tabs[1]:
    st.header("📂 Bases de datos")

   ## Colombia
    archivo1 = ruta_colombia

    if archivo1 is not None:
        try:
            df = pd.read_csv(archivo1, encoding='utf-8')
        except:
            df = pd.read_csv(archivo1, encoding='latin-1')

        st.subheader("🔍 Vista previa de la base de datos:  _Producción de Energía en Colombia_")
        st.dataframe(df.head(10))

        cols = st.columns([3,3])
        with cols[1].container(border=True, height="stretch"):
            st.subheader("📊 Información del dataset")
            st.write("Filas:", df.shape[0])
            st.write("Columnas:", df.shape[1])
        with cols[0].container(border=True, height="stretch"):
            st.subheader("🧾 Tipos de datos")
            st.write(df.dtypes)
   
   ## Solar
   # archivo = st.file_uploader("Sube tu archivo CSV", type=["csv"])
    archivo2 = ruta_solar

    if archivo2 is not None:
        try:
            df = pd.read_csv(archivo2, encoding='utf-8')
        except:
            df = pd.read_csv(archivo2, encoding='latin-1')


        st.subheader("🔍 Vista previa de la base de datos:  _Proyectos de Energía Solar en Colombia_")
        st.dataframe(df.head(10))
        cols = st.columns([3,3])
        with cols[1].container(border=True, height="stretch"):
            st.subheader("📊 Información del dataset")
            st.write("Filas:", df.shape[0])
            st.write("Columnas:", df.shape[1])

        with cols[0].container(border=True, height="stretch"):
            st.subheader("🧾 Tipos de datos")
            st.write(df.dtypes)

        ##Dicionario de variables
        # --- ESTRUCTURA DE DATOS CON FUENTES ASIGNADAS ---
    DATA = {
        
        "Producción de Energía en Colombia": {
            "fuente_full": "Producción de Energía en Colombia",
            "color": "#007BFF", # Azul
            "variables": {
                "Country": "Pais.",
                "Balance": "Cubrimiento de la oferta de electricidad en un país.",
                "Time": "Fecha de la toma de la medida.",
                "Product": "Tipo de energía.",
                "Value": "Valor de la energía.",
                "Unit": "Unidad en la que se mide la energía GW/H.",
                "Producción Neta (NETPROD)": "Electricidad real que sale de las centrales hacia la red, neta de consumos propios.",
                "Importaciones / Exportaciones": "Flujo de energía transfronterizo. El tránsito se reporta en ambas categorías.",
                "Bombeo (EPUMPST)": "Energía usada para mover agua a embalses superiores (almacenamiento mecánico).",
                "Pérdidas de Distribución (DISTLOSS)": "Energía disipada en el transporte (calor en cables y transformadores).",
                "Consumo Final Calculado (TFC_ENGY_CALC)": "Balance: Producción + Importaciones - Exportaciones - Bombeo - Pérdidas.",
                "Combustibles Fósiles Totales": "Generación total basada en recursos no renovables (Carbón + Gas + Petróleo).",
                "Carbón (COAL)": "Energía proveniente de carbón mineral y gases de procesos industriales.",
                "Petróleo y Derivados (OIL_TOTAL)": "Uso de crudo, fueloil o gases de refinería para generación eléctrica.",
                "Gas Natural (NATURAL_GAS)": "Generación basada en gas metano, combustible clave en la transición.",
                "Otros No Renovables": "Quema de residuos industriales o desechos municipales no biológicos.",
                "Renovables Totales": "Suma de todas las fuentes limpias (Hidro, Viento, Solar, Geotérmica, Biomasa).",
                "Hidroeléctrica (HYDRO)": "Energía del agua. Es la base principal de la matriz colombiana.",
                "Eólica (WIND)": "Energía del viento capturada por aerogeneradores onshore u offshore.",
                "Solar (SOLAR)": "Generación fotovoltaica o térmica a partir de radiación solar.",
                "Geotérmica (GEOTHERMAL)": "Energía del calor interno de la tierra.",
                "Renovables Combustibles": "Biomasa sólida, biocombustibles líquidos o biogás orgánico.",
                "Nuclear (NUCLEAR)": "Generación eléctrica mediante procesos de fisión atómica.",
                "No Especificado": "Cualquier otra fuente de energía no clasificada en las categorías anteriores."
            }
        },
        "Proyectos de Energía Solar en Colombia": {
            "fuente_full": "Proyectos de Energía Solar en Colombia",
            "color": "#28a745", # Verde
            "variables": {
                "Proyecto": "Identificador de cada uno de los proyectos que hacen parte de las metas en cada corte reportado",
                "Tipo": "Identifica la fuente primaria (Solar, Eólica, Biomasa). Es el pilar de la descarbonización.",
                "Capacidad [MW]": "Potencia neta real entregable. Es la medida de magnitud del proyecto ante el SIN.",
                "Departamento": "Nombre del departamento del proyecto referenciado",
                "Municipio": "Nombre del municipio del proyecto referenciado, para proyectos grandes se toma el municipio principal",
                "Código Departamento": "Código del Departamento de acuerdo a DIVIPOLA",
                "Código Municipio": "Código del Municipio de acuerdo a DIVIPOLA",
                "Fecha estimada FPO": "Fecha de Puesta en Operación. Hito donde el proyecto inicia su vida útil comercial.",
                "Energía [kWh/día]": "Estimación de generación diaria usando factores de eficiencia (0.2 solar / 0.4 otros).",
                "Usuarios": "Impacto social: familias beneficiadas según consumo de subsistencia (173 kWh/mes).",
                "Inversión estimada [COP]": "Valor capital del proyecto calculado proporcionalmente a su capacidad instalada.",
                "Empleos estimados": "Proyección de mano de obra directa para las fases de construcción y operación.",
                "Emisiones CO2 [Ton/año]": "Beneficio ambiental: toneladas de gases de efecto invernadero evitadas anualmente."
            }
        }
    }

    # --- INTERFAZ ---

    st.title("📖 Diccionario de Variables")
    st.markdown("---")

    # 1. Agrupador por Fuente
    st.subheader("📁 Seleccione la Fuente de Datos")
    fuente_sel = st.pills(
        "Fuente de información:",
        options=list(DATA.keys()),
        default=list(DATA.keys())[0]
    )

    # Mostrar la descripción de la fuente seleccionada
    st.caption(f"**Fuente:** {DATA[fuente_sel]['fuente_full']}")

    # Layout de columnas
    col_nav, col_info = st.columns([1, 2.2], gap="large")

    with col_nav:
        st.subheader("🔍 Variables")
        # El radio button se filtra según la fuente elegida
        opcion = st.radio(
            "Seleccione un término:",
            options=list(DATA[fuente_sel]["variables"].keys()),
            label_visibility="collapsed"
        )

    with col_info:
        st.subheader("📋 Definición Metodológica")
        
        # Color dinámico según la fuente
        color_tarjeta = DATA[fuente_sel]["color"]
        
        with st.container(border=True):
            st.markdown(f"<h2 style='color: {color_tarjeta}; margin-bottom: 0;'>{opcion}</h2>", unsafe_allow_html=True)
            st.write(f"**Origen de datos:** {fuente_sel}")
            st.write("---")
            
            # Descripción llamativa
            desc_texto = DATA[fuente_sel]["variables"][opcion]
            st.info(f"**Definición:**\n\n{desc_texto}")
            
            st.markdown(f"<p style='font-size: 0.8rem; opacity: 0.7;'>Metodología alineada con: {DATA[fuente_sel]['fuente_full']}</p>", unsafe_allow_html=True)

    # --- VISTA GLOBAL SIEMPRE DESPLEGADA ---
    st.divider()
    st.subheader("📚 Vista General del Diccionario")

    for fuente, info in DATA.items():
        with st.expander(f"Ver todas las variables de: {fuente}", expanded=True):
            st.markdown(f"**Contexto:** *{info['fuente_full']}*")
            for var, desc in info["variables"].items():
                c1, c2 = st.columns([1, 3])
                c1.markdown(f"**{var}**")
                c2.write(desc)
                st.markdown("<hr style='margin:0; border:0.1px solid #f9f9f9'>", unsafe_allow_html=True)

# -------------------------------
# 📊 PESTAÑA 3: Producción de Energía
# -------------------------------
with tabs[2]:
    st.header("⚡Producción de Energía")

    # Cargar tabla_resumen desde la carpeta Codigo
    path_tabla = ruta_tabla_resumen
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

    st.subheader("♻️ Renovables Vs No Renovable")
    st.dataframe(tabla_resumen)

    st.subheader("⛅ Evolución temporal de energía")
    # Cargar datos_final para gráfica de líneas
    path_datos = ruta_datos_final
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
    
        # 1. Crear las columnas para el texto y la posición central vertical
        tabla_resumen["Label"] = tabla_resumen["Value"].map("{:,.1f} GWh".format)
        tabla_resumen["ValueMid"] = tabla_resumen["Value"] / 2

        # 2. Definir la base del gráfico (El eje X se comparte)
        base = alt.Chart(tabla_resumen).encode(
            alt.X("Product:N").title("Tipo de Energía")
        )

        # 3. Capa de las barras (Usan el valor total en Y)
        bars = base.mark_bar().encode(
            alt.Y("Value:Q").title("Valor (GWh)"),
            alt.Color("Product:N", legend=alt.Legend(orient="bottom", title=None)),
            tooltip=["Product:N", "Value:Q", "Unit:N"]
        )

        # 4. Capa del texto centrado (Usan la mitad del valor en Y)
        text = base.mark_text(
            align='center',
            baseline='middle',
            size=14,
            fontWeight="bold",
            color="white"
        ).encode(
            alt.Y("ValueMid:Q"), # Posición en la mitad de la barra vertical
            text=alt.Text("Label:N")
        )

        # 5. Combinar capas y renderizar
        chart = alt.layer(bars, text).properties(
            height=300, padding={"top": 30, "left": 60, "right": 60, "bottom": 10}
        ).configure_view(
            strokeWidth=0
        )

        st.altair_chart(chart, use_container_width=True)

    with cols[0].container(border=True, height="stretch"):
    # 1. Aseguramos el cálculo del porcentaje
        tabla_resumen["Porcentaje"] = (tabla_resumen["Value"] / tabla_resumen["Value"].sum()) * 100
        
        # Base compartida para que el texto y el arco coincidan perfectamente
        base = alt.Chart(tabla_resumen).encode(
            theta=alt.Theta("Value:Q", stack=True)
        )

        # El arco (La torta)
        chart = base.mark_arc(outerRadius=120).encode(
            color=alt.Color("Product:N", legend=alt.Legend(orient="bottom")),
            tooltip=["Product:N", "Value:Q", alt.Tooltip("Porcentaje:Q", format=".1f")]
        )

        # El texto (Corregido)
        text = base.mark_text(
            radius=85,          # Radio donde se ubica el texto
            size=18, 
            fontWeight="bold", 
            fill="white"
        ).encode(
            # El formato '.1f' es para un decimal, y agregamos el '%' literal al final
            text=alt.Text("Porcentaje:Q", format=".1f") 
        )

        tabla_resumen["Label"] = tabla_resumen["Porcentaje"].map("{:.1f}%".format)
        
        # Versión final usando la columna 'Label' para evitar errores de formato
        text = base.mark_text(radius=80, size=18, fontWeight="bold", fill="white").encode(
            text=alt.Text("Label:N") # N de Nominal/Texto
        )

        st.altair_chart(alt.layer(chart, text).properties(height=300, padding={"top": 30, "left": 10, "right": 10, "bottom": 10}), use_container_width=True)


    st.markdown("### Gráfico de barras horizontal de energías renovables")
    df_renovables = pd.read_csv(ruta_renovables)
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
    # 1. Ordenamos el DataFrame explícitamente de mayor a menor
    df_renovables_agrupado = df_renovables_agrupado.sort_values(by="Value", ascending=False)
    # 2. Guardamos ese orden exacto en una lista
    orden_categorias = df_renovables_agrupado["Product"].tolist()
    # --------------------------
    cutoff = 150000  # Límite para decidir si va adentro o afuera

    # Crear la columna de formato de texto (Única columna extra que necesitamos)
    df_renovables_agrupado["Label"] = df_renovables_agrupado["Value"].map("{:,.1f} GWh".format)

    # 2. Definir la base del gráfico compartida
    base = alt.Chart(df_renovables_agrupado).encode(
        alt.Y("Product:N", sort=alt.EncodingSortField(field="Value", order="descending")).title("Tipo de Energía")
    )

    # 3. Capa de las barras
    bars = base.mark_bar().encode(
        alt.X("Value:Q").title("Valor (GWh)"),
        alt.Color("Product:N", scale=alt.Scale(scheme="category10"), legend=alt.Legend(orient="bottom", title=None)),
        tooltip=["Product:N", "Value:Q"]
    )

    # 4. Capa de texto para barras LARGAS (Texto por DENTRO)
    text_inside = base.mark_text(
        align='right',     # Justificado a la derecha
        baseline='middle',
        dx=-5,             # Empujado 5px hacia la izquierda (adentro de la barra)
        size=14,
        fontWeight="bold",
        color="white"      # Blanco para que contraste con el color de la barra
    ).encode(
        alt.X("Value:Q"),
        text=alt.Text("Label:N")
    ).transform_filter(
        alt.datum.Value > cutoff # Filtramos: Solo se dibuja si el valor es mayor al límite
    )

    # 5. Capa de texto para barras CORTAS (Texto por FUERA)
    text_outside = base.mark_text(
        align='left',      # Justificado a la izquierda
        baseline='middle',
        dx=5,              # Empujado 5px hacia la derecha (afuera de la barra)
        size=14,
        fontWeight="bold",
        color="#333333"    # Gris oscuro/Negro para que contraste con el fondo blanco de la pantalla
    ).encode(
        alt.X("Value:Q"),
        text=alt.Text("Label:N")
    ).transform_filter(
        alt.datum.Value <= cutoff # Filtramos: Solo se dibuja si el valor es menor o igual al límite
    )

    # 6. Combinar todas las capas (Barras + Texto Adentro + Texto Afuera)
    chart_final = alt.layer(bars, text_inside, text_outside).properties(
        height=400
    ).configure_axis(
        grid=True
    ).configure_view(
        strokeWidth=0
    )

    st.altair_chart(chart_final, use_container_width=True)

    st.markdown("### Evolución temporal de energías renovables")
    # Cargar datos para gráfica de líneas
    datos_final = pd.read_csv(ruta_renovables)
    
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

        st.markdown("### Evolución temporal sin Hidroeléctrica")
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
    st.header("🔅 Atlas Solar")

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


# -------------------------------
# 📊 PESTAÑA 5: Análisis Descriptivo
# -------------------------------
with tabs[4]:
    st.header("📈 Análisis Descriptivo")
    # --- 1. CONFIGURACIÓN INICIAL Y RUTA DE DATOS ---
    # Usar barra normal (/) evita errores de lectura de rutas en Python
    #RUTA_DATOS = "Documentos\\solar.csv" 

    st.set_page_config(page_title="Análisis Energético y de CO2", layout="wide")

    st.subheader("🍀 Análisis de Energía y Emisiones Evitadas de CO2")
    st.markdown("""
    Esta aplicación recrea el análisis de normalidad, dispersión y el modelo de regresión lineal 
    para los factores de Energía Solar generada y el CO2 desplazado (evitado).
    """)

    # --- 2. LECTURA DE DATOS ---
    @st.cache_data
    def cargar_datos(ruta):
        if ruta.endswith('.csv'):
            return pd.read_csv(ruta)
        else:
            return pd.read_excel(ruta)

    try:
        df_clean = cargar_datos(ruta_solar)
        
        # --- SECCIÓN 1: HISTOGRAMAS POR APARTE ---
        st.header("1. Distribución de las Variables")
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Histograma: Energía Solar")
            fig_en, ax_en = plt.subplots()
            sns.histplot(df_clean['Energía [kWh/año]'], kde=True, color="royalblue", ax=ax_en)
            ax_en.set_title("Energía [kWh/año]")
            st.pyplot(fig_en, clear_figure=True)
            
            stat, p = shapiro(df_clean['Energía [kWh/año]'].dropna())
            st.write(f"**P-valor (Shapiro):** {p:.4e}")

        with col2:
            st.subheader("Histograma: CO2 Evitado")
            fig_co2, ax_co2 = plt.subplots()
            sns.histplot(df_clean['Emisiones CO2 [Ton/año]'], kde=True, color="firebrick", ax=ax_co2)
            ax_co2.set_title("Emisiones CO2 Evitadas [Ton/año]")
            st.pyplot(fig_co2, clear_figure=True)
            
            stat, p = shapiro(df_clean['Emisiones CO2 [Ton/año]'].dropna())
            st.write(f"**P-valor (Shapiro):** {p:.4e}")

        # --- SECCIÓN 2: DISPERSIÓN Y REGRESIÓN ---
        st.header("2. Modelo de Regresión Lineal")
        
        X = sm.add_constant(df_clean['Energía [kWh/año]'].dropna())
        y = df_clean['Emisiones CO2 [Ton/año]'].dropna()
        model = sm.OLS(y, X).fit()
        
        fig_reg, ax_reg = plt.subplots(figsize=(10, 5))
        sns.regplot(x='Energía [kWh/año]', y='Emisiones CO2 [Ton/año]', data=df_clean, 
                    ax=ax_reg, line_kws={"color": "red"}, scatter_kws={'color': 'royalblue'})
        ax_reg.set_title("Ajuste Lineal: Energía Solar vs CO2 Evitado")
        st.pyplot(fig_reg, clear_figure=True)

        # Variables del modelo
        intercepto = model.params.iloc[0] 
        pendiente = model.params.iloc[1]  
        r2 = model.rsquared

        st.markdown("---")
        st.header("📊 Resultados del Modelo Descriptivo")

        # 1. Tarjeta principal resaltada con la ecuación actualizada
        st.success(f"**Ecuación Matemática:** CO₂ Evitado = ({pendiente:.5f} × Energía) + {intercepto:.4f}")

        # 2. Métricas Clave
        col1, col2, col3 = st.columns(3)
        col1.metric(label="Precisión del Modelo (R²)", value=f"{r2 * 100:.1f}%")
        col2.metric(label="Factor de Desplazamiento", value=f"{pendiente:.4f}", delta="Ton CO₂ / kWh", delta_color="off")
        
        p_valor_energia = model.pvalues.iloc[1]
        es_significativo = "Sí" if p_valor_energia < 0.05 else "No"
        col3.metric(label="Estadísticamente Significativo", value=es_significativo)

        # 3. Tabla de coeficientes
        st.markdown("#### 🔍 Detalle de los Parámetros")
        
        tabla_coeficientes = pd.DataFrame({
            "Variable": ["Constante (Base)", "Energía [kWh/año]"],
            "Valor (Coeficiente)": [intercepto, pendiente],
            "P-Valor": [model.pvalues.iloc[0], model.pvalues.iloc[1]],
            "Interpretación": [
                "Ahorro base (teórico)", 
                "Aumento del ahorro de CO₂ por cada 1 kWh extra"
            ]
        })
        
        st.dataframe(
            tabla_coeficientes.style.format({
                "Valor (Coeficiente)": "{:.5f}",
                "P-Valor": "{:.5f}"
            }),
            use_container_width=True,
            hide_index=True
        )

        # 4. Insight de negocio
        if r2 > 0.99:
            st.info("💡 **Insight Analítico:** Un R² de 1.000 indica una relación determinista. Esto confirma que los datos de Emisiones representan un cálculo teórico donde se aplica un factor de desplazamiento de red al consumo de energía, más que mediciones físicas directas de sensores.")

        # --- SECCIÓN 3: IMPACTO AMBIENTAL ---
        st.header("🌱 Impacto Ambiental: Resumen del Proyecto")

        arboles_equivalentes = (pendiente * df_clean['Energía [kWh/año]'].sum()) / 0.02

        col_kpi1, col_kpi2, col_kpi3 = st.columns(3)

        with col_kpi1:
            st.metric("Factor de Ahorro Red", f"{pendiente:.4f} Ton/kWh", help="CO2 evitado de la matriz fósil por cada kWh solar")

        with col_kpi2:
            total_ahorro = df_clean['Emisiones CO2 [Ton/año]'].sum()
            st.metric("Ahorro Total de los Proyectos", f"{total_ahorro:,.2f} Ton", delta="CO₂ Evitadas", delta_color="normal", help="Suma total de toneladas de CO₂ mitigadas de todos los proyectos. Representa el impacto ambiental acumulado de toda la energía solar generada en la muestra.")

        with col_kpi3:
            st.metric("Equivalencia en Bosque", f"{int(arboles_equivalentes):,} Árboles", help="Árboles necesarios para absorber el mismo CO2 en un año")

        st.success(f"""
        💡 **Análisis Técnico:** El modelo confirma que por cada **1 kWh** generado por el sistema solar, 
        se mitigan **{pendiente:.5f} toneladas de CO₂** (equivalente a **{pendiente*1000:.2f} kg de CO₂**) 
        que de otro modo habrían sido producidas por fuentes tradicionales en la red eléctrica.
        """)

    except FileNotFoundError:
        st.error(f"❌ No se encontró el archivo en la ruta: `{ruta_solar}`. Por favor verifica que la ruta relativa sea correcta respecto a donde estás ejecutando Streamlit.")
    except KeyError as e:
        st.error(f"❌ El archivo se cargó, pero no se encontró la columna {e}. Verifica que los nombres coincidan exactamente con 'Energía [kWh/año]' y 'Emisiones CO2 [Ton/año]'.")

# Línea divisoria
st.divider()

# Footer sencillo
st.markdown(
    """
    <div style="text-align: center;">
        <p>© 2026 - Todos los derechos reservados</p>
    </div>
    """,
    unsafe_allow_html=True
)