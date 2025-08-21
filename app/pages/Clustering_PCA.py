# Importa las librerías necesarias.
import streamlit as st  # Para crear la interfaz web.
import pandas as pd     # Para la manipulación de datos.
import plotly.express as px # Para crear gráficos interactivos.
from sklearn.preprocessing import StandardScaler # Para estandarizar los datos (muy importante para PCA y K-means).
from sklearn.decomposition import PCA          # Para el Análisis de Componentes Principales (reducir dimensiones).
from sklearn.cluster import KMeans             # Para el algoritmo de clustering K-means.

# Importa la función 'load_data' desde el archivo principal 'Pagina_Principal.py'.
# Esto permite que todas las páginas usen los mismos datos cacheados.
from Pagina_Principal import load_data

# Configura las propiedades de la página, como el título en la pestaña del navegador y el layout.
st.set_page_config(page_title="Clustering y PCA", layout="wide")
# Muestra el título principal de la página.
st.title("Segmentación de Países y Reducción de Dimensionalidad")

# Llama a la función para cargar los datos crudos y los datos agrupados por país.
df_raw, df_country = load_data()

# --- 4.1 y 4.2: K-means y PCA ---
# Encabezado para la sección de clustering.
st.header("Clustering de Países con K-means y PCA")
# Define la lista de características (columnas) que se usarán para el análisis.
features = ['Confirmed', 'Deaths', 'Recovered', 'Active', 'CFR']
# Crea una copia del DataFrame, eliminando las filas que tengan valores nulos en las columnas seleccionadas.
# .copy() se usa para evitar advertencias de pandas al modificar el DataFrame más adelante.
df_cluster = df_country.dropna(subset=features).copy()
# Crea un DataFrame que contiene solo las columnas de características para el modelado.
df_cluster_features = df_cluster[features]

# Escala los datos para que todas las características tengan la misma importancia (media 0, desviación estándar 1).
scaler = StandardScaler() # Crea una instancia del escalador.
scaled_features = scaler.fit_transform(df_cluster_features) # Ajusta y transforma los datos.

# Aplica el Análisis de Componentes Principales (PCA) para reducir la dimensionalidad.
# Crea un slider para que el usuario elija cuántas "super-variables" (componentes) quiere generar.
n_components = st.slider("Número de Componentes Principales (PCA):", 2, 5, 2)
pca = PCA(n_components=n_components) # Crea una instancia de PCA con el número de componentes elegido.
principal_components = pca.fit_transform(scaled_features) # Aplica PCA a los datos escalados.
# Crea un nuevo DataFrame con los resultados de PCA.
df_pca = pd.DataFrame(data=principal_components, columns=[f'PC{i+1}' for i in range(n_components)])

# Aplica el algoritmo K-means para agrupar los países en clusters.
# Crea un slider para que el usuario elija cuántos grupos (clusters) quiere encontrar.
n_clusters = st.slider("Número de Clusters (K-means):", 2, 10, 4)
# Crea una instancia de K-means. random_state asegura que los resultados sean reproducibles.
kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
# Aplica K-means a los datos escalados y añade la etiqueta del cluster a cada país en el DataFrame.
df_cluster['Cluster'] = kmeans.fit_predict(scaled_features)
# Añade la columna de clusters al DataFrame de PCA para poder colorear el gráfico.
df_pca['Cluster'] = df_cluster['Cluster']
# Añade la columna de nombres de países al DataFrame de PCA para mostrarla en el gráfico.
df_pca['Country'] = df_cluster['Country_Region']

# Visualiza los resultados del clustering.
st.subheader("Scatter Plot de Clusters (PC1 vs PC2)")
# Crea un gráfico de dispersión interactivo con Plotly.
fig_pca = px.scatter(
    df_pca,
    x='PC1',                       # El eje X es el Componente Principal 1.
    y='PC2',                       # El eje Y es el Componente Principal 2.
    color='Cluster',               # El color de cada punto (país) se basa en el cluster al que pertenece.
    hover_name='Country',          # Muestra el nombre del país al pasar el cursor sobre un punto.
    title="Segmentación de Países basada en PCA y K-means"
)
# Muestra el gráfico en la aplicación.
st.plotly_chart(fig_pca, use_container_width=True)

# --- 4.3: Interpretación de Clusters ---
# Encabezado para la sección de interpretación.
st.header("Interpretación de los Clusters")
# Calcula el valor promedio de cada característica para cada cluster.
cluster_summary = df_cluster.groupby('Cluster')[features].mean().reset_index()
# Muestra la tabla con los promedios, lo que ayuda a entender qué define a cada grupo.
st.dataframe(cluster_summary)
# Muestra un cuadro de información con un ejemplo de cómo interpretar los resultados.
st.info("""
**Interpretación (Ejemplo):**
- **Cluster 0:** Podría representar países con un alto volumen de casos confirmados y recuperados, pero una CFR moderada.
- **Cluster 1:** Países con bajo volumen general de casos.
- **Cluster 2:** Países con una alta tasa de fatalidad (CFR) en comparación con su número de casos.
""")
