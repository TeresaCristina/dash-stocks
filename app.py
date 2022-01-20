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
from datetime import date
import plotly.express as px
import datetime

stocks_test = ["PPL", "SPY", "ENB", "AQN"]
yahooStocks = 'PPL SPY ENB AQN'

# dates for the info table
def format_date(myDate):
    return myDate.strftime("%Y-%m-%d")

def get_today():
    return format_date(date.today())

def get_tomorrow():
    tomorrow = date.today() + datetime.timedelta(days=1)
    return format_date(tomorrow)

# get data from yahoo finance for info table
yf.pdr_override()  # hijack data from yfinance
ydata = pdr.get_data_yahoo(yahooStocks, start=get_today(), end=get_tomorrow())
df = pd.DataFrame(ydata['Open'])  # get recent quote
for stock in stocks_test:
    df[stock] = df[stock].map(lambda x: '{0:.2f}'.format(x)) # format 2 digits
df_t = df.T
df_t.columns = ['Quote']
df_t.insert(0, "Ticket", stocks_test, True)

# Graph

app = dash.Dash(__name__)

app.layout = html.Div([
    # First Division (Table, Ticker Info)
    html.Div([
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df_t.columns],
            data=df_t.to_dict('records')
        )], style={'padding': 10, 'flex': 1}),
    # Second Division (Dropdown, Graph)
    html.Div([
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id="ticker",
                    options=[{"label": x, "value": x}
                             for x in df_t.columns[1:]],
                    value=df_t.columns[1],
                    clearable=False,

                )], style={'padding': 10, 'flex': 1},),
            html.Div([
                dcc.Dropdown(
                    id="second_ticker",
                    options=[{"label": x, "value": x}
                             for x in df_t.columns[1:]],
                    value=df_t.columns[1],
                    clearable=False
                )], style={'padding': 10, 'flex': 1},),
        ], style={'display': 'flex', 'flex-direction': 'row'}),
        html.Div([
            dcc.Graph(id="time-series-chart")
        ]),
    ], style={'padding': 10, 'flex': 1}),
], style={'display': 'flex', 'flex-direction': 'row'}
)

# Graph updates (reacts to user choices)
@app.callback(
    Output("time-series-chart", "figure"),
    Input("ticker", "value"),
    Input("second_ticker", "value"),
)
def display_hist_data(ticker, second_ticker):
    fig = px.line(df_t, x='Quote', y=ticker)
    fig = px.line(df_t, x='Quote', y=second_ticker)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
