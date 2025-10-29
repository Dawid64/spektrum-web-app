import streamlit as st

from client import components
# from client.components.authorization import after_login

st.set_page_config(layout="centered")
st.title("Chamber settings")


def settings():
    tab1, tab2 = st.tabs(["Chamber 1", "Chamber 2"])
    with tab1:
        components.config_form("Chamber-1")

    with tab2:
        components.config_form("Chamber-2")


# roles = after_login(settings, required_role="maintainer")
