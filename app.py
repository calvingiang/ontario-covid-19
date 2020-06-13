import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
# from pandas_datareader.data import DataReader
# import time
# from collections import deque
# import plotly.graph_objs as go
# import random
import pandas
from get_data import get_cases_only
from operators import (html_graph, make_bar_graph, make_line_graph)

cases_df = get_cases_only()

x = list(cases_df['Reported Date'])
y_cases = list(cases_df['New Cases'])
y_total_cases = list(cases_df['Total Cases'])

new_case_bar = make_bar_graph(x=x, y=y_cases, color="#1891c3",
                              title='Historical New Cases in Ontario')
total_case_graph = make_line_graph(x=x, y=y_total_cases, color="#1891c3",
                                 title='Historical Total Cases in Ontario')


# Initiate the app
external_css = ["https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css"]
external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#app = dash.Dash()#external_scripts=external_js,
                #external_stylesheets=external_css)



server = app.server

app.layout = html.Div(children=[
    html.H1('Ontario Covid-19', style={'textAlign': 'center'}),

    html_graph(classname='Historical New Cases', graph=new_case_bar),

    html.Br(),

    html_graph(classname='Historical New Cases', graph=total_case_graph),

    html.Br(),

    html.Div(className="reaponsive-table",
            children=[
                dcc.Graph(id='new_cases1',
                      figure ={
                          'data': [{'x':x, 'y':y_cases, 'type': 'line',
                                    'name':'cases'},
                                   ],
                      'layout': {
                          'title': 'Historical New Cases in Ontario',
                      },

                      }),
                dcc.Graph(id='total_cases1',
                     figure={
                         'data': [{'x': x, 'y': y_total_cases,
                                   'type': 'line',
                                   'name': 'cases'},
                                  ],
                         'layout': {
                             'title': 'Historical Total Cases in Ontario'
                         }
                     })
               ],
            style={'border': 'solid', 'border-width': '0.1px',
                   'columnCount': 2},
         ),

    html.Div(html.P([html.Br()])),

    html.Div(className="reaponsive-table",
        children=[
            dcc.Graph(id='new_cases',
                      figure ={
                            'data': [{'x':x, 'y':y_cases, 'type': 'bar',
                                     'name':'cases'},
                                     {'x':x, 'y':y_cases, 'type': 'line',
                                     'name':'cases1'}
                                   ],
                      'layout': {
                          'title': 'Historical New Cases in Ontario'
                      }
                      }),
        ],
        style={'border': 'solid', 'border-width': '0.2px',
               'whiteSpace': 'normal'},
             ),

    html.Div(html.P([html.Br()])),

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
