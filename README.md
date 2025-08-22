Laboratorio 1.1: Análisis Avanzado de COVID-19
Este proyecto contiene un análisis estadístico completo, modelado predictivo y un dashboard interactivo sobre los datos de incidencia de COVID-19 de la Universidad Johns Hopkins.

Estructura del Proyecto
app/app.py: Aplicación principal de Streamlit.

reports/: Contiene los informes de análisis y la propuesta de startup.

requirements.txt: Dependencias del proyecto.

.gitignore: Archivo para excluir directorios y archivos de Git.

Cómo Ejecutar
Clona el repositorio.

Crea un entorno virtual: python -m venv venv

Activa el entorno: source venv/bin/activate (Linux/macOS) o .\venv\Scripts\Activate.ps1 (Windows).

Instala las dependencias: pip install -r requirements.txt

Ejecuta la aplicación: streamlit run app/app.py

-------------------------------------------------------------

🔬 Dashboard de Análisis de Incidencias de COVID-19
📋 Visión General del Proyecto
Este proyecto es una aplicación web interactiva desarrollada con Streamlit para analizar, visualizar y modelar los datos de incidencias de COVID-19. Basado en el conjunto de datos de la Universidad Johns Hopkins, el dashboard busca ofrecer una visión completa de la pandemia a nivel global, desde el análisis exploratorio hasta técnicas avanzadas de Machine Learning y estadística.

La aplicación está estructurada con múltiples páginas que permiten una navegación fluida entre los diferentes tipos de análisis.

🔗 Demostración en Vivo
Puedes explorar la aplicación en funcionamiento en el siguiente enlace:

📊 Dashboard COVID-19 - covid19-data-analysis-ef.streamlit.app

📂 Estructura del Proyecto
El repositorio está organizado de la siguiente manera:

app/: Contiene todos los archivos de la aplicación Streamlit.

Pagina_Principal.py: La página de inicio del dashboard con KPIs clave y visualizaciones globales.

pages/: Directorio que aloja las páginas adicionales de la aplicación.

Calidad_Datos.py: Análisis de calidad de datos, valores nulos y un gráfico de control simulado.

Clustering_PCA.py: Aplicación de técnicas de aprendizaje no supervisado para segmentar países.

Estadistica.py: Análisis estadístico con intervalos de confianza y tests de hipótesis.

Modelado_Temporal.py: (Nota: Aunque el archivo está, actualmente no se muestra el código de modelado temporal en el repositorio).

requirements.txt: Lista de dependencias de Python necesarias para ejecutar la aplicación.

report/: Documentos en formato Markdown con los hallazgos y propuestas del análisis.

estadistica.md: Resumen de los resultados del análisis estadístico.

startup.md: Propuesta de una startup basada en los hallazgos del proyecto.

✨ Funcionalidades Clave
Dashboard Principal Interactivo: Visualiza KPIs globales, un mapa coroplético de casos y gráficos de barras de los países más afectados.

Análisis de Calidad de Datos: Muestra la distribución de la tasa de mortalidad y simula un gráfico de control para la detección de anomalías.

Análisis Estadístico Avanzado: Calcula intervalos de confianza para la Tasa de Mortalidad (CFR) y realiza un test de hipótesis para comparar la CFR entre dos países.

Clustering y PCA: Utiliza Análisis de Componentes Principales (PCA) para reducir la dimensionalidad de los datos y aplica K-means para agrupar países con características de incidencia de COVID-19 similares.

🛠️ Cómo Ejecutar el Proyecto Localmente
Para clonar este repositorio y ejecutar la aplicación en tu máquina local, sigue estos pasos:

Clonar el repositorio:

git clone https://github.com/EdwinFlores19/Incidencias-Covid-19.git
cd Incidencias-Covid-19

Crear y activar un entorno virtual (recomendado):

python -m venv venv
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate

Instalar las dependencias:

pip install -r requirements.txt

Ejecutar la aplicación:

streamlit run app/Pagina_Principal.py

La aplicación se abrirá en tu navegador por defecto en la dirección http://localhost:8501.

📦 Dependencias
Las librerías requeridas para este proyecto se listan en el archivo requirements.txt:

streamlit

pandas

plotly

scipy

statsmodels

scikit-learn

numpy

openpyxl

prophet

👨‍💻 Autor
Edwin Flores
