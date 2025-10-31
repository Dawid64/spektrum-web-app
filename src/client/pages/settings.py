import streamlit as st

from client import components
from client.components.authorization import after_login
from logic.shared import CHAMBER_NAMES

st.set_page_config(layout="centered")
st.title("Chamber settings")


def settings():
    for name, tab in zip(CHAMBER_NAMES, st.tabs(CHAMBER_NAMES)):
        with tab:
            components.config_form(name)


roles = after_login(settings, required_role="maintainer")
