# Importa las librerías necesarias para la aplicación.
import streamlit as st          # Para crear la interfaz web interactiva.
import pandas as pd             # Para la manipulación y análisis de datos.
import plotly.express as px     # Para crear gráficos interactivos y de alta calidad.
import numpy as np              # Para operaciones numéricas, especialmente la generación de datos aleatorios.

# CORRECCIÓN: Ahora se importa directamente desde app.py, que está en el directorio padre.
# Esto permite que todas las páginas usen la misma función de carga de datos cacheada.
from app import load_data

# Configura las propiedades iniciales de la página web.
st.set_page_config(page_title="Calidad de Datos", layout="wide")
# Muestra el título principal de la página.
st.title("Análisis de Calidad de Datos")

# Llama a la función para cargar los datos crudos y los datos agrupados por país.
df_raw, df_country = load_data()

# Encabezado para la primera sección de la página.
st.header("Análisis de Valores Nulos y Consistencia")
# Sub-encabezado para la tabla de valores nulos.
st.subheader("Valores Nulos en el Dataset Crudo")
# Calcula la suma de valores nulos (NaN) para cada columna del DataFrame original.
null_counts = df_raw.isnull().sum()
# Muestra en una tabla solo las columnas que tienen al menos un valor nulo.
st.dataframe(null_counts[null_counts > 0])
# Muestra un cuadro de información con una interpretación de los resultados.
st.info("La columna 'CFR' (Case_Fatality_Ratio) es la que presenta más valores nulos, probablemente por divisiones entre cero o datos no reportados.")

# Sub-encabezado para el histograma.
st.subheader("Distribución de la Tasa de Mortalidad (CFR)")
# Crea una figura de histograma para visualizar cómo se distribuyen los valores de CFR entre los países.
fig_hist_cfr = px.histogram(df_country, x='CFR', nbins=50, title="Histograma de la Tasa de Mortalidad por País")
# Muestra el gráfico en la aplicación, haciendo que ocupe todo el ancho disponible.
st.plotly_chart(fig_hist_cfr, use_container_width=True)

# --- 2.5: Gráfico de Control (Simulado) ---
# Encabezado para la sección del gráfico de control.
st.header("Gráfico de Control para Detección de Anomalías")
# Muestra una advertencia indicando que los datos son simulados.
st.warning("Esta sección es una demostración conceptual.")
# Muestra un cuadro de información explicando el propósito de un gráfico de control.
st.info("""
Un gráfico de control se usaría sobre una serie de tiempo (ej. muertes diarias) para detectar puntos que se desvían más de 3 desviaciones estándar de la media móvil, indicando posibles anomalías en los reportes.
""")

# Simulación de datos para el gráfico.
# Crea un rango de 49 fechas consecutivas empezando desde el 1 de marzo de 2022.
dias = pd.date_range(start="2022-03-01", periods=49)
# Genera 49 números enteros aleatorios entre 50 y 150 para simular las muertes diarias.
muertes_diarias = np.random.randint(50, 150, size=49)
# Introduce manualmente un valor atípico (anomalía) en el día 21 para demostrar cómo lo detectaría el gráfico.
muertes_diarias[20] = 300 # Anomalía
# Crea un DataFrame de pandas con las fechas y los datos de muertes simuladas.
df_control = pd.DataFrame({'Fecha': dias, 'Muertes Diarias': muertes_diarias})
# Calcula la media móvil de 7 días para suavizar la tendencia de los datos.
df_control['Media Móvil'] = df_control['Muertes Diarias'].rolling(window=7).mean()
# Calcula el límite de control superior (media móvil + 3 desviaciones estándar móviles).
df_control['Límite Superior'] = df_control['Media Móvil'] + 3 * df_control['Muertes Diarias'].rolling(window=7).std()
# Calcula el límite de control inferior (media móvil - 3 desviaciones estándar móviles).
df_control['Límite Inferior'] = df_control['Media Móvil'] - 3 * df_control['Muertes Diarias'].rolling(window=7).std()

# Crea la figura base del gráfico de control con una línea para las muertes diarias.
fig_control = px.line(df_control, x='Fecha', y='Muertes Diarias', title="Gráfico de Control Simulado de Muertes Diarias")
# Añade la línea de la media móvil al gráfico.
fig_control.add_scatter(x=dias, y=df_control['Media Móvil'], mode='lines', name='Media Móvil')
# Añade la línea del límite superior, punteada y de color rojo.
fig_control.add_scatter(x=dias, y=df_control['Límite Superior'], mode='lines', name='Límite Superior', line=dict(dash='dash', color='red'))
# Añade la línea del límite inferior, punteada y de color rojo.
fig_control.add_scatter(x=dias, y=df_control['Límite Inferior'], mode='lines', name='Límite Inferior', line=dict(dash='dash', color='red'))
# Muestra el gráfico completo en la aplicación.
st.plotly_chart(fig_control, use_container_width=True)
