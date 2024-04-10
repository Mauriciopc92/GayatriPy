import streamlit as st
import pandas as pd
import yfinance as yf
import webbrowser
from datetime import datetime, timedelta
import streamlit.components.v1 as components



st.set_page_config(
    page_title="Backtest",
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

with st.sidebar:
    ticker = st.text_input('Digite o Ticker', '')
    #start = st.date_input("Data de inicio", value=oneMago)
    #end = st.date_input("Data de fim",value="today")
    #periodo = st.selectbox("Escolha o Tempo Grafico",('1d', '1wk', '1mo', '3mo', '6mo', 'ytd', '1y', '2y', '5y', '10y', 'max'), index=None, placeholder= "Time Frame")

st.header("Próximos Balanços")


#components.html("""<iframe frameborder="0" scrolling="no" height=82 width="231" allowtransparency="true" marginwidth="0" marginheight="0" src="https://sslirates.investing.com/index.php?rows=2&bg1=000000&bg2=000000&text_color=e3e3e3&enable_border=hide&border_color=0452A1&header_bg=0452A1&header_text=FFFFFF&force_lang=12" align="center"></iframe><br /><table width="200"><tbody><tr><td style="text-align:left"><a href="//www.investing.com" rel="nofollow" target="_blank"><img style="vertical-align:middle;" title="Investing.com" alt="Investing.com" border="0" src="https://92f8049275b46d631f32-c598b43a8fdedd4f0b9230706bd7ad18.ssl.cf1.rackcdn.com/forexpros_en_logo.png"></a></td></tr><tr><td><span style="font-size: 11px;color: #333333;text-decoration: none;">Taxas de Juros fornecidas por <a href="https://br.investing.com/" rel="nofollow" target="_blank" style="font-size: 11px;color: #06529D; font-weight: bold;" class="underline_link">Investing.com Brasil</a>.</span></td></tr></tbody></table>""")