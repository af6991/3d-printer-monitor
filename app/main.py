import streamlit as st #Provides fucntion

import pandas as pd
import numpy as np
import os

# Sets upp the app's layout and browser title
st.set_page_config(page_title="3D Printer Monitor", layout="wide")

# Load data
DATA_PATH = os.path.join("..", "data", "printer_log.csv")

# Read Data and convert timestamp column to datetime object
df = pd.read_csv("printer_log.csv", parse_dates=["timestamp"])

st.title("🖨️ 3D Printer Monitoring Dashboard")
st.markdown("Monitor your printer's performance and early failure signals.")
# Line charts
st.subheader("Temperature Monitoring")

#st.line_chart(...) creates a time-series plot, with x-axis as time and y-axis as value
st.line_chart(df.set_index("timestamp")
              [["nozzle_temp", "bed_temp"]],
              height=300
              #we set timestamp as the index so the X-axis is time
              #we plot both nozzle_temp and bed_temp on the Y-axis;
              #we set height to 300 pixels
              )

# Progress and Timer
st.subheader("Print Progress")
progress = df["progress"].iloc[-1]
st.progress(progress / 100)

time_elapsed = df["time_elapsed"].iloc[-1]
st.metric("Print Time Elapsed (min)", f"{time_elapsed}")

# Placeholders for failure detection logic (Day 3)
st.warning("⚠️ Failure detection logic coming soon...")