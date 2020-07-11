import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas
import plotly.express as px
import plotly.graph_objects as go


def ontario_other_data():
    df = pandas.read_csv('./src/ontario.csv')
    return df.iloc[:, 3:]

def custom_layout(fig):
    fig.layout.plot_bgcolor = '#ffffff'
    fig.layout.paper_bgcolor = '#fff'
    fig.layout.yaxis.gridcolor = 'lightgray'
    fig.layout.xaxis.gridcolor = 'lightgray'
    fig.update_layout(hovermode="x")
    fig.update_layout(title_x=0.5)
    return fig


def make_bar_graph(x, y, title, color=None):
    if color:
        color = dict(color="{}".format(color))
    else:
        color = None
    fig = go.Figure(
        data=[go.Bar(y=y, x=x, marker=color)],
        layout_title_text=title,
    )
    fig = custom_layout(fig)
    return fig


def make_line_graph(x, y, title, color=None):
    if color:
        color = dict(color="{}".format(color))
    else:
        color = None
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, marker=color))
    fig.layout.title = title
    fig = custom_layout(fig)

    return fig


def get_multibargraph(df, x_column, y_column, group_split, title=None):
    fig = px.bar(df, x=x_column, y=y_column, color=group_split,
                       barmode='group',
                       height=400)
    if title:
        fig.layout.title = title
    fig = custom_layout(fig)
    return fig

def get_multi_linegraph(df, x_column, y_column, unique_feature_list,
                        title=None):
    random_color_list = ['#4E79A7', '#F28E2B', '#E15759', '#76B7B2', '#59A14F',
                         '#EDC948', '#B07AA1', '#FF9DA7', '#9C755F', '#BAB0AC']
    fig = go.Figure()
    num = 0
    for name in unique_feature_list:
        if num > 7:
            num = 0
        x = list(df.loc[df[y_column] == name][x_column])
        y = list(df.loc[df[y_column] == name].total)
        fig.add_trace(go.Scatter(x=x, y=y, name=name.lower(),
                                 line=dict(color=random_color_list[num],
                                           width=3)))
        num += 1
    if title:
        fig.layout.title = title
    fig = custom_layout(fig)
    return fig
    print('')

def html_graph(classname, graph):
    return html.Div(className=classname,
                    children=[
                              dcc.Graph(figure=graph)
                             ],
                    style={'border': 'solid', 'border-width': '0.1px',
                           'columnCount': 1},
                    )

