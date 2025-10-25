import streamlit as st
from client.components.time_series_plot import time_series

st.set_page_config(layout="wide")
st.title("Dashboard")

# TODO: Create dashboard
time_series()
