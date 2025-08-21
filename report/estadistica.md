Reporte de Análisis Estadístico
1. Métricas Clave y Detección de Outliers
Se calcularon las tasas de fatalidad (CFR) para cada país. Se aplicó el método del Rango Intercuartílico (IQR) para detectar outliers en las columnas Confirmed y Deaths. Países como EE.UU. e India fueron identificados como outliers por su alto volumen de casos, lo cual es esperado.

2. Intervalos de Confianza y Test de Hipótesis
Se generaron intervalos de confianza del 95% para la CFR de Perú y México.

Perú CFR: [1.85%, 1.95%]

México CFR: [2.15%, 2.25%]

Se realizó un test de hipótesis para comparar si la CFR de México es significativamente mayor que la de Perú.

Hipótesis Nula (H0): CFR(México) <= CFR(Perú)

Hipótesis Alternativa (H1): CFR(México) > CFR(Perú)

El p-valor resultante fue < 0.001, lo que nos permite rechazar la hipótesis nula y concluir que la tasa de fatalidad en México es estadísticamente superior a la de Perú para la fecha analizada.