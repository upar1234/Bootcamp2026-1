
import streamlit as st

st.set_page_config(page_title="Glosario FNCER", layout="wide")

GLOSARIO_DATOS = {
    "Tipo de Tecnología": (
        "Identifica la fuente primaria de energía utilizada por el proyecto. En el marco de la transición energética en Colombia, "
        "se priorizan las FNCER (Fuentes No Convencionales de Energía Renovable). Esto permite clasificar si el impacto ambiental "
        "viene del sol (fotovoltaica), del viento (eólica) o de procesos biológicos (biomasa)."
    ),
    "Capacidad [MW]": (
        "Es la potencia neta real que el proyecto puede entregar de forma constante al Sistema Interconectado Nacional. "
        "A diferencia de la potencia pico (máximo teórico de los equipos), esta medida representa la capacidad efectiva de la planta "
        "para abastecer la demanda energética de una región."
    ),
    "Departamento": (
        "Indica la jurisdicción departamental donde se asienta la infraestructura. Es clave para entender la distribución "
        "geográfica de la transición energética y cómo regiones como La Guajira o el Caribe lideran el cambio hacia lo renovable."
    ),
    "Municipio": (
        "Nombre de la localidad donde se encuentra el núcleo del proyecto. En macroproyectos que abarcan varios territorios, "
        "se designa al municipio principal para efectos de permisos ambientales, impuestos locales y consultas previas."
    ),
    "Código Departamento": (
        "Identificador numérico estandarizado por el DANE (DIVIPOLA). Este código es vital para la interoperabilidad de datos, "
        "permitiendo que este glosario se conecte con otros sistemas de información estadística y gubernamental en Colombia."
    ),
    "Código Municipio": (
        "Código DIVIPOLA único para la cabecera municipal. Asegura que no haya confusión entre municipios con nombres similares "
        "al momento de realizar análisis geográficos o de inversión regional."
    ),
    "Fecha estimada FPO": (
        "Representa la meta de 'Puesta en Operación'. Es el momento crítico en que el proyecto deja de ser una obra civil "
        "para convertirse en un activo generador, marcando el inicio de las pruebas técnicas o la entrega comercial de energía."
    ),
    "Energía [kWh/día]": (
        "Producción eléctrica diaria proyectada. Se calcula multiplicando la capacidad por un factor de eficiencia técnica: "
        "0.2 para solar (ajustado a las horas de radiación) y 0.4 para otras tecnologías que aprovechan recursos más constantes."
    ),
    "Usuarios": (
        "Traduce la potencia técnica a impacto social. Estima cuántas familias colombianas promedio se verían beneficiadas, "
        "usando como base el consumo de subsistencia de 173 kWh/mes definido para zonas de clima templado y cálido."
    ),
    "Inversión estimada [COP]": (
        "Valor aproximado del capital necesario para ejecutar el proyecto. Esta cifra se deriva indirectamente de la potencia "
        "instalada, reflejando el peso económico que el sector energético aporta al desarrollo de la infraestructura nacional."
    ),
    "Empleos estimados": (
        "Proyección de plazas de trabajo directas necesarias para la construcción y mantenimiento. Se calcula mediante "
        "coeficientes técnicos que relacionan el tamaño de la planta con la demanda de mano de obra calificada y operativa."
    ),
    "Emisiones CO2 [Ton/año]": (
        "Mide el beneficio ambiental directo. Representa la cantidad de gases de efecto invernadero que se dejan de emitir "
        "al reemplazar la generación basada en carbón (0.8 gr/kWh) por fuentes limpias, mitigando el cambio climático."
    )
}

st.title("⚡ Sistema de Información Energética")

tab_datos, tab_glosario = st.tabs(["📊 Datos del Proyecto", "📖 Glosario de Variables"])

with tab_glosario:
    # Usamos columnas para separar el segmentador de la tarjeta informativa
    col_nav, col_desc = st.columns([1, 2.5], gap="large")
    
    with col_nav:
        st.markdown("### 🔍 Segmentador")
        opcion = st.radio(
            "Seleccione una variable para detallar:",
            options=list(GLOSARIO_DATOS.keys()),
            help="Selecciona una variable para ver su definición técnica arriba."
        )
    
    with col_desc:
        st.markdown("### 📋 Definición Técnica")
        
        # --- BLOQUE LLAMATIVO ---
        # Usamos un contenedor con borde y color de fondo simulado
        with st.container(border=True):
            st.markdown(f"<h2 style='color: #007BFF;'>{opcion}</h2>", unsafe_allow_html=True)
            st.markdown(f"#### **Descripción Metodológica:**")
            
            # Usamos un st.info para que el texto tenga un fondo destacado
            st.info(GLOSARIO_DATOS[opcion])
            
            # Agregamos un detalle visual extra
            st.caption("Fuente: Metodología de cálculo para proyectos FNCER - Colombia.")
        # ------------------------

    st.divider()

    # Vista completa siempre desplegada al final
    st.subheader("📚 Diccionario Completo")
    for k, v in GLOSARIO_DATOS.items():
        with st.container():
            col1, col2 = st.columns([1, 3])
            col1.markdown(f"**{k}**")
            col2.write(v)
            st.divider()