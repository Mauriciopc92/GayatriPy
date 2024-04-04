import streamlit as st
import pandas as pd
import webbrowser
import yfinance as yf
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu


st.set_page_config(
    page_title="Panorama",
    page_icon="C:/Users/mauri/OneDrive/Documentos/Code/Gayatri/icons/search_candles.png",
    layout="wide"
)

def get_ticker_data(ticker, startDate, endDate): # period,
    stock = yf.Ticker(f"{ticker}.sa")
    hist = stock.history(start=startDate, end=endDate)#period=period, 
    fechamento = hist['Close']
    return fechamento

def get_benchmark_data(benchmark, startDate, endDate): # period,
    bench = yf.Ticker(benchmark)
    hist_bench = bench.history(start=startDate, end=endDate) #period=period,
    fechamento_bench = hist_bench['Close']
    return fechamento_bench

#def merge_data(fechamento, fechamento_bench, stock, bench):
    # Unir os DataFrames usando a coluna de data em comum
    df_merged = pd.merge(fechamento, fechamento_bench, on='Date', suffixes=(stock, bench))
    # Resetar o índice
    df_merged = df_merged.reset_index()
    df_merged["Date"] = df_merged["Date"].astype(str).str.slice(0, -15)
    return df_merged

today = datetime.now()
oneYago = today - timedelta(days=365)
threeMago = today - timedelta(days=90)
oneMago = today - timedelta(days=30)
oneWago = today - timedelta(days=7)

#topbar = option_menu(None, ["Home", "Upload", "Tasks", 'Settings'], 
#    icons=['house', 'cloud-upload', "list-task", 'gear'], 
#    menu_icon="cast", default_index=0, orientation="horizontal")
    #https://icons.getbootstrap.com

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

st.header(f"{empresa.info['longName']}")
st.divider()

col3, col4, col5, col6 = st.columns(4)
col3.metric("Preço", "R$ {:.2f}".format(empresa.info['currentPrice']), " ")
col4.metric("Variação no dia", "R$ {:.2f}".format(empresa.info['currentPrice'] - yestPrice), 
            "{:.2f}%".format(((empresa.info['currentPrice'] - yestPrice) /yestPrice) *100))
col5.metric("52 Semanas", 
            "R$ {:.2f} - {:.2f}".format(empresa.info['fiftyTwoWeekLow'], empresa.info['fiftyTwoWeekHigh']), 
            "{:.2f}%".format(empresa.info['52WeekChange']))
col6.metric("Ratio", "{:.2f}%".format(pctChange["%Ratio"].iloc[0]), " ")
st.divider()
st.write("Desempenho de {} vs IBOV (%)".format(ticker.upper()))
st.line_chart(
pctChange, x="Data", y=["% IBOV", "% {}".format(ticker.upper())], color=["#16acc9", "#c98e02"]  # Optional
)
st.write("Desempenho de {} vs Empresas do Setor (%)".format(ticker.upper()))
st.line_chart(
pctChange, x="Data", y=["% IBOV", "% {}".format(ticker.upper())], color=["#16acc9", "#c98e02"]  # Optional
)    
st.divider()

# Setores: 43
# Petroleo, gas e biocombustiveis
#https://www.fundamentus.com.br/resultado.php?setor=30

#Subsetor/segmento: 86
#Exploracao, refino e distribuicao
#https://www.fundamentus.com.br/resultado.php?segmento=52
