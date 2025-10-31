import streamlit as st

from client import components
from logic.shared import CHAMBER_NAMES

st.set_page_config(layout="centered")
st.title("Chamber settings")


tabs = st.tabs(CHAMBER_NAMES)
for name, tab in zip(CHAMBER_NAMES, tabs):
    with tab:
        components.config_form(name)
