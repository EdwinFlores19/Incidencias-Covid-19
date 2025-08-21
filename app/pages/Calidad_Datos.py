# Importa las librerías necesarias para la aplicación.
import streamlit as st  # Para crear la interfaz web interactiva.
import pandas as pd     # Para la manipulación y análisis de datos.
import plotly.express as px # Para crear gráficos interactivos.
import io               # Para manejar la conversión de datos a bytes (necesario para la descarga de archivos).

# --- Configuración de la Página ---
# Establece las propiedades iniciales de la página web.
st.set_page_config(
    page_title="Dashboard COVID-19 Avanzado", # Título que aparece en la pestaña del navegador.
    page_icon="🔬",                          # Ícono que aparece en la pestaña del navegador.
    layout="wide"                           # Hace que el contenido ocupe todo el ancho de la pantalla.
)


# --- Funciones de Carga y Procesamiento de Datos ---
# El decorador @st.cache_data le dice a Streamlit que "recuerde" el resultado de esta función.
# De esta forma, los datos se descargan y procesan solo una vez, haciendo la app mucho más rápida.
@st.cache_data
def load_data():
    # Define la URL del archivo CSV con los datos.
    url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/04-18-2022.csv'
    # Lee los datos desde la URL y los carga en un DataFrame de pandas.
    df = pd.read_csv(url)

    # Limpieza básica de los datos.
    # Renombra la columna 'Case_Fatality_Ratio' a 'CFR' para que sea más corta y fácil de usar.
    # inplace=True modifica el DataFrame directamente sin necesidad de reasignarlo (df = ...).
    df.rename(columns={'Case_Fatality_Ratio': 'CFR'}, inplace=True)
    # Convierte la columna 'CFR' a un tipo de dato numérico. Si encuentra un valor que no puede convertir, lo reemplaza con NaN (Not a Number).
    df['CFR'] = pd.to_numeric(df['CFR'], errors='coerce')

    # Agrupa los datos por país para obtener los totales.
    # .groupby('Country_Region') agrupa todas las filas que pertenecen al mismo país.
    # .agg({...}) aplica una función de agregación (en este caso, 'sum') a cada columna especificada.
    # .reset_index() convierte el resultado agrupado de nuevo en un DataFrame estándar.
    df_pais = df.groupby('Country_Region').agg({
        'Confirmed': 'sum',
        'Deaths': 'sum',
        'Recovered': 'sum',
        'Active': 'sum'
    }).reset_index()

    # (Punto 2.1 del lab) Calcula la Tasa de Mortalidad (Case Fatality Ratio) para cada país.
    # La fórmula es (Muertes / Confirmados) * 100. .round(2) redondea el resultado a 2 decimales.
    df_pais['CFR'] = (df_pais['Deaths'] / df_pais['Confirmed'] * 100).round(2)

    # La función devuelve dos DataFrames: el original (crudo) y el procesado por país.
    return df, df_pais


# Llama a la función para cargar los datos y los guarda en dos variables.
df_raw, df_country = load_data()

# --- Barra Lateral (Sidebar) con Filtros ---
# Añade un encabezado a la barra lateral izquierda.
st.sidebar.header("Filtros Globales")
# Crea un widget de selección múltiple en la barra lateral para que el usuario elija los países.
selected_countries = st.sidebar.multiselect(
    'Selecciona Países',
    options=sorted(df_country['Country_Region'].unique()), # Las opciones son la lista de países únicos, ordenados alfabéticamente.
    default=['US', 'India', 'Brazil', 'France', 'Germany', 'Peru'] # Países seleccionados por defecto al cargar la app.
)

# Crea un widget de slider (barra deslizante) en la barra lateral.
confirmed_threshold = st.sidebar.slider(
    'Umbral Mínimo de Casos Confirmados',
    min_value=0,                                  # Valor mínimo del slider.
    max_value=int(df_country['Confirmed'].max()), # Valor máximo del slider (el máximo de casos de un país).
    value=100000,                                 # Valor inicial del slider.
    step=10000                                    # Incremento del slider.
)

# Filtra el DataFrame de países basándose en las selecciones del usuario en la barra lateral.
# Se crea una nueva variable para almacenar el resultado del filtro.
df_filtered_sidebar = df_country[
    (df_country['Country_Region'].isin(selected_countries)) & # Condición 1: el país debe estar en la lista seleccionada.
    (df_country['Confirmed'] >= confirmed_threshold)         # Condición 2: los casos confirmados deben ser mayores o iguales al umbral.
    ]

# --- Título Principal ---
# Muestra el título principal de la aplicación en el área de contenido.
st.title("🔬 Dashboard de Análisis Avanzado de COVID-19")
# Muestra un subtítulo o texto con formato Markdown.
st.markdown("Laboratorio 1.1 - Análisis Estadístico, Modelado y Propuesta de Innovación")

# --- 5.2: KPIs Principales ---
# Muestra un encabezado para la sección de indicadores clave.
st.header("Indicadores Clave de Rendimiento (KPIs) Globales")
# Calcula el total de casos confirmados sumando la columna 'Confirmed'.
total_confirmed = df_country['Confirmed'].sum()
# Calcula el total de fallecidos sumando la columna 'Deaths'.
total_deaths = df_country['Deaths'].sum()
# Calcula la tasa de mortalidad global.
global_cfr = (total_deaths / total_confirmed) * 100

# Crea tres columnas para organizar los KPIs horizontalmente.
col1, col2, col3 = st.columns(3)
# Muestra el total de confirmados en la primera columna usando un formato de "métrica".
# f"{variable:,.0f}" formatea el número con comas como separadores de miles y sin decimales.
col1.metric("Total Confirmados", f"{total_confirmed:,.0f}")
# Muestra el total de fallecidos en la segunda columna.
col2.metric("Total Fallecidos", f"{total_deaths:,.0f}")
# Muestra la tasa de mortalidad global en la tercera columna, formateada a 2 decimales.
col3.metric("Tasa de Mortalidad Global (CFR)", f"{global_cfr:.2f}%")

# --- Pestaña Principal: Visión General ---
# Encabezado para la sección de visualizaciones.
st.header("Visión General de la Pandemia")

# Sub-encabezado para el gráfico de barras.
st.subheader("Top N Países por Métrica")
# Crea un menú desplegable para que el usuario elija qué métrica visualizar.
metric_select = st.selectbox("Selecciona una Métrica:", ['Confirmed', 'Deaths', 'Recovered', 'Active', 'CFR'])
# Crea un slider para que el usuario elija cuántos países mostrar en el gráfico.
top_n = st.slider("Número de países a mostrar:", 5, 50, 10)

# Selecciona los 'N' países con los valores más altos para la métrica elegida.
top_n_data = df_country.nlargest(top_n, metric_select)
# Crea una figura de gráfico de barras interactivo con Plotly Express.
fig_top_n = px.bar(top_n_data, x='Country_Region', y=metric_select, title=f"Top {top_n} Países por {metric_select}")
# Muestra el gráfico en la aplicación, haciendo que ocupe todo el ancho disponible.
st.plotly_chart(fig_top_n, use_container_width=True)

# Sub-encabezado para el mapa.
st.subheader("Mapa Interactivo de Casos Confirmados")
# Crea una figura de mapa coroplético (mapa del mundo coloreado por valor).
fig_map = px.choropleth(
    df_country,
    locations="Country_Region",        # Columna con los nombres de los países.
    locationmode='country names',      # Le dice a Plotly que use nombres de países para ubicarlos.
    color="Confirmed",                 # La columna que determinará el color de cada país.
    hover_name="Country_Region",       # El nombre que aparecerá al pasar el cursor sobre un país.
    color_continuous_scale=px.colors.sequential.Plasma, # La paleta de colores a usar.
    title="Distribución Mundial de Casos Confirmados"
)
# Muestra el mapa en la aplicación.
st.plotly_chart(fig_map, use_container_width=True)

# --- 5.4: Exportación de Datos ---
# Encabezado en la barra lateral para la sección de descarga.
st.sidebar.header("Exportación de Datos")


# Define una función (también cacheada) para convertir un DataFrame a un archivo CSV en memoria.
@st.cache_data
def convert_df_to_csv(df):
    # .to_csv() convierte el DataFrame a formato CSV. index=False evita que se guarde el índice.
    # .encode('utf-8') convierte el texto a bytes, que es el formato que necesita el botón de descarga.
    return df.to_csv(index=False).encode('utf-8')


# Llama a la función para convertir el DataFrame filtrado por el usuario.
csv = convert_df_to_csv(df_filtered_sidebar)
# Crea un botón de descarga en la barra lateral.
st.sidebar.download_button(
    label="Descargar datos filtrados en CSV", # Texto que aparece en el botón.
    data=csv,                                 # Los datos (en bytes) que se descargarán.
    file_name='covid_data_filtrada.csv',      # Nombre del archivo que se descargará.
    mime='text/csv',                          # El tipo de archivo (MIME type).
)
