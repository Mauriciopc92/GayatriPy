import yfinance as yf

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


#Importar as datas dos Proximos balancos
#def get_upcoming_earnings()


#Gerar lista de setores e salvar no csv, checar se ha novas empresas nos setores e adicionar ao csv
#def get_sector()

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