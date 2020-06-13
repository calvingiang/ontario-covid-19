import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go


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
    custom_layout(fig)
    return fig


def make_line_graph(x, y, title, color=None):
    if color:
        color = dict(color="{}".format(color))
    else:
        color = None
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, name=title,marker=color))

    fig.layout.plot_bgcolor = '#ffffff'
    fig.layout.paper_bgcolor = '#fff'
    fig.layout.yaxis.gridcolor = 'lightgray'
    fig.layout.xaxis.gridcolor = 'lightgray'
    #fig.update_layout(hovermode="x")
    fig.update_layout(title_x=0.5)
    #fig.update_annotations(dict(font=color))

    return fig


def html_graph(classname, graph):
    return html.Div(className=classname,
                    children=[
                              dcc.Graph(figure=graph)
                             ],
                    style={'border': 'solid', 'border-width': '0.1px',
                           'columnCount': 1},
                    )
