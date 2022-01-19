import dash
from dash import dcc
from dash import html
import pandas as pd
import yfinance as yf
from dash import dash_table
from dash.dash_table import DataTable, FormatTemplate
import pandas_datareader 
from pandas_datareader import data as pdr

stocks = ["PPL", "SPY"]
yahooStocks = 'PPL SPY'

yf.pdr_override() # hijack data from yfinance
pd.options.display.float_format = '{:,.2f}'.format # makes every float in dataframe 2 digits

# get data
mydata = pdr.get_data_yahoo( yahooStocks, start="2022-01-19", end="2022-01-20")
df = pd.DataFrame(mydata['Open']) # get recent quote

# format data
for stock in stocks:
    df[stock] = df[stock].map(lambda x: '{0:.2f}'.format(x))

df_t = df.T
df_t.columns = ['Quote'] 
df_t.insert(0, "Ticket", stocks, True)

print(df_t)
# dash app
app = dash.Dash(__name__)

# money = FormatTemplate.money(2)

app.layout = dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in df_t.columns],
    data=df_t.to_dict('records'),
)

if __name__ == '__main__':
    app.run_server(debug=True)