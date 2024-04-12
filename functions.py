import yfinance as yf
import pandas as pd
from io import StringIO
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = Options()
chrome_options.add_argument('--headless')

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

def get_ticker_list():
    driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get('https://fundamentus.com.br/resultado.php')
    local_tabela = '/html/body/div[1]/div[2]/table'
    tabela = driver.find_element('xpath', local_tabela)
    html_tabela = tabela.get_attribute('outerHTML')
    tabela = pd.read_html(StringIO(str(html_tabela)))[0]  # FutureWarning: Passing literal html to 'read_html' is deprecated and will be removed in a future version. To read from a literal string, wrap it in a 'StringIO' object.
    driver.quit()
    tickers = tabela["Papel"].sort_values()
    tickers.to_csv('data/tickers.csv', index=False)
    return tickers

#Gerar lista de setores e salvar no csv, checar se ha novas empresas nos setores e adicionar ao csv
def get_sector():
    tickers = pd.read_csv('data/tickers.csv')
    driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get('https://www.fundamentus.com.br/detalhes.php?papel=ALPA4')
    local_tabela = '/html/body/div[1]/div[2]/table'
    tabela = driver.find_element('xpath', local_tabela)    
    pass

#Importar as datas dos Proximos balancos
def get_upcoming_earnings():
    pass






### ANOTACOES ###

# Setores: 43
# Petroleo, gas e biocombustiveis
#https://www.fundamentus.com.br/resultado.php?setor=30

#Subsetor/segmento: 86
#Exploracao, refino e distribuicao
#https://www.fundamentus.com.br/resultado.php?segmento=52

#def merge_data(fechamento, fechamento_bench, stock, bench):
    # Unir os DataFrames usando a coluna de data em comum
    #df_merged = pd.merge(fechamento, fechamento_bench, on='Date', suffixes=(stock, bench))
    # Resetar o índice
    #df_merged = df_merged.reset_index()
    #df_merged["Date"] = df_merged["Date"].astype(str).str.slice(0, -15)
    #return df_merged