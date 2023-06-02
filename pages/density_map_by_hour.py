#!/usr/bin/env python
# coding: utf-8


from datetime import datetime, date
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd

# Data import
noise_map = pd.read_csv("./data/Percentile Noise Weather for APP_Un-scaled_NAdropped.csv")
noise_map.head()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
dash.register_page(__name__, path='/')
layout = html.Div([
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
    html.H3("Noise level in Leuven 2022, by hour", style={'textAlign': 'center'}),
    dcc.Slider(
        id="hour-slider",
        min=0, max=23,
        step=None,
        value=0,
        marks={str(hour): str(hour) + ":00" for hour in range(0, 23)}
    ),
    dcc.Graph(id="noise-map")
])


@app.callback(
    Output("noise-map", "figure"),
    Input("noise-date-picker", "date"),
    Input("hour-slider", "value"))
def update_output(date_value, hour_value):
    date_object = date.fromisoformat(date_value)
    month = date_object.month
    day = date_object.day
    noise_map_date = noise_map[(noise_map["month"] == month)
                               & (noise_map["day"] == day)
                               & (noise_map["hour"] == hour_value)]

    fig = px.density_mapbox(noise_map_date, lat="latitude", lon="longitude",
                            z="laf005_per_hour", radius=20, zoom=16, height=650, range_color=[40, 80],
                            center={"lat": 50.87467323, "lon": 4.699916431},
                            mapbox_style="open-street-map",
                            hover_data={"description_x": True, "latitude": False,
                                        "longitude": False, "laf005_per_hour": True})
    fig.update_layout(transition_duration=500)
    return fig

# if __name__ == '__main__':
#     app.run_server(debug=True)
