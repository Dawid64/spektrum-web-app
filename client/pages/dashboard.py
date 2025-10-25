import streamlit as st
from client import components

st.set_page_config(layout="wide")
st.title("Dashboard")

# TODO: Create dashboard
components.time_series()
