# Proyecto de Análisis de Datos: Energía Solar y Huella de Carbono en Colombia

## 1. Descripción general
Este proyecto está enfocado en el análisis de la transición energética en Colombia, con énfasis en la energía solar y su impacto en la reducción de emisiones de CO₂. Se incluye la carga, transformación y análisis de datos oficiales de producción de energía, proyectos solares y métricas estimadas de mitigación ambiental.

## 2. Objetivo
Evaluar la asociación entre la producción de energía renovable —especialmente solar— y la reducción de emisiones de CO₂ en el país. El proyecto busca apoyar la toma de decisiones mediante análisis descriptivo, visualizaciones interactivas y un modelo simple de regresión que cuantifica el ahorro de carbono estimado.

## 3. Datos utilizados
- `Documentos/colombia.csv`: datos de producción de energía en Colombia por fuente, balance y fecha.
- `Documentos/solar.csv`: registro de proyectos de energía solar en Colombia, con variables de capacidad, ubicación, energía estimada y emisiones de CO₂ evitadas.
- `df_solo_renovables.csv`: datos filtrados para energía renovable, usados en comparaciones y en el análisis temporal.
- `Codigo/tabla_resumen.csv`: resumen de producción energética por categoría renovable y no renovable.
- `Codigo/datos_final.csv`: datos consolidados de producción para el análisis temporal.
- `Documentos/colombia.geo.json`: archivo geoespacial para construir mapas de calor e indicadores por departamento.

## 4. Metodología
El flujo de trabajo del proyecto incluye:

1. Lectura de datos
   - Se cargan CSV con pandas, con manejo de codificaciones `utf-8` y `latin-1`.
   - Se verifican tipos de datos y estructuras de los datasets.

2. Limpieza y normalización
   - Se estandarizan nombres de departamentos y categorías.
   - Se integran fuentes de datos de energía y emisiones.
   - Se calculan métricas derivadas como energía anual estimada, capacidad en MW y emisiones de CO₂ evitadas.

3. Análisis exploratorio
   - Se genera un diccionario de variables para comprender cada campo del dataset.
   - Se observan distribuciones de energía solar y emisiones evitadas.
   - Se analizan proporciones renovable vs no renovable.

4. Visualización interactiva
   - Se construye una app Streamlit (`Frontend/Clase1.py`) que muestra:
     - vista previa de datasets,
     - diccionario de variables,
     - comparativos de energía renovable vs no renovable,
     - evolución temporal de generación energética,
     - atlas solar con mapas geoespaciales y globos por departamento,
     - mapas de emisiones de CO₂ evitadas.

5. Modelo descriptivo
   - Se aplica un modelo de regresión lineal para relacionar `Energía [kWh/año]` con `Emisiones CO2 [Ton/año]`.
   - Se evalúan indicadores estadísticos:
     - R² del modelo,
     - coeficiente de pendiente,
     - valor-p para significancia.

6. Interpretación ambiental
   - Se calcula el ahorro total de CO₂ de los proyectos solares.
   - Se realiza una equivalencia aproximada en árboles para contextualizar el impacto.

## 5. Resultados principales

### 5.1. Calidad de los datos
- Los datasets permiten analizar sectores energéticos a nivel nacional y regional.
- El proyecto incluye un diccionario de variables para facilitar la interpretación de campos como `Product`, `Value`, `Energía [kWh/día]`, `Emisiones CO2 [Ton/año]`, `Capacidad [MW]` y otros.

### 5.2. Comparación renovables vs no renovables
- Se construyen tablas y gráficos para comparar la generación de energía renovable frente a no renovable.
- El análisis temporal muestra la evolución de ambas categorías en la matriz eléctrica.
- La visualización de barras y tortas destaca la participación relativa de las fuentes.

### 5.3. Análisis espacial
- Se crea un atlas solar con mapas de calor por departamento usando `colombia.geo.json`.
- Se visualiza la generación solar estimada por departamento y el impacto de emisiones de CO₂ evitadas.
- Se utilizan mapas de choropleth y globos geoespaciales para identificar áreas con mayor potencial solar.

### 5.4. Distribución y normalidad
- Se realizan histogramas para las variables principales:
  - `Energía [kWh/año]`
  - `Emisiones CO2 [Ton/año]`
- Se aplica la prueba de Shapiro para analizar la normalidad de estas variables.

### 5.5. Modelo de regresión lineal
- El modelo lineal relaciona la energía solar generada con las emisiones de CO₂ evitadas.
- Los resultados muestran una relación muy fuerte en el conjunto de datos, con un R² elevado.
- Esto sugiere que los valores de CO₂ evitado están estrechamente vinculados a la energía estimada en los proyectos, lo cual es consistente con una métrica calculada a partir de factores de desplazamiento.

### 5.6. Impacto ambiental
- Se calcula el ahorro total de CO₂ de los proyectos solares disponibles en los datos.
- Se traduce ese ahorro en una equivalencia de árboles necesarios para absorber la misma cantidad de CO₂ en un año.
- El análisis enfatiza el valor ambiental de la energía solar como mitigación de emisiones de carbono.

## 6. Conclusiones
- El proyecto evidencia que la energía solar es un componente clave en la transición energética de Colombia.
- Aunque la matriz aún depende de fuentes fósiles, los datos indican un aumento en la participación renovable y un beneficio ambiental asociado.
- El fuerte ajuste del modelo lineal señala que el cálculo de emisiones evitadas está bien representado por la energía solar generada, pero también invita a interpretar los resultados como un escenario teórico basado en factores de desplazamiento.
- Las visualizaciones y el atlas geoespacial facilitan la identificación de regiones con mayor capacidad solar y potencial de reducción de huella de carbono.

## 7. Estructura del repositorio

- `Frontend/Clase1.py`: aplicación Streamlit de análisis, visualización y modelado.
- `descriptivo.py`: análisis descriptivo de energía solar y CO₂.
- `Codigo/mapas.py`: generación de mapas con datos solares y emisiones.
- `Codigo/limpieza_mes.py`: scripts de limpieza y preparación de datos.
- `Documentos/solar.csv`: dataset de proyectos solares.
- `Documentos/colombia.csv`: dataset de producción energética nacional.
- `Documentos/colombia.geo.json`: geodatos de departamentos.
- `df_solo_renovables.csv`: datos filtrados para análisis renovable.
- `Codigo/tabla_resumen.csv` y `Codigo/datos_final.csv`: datos consolidados para gráficos y evolución temporal.

## 8. Requisitos y ejecución

Requisitos principales:
- Python
- pandas
- numpy
- matplotlib
- seaborn
- scipy
- statsmodels
- plotly.express
- streamlit

Para ejecutar la app Streamlit:

```bash
streamlit run Frontend/Clase1.py
```

## 9. Valor para el análisis de datos
Este proyecto aporta un caso práctico de análisis completo aplicado a energía y sostenibilidad, combinando:
- limpieza y transformación de datos,
- creación de diccionarios de variables,
- análisis descriptivo,
- visualización interactiva,
- modelado estadístico,
- y comunicación de resultados ambientales.
