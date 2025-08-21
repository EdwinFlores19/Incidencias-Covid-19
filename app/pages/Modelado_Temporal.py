# Importa las librerías necesarias.
import streamlit as st  # Para crear la interfaz web.
import pandas as pd     # Para la manipulación y análisis de datos.
import plotly.express as px # Para crear gráficos interactivos.
from scipy import stats # Específicamente para funciones estadísticas como los intervalos de confianza.
import numpy as np      # Para operaciones numéricas, especialmente con arrays.

# Importa la función 'load_data' desde el archivo principal 'Pagina_Principal.py'.
# Esto permite que todas las páginas usen los mismos datos cacheados.
from Pagina_Principal import load_data

# Configura las propiedades de la página, como el título en la pestaña del navegador y el layout.
st.set_page_config(page_title="Estadística Avanzada", layout="wide")
# Muestra el título principal de la página.
st.title("Estadística Descriptiva y Avanzada")

# Llama a la función para cargar los datos crudos y los datos agrupados por país.
df_raw, df_country = load_data()

# --- 2.1 y 2.4: Métricas y Detección de Outliers ---
# Encabezado para la primera sección de análisis.
st.header("Métricas Clave y Detección de Outliers")
# Muestra una tabla con las estadísticas descriptivas (media, std, min, max, etc.) del DataFrame por país.
st.dataframe(df_country.describe())

# Sub-encabezado para la sección de boxplots.
st.subheader("Boxplots para Detección de Outliers")
# Crea una figura de diagrama de caja (boxplot) con Plotly para visualizar la distribución y los outliers.
fig_box = px.box(df_country, y=['Confirmed', 'Deaths', 'Recovered', 'Active'],
                 title="Diagramas de Caja para Métricas Principales")
# Muestra el gráfico en la aplicación, haciendo que ocupe todo el ancho disponible.
st.plotly_chart(fig_box, use_container_width=True)

# --- 2.2: Intervalos de Confianza ---
# Encabezado para la sección de intervalos de confianza.
st.header("Intervalos de Confianza para CFR")
# Crea un widget de selección múltiple para que el usuario elija los países a analizar.
countries_ic = st.multiselect("Selecciona países para calcular IC del CFR:",
                              options=df_country['Country_Region'].unique(), default=['Peru', 'Mexico'])

# Comprueba si el usuario ha seleccionado al menos un país.
if countries_ic:
    results = [] # Inicializa una lista vacía para guardar los resultados.
    # Itera sobre cada país seleccionado por el usuario.
    for country in countries_ic:
        # Filtra el DataFrame para obtener solo los datos del país actual.
        data = df_country[df_country['Country_Region'] == country]
        # Extrae el número de casos confirmados. .iloc[0] selecciona el primer (y único) valor.
        confirmed = data['Confirmed'].iloc[0]
        # Extrae el número de fallecidos.
        deaths = data['Deaths'].iloc[0]

        # Se asegura de que el número de confirmados sea mayor que cero para evitar divisiones por cero.
        if confirmed > 0:
            # Calcula la proporción de muertes (p-hat), que es la estimación de la CFR.
            p_hat = deaths / confirmed
            # Calcula el error estándar de la proporción.
            se = np.sqrt((p_hat * (1 - p_hat)) / confirmed)
            # Calcula el intervalo de confianza del 95% para la proporción usando la distribución normal.
            ci = stats.norm.interval(0.95, loc=p_hat, scale=se)
            # Agrega un diccionario con los resultados formateados a la lista de resultados.
            results.append({
                'País': country,
                'CFR (%)': f"{(p_hat * 100):.2f}",
                'IC 95% Límite Inferior (%)': f"{(ci[0] * 100):.2f}",
                'IC 95% Límite Superior (%)': f"{(ci[1] * 100):.2f}"
            })
    # Muestra los resultados en una tabla estática.
    st.table(pd.DataFrame(results))

# --- 2.3: Test de Hipótesis ---
# Encabezado para la sección de test de hipótesis.
st.header("Test de Hipótesis para Comparar CFR")
# Crea dos columnas para colocar los selectores de países uno al lado del otro.
col1, col2 = st.columns(2)
# Crea un selector en la primera columna para el País 1, con Perú como valor por defecto.
country1 = col1.selectbox("Selecciona País 1:", options=df_country['Country_Region'].unique(), index=150)  # Peru
# Crea un selector en la segunda columna para el País 2, con México como valor por defecto.
country2 = col2.selectbox("Selecciona País 2:", options=df_country['Country_Region'].unique(), index=122)  # Mexico

# Comprueba si el usuario ha hecho clic en el botón para realizar el test.
if st.button("Realizar Test de Hipótesis (CFR País 2 > CFR País 1)"):
    # Importa la función necesaria para el test de proporciones desde la librería statsmodels.
    from statsmodels.stats.proportion import proportions_ztest

    # Filtra los datos para obtener la fila correspondiente al País 1.
    data1 = df_country[df_country['Country_Region'] == country1]
    # Filtra los datos para obtener la fila correspondiente al País 2.
    data2 = df_country[df_country['Country_Region'] == country2]

    # Crea un array de NumPy con el número de "éxitos" (muertes) para cada país.
    count = np.array([data2['Deaths'].iloc[0], data1['Deaths'].iloc[0]])
    # Crea un array de NumPy con el número de "observaciones" (casos confirmados) para cada país.
    nobs = np.array([data2['Confirmed'].iloc[0], data1['Confirmed'].iloc[0]])

    # Realiza el test Z para dos proporciones. 'alternative='larger'' especifica que es un test de una cola.
    stat, pval = proportions_ztest(count, nobs, alternative='larger')

    # Muestra las hipótesis del test en la aplicación.
    st.write(f"**Hipótesis Nula (H0):** CFR({country2}) <= CFR({country1})")
    st.write(f"**Hipótesis Alternativa (H1):** CFR({country2}) > CFR({country1})")
    # Muestra el p-valor resultante en un formato de métrica.
    st.metric("P-valor", f"{pval:.4f}")
    # Comprueba si el p-valor es menor que el nivel de significancia (0.05).
    if pval < 0.05:
        # Si es menor, se rechaza la H0 y se muestra un mensaje de éxito.
        st.success("Se rechaza la hipótesis nula. La CFR del País 2 es significativamente mayor que la del País 1.")
    else:
        # Si no es menor, no se puede rechazar la H0 y se muestra un mensaje de advertencia.
        st.warning("No se puede rechazar la hipótesis nula.")
