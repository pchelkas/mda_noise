#!/usr/bin/env python
# coding: utf-8



from datetime import datetime,date
import plotly.express as px
import dash
from dash import dcc, html, ctx
from dash.dependencies import Input, Output
import pandas as pd





# Data import
noise_map = pd.read_csv("Percentile Noise Weather for APP_Un-scaled_NAdropped.csv")
noise_map.head()




external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
        dcc.DatePickerSingle(
        id="noise-date-picker",
        calendar_orientation="horizontal",
        day_size=39,
        number_of_months_shown=1,
        min_date_allowed=date(2022, 2, 17),
        max_date_allowed=date(2022, 12, 31),
        initial_visible_month=date(2022, 2, 17),
        date=date(2022, 2, 17),
        month_format="MMMM, YYYY"
    ),
        html.Div(id="output-date-picker"),
        html.H3("Noise level in Leuven 2022, by hour", style={'textAlign': 'center'}),
        html.Button('laf005', id='btn-nclicks-1', n_clicks=0),
        html.Button('laf995', id='btn-nclicks-2', n_clicks=0),
        html.Div(id='container-button-timestamp'),
        dcc.Slider(
        id="hour-slider",
        min=0, max=23,
        step=None,
        value=0,
        marks={str(hour): str(hour)+":00" for hour in range(0, 24)}
        ),
        dcc.Graph(id="noise-map")
])

@app.callback(
    Output('output-date-picker', 'children'),
    Output('container-button-timestamp', 'children'),
    Output("noise-map", "figure"),
    Input("noise-date-picker", "date"),
    Input("hour-slider","value"),
    Input('btn-nclicks-1', 'n_clicks'),
    Input('btn-nclicks-2', 'n_clicks'),
)

def update_output(date_value, hour_value, btn1, btn2):
    date_object = date.fromisoformat(date_value)

    string_prefix = 'You have selected: '
    date_string = date_object.strftime('%b %d, %A')
    month = date_object.month
    day = date_object.day
    noise_map_date = noise_map[(noise_map["month"]==month)
                               &(noise_map["day"]==day)
                               &(noise_map["hour"]==hour_value)]

    msg = "Noise map of laf 0.5% was selected"
    fig = px.density_mapbox(noise_map_date,lat="latitude", lon="longitude",
                            z="laf005_per_hour", radius=20, zoom=16, height=650, range_color=[40,80],
                            center={"lat":50.87467323, "lon":4.699916431},
                            mapbox_style="open-street-map",
                            hover_data={"description_x":True, "latitude":False,
                                        "longitude":False, "laf005_per_hour":True})
    if "btn-nclicks-1" == ctx.triggered_id:
        msg = "Noise map of laf 0.5% was selected"
        fig = px.density_mapbox(noise_map_date,lat="latitude", lon="longitude",
                            z="laf005_per_hour", radius=20, zoom=16, height=650, range_color=[40,80],
                            center={"lat":50.87467323, "lon":4.699916431},
                            mapbox_style="open-street-map",
                            hover_data={"description_x":True, "latitude":False,
                                        "longitude":False, "laf005_per_hour":True})
    elif "btn-nclicks-2" == ctx.triggered_id:
        msg = "Noise map of laf 99.5% was selected"
        fig =   px.density_mapbox(noise_map_date,lat="latitude", lon="longitude",
                            z="laf995_per_hour", radius=20, zoom=16, height=650, range_color=[30,60],
                            center={"lat":50.87467323, "lon":4.699916431},
                            mapbox_style="open-street-map",
                            hover_data={"description_x":True, "latitude":False,
                                        "longitude":False, "laf005_per_hour":True})

    fig.update_layout(transition_duration=500)
    return string_prefix+date_string, html.Div(msg), fig

if __name__ == '__main__':
    app.run_server(debug=True)







