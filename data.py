import yfinance as yf
import pandas as pd
from pandas_datareader import data as pdr

from formatDate import *

stocks_porfolio = ["VAB.TO", "XGD.TO", "LBS.TO", "VCN.TO", "VDY.TO", "VFV.TO",
                   "VSP.TO", "SRU.UN", "DFN.TO", "CGL.TO", "VGV.TO", "PPL", "SPY", "ENB", "AQN"]
yahooStocks = 'VAB.TO XGD.TO LBS.TO VCN.TO VDY.TO VFV.TO VSP.TO SRU.UN DFN.TO CGL.TO VGV.TO PPL SPY ENB AQN'

# data for the table
def format_quote_value(list_stocks):
    for stock in stocks_porfolio:
        list_stocks[stock] = list_stocks[stock].map(
            lambda x: '{0:.2f}'.format(x))  # format 2 digits
    return list_stocks

def add_ticker_column(list_stocks):
    list_stocks.insert(0, "Ticker", stocks_porfolio, True)
    for stock in stocks_porfolio:
        list_stocks.at[stock, 'Ticker'] = stock
    return list_stocks

def format_table_info(list_stocks):
    df_quote = format_quote_value(list_stocks)
    df_t = df_quote.T
    df_t.columns = ['Quote']
    df_final = add_ticker_column(df_t)
    return df_final

def get_table_info():
    yf.pdr_override()  # hijack data from yfinance
    ydata = pdr.get_data_yahoo(
        yahooStocks, start=get_today(), end=get_tomorrow())
    df = pd.DataFrame(ydata['Open'])  # get table with recent quote
    df_final = format_table_info(df)
    return df_final

# data for the graph
def get_graph_info():
    ydata = pdr.get_data_yahoo(yahooStocks, start=get_years(5), end=get_tomorrow())
    return pd.DataFrame(ydata['Open'])  # get table with recent quote

def format_historical_data(list_stocks):
    list_stocks['MyDate'] = ""
    list_stocks['MyDate']=list_stocks.index
    return list_stocks
    