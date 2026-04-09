import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt

# Configuración de la página
st.set_page_config(layout="centered", page_title="TalentoTech", page_icon=":bar_chart:")

st.title("📊 Análisis de datos - Transición energética")

# Header
t1, t2 = st.columns([0.5, 0.5])
t1.image('imagentalento.jpg', width=300)
t2.markdown("""
### 👥 Equipo de trabajo
- Johan Ospina  
- Liliana Jimenez  
- Andi  
- Alejandro Aristizabal  
""")

# Tabs
tabs = st.tabs(["🏠 Inicio", "📂 Visualización de datos", "📊 Gráficos interactivos"])

# -------------------------------
# 🏠 PESTAÑA 1: INFORMACIÓN
# -------------------------------
with tabs[0]:
    st.header("📌 Descripción del proyecto")

    st.markdown("""
    Este proyecto analiza la relación entre los tipos de generación de energía 
    y las emisiones de CO₂ en Colombia entre 2014 y 2025.

    ### 🎯 Objetivo
    Evaluar si el crecimiento de energías renovables ha contribuido a la reducción de emisiones.

    ### 📚 Estado del arte
    La transición energética es clave para mitigar el cambio climático. 
    Colombia ha avanzado en energías limpias como solar e hidráulica, 
    pero aún depende de fuentes fósiles.

    ### ⚙️ Proceso del proyecto
    - Limpieza y transformación de datos (Python)
    - Integración en base de datos (SQL)
    - Análisis exploratorio
    - Visualización en Streamlit
    """)

    st.subheader("📷 Ejemplo de visualización")
    fig, ax = plt.subplots()
    sns.barplot(x=['Solar', 'Hidro', 'Carbón'], y=[10, 30, 50], ax=ax)
    st.pyplot(fig)


# -------------------------------
# 📂 PESTAÑA 2: SUBIR Y VER DATOS
# -------------------------------
with tabs[1]:
    st.header("📂 Cargar y visualizar dataset")

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
# 📊 PESTAÑA 3: GRÁFICOS INTERACTIVOS
# -------------------------------
with tabs[2]:
    st.header("📊 Generador de gráficos interactivos")

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

        # Escalado automático
        if col_y in numericas:
            max_val = df[col_y].max()

            if max_val > 1_000_000:
                df[col_y] = df[col_y] / 1_000_000
                unidad = "Millones"
            elif max_val > 1_000:
                df[col_y] = df[col_y] / 1_000
                unidad = "Miles"
            else:
                unidad = "Unidades"
        else:
            unidad = ""

        st.write(f"Escala aplicada: {unidad}")

        # Selector de tipo de gráfica
        tipo_grafico = st.selectbox(
            "Selecciona el tipo de gráfico",
            ["Barras", "Línea", "Torta", "Barras apiladas"]
        )

        # Agrupar datos si es necesario
        df_group = df.groupby(col_x)[col_y].sum().reset_index()

        # ------------------ GRÁFICOS ------------------

        if st.button("Generar gráfico"):

            fig, ax = plt.subplots()

            if tipo_grafico == "Barras":
                sns.barplot(data=df_group, x=col_x, y=col_y, ax=ax)

                # Reducir etiquetas
                if len(df_group[col_x]) > 10:
                    ax.set_xticks(ax.get_xticks()[::3])
                plt.xticks(rotation=90, fontsize=8)

            elif tipo_grafico == "Línea":
                sns.lineplot(data=df_group, x=col_x, y=col_y, ax=ax, marker="o")

                # SOLO si parece tiempo (muchos valores)
                if len(df_group[col_x]) > 10:
                    ax.set_xticks(ax.get_xticks()[::3])

                plt.xticks(rotation=90, fontsize=8)

            elif tipo_grafico == "Torta":
                ax.pie(df_group[col_y], labels=df_group[col_x], autopct='%1.1f%%')
                ax.set_title("Distribución")

            elif tipo_grafico == "Barras apiladas":
                col_stack = st.selectbox("Selecciona columna para apilar", columnas)

                df_pivot = df.pivot_table(
                    index=col_x,
                    columns=col_stack,
                    values=col_y,
                    aggfunc='sum'
                )

                df_pivot.plot(kind='bar', stacked=True, ax=ax)

                # Si hay muchas categorías
                if len(df_pivot.index) > 10:
                    ax.set_xticks(ax.get_xticks()[::2])

                plt.xticks(rotation=90, fontsize=8)

            # Ajuste final general
            ax.set_ylabel(f"{col_y} ({unidad})")
            plt.tight_layout()

            st.pyplot(fig)