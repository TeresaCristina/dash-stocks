import dash
from dash import dcc
from dash import html
import pandas as pd
import yfinance as yf
from dash import dash_table
from dash.dash_table import DataTable, FormatTemplate
from pandas_datareader import data as pdr
from dash.dependencies import Output, Input
import plotly
import random
import plotly.graph_objs as go
from collections import deque

import plotly.express as px


stocks_test = ["PPL", "SPY", "ENB", "AQN"]
yahooStocks = 'PPL SPY ENB AQN'

yf.pdr_override()  # hijack data from yfinance
# makes every float in dataframe 2 digits
pd.options.display.float_format = '{:,.2f}'.format

# get data
mydata = pdr.get_data_yahoo(yahooStocks, start="2022-01-19", end="2022-01-20")
df = pd.DataFrame(mydata['Open'])  # get recent quote

# format data
for stock in stocks_test:
    df[stock] = df[stock].map(lambda x: '{0:.2f}'.format(x))

df_t = df.T
df_t.columns = ['Quote']
df_t.insert(0, "Ticket", stocks_test, True)

print(df_t)
# dash app
# X = deque(maxlen = 20)
# X.append(1)

# Y = deque(maxlen = 20)
# Y.append(1)
df_test = px.data.stocks()
app = dash.Dash(__name__)

# # money = FormatTemplate.money(2)

app.layout = html.Div(
    [
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df_t.columns],
            data=df_t.to_dict('records')),
        dcc.Dropdown(
            id="ticker",
            options=[{"label": x, "value": x} for x in df_test.columns[1:]],
            value=df_test.columns[1],
            clearable=False,
        ),
         dcc.Dropdown(
            id="second_ticker",
            options=[{"label": x, "value": x} for x in df_test.columns[1:]],
            value=df_test.columns[1],
            clearable=False,
        ),
        dcc.Graph(id="time-series-chart"),
    ]
)

@app.callback(
    Output("time-series-chart", "figure"), 
    [Input("ticker", "value")])
def display_time_series(ticker):
    fig = px.line(df_test, x='date', y=ticker)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
