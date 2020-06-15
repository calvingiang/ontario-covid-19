import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas
import plotly.express as px
from datetime import datetime
from get_data import get_cases_only
from operators import (html_graph, make_bar_graph, make_line_graph,
                       get_multi_linegraph, get_multibargraph)


# case data
cases_df = get_cases_only()
x = list(cases_df['Reported Date'])
y_cases = list(cases_df['New Cases'])
y_total_cases = list(cases_df['Total Cases'])

# new case today

case_url = 'https://data.ontario.ca/dataset/f4112442-bdc8-45d2-be3c-12efae72fb27/resource/455fd63b-603d-4608-8216-7d8647f43350/download/conposcovidloc.csv'
status_url = 'https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/resource/ed270bb8-340b-41f9-a7c6-e8ef587e6d11/download/covidtesting.csv'
today = x[-1]
yesterday = x[-2]
today_case = y_cases[-1]
yesterday_case = y_cases[-2]
top_table_dict = {'Date':[today, yesterday], 'New Cases': [str(int(today_case)), str(int(yesterday_case))], 'Source': [case_url, status_url]}
top_table = pandas.DataFrame(data=top_table_dict)

# new case bar graph
new_case_bar = make_bar_graph(x=x, y=y_cases, color="#1891c3",
                              title='Historical New Cases in Ontario')

# total case bar graph
total_case_graph = make_line_graph(x=x, y=y_total_cases, color="#1891c3",
                                   title='Historical Total Cases in Ontario')

# case details
other_df = pandas.read_csv('./src/ontario.csv')

# city graph
reporting_city_df = (other_df.groupby(['Reporting_PHU_City']).size()
                     .reset_index().rename(columns={0: 'total'})
                     .sort_values('total',ascending=False)
                     )

x_city = list(reporting_city_df['Reporting_PHU_City'])
y_city_cases = list(reporting_city_df['total'])
new_city_case_bar = make_bar_graph(x=x_city, y=y_city_cases, color="#1891c3",
                              title='Total Cases Reported in Cities')

# travel related
travel_related_df = (other_df.groupby(['Case_AcquisitionInfo']).size()
                     .reset_index().rename(columns={0: 'total'})
                     .sort_values('total',ascending=False)
                     )
x_acquisition = list(travel_related_df['Case_AcquisitionInfo'])
y_acquisition = list(travel_related_df['total'])
travel_related_bar = make_bar_graph(x=x_acquisition, y=y_acquisition,
                                    color="#1891c3",
                                    title='Covid Contact')
# age group and fatal
fatal_df = other_df.groupby(['Age_Group','Outcome1']).size().reset_index().rename(columns={0: 'total'})
fatal_fig = get_multibargraph(fatal_df, x_column="Age_Group", y_column="total",
                              group_split='Outcome1', title="Cases Outcome per Age Group")


# age graph
age_df = other_df.groupby(['Accurate_Episode_Date', 'Age_Group']
                             ).size().reset_index().rename(columns={0: 'total'})
age_list = list(age_df['Age_Group'].unique())
age_line_graph = get_multi_linegraph(age_df, 'Accurate_Episode_Date',
                                        'Age_Group', age_list,
                                        'Cases by Age Group')

# gender graph
gender_df = other_df.groupby(['Accurate_Episode_Date', 'Client_Gender']
                             ).size().reset_index().rename(columns={0: 'total'})
gender_list = ['FEMALE', 'MALE']
gender_line_graph = get_multi_linegraph(gender_df, 'Accurate_Episode_Date',
                                        'Client_Gender', gender_list,
                                        'Cases by Gender')

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
    html.Div([
        html.P(html.A('Contact Us', href='https://calvingiang.github.io/CV/contact_info.html'), style={'textAlign': 'right', 'font-size': '14px'}),

    ]),

    html.Div([
        html.P('Last updated on {} UCT'.format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")), style={'textAlign': 'right', 'font-size': '12px'})
    ]),

    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in top_table.columns],
        data=top_table.to_dict('records'),
        style_cell = {
                    'font_family': 'arial',
                    'font_size': '16px',
                    'text_align': 'center'
                    }
    ),
    html.Br(),
    html_graph(classname='Historical New Cases', graph=new_case_bar),
    html.Br(),
    html_graph(classname='Historical Total Cases', graph=total_case_graph),
    html.Br(),
    html_graph(classname='Cases by City', graph=new_city_case_bar),
    html.Br(),
    html_graph(classname='Covid Spread', graph=travel_related_bar),
    html.Br(),
    html_graph(classname='fatal', graph=fatal_fig),
    html.Br(),
    html_graph(classname='Age Group', graph=age_line_graph), #fatal_fig
    html.Br(),
    html_graph(classname='Cases by Gender', graph=gender_line_graph),
    html.Br(),




    html.Div(html.P([html.Br()])),

    ])


if __name__ == '__main__':
    app.run_server(debug=True)

sidebysidegraph = """ html.Div(className="reaponsive-table",
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
         ),"""
