import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

from app.app import load_data

st.set_page_config(page_title="Clustering y PCA", layout="wide")
st.title("Segmentación de Países y Reducción de Dimensionalidad")

df_raw, df_country = load_data()

# --- 4.1 y 4.2: K-means y PCA ---
st.header("Clustering de Países con K-means y PCA")
features = ['Confirmed', 'Deaths', 'Recovered', 'Active', 'CFR']
df_cluster = df_country.dropna(subset=features)
df_cluster_features = df_cluster[features]

# Escalar datos
scaler = StandardScaler()
scaled_features = scaler.fit_transform(df_cluster_features)

# Aplicar PCA
n_components = st.slider("Número de Componentes Principales (PCA):", 2, 5, 2)
pca = PCA(n_components=n_components)
principal_components = pca.fit_transform(scaled_features)
df_pca = pd.DataFrame(data=principal_components, columns=[f'PC{i+1}' for i in range(n_components)])

# Aplicar K-means
n_clusters = st.slider("Número de Clusters (K-means):", 2, 10, 4)
kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
df_cluster['Cluster'] = kmeans.fit_predict(scaled_features)
df_pca['Cluster'] = df_cluster['Cluster']
df_pca['Country'] = df_cluster['Country_Region']

# Visualizar
st.subheader("Scatter Plot de Clusters (PC1 vs PC2)")
fig_pca = px.scatter(
    df_pca,
    x='PC1',
    y='PC2',
    color='Cluster',
    hover_name='Country',
    title="Segmentación de Países basada en PCA y K-means"
)
st.plotly_chart(fig_pca, use_container_width=True)

# --- 4.3: Interpretación de Clusters ---
st.header("Interpretación de los Clusters")
cluster_summary = df_cluster.groupby('Cluster')[features].mean().reset_index()
st.dataframe(cluster_summary)
st.info("""
**Interpretación (Ejemplo):**
- **Cluster 0:** Podría representar países con un alto volumen de casos confirmados y recuperados, pero una CFR moderada.
- **Cluster 1:** Países con bajo volumen general de casos.
- **Cluster 2:** Países con una alta tasa de fatalidad (CFR) en comparación con su número de casos.
""")
