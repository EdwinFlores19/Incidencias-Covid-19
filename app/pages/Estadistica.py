import streamlit as st
import pandas as pd
import plotly.express as px
from scipy import stats
import numpy as np

# Importar la función de carga desde la app principal
# CORRECCIÓN: Ahora se importa directamente desde app.py
from Pagina_Principal import load_data

st.set_page_config(page_title="Estadística Avanzada", layout="wide")
st.title("Estadística Descriptiva y Avanzada")

df_raw, df_country = load_data()

# --- 2.1 y 2.4: Métricas y Detección de Outliers ---
st.header("Métricas Clave y Detección de Outliers")
st.dataframe(df_country.describe())

st.subheader("Boxplots para Detección de Outliers")
fig_box = px.box(df_country, y=['Confirmed', 'Deaths', 'Recovered', 'Active'],
                 title="Diagramas de Caja para Métricas Principales")
st.plotly_chart(fig_box, use_container_width=True)

# --- 2.2: Intervalos de Confianza ---
st.header("Intervalos de Confianza para CFR")
countries_ic = st.multiselect("Selecciona países para calcular IC del CFR:",
                              options=df_country['Country_Region'].unique(), default=['Peru', 'Mexico'])

if countries_ic:
    results = []
    for country in countries_ic:
        data = df_country[df_country['Country_Region'] == country]
        confirmed = data['Confirmed'].iloc[0]
        deaths = data['Deaths'].iloc[0]

        if confirmed > 0:
            p_hat = deaths / confirmed
            se = np.sqrt((p_hat * (1 - p_hat)) / confirmed)
            ci = stats.norm.interval(0.95, loc=p_hat, scale=se)
            results.append({
                'País': country,
                'CFR (%)': f"{(p_hat * 100):.2f}",
                'IC 95% Límite Inferior (%)': f"{(ci[0] * 100):.2f}",
                'IC 95% Límite Superior (%)': f"{(ci[1] * 100):.2f}"
            })
    st.table(pd.DataFrame(results))

# --- 2.3: Test de Hipótesis ---
st.header("Test de Hipótesis para Comparar CFR")
col1, col2 = st.columns(2)
country1 = col1.selectbox("Selecciona País 1:", options=df_country['Country_Region'].unique(), index=150)  # Peru
country2 = col2.selectbox("Selecciona País 2:", options=df_country['Country_Region'].unique(), index=122)  # Mexico

if st.button("Realizar Test de Hipótesis (CFR País 2 > CFR País 1)"):
    from statsmodels.stats.proportion import proportions_ztest

    data1 = df_country[df_country['Country_Region'] == country1]
    data2 = df_country[df_country['Country_Region'] == country2]

    count = np.array([data2['Deaths'].iloc[0], data1['Deaths'].iloc[0]])
    nobs = np.array([data2['Confirmed'].iloc[0], data1['Confirmed'].iloc[0]])

    stat, pval = proportions_ztest(count, nobs, alternative='larger')

    st.write(f"**Hipótesis Nula (H0):** CFR({country2}) <= CFR({country1})")
    st.write(f"**Hipótesis Alternativa (H1):** CFR({country2}) > CFR({country1})")
    st.metric("P-valor", f"{pval:.4f}")
    if pval < 0.05:
        st.success("Se rechaza la hipótesis nula. La CFR del País 2 es significativamente mayor que la del País 1.")
    else:
        st.warning("No se puede rechazar la hipótesis nula.")
