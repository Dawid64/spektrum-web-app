import streamlit as st
from client.logic.shared import get_shared
from client import components

config = get_shared()

st.title("Chamber settings")


tab1, tab2 = st.tabs(["Chamber 1", "Chamber 2"])
with tab1:
    components.config_form("Chamber_1")

with tab2:
    components.config_form("Chamber_2")
