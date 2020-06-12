import dash
import dash_core_components as dcc
import dash_html_components as html
from pandas_datareader.data import DataReader
import time
from collections import deque
import plotly.graph_objs as go
import random
from get_data import get_cases_only

cases_df = get_cases_only()

x = list(cases_df['Reported Date'])
y = list(cases_df['New Cases'])
# first lesson
app = dash.Dash()
app.layout = html.Div(children=[
    html.H1('Covid-19 New Cases in Ontario'),
    dcc.Graph(id='example',
              figure ={
                  'data': [{'x':x, 'y':y, 'type': 'bar',
                            'name':'cases'},
                           ],
              'layout': {
                  'title': 'Basic Dash Example'
              }
              })

    ])



if __name__ == '__main__':
    app.run_server(debug=True)