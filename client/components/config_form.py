from collections.abc import Callable
import streamlit as st
from client.logic import get_shared
from copy import copy
from client.logic.utils import get_logger


def callback_generator(chamber: str) -> Callable:
    logger = get_logger(chamber)
    config = get_shared()[chamber]

    def callback():
        with config.lock:
            config.watering["interval"] = st.session_state[
                f"{chamber}_watering_frequency"
            ]
            config.watering["quantity"] = st.session_state[
                f"{chamber}_watering_quantity"
            ]
            config.camera_frequency = st.session_state[f"{chamber}_camera_frequency"]
            config.light_time = st.session_state[f"{chamber}_light_frequency"]
            config.sensor_delay = st.session_state[f"{chamber}_sensors_delay"]
            config.save()
        logger.info(
            f"""Parameters has been changed to:\n Watering frequency: {
                st.session_state[f"{chamber}_watering_frequency"]
            }\n Watering quantity: {
                st.session_state[f"{chamber}_watering_quantity"]
            }\n Camera frequency: {
                st.session_state[f"{chamber}_camera_frequency"]
            }\n Light time: {
                st.session_state[f"{chamber}_light_frequency"]
            }\n Sensor delay: {st.session_state[f"{chamber}_sensors_delay"]}"""
        )

    return callback


def config_form(chamber: str):
    with st.form(f"{chamber}-settings"):
        current_config = get_shared()[chamber]
        with current_config.lock:
            config = copy(current_config)
        cols = st.columns([1, 1])
        with cols[0]:
            st.number_input(
                "Watering time (Currently not used)",
                value=10,
                placeholder="Type a number...",
                key=f"{chamber}_watering_time",
            )
            st.number_input(
                "Watering frequency",
                value=config.watering["interval"],
                placeholder="Type a number...",
                key=f"{chamber}_watering_frequency",
            )
            st.number_input(
                "Water quantity",
                value=config.watering["quantity"],
                placeholder="Type a number...",
                key=f"{chamber}_watering_quantity",
            )
        with cols[1]:
            st.number_input(
                "Photo shoot frequency (minutes)",
                value=config.camera_frequency,
                placeholder="Type a number...",
                key=f"{chamber}_camera_frequency",
            )
            st.number_input(
                "Light time",
                value=config.light_time,
                placeholder="Type a number...",
                key=f"{chamber}_light_frequency",
            )
            st.number_input(
                "Sensors delay",
                value=config.sensor_delay,
                placeholder="Type a number...",
                key=f"{chamber}_sensors_delay",
            )
        st.form_submit_button("Save", on_click=callback_generator(chamber))
