import streamlit as st
from client.logic.shared import get_shared

config = get_shared()

st.title("Settings")


def callback():
    value: int = st.session_state.slider123
    with config.lock:
        print(f"Setting the value to: {value}")
        config.watering["interval"] = value


st.slider("The slider", 1, 10, on_change=callback, key="slider123")
