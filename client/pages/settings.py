import streamlit as st

from client import components

st.set_page_config(layout="centered")
st.title("Chamber settings")


tab1, tab2 = st.tabs(["Chamber 1", "Chamber 2"])
with tab1:
    components.config_form("Chamber-1")

with tab2:
    components.config_form("Chamber-2")
