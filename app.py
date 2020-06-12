import dash
import dash_core_components as dcc
import dash_html_components as html
# from pandas_datareader.data import DataReader
# import time
# from collections import deque
# import plotly.graph_objs as go
# import random
from get_data import get_cases_only

cases_df = get_cases_only()

x = list(cases_df['Reported Date'])
y_cases = list(cases_df['New Cases'])
y_total_cases = list(cases_df['Total Cases'])

# first lesson
########### Initiate the app
external_css = ["https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css"]
external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']
app = dash.Dash()#external_scripts=external_js,
                #external_stylesheets=external_css)

server = app.server

app.layout = html.Div(children=[
    html.H1('Ontario Covid-19'),
    html.Div(className="reaponsive-table",
        children=[
            dcc.Graph(id='new_cases',
                      figure ={
                          'data': [{'x':x, 'y':y_cases, 'type': 'line',
                                    'name':'cases'},
                                   ],
                      'layout': {
                          'title': 'Historical New Cases in Ontario'
                      }
                      }),
           ],
        style={'border': 'solid', 'border-width': '0.2px'},
     ),

    html.Div(className="reaponsive-table",
        children=[
           dcc.Graph(id='total_cases',
                     figure={
                         'data': [{'x': x, 'y': y_total_cases,
                                   'type': 'line',
                                   'name': 'cases'},
                                  ],
                         'layout': {
                             'title': 'Historical Total Cases in Ontario'
                         }
                     }),
           ],
        style={'border': 'solid', 'border-width': '0.2px'},
     )


    ])

if __name__ == '__main__':
    app.run_server(debug=True)
