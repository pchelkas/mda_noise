import dash
from dash import html, dcc



dash.register_page(__name__)

layout = html.Div(children=[
    html.H1(children='This is our Test page'),

    html.Div(children='''
        This is our test content.
    '''),

])