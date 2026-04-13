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
t1.image('Frontend\imagentalento.jpg', width=300)
t2.markdown("""
### 👥 Equipo de trabajo
- Johan Ospina  
- Liliana Jimenez  
- Andi  
- Alejandro Aristizabal  
""")

# Tabs
tabs = st.tabs(["🏠 Inicio", "📂 Visualización de datos", "📊 Gráficos interactivos", "✅ Ver resultado"])

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
                sns.barplot(data=df_group, y=col_x, x=col_y, ax=ax)

                # Etiquetas en eje Y para categorías
                ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=8)

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

                df_pivot.plot(kind='barh', stacked=True, ax=ax)

                ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=8)

            # Ajuste final general
            ax.set_ylabel(f"{col_y} ({unidad})")
            plt.tight_layout()

            st.pyplot(fig)

with tabs[3]:
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

    st.subheader("📊 Renovables Vs Fósiles")
    st.dataframe(tabla_resumen)

    "### Evolución temporal de energía"
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

    "### Distribución renovable vs no renovable"
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
    
    chart = alt.Chart(df_renovables_agrupado).mark_bar().encode(
        alt.X("Value:Q").title("Valor (GWh)"),
        alt.Y("Product:N").title("Tipo de Energía"),
        alt.Color("Product:N", scale=alt.Scale(scheme="category10"), legend=alt.Legend(orient="bottom")),
        tooltip=["Product:N", "Value:Q"]
    ).properties(height=400)
    
    st.altair_chart(chart, use_container_width=True)


    st.markdown("### Evolución temporal de energías renovables")
    # Cargar datos para gráfica de líneas
    datos_final = pd.read_csv("C:\\Users\\USUARIO\\Documents\\Datos\\Bootcamp\\Bootcamp2026-1\\df_solo_renovables.csv")
    
    if not datos_final.empty and "Time" in datos_final.columns:
        # Convertir Time a datetime
        datos_final["Time"] = pd.to_datetime(datos_final["Time"])
        
        # Agrupar por fecha y producto (mantener cada tipo de energía por separado)
        df_lineas = datos_final.groupby(["Time", "Product"])["Value"].sum().reset_index()
        
        # Crear gráfico de líneas general
        line_chart = alt.Chart(df_lineas).mark_line(point=True).encode(
            x=alt.X("Time:T", title="Fecha"),
            y=alt.Y("Value:Q", title="Valor (GWh)"),
            color=alt.Color("Product:N", scale=alt.Scale(scheme="category10"), legend=alt.Legend(orient="bottom")),
            tooltip=["Time:T", "Product:N", "Value:Q"]
        ).properties(height=400).configure_axis(grid=True)
        
        st.altair_chart(line_chart, use_container_width=True)

        st.markdown("### Evolución temporal sin Hydro")
        df_lineas_sin_hydro = df_lineas[df_lineas["Product"] != "Hydro"]

        line_chart_sin_hydro = alt.Chart(df_lineas_sin_hydro).mark_line(point=True).encode(
            x=alt.X("Time:T", title="Fecha"),
            y=alt.Y("Value:Q", title="Valor (GWh)"),
            color=alt.Color("Product:N", scale=alt.Scale(scheme="category10"), legend=alt.Legend(orient="bottom")),
            tooltip=["Time:T", "Product:N", "Value:Q"]
        ).properties(height=400).configure_axis(grid=True)

        st.altair_chart(line_chart_sin_hydro, use_container_width=True)
    else:
        st.warning("No se pudieron cargar los datos para la gráfica de líneas")