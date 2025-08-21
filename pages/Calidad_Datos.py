import streamlit as st
import pandas as pd
import plotly.express as px

from app.app import load_data

st.set_page_config(page_title="Calidad de Datos", layout="wide")
st.title("Análisis de Calidad de Datos")

df_raw, df_country = load_data()

st.header("Análisis de Valores Nulos y Consistencia")
st.subheader("Valores Nulos en el Dataset Crudo")
null_counts = df_raw.isnull().sum()
st.dataframe(null_counts[null_counts > 0])
st.info("La columna 'CFR' (Case_Fatality_Ratio) es la que presenta más valores nulos, probablemente por divisiones entre cero o datos no reportados.")

st.subheader("Distribución de la Tasa de Mortalidad (CFR)")
fig_hist_cfr = px.histogram(df_country, x='CFR', nbins=50, title="Histograma de la Tasa de Mortalidad por País")
st.plotly_chart(fig_hist_cfr, use_container_width=True)

# --- 2.5: Gráfico de Control (Simulado) ---
st.header("Gráfico de Control para Detección de Anomalías")
st.warning("Esta sección es una demostración conceptual.")
st.info("""
Un gráfico de control se usaría sobre una serie de tiempo (ej. muertes diarias) para detectar puntos que se desvían más de 3 desviaciones estándar de la media móvil, indicando posibles anomalías en los reportes.
""")

# Simulación de datos para el gráfico
dias = pd.date_range(start="2022-03-01", periods=49)
muertes_diarias = np.random.randint(50, 150, size=49)
muertes_diarias[20] = 300 # Anomalía
df_control = pd.DataFrame({'Fecha': dias, 'Muertes Diarias': muertes_diarias})
df_control['Media Móvil'] = df_control['Muertes Diarias'].rolling(window=7).mean()
df_control['Límite Superior'] = df_control['Media Móvil'] + 3 * df_control['Muertes Diarias'].rolling(window=7).std()
df_control['Límite Inferior'] = df_control['Media Móvil'] - 3 * df_control['Muertes Diarias'].rolling(window=7).std()

fig_control = px.line(df_control, x='Fecha', y='Muertes Diarias', title="Gráfico de Control Simulado de Muertes Diarias")
fig_control.add_scatter(x=dias, y=df_control['Media Móvil'], mode='lines', name='Media Móvil')
fig_control.add_scatter(x=dias, y=df_control['Límite Superior'], mode='lines', name='Límite Superior', line=dict(dash='dash', color='red'))
fig_control.add_scatter(x=dias, y=df_control['Límite Inferior'], mode='lines', name='Límite Inferior', line=dict(dash='dash', color='red'))
st.plotly_chart(fig_control, use_container_width=True)
