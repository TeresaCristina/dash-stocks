import dash
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Output, Input
import plotly.express as px

from formatDate import *
from data import *
from style import *

# get data from yahoo finance for info table
df_t = get_table_info()

data = get_graph_info()
data_f = format_historical_data(data)




# Graph
app = dash.Dash(__name__)

app.layout = html.Div([
    # First Division (Table, Ticker Info)
    html.Div([
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df_t.columns],
            data=df_t.to_dict('records'),
            style_cell_conditional=style_table_cell,
            style_as_list_view=True,
            style_header={
                'backgroundColor': 'gray',
                'fontWeight': 'bold',
                'color': "White"
            },
            style_data_conditional=[{
                'if': {'column_id': 'Ticker'},
                'font-weight': 'bold'
            }],
            fixed_rows={'headers': True},
            style_table={'height': 400}
        )], style={'padding': 10, 'flex': 1}),
    # Second Division (Dropdown, Graph)
    html.Div([
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id="ticker",
                    options=[{"label": x, "value": x}
                             for x in data_f.columns[1:]],
                    value=data_f.columns[1],
                    clearable=False,

                )], style={'padding': 10, 'flex': 1},),
            html.Div([
                dcc.Dropdown(
                    id="second_ticker",
                    options=[{"label": x, "value": x}
                             for x in data_f.columns[1:]],
                    value=data_f.columns[1],
                    clearable=False
                )], style={'padding': 10, 'flex': 1},),
        ], style={'display': 'flex', 'flex-direction': 'row'}),
        html.Div([
            dcc.Graph(id="time-series-chart")
        ]),
    ], style={'padding': 10, 'flex': 2}),
], style={'display': 'flex', 'flex-direction': 'row'}
)

# Graph updates (reacts to user choices)

@app.callback(
    Output("time-series-chart", "figure"),
    Input("ticker", "value"),
    Input("second_ticker", "value"),
)
def display_hist_data(ticker, second_ticker):
    fig = px.line(data_f, x='MyDate', y=ticker)
    fig = px.line(data_f, x='MyDate', y=second_ticker)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
