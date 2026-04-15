import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Diccionario de Variables", layout="wide", page_icon="📖")

# --- ESTRUCTURA DE DATOS CON FUENTES ASIGNADAS ---
DATA = {
    "Meta FNCER": {
        "fuente_full": "Meta FNCER: Incorporar en la matriz energética nueva capacidad instalada a partir de Fuentes No Convencionales de Energía Renovable - FNCER",
        "color": "#28a745", # Verde
        "variables": {
            "Tipo de Tecnología": "Identifica la fuente primaria (Solar, Eólica, Biomasa). Es el pilar de la descarbonización.",
            "Capacidad [MW]": "Potencia neta real entregable. Es la medida de magnitud del proyecto ante el SIN.",
            "Departamento / Municipio": "Ubicación geográfica. Incluye códigos DIVIPOLA para trazabilidad estadística nacional.",
            "Fecha estimada FPO": "Fecha de Puesta en Operación. Hito donde el proyecto inicia su vida útil comercial.",
            "Energía [kWh/día]": "Estimación de generación diaria usando factores de eficiencia (0.2 solar / 0.4 otros).",
            "Usuarios": "Impacto social: familias beneficiadas según consumo de subsistencia (173 kWh/mes).",
            "Inversión estimada [COP]": "Valor capital del proyecto calculado proporcionalmente a su capacidad instalada.",
            "Empleos estimados": "Proyección de mano de obra directa para las fases de construcción y operación.",
            "Emisiones CO2 [Ton/año]": "Beneficio ambiental: toneladas de gases de efecto invernadero evitadas anualmente."
        }
    },
    "Monthly Electricity Statistics": {
        "fuente_full": "Monthly Electricity Statistics",
        "color": "#007BFF", # Azul
        "variables": {
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