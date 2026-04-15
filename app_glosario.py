import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Glosario Técnico FNCER", layout="wide", page_icon="⚡")

# Diccionario con descripciones enriquecidas y explicativas
GLOSARIO_DATOS = {
    "Tipo de Tecnología": (
        "Identifica la fuente primaria de energía utilizada por el proyecto. En el marco de la transición energética en Colombia, "
        "se priorizan las FNCER (Fuentes No Convencionales de Energía Renovable). Esto permite clasificar si el impacto ambiental "
        "viene del sol (fotovoltaica), del viento (eólica) o de procesos biológicos (biomasa)."
    ),
    "Capacidad [MW]": (
        "Es la potencia neta real que el proyecto puede entregar de forma constante al Sistema Interconectado Nacional. "
        "A diferencia de la potencia pico (máximo teórico de los equipos), esta medida representa la capacidad efectiva de la planta "
        "para abastecer la demanda energética de una región de manera fiable."
    ),
    "Departamento": (
        "Indica la jurisdicción departamental donde se asienta la infraestructura. Es clave para entender la distribución "
        "geográfica de la transición energética y cómo regiones estratégicas lideran el cambio hacia matrices más limpias."
    ),
    "Municipio": (
        "Nombre de la localidad donde se encuentra el núcleo del proyecto. En macroproyectos que abarcan varios territorios, "
        "se designa al municipio principal para efectos de permisos ambientales, impuestos locales y consultas previas."
    ),
    "Código Departamento": (
        "Identificador numérico estandarizado por el DANE (DIVIPOLA). Este código es vital para la interoperabilidad de datos, "
        "permitiendo que este sistema se conecte con otras bases de datos estadísticas y gubernamentales de Colombia sin errores de digitación."
    ),
    "Código Municipio": (
        "Código DIVIPOLA único para la cabecera municipal. Asegura que no haya confusión entre municipios con nombres similares "
        "al momento de realizar análisis geográficos, cruces de inversión regional o reportes de regalías."
    ),
    "Fecha estimada FPO": (
        "Representa la meta de 'Puesta en Operación'. Es el momento crítico en que el proyecto deja de ser una obra civil "
        "para convertirse en un activo generador, marcando el inicio formal de las pruebas técnicas o la entrega comercial de energía a la red."
    ),
    "Energía [kWh/día]": (
        "Producción eléctrica diaria proyectada. Se calcula multiplicando la capacidad por un factor de eficiencia técnica: "
        "0.2 para solar (ajustado a las horas de irradiación efectiva) y 0.4 para otras tecnologías que aprovechan recursos más constantes."
    ),
    "Usuarios": (
        "Traduce la potencia técnica a impacto social tangible. Estima cuántas familias colombianas promedio se verían beneficiadas, "
        "usando como base el consumo de subsistencia de 173 kWh/mes definido para la mayoría de regiones del país."
    ),
    "Inversión estimada [COP]": (
        "Valor aproximado del capital necesario para ejecutar el proyecto. Esta cifra se deriva indirectamente de la potencia "
        "instalada, reflejando el peso económico y el flujo de inversión que el sector energético aporta al desarrollo nacional."
    ),
    "Empleos estimados": (
        "Proyección de plazas de trabajo directas necesarias para la construcción, operación y mantenimiento. Se calcula mediante "
        "coeficientes técnicos que relacionan el tamaño de la planta con la demanda de mano de obra calificada y operativa local."
    ),
    "Emisiones CO2 [Ton/año]": (
        "Mide el beneficio ambiental directo y la descarbonización. Representa la cantidad de gases de efecto invernadero que se dejan de emitir "
        "al reemplazar la generación basada en combustibles fósiles (carbón) por fuentes limpias, mitigando el impacto del cambio climático."
    )
}

# Título principal de la aplicación
st.title("⚡ Glosario de Variables - Proyectos Energéticos")
st.markdown("---")

# Layout principal: Segmentador a la izquierda, Detalle a la derecha
col_slicer, col_card = st.columns([1, 2.2], gap="large")

with col_slicer:
    st.subheader("🔍 Selección de Variable")
    # Segmentador de datos tipo Radio
    opcion = st.radio(
        "Seleccione el término que desea explorar:",
        options=list(GLOSARIO_DATOS.keys()),
        label_visibility="visible"
    )

with col_card:
    st.subheader("📋 Detalle de Metodología")
    
    # Tarjeta de información destacada
    with st.container(border=True):
        st.markdown(f"<h2 style='color: #007BFF; margin-bottom: 0;'>{opcion}</h2>", unsafe_allow_html=True)
        st.write("---")
        st.markdown("#### **Explicación Detallada:**")
        # Cuadro informativo llamativo
        st.info(GLOSARIO_DATOS[opcion])
        
        st.caption("Esta descripción incluye criterios técnicos de capacidad, factores de planta e impacto social/ambiental.")

st.markdown("### 📚 Diccionario Completo (Vista Rápida)")
# Sección final con todas las variables siempre visibles
for variable, descripcion in GLOSARIO_DATOS.items():
    with st.container():
        c1, c2 = st.columns([1, 3])
        c1.markdown(f"**{variable}**")
        c2.write(descripcion)
        st.markdown("<div style='margin-bottom: 10px; border-bottom: 1px dashed #ddd;'></div>", unsafe_allow_html=True)