"""
Export_41 contains "Noise Events"
In this file, certain noise events are singled out. Each of these events get assigned a certainty:
- 32% that a car is passing by
- 65% that somebody is shouting
- On 15 April (16:25:48), the system picked up a human voice singing. That was a Friday
evening, maybe a student happy to go home after a busy week...
"""
import os.path
import sys
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

DATA_DIR = os.path.join(sys.argv[0].rstrip('/count_events.py').rstrip("vis_41"), "data/export_41")
DATA_LIST = os.listdir(DATA_DIR)

places = ["Naamsestraat_35_maxim", "Naamsestraat_57_xior", "Naamsestraat_62_taste", "Calvarie_Chapel",
          "Parkstraat_2_la_filosovia", "Naamsestraat_81", "Kiosk_stadspark", "Vrijthof", "Naamsestraat_76_his_hears"]

# Count every detected class
events_count = pd.DataFrame()
for file_name in DATA_LIST:
    file_dir = os.path.join(DATA_DIR, file_name)
    data = pd.read_csv(file_dir, sep=";")
    sorted_counts = data.loc[:,"noise_event_laeq_primary_detected_class"][data["noise_event_laeq_primary_detected_certainty"]>=0].value_counts().to_frame()
    counts = pd.DataFrame(sorted_counts.values.T, columns=sorted_counts.index)
    events_count = pd.concat([events_count, counts])

events_count["places"] = places
events_count = events_count.fillna(0)
events_count = events_count.melt(id_vars=["places"], value_vars=events_count.columns)
events_count = events_count.rename(columns={"noise_event_laeq_primary_detected_class": "class"})
print(events_count)

fig = px.bar(events_count, x="places", y="value", color="class", title="Detected Class Counts")
fig.show()

