import streamlit as st
import pandas as pd
import plotly.express as px
import io

# --- Configuración de la Página ---
st.set_page_config(
    page_title="Dashboard COVID-19 Avanzado",
    page_icon="🔬",
    layout="wide"
)


# --- Funciones de Carga y Procesamiento de Datos ---
@st.cache_data
def load_data():
    url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/04-18-2022.csv'
    df = pd.read_csv(url)

    # Limpieza básica
    df.rename(columns={'Case_Fatality_Ratio': 'CFR'}, inplace=True)
    df['CFR'] = pd.to_numeric(df['CFR'], errors='coerce')

    # Agregado por país
    df_pais = df.groupby('Country_Region').agg({
        'Confirmed': 'sum',
        'Deaths': 'sum',
        'Recovered': 'sum',
        'Active': 'sum'
    }).reset_index()

    # 2.1: Calcular métricas clave (CFR)
    df_pais['CFR'] = (df_pais['Deaths'] / df_pais['Confirmed'] * 100).round(2)

    return df, df_pais


df_raw, df_country = load_data()

# --- Barra Lateral (Sidebar) con Filtros ---
st.sidebar.header("Filtros Globales")
selected_countries = st.sidebar.multiselect(
    'Selecciona Países',
    options=sorted(df_country['Country_Region'].unique()),
    default=['US', 'India', 'Brazil', 'France', 'Germany', 'Peru']
)

confirmed_threshold = st.sidebar.slider(
    'Umbral Mínimo de Casos Confirmados',
    min_value=0,
    max_value=int(df_country['Confirmed'].max()),
    value=100000,
    step=10000
)

# Filtrar datos según la selección
df_filtered_sidebar = df_country[
    (df_country['Country_Region'].isin(selected_countries)) &
    (df_country['Confirmed'] >= confirmed_threshold)
    ]

# --- Título Principal ---
st.title("🔬 Dashboard de Análisis Avanzado de COVID-19")
st.markdown("Laboratorio 1.1 - Análisis Estadístico, Modelado y Propuesta de Innovación")

# --- 5.2: KPIs Principales ---
st.header("Indicadores Clave de Rendimiento (KPIs) Globales")
total_confirmed = df_country['Confirmed'].sum()
total_deaths = df_country['Deaths'].sum()
global_cfr = (total_deaths / total_confirmed) * 100

col1, col2, col3 = st.columns(3)
col1.metric("Total Confirmados", f"{total_confirmed:,.0f}")
col2.metric("Total Fallecidos", f"{total_deaths:,.0f}")
col3.metric("Tasa de Mortalidad Global (CFR)", f"{global_cfr:.2f}%")

# --- Pestaña Principal: Visión General ---
st.header("Visión General de la Pandemia")

st.subheader("Top N Países por Métrica")
metric_select = st.selectbox("Selecciona una Métrica:", ['Confirmed', 'Deaths', 'Recovered', 'Active', 'CFR'])
top_n = st.slider("Número de países a mostrar:", 5, 50, 10)

top_n_data = df_country.nlargest(top_n, metric_select)
fig_top_n = px.bar(top_n_data, x='Country_Region', y=metric_select, title=f"Top {top_n} Países por {metric_select}")
st.plotly_chart(fig_top_n, use_container_width=True)

st.subheader("Mapa Interactivo de Casos Confirmados")
fig_map = px.choropleth(
    df_country,
    locations="Country_Region",
    locationmode='country names',
    color="Confirmed",
    hover_name="Country_Region",
    color_continuous_scale=px.colors.sequential.Plasma,
    title="Distribución Mundial de Casos Confirmados"
)
st.plotly_chart(fig_map, use_container_width=True)

# --- 5.4: Exportación de Datos ---
st.sidebar.header("Exportación de Datos")


@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')


csv = convert_df_to_csv(df_filtered_sidebar)
st.sidebar.download_button(
    label="Descargar datos filtrados en CSV",
    data=csv,
    file_name='covid_data_filtrada.csv',
    mime='text/csv',
)
