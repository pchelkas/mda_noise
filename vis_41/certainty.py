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
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
pd.set_option('display.max_rows', None)

DATA_DIR = os.path.join(sys.argv[0].rstrip('/certainty.py').rstrip("vis_41"), "data/export_41")
DATA_LIST = os.listdir(DATA_DIR)

places = ["Naamsestraat_35_maxim", "Naamsestraat_57_xior", "Naamsestraat_62_taste", "Calvarie_Chapel",
          "Parkstraat_2_la_filosovia", "Naamsestraat_81", "Kiosk_stadspark", "Vrijthof", "Naamsestraat_76_his_hears"]

for file_name, place in zip(DATA_LIST, places):
    file_dir = os.path.join(DATA_DIR, file_name)
    data = pd.read_csv(file_dir, sep=";")
    certainty = data.loc[:, ["noise_event_laeq_primary_detected_certainty"]]
    certainty = certainty.replace(0, np.nan).dropna()
    plt.hist(certainty)
    plt.title(place)
    plt.show()

    model_id = data.loc[:, ["noise_event_laeq_model_id"]].dropna()
    model_id_count = model_id.value_counts()
    print(place)
    print(model_id_count)