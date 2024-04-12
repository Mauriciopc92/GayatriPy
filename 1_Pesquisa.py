from functions import get_ticker_data, get_benchmark_data, get_ticker_list
import streamlit as st
import pandas as pd
import webbrowser
import yfinance as yf
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Panorama",
    page_icon= "icons\search_candles.png",
    layout="wide"
)

today = datetime.now()
oneYago = today - timedelta(days=365)
threeMago = today - timedelta(days=90)
oneMago = today - timedelta(days=30)
oneWago = today - timedelta(days=7)

#topbar = option_menu(None, ["Home", "Upload", "Tasks", 'Settings'], 
#    icons=['house', 'cloud-upload', "list-task", 'gear'], 
#    menu_icon="cast", default_index=0, orientation="horizontal")
    #https://icons.getbootstrap.com

# Atualiza a lista de Tickers no primeiro dia do mes, nos demais, le do arquivo csv
if today.day == 1:
    ticker_list = get_ticker_list()
else:
    ticker_list = pd.read_csv("data/tickers.csv")

ticker_list

with st.sidebar:
    ticker = st.text_input('Digite o Ticker', 'PETR4')
    start = st.date_input("Data de inicio", value=oneMago)
    end = st.date_input("Data de fim",value="today")
    #periodo = st.selectbox("Escolha o Tempo Grafico",('1d', '1wk', '1mo', '3mo', '6mo', 'ytd', '1y', '2y', '5y', '10y', 'max'), index=None, placeholder= "Time Frame")

benchClose = get_benchmark_data("^BVSP", start, end) # periodo,
stockClose = get_ticker_data(ticker, start, end) # periodo,

benchPctChange = benchClose.pct_change() * 100
stockPctChange = stockClose.pct_change() * 100
pctChange = pd.DataFrame({
    'Data': benchClose.index,
    '% IBOV': benchPctChange.values,
    '% {}'.format(ticker.upper()): stockPctChange.values
})
pctChange = pctChange.dropna()
pctChange["Data"] = pctChange["Data"].astype(str).str.slice(0, 10)
pctChange["% IBOV"] = pctChange["% IBOV"].astype(float)
pctChange['% {}'.format(ticker.upper())] = pctChange['% {}'.format(ticker.upper())].astype(float)
pctChange = pctChange.iloc[::-1].reset_index(drop=True) # Ordena as linhas pelo mais recente
pctChange["%Ratio"] = pctChange['% {}'.format(ticker.upper())] / pctChange["% IBOV"]

ratio = stockClose/benchClose
empresa = yf.Ticker(f"{ticker}.sa")
hist = empresa.history(start=start, end=end) #period=periodo, 
yestPrice = hist["Close"].iloc[-1]
earnings = empresa.earnings_dates.drop_duplicates()

st.header(f"{empresa.info['longName']}")
st.divider()
col1, col2 = st.columns(2)
#st.write(empresa.info)
with col1:
    col3, col4 = st.columns(2)
    with col3:
        st.metric("Preço", "R$ {:.2f}".format(empresa.info['currentPrice']), " ")
        st.metric("Variação no dia", "R$ {:.2f}".format(empresa.info['currentPrice'] - yestPrice), 
                "{:.2f}%".format(((empresa.info['currentPrice'] - yestPrice) /yestPrice) *100))
    with col4:
        st.metric("Média de 52 Semanas", 
                "R$ {:.2f}".format(empresa.info['fiftyDayAverage']), 
                "{:.2f}%".format(empresa.info['52WeekChange']))
        st.metric("Ratio", "{:.2f}%".format(pctChange["%Ratio"].iloc[0]), " ")

    st.divider()

    st.write("Desempenho de {} vs IBOV (%)".format(ticker.upper()))
    st.line_chart(
    pctChange, x="Data", y=["% IBOV", "% {}".format(ticker.upper())], color=["#16acc9", "#c98e02"]  # Optional
    )
    st.write("Desempenho de {} vs Empresas do Setor (%)".format(ticker.upper()))
    st.line_chart(
    pctChange, x="Data", y=["% IBOV", "% {}".format(ticker.upper())], color=["#16acc9", "#c98e02"]  # Optional
    )    

with col2:
    st.write("Balanços de {}".format(ticker.upper()))
    #st.write(earnings)
    st.bar_chart(earnings["Reported EPS"])

st.divider()





