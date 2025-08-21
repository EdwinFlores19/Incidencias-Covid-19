import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error

st.set_page_config(page_title="Modelado Temporal", layout="wide")
st.title("Modelado y Proyecciones Temporales")


# --- Carga de Datos de Series Temporales ---
@st.cache_data
def load_time_series_data():
    ts_confirmed_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
    df = pd.read_csv(ts_confirmed_url)

    # Transformar el formato de los datos
    df = df.drop(columns=['Lat', 'Long', 'Province/State'])
    df_melted = df.melt(id_vars=['Country/Region'], var_name='Date', value_name='Confirmed')
    df_melted['Date'] = pd.to_datetime(df_melted['Date'], format='%m/%d/%y')

    # Agrupar por país y fecha
    df_ts = df_melted.groupby(['Country/Region', 'Date'])['Confirmed'].sum().reset_index()
    return df_ts


df_timeseries = load_time_series_data()

st.info("""
Esta sección implementa un modelo de pronóstico **Prophet** para proyectar los casos confirmados a 14 días.
Se incluye la validación del modelo mediante backtesting.
""")

# --- Interfaz de Usuario ---
st.sidebar.header("Configuración del Modelo")
all_countries = sorted(df_timeseries['Country/Region'].unique())
selected_country = st.sidebar.selectbox(
    "Selecciona un país para el pronóstico:",
    all_countries,
    index=all_countries.index('Peru')
)

# --- 3.1: Generar y Visualizar Series de Tiempo ---
st.header(f"Serie de Tiempo para {selected_country}")
df_country_ts = df_timeseries[df_timeseries['Country/Region'] == selected_country].copy()
df_country_ts['Daily New Cases'] = df_country_ts['Confirmed'].diff().fillna(0)
df_country_ts['7-Day Rolling Mean'] = df_country_ts['Daily New Cases'].rolling(window=7).mean()

fig_ts = px.line(df_country_ts, x='Date', y='7-Day Rolling Mean',
                 title=f"Nuevos Casos Diarios (Media Móvil de 7 Días) en {selected_country}")
st.plotly_chart(fig_ts, use_container_width=True)

# --- 3.2 y 3.4: Implementación y Gráfica del Modelo ---
st.header("Pronóstico de Casos Confirmados a 14 Días")

if st.button("Ejecutar Pronóstico"):
    with st.spinner("Entrenando modelo Prophet y generando proyección..."):
        # Preparar datos para Prophet
        df_prophet = df_country_ts[['Date', 'Confirmed']].rename(columns={'Date': 'ds', 'Confirmed': 'y'})

        # 3.3: Validación del modelo con backtesting
        # Dividir datos: 30 días para test, el resto para train
        train_df = df_prophet.iloc[:-30]
        test_df = df_prophet.iloc[-30:]

        # Entrenar modelo de validación
        validation_model = Prophet()
        validation_model.fit(train_df)
        future_validation = validation_model.make_future_dataframe(periods=30)
        forecast_validation = validation_model.predict(future_validation)

        # Calcular errores
        y_true = test_df['y']
        y_pred = forecast_validation['yhat'][-30:]
        mae = mean_absolute_error(y_true, y_pred)
        mape = mean_absolute_percentage_error(y_true, y_pred)

        # Entrenar modelo final con todos los datos
        final_model = Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=False)
        final_model.fit(df_prophet)
        future_final = final_model.make_future_dataframe(periods=14)
        forecast_final = final_model.predict(future_final)

        # Gráfico del pronóstico
        st.subheader("Gráfico de Proyección")
        fig_forecast = go.Figure()
        # Intervalo de confianza
        fig_forecast.add_trace(go.Scatter(
            x=forecast_final['ds'], y=forecast_final['yhat_upper'], fill=None, mode='lines',
            line_color='rgba(0,176,246,0.2)', name='Límite Superior'
        ))
        fig_forecast.add_trace(go.Scatter(
            x=forecast_final['ds'], y=forecast_final['yhat_lower'], fill='tonexty', mode='lines',
            line_color='rgba(0,176,246,0.2)', name='Límite Inferior'
        ))
        # Datos históricos
        fig_forecast.add_trace(go.Scatter(
            x=df_prophet['ds'], y=df_prophet['y'], mode='markers', name='Datos Históricos',
            marker=dict(color='black', size=4)
        ))
        # Predicción
        fig_forecast.add_trace(go.Scatter(
            x=forecast_final['ds'], y=forecast_final['yhat'], mode='lines', name='Predicción', line=dict(color='red')
        ))
        fig_forecast.update_layout(title=f'Pronóstico de Casos Confirmados para {selected_country}',
                                   xaxis_title='Fecha', yaxis_title='Casos Confirmados')
        st.plotly_chart(fig_forecast, use_container_width=True)

        # Mostrar métricas de validación
        st.subheader("Validación del Modelo (Backtesting a 30 días)")
        col1, col2 = st.columns(2)
        col1.metric("Error Absoluto Medio (MAE)", f"{mae:,.0f}")
        col2.metric("Error Porcentual Absoluto Medio (MAPE)", f"{mape:.2%}")

        st.subheader("Datos del Pronóstico a 14 días")
        st.dataframe(forecast_final[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(14))
else:
    st.info("Haz clic en el botón para generar el pronóstico.")
