import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy.stats import shapiro

# --- 1. CONFIGURACIÓN INICIAL Y RUTA DE DATOS ---
# Usar barra normal (/) evita errores de lectura de rutas en Python
RUTA_DATOS = "Documentos/solar.csv" 

st.set_page_config(page_title="Análisis Energético y de CO2", layout="wide")

st.title("🍀 Análisis de Energía y Emisiones Evitadas de CO2")
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
    df_clean = cargar_datos(RUTA_DATOS)
    
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
    st.error(f"❌ No se encontró el archivo en la ruta: `{RUTA_DATOS}`. Por favor verifica que la ruta relativa sea correcta respecto a donde estás ejecutando Streamlit.")
except KeyError as e:
    st.error(f"❌ El archivo se cargó, pero no se encontró la columna {e}. Verifica que los nombres coincidan exactamente con 'Energía [kWh/año]' y 'Emisiones CO2 [Ton/año]'.")