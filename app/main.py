import streamlit as st #Provides fucntion

import pandas as pd
import numpy as np
import os

# Sets upp the app's layout and browser title
st.set_page_config(page_title="3D Printer Monitor", layout="wide")

# Read Data and convert timestamp column to datetime object
df = pd.read_csv("./app/printer_log.csv", parse_dates=["timestamp"])

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

d_nozzle = int(df["nozzle_temp"].iloc[-2] - df["nozzle_temp"].iloc[-1])
d_bed = int(df["bed_temp"].iloc[-2] - df["bed_temp"].iloc[-1])
d_time = int(df["time_elapsed"].iloc[-2] - df["time_elapsed"].iloc[-1])

# Temperature Metrics
with st.container():
    st.subheader("Temperature Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Nozzle Temp (°C)", df["nozzle_temp"].iloc[-1], d_nozzle)
    col2.metric("Bed Temp (°C)", df["bed_temp"].iloc[-1], d_bed)
    col3.metric("Time Elapsed (minutes)", df["time_elapsed"].iloc[-1], d_time)



# Error Alerts

alerts = []


with st.container():  
    #check if that nozzle temperature is to low
    if df["nozzle_temp"].iloc[-1] < 160:
        alerts.append("Nozzle temperature too low")

    if df["bed_temp"].iloc[-1] < 60:
        alerts.append("Bed temperature too low, bed detachment possible")
        
    if df["layer_shift"].iloc[-1] == True:
        alerts.append("Layer shift detected - mechanical instability or sudden jerk")
        
    if df["time_elapsed"].iloc[-1] > 300:
        alerts.append("Abnormal printing time - possible mechanical failure")
        
    if len(alerts) == 0:
        st.success("No alerts detected")
        
    else:
        for alert in alerts:
            st.warning(alert)
