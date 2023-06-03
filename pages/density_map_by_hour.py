import dash
from dash import html, dcc, callback
import pandas as pd
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from datetime import date

dash.register_page(__name__)
########################################################################################################################
#                                            DATA LOADING                                                 #
########################################################################################################################
noise_map = pd.read_csv("s3://mda-maindata/assets/Percentile_Noise_Weather_for_APP_Un-scaled_NAdropped.csv")

########################################################################################################################
#                                         DEFINING CALLBACK FUNCTIONS                                             #
########################################################################################################################
@callback(
    Output(component_id='output-date-picker', component_property='children'),
    Output(component_id='container-button-timestamp', component_property='children'),
    Output(component_id="noise-density-map", component_property="figure"),
    Input(component_id="noise-date-picker", component_property="date"),
    Input(component_id="hour-slider",component_property="value"),
    Input(component_id='btn-nclicks-1', component_property='n_clicks'),
    Input(component_id='btn-nclicks-2', component_property='n_clicks')
)
def update_density_map(date_value,hour,btn1,btn2):
    date_object = date.fromisoformat(date_value)
    month = date_object.month
    day = date_object.day
    noise_map_date = noise_map[(noise_map["month"] == month)
                               & (noise_map["day"] == day)
                               & (noise_map["hour"] == hour)]
    string_prefix = 'You have selected: '
    date_string = date_object.strftime('%b %d, %A')
    
    msg = "You have selected noise map of laf 0.5%"
    fig = px.scatter_mapbox(noise_map_date,
                            lat="latitude",
                            lon="longitude",
                            size="laf005_per_hour",
                            color="laf005_per_hour",
                            size_max=30,
                            zoom=15, height=650,
                            range_color=[40, 80],
                            center={"lat": 50.87467323, "lon": 4.699916431},
                            mapbox_style="open-street-map",
                            hover_data={"description_x": True, "latitude": False,
                                        "longitude": False, "laf005_per_hour": True},
                            color_continuous_scale="Blues"
                            )
    if "btn-nclicks-1" == ctx.triggered_id:
        msg = "You have selected noise map of laf 0.5%"
        fig = px.scatter_mapbox(noise_map_date,
                            lat="latitude",
                            lon="longitude",
                            size="laf005_per_hour",
                            color="laf005_per_hour",
                            size_max=30,
                            zoom=15, height=650,
                            range_color=[40, 80],
                            center={"lat": 50.87467323, "lon": 4.699916431},
                            mapbox_style="open-street-map",
                            hover_data={"description_x": True, "latitude": False,
                                        "longitude": False, "laf005_per_hour": True},
                            color_continuous_scale="Blues"
                            )

    elif "btn-nclicks-2" == ctx.triggered_id:
        msg = "You have selected noise map of laf 99.5%"
        fig = px.scatter_mapbox(noise_map_date,
                            lat="latitude",
                            lon="longitude",
                            size="laf995_per_hour",
                            color="laf995_per_hour",
                            size_max=30,
                            zoom=15, height=650,
                            range_color=[30, 60],
                            center={"lat": 50.87467323, "lon": 4.699916431},
                            mapbox_style="open-street-map",
                            hover_data={"description_x": True, "latitude": False,
                                        "longitude": False, "laf005_per_hour": True},
                            color_continuous_scale="Blues"
                            )
    
    return string_prefix+date_string, html.Div(msg), fig

########################################################################################################################
#                                            LAYOUT FORMATTING                                                    #
########################################################################################################################

layout = dbc.Container([
    dbc.Row([
        html.Div([
            html.H2(children="Noise level in Leuven 2022, by hour")
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.Div([
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
                ),html.Div(id="output-date-picker")])
        ]),
        dbc.Col([
                html.Button('laf005', id='btn-nclicks-1', n_clicks=0),
                html.Button('laf995', id='btn-nclicks-2', n_clicks=0),
                html.Div(id='container-button-timestamp')
        ])

    ]),

    dbc.Row([
        dbc.Col([
                html.Div([
                    dcc.Slider(
                        id="hour-slider",
                        min=0,max=23,
                        step=None,
                        value=0,
                        marks={str(hour): str(hour) + ":00" for hour in range(0, 24)},
                        updatemode="drag"
                    )
            ])
        ])
    ]),
    dbc.Row([
        dcc.Graph(id="noise-density-map")
    ])
])
