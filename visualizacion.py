#-------------------------------------------------------------------------------
# Nombre: Proyecto Individual 2
# Titulo: Mercado Bursatil
# Author:Jose Manuel Bracho Navarro
# Fecha:     28/02/2023
#-------------------------------------------------------------------------------


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import plotly.express as px
import datetime
import seaborn as sns
import pandas_datareader as pdr
import emoji

st.image('https://d31uz8lwfmyn8g.cloudfront.net/Assets/logo-henry-white-lg.png')

#Titulo
st.title('Propuesta de Inversion - Chevron (CVX)')
st.markdown('***')




spy = pd.read_csv('spy.csv')
xle = pd.read_csv('xle.csv')
cvx = pd.read_csv('cvx.csv')
cvx2 = pd.read_csv('cvx2.csv')
petroleo = pd.read_csv('petroleo.csv')
empresas = pd.read_csv("empresas.csv")

spy.set_index("Date", inplace=True)
xle.set_index("Date", inplace=True)
cvx.set_index("Date", inplace=True)
petroleo.set_index("Date", inplace=True)
empresas.set_index("Date", inplace=True)

##Datos

col1, col2 = st.columns(2)

with col1:
    st.subheader(emoji.emojize(':money_with_wings: Market Cap:'))
    st.write('313.11B U$D')
    st.subheader(emoji.emojize(':dollar: Ventas:'))
    st.write('235.75B U$D')
    st.subheader(emoji.emojize(':top: G/A en el 2022:'))
    st.write('124.60%')

    
with col2:
    st.subheader(emoji.emojize(':chart_with_upwards_trend: Precio De La Accion:'))
    st.write('162.41 U$D')
    st.subheader(emoji.emojize(':moneybag: Income :'))
    st.write('35.47B U$D')
    st.subheader(emoji.emojize(':chart_with_upwards_trend: Dividendos %:'))
    st.write('3.72%')

# KPI 1: Porcentaje de cambio en el precio de cierre
change_pct = (cvx["Adj Close"][-1] - cvx["Adj Close"][0]) / cvx["Adj Close"][0] * 100
st.subheader(f":chart_with_upwards_trend: Porcentaje de cambio en el precio de cierre:")
st.write(f"{change_pct:.2f}%")

# KPI 2: Precio promedio de cierre
avg_close_price = cvx["Adj Close"].mean()
st.subheader(f":money_with_wings: Precio promedio de cierre:")
st.write(f"{avg_close_price:.2f} U$D")

# KPI 3: Volatilidad de la acción de CVX en comparación con otras empresas del sector petrolero
# Obtener los datos de las empresas del sector
tickers = ["CVX", "BKR", "HAL", "SLB", "CTRA"]  # Agrega aquí los tickers de las empresas que deseas comparar
petroleum_sector = yf.download(tickers, start='2000-01-01', end='2023-01-22', group_by='ticker')

# Calcular la desviación estándar del precio de cierre ajustado de cada empresa
std_cvx = petroleum_sector["CVX"]["Adj Close"].std()
std_BKR = petroleum_sector["BKR"]["Adj Close"].std()
std_HAL = petroleum_sector["HAL"]["Adj Close"].std()
std_SLB = petroleum_sector["SLB"]["Adj Close"].std()
std_CTRA = petroleum_sector["CTRA"]["Adj Close"].std()

# Crear un DataFrame con los resultados
data = {"Ticker": ["CVX", "BKR", "HAL", "SLB", "CTRA"],
        "Desviación estándar del precio de cierre ajustado": [std_cvx, std_BKR, std_HAL, std_SLB, std_CTRA]}
df = pd.DataFrame(data)

# Mostrar el DataFrame en Streamlit
st.subheader(":fire: Volatilidad de la acción de CVX en comparación con otras empresas del sector petrolero :fire:")
st.write(df)



# 1. VALOR DE CHEVRON

#Gráfico de líneas
st.header('Grafica de la accion CVX')
st.line_chart(cvx.Close)


# 2. Mejor dia de la semana para invertir en CVX
st.header('Mejor Dia De La Semana Para Invertir En CVX')

# Definir el orden de los días de la semana
weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

# Convertir la columna Date 
cvx2["Date"] = pd.to_datetime(cvx2["Date"])
cvx2["Weekday"] = cvx2["Date"].dt.day_name()

# Calcular el rendimiento diario
cvx2["Daily Return"] = cvx2["Adj Close"].pct_change()

# Añadir una columna que contenga el día de la semana correspondiente a cada fecha
cvx2["Weekday"] = cvx2["Date"].dt.day_name()

# Convertir la columna Weekday en una categoría con un orden personalizado de días de la semana
cvx2["Weekday"] = pd.Categorical(cvx2["Weekday"], categories=weekday_order, ordered=True)

# Agrupar los datos por día de la semana y calcular el rendimiento promedio
mean_return = cvx2.groupby("Weekday")["Daily Return"].mean().reset_index()

# Visualizar los resultados en una gráfica de barras
fig = px.bar(mean_return, x="Weekday", y="Daily Return", color="Weekday",
             color_discrete_sequence=px.colors.qualitative.Pastel)
fig.update_layout(title="Rendimiento promedio diario de la acción de Chevron (CVX) por día de la semana")
st.plotly_chart(fig)


#3. Gráfico de empresas históricos: Un gráfico que muestre los precios de cierre históricos de Chevron, el XLE y el SPY desde el 2000.
#  Esto podría ayudar a ilustrar cómo ha evolucionado el precio de Chevron en comparación con el sector energético específicamente.

st.header('Relacion entre los precios de chevron y el XLE (Indice del sector energetico)')

# Tickers de Chevron y del petróleo crudo
chevron = cvx
xle = xle

# Creación de un DataFrame con los precios de Chevron y del petróleo crudo
prices_df = pd.DataFrame({"Chevron": cvx["Adj Close"], "XLE": xle["Adj Close"]})

# Creación del gráfico de líneas
fig = px.line(prices_df, title="Relación entre los precios de Chevron y del XLE")

# Agregar las series de datos para Chevron y el petróleo crudo
fig.add_scatter(x=prices_df.index, y=prices_df["Chevron"], name="Chevron")
fig.add_scatter(x=prices_df.index, y=prices_df["XLE"], name="XLE")

# Mostrar el gráfico en Streamlit
st.plotly_chart(fig)



# 4. Relacion con los precios de chevron y el petroleo crudo

st.header('Relacion entre los precios de chevron y el petroleo crudo')

# Tickers de Chevron y del petróleo crudo
chevron = cvx
crude_oil = petroleo

# Creación de un DataFrame con los precios de Chevron y del petróleo crudo
prices_df = pd.DataFrame({"Chevron": cvx["Adj Close"], "Crude Oil": crude_oil["Adj Close"]})

# Creación del gráfico de líneas
fig = px.line(prices_df, title="Relación entre los empresas de Chevron y del petróleo crudo")

# Agregar las series de datos para Chevron y el petróleo crudo
fig.add_scatter(x=prices_df.index, y=prices_df["Chevron"], name="Chevron")
fig.add_scatter(x=prices_df.index, y=prices_df["Crude Oil"], name="Petróleo crudo")

# Mostrar el gráfico en Streamlit
st.plotly_chart(fig)


# 5. comparacion con otras empresas del sector energetico

st.header('Relacion entre los precios de Chevron(CVX) y 4 empresas importantes del sector energetico')

# Seleccionar solo los precios de cierre
precios_cierre = empresas.filter(regex='_Close')

# Renombrar las columnas eliminando el sufijo "_Close"
nombres_empresas = [nombre[:-6] for nombre in precios_cierre.columns]
precios_cierre.columns = nombres_empresas

# Crear el DataFrame para el gráfico
df = precios_cierre.reset_index()

# Convertir la columna "Date" en índice
df = df.set_index('Date')

# Crear el gráfico de líneas
fig = px.line(df, title="Relación entre los precios de cierre de las empresas BKR, CVX, HAL, SLB y CTRA")

# Agregar las series de datos para cada empresa
for empresa in nombres_empresas:
    fig.add_scatter(x=df.index, y=df[empresa], name=empresa)

# Mostrar el gráfico en Streamlit
st.plotly_chart(fig)






