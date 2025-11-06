from collections.abc import Callable
import streamlit as st
from serial.tools.list_ports import comports
from serial.tools.list_ports_common import ListPortInfo
from client.utils import get_logger
from logic import get_shared, create_arduino_controller
from logic.chamber import Field


def callback_generator(chamber: str, reader: list[Field]) -> Callable:
    logger = get_logger(chamber)
    config = get_shared()[chamber]

    def callback():
        form_values = {
            field.name: st.session_state[f"{chamber}-{field.name}"] for field in reader
        }
        with config:
            config.set(**form_values)
            config.save()
            config.arduino = create_arduino_controller(
                st.session_state[f"{chamber}-port"].split(" ")[0]
            )
        logger.info(
            "Parameters has been changed to:\n\t"
            + "\n\t".join(
                f"{field.fullname}: {form_values[field.name]}" for field in reader
            )
        )

    return callback


def config_form(chamber: str):
    port_map: dict[str, ListPortInfo | None] = {"None": None} | {
        str(port): port for port in comports()
    }
    port_list = list(port_map.keys())
    config = get_shared()[chamber]
    with st.form(f"{chamber}-settings"):
        with config:
            reader = config.reader()
            port = config.arduino.port
        try:
            starting_index = port_list.index(port)
        except ValueError:
            get_logger("Port-detection").error(
                f"Port {port} not found in available ports"
            )
            starting_index = 0

        n = (len(reader) + 1) // 2
        cols = st.columns([1, 1])
        with cols[0]:
            for field in reader[:n]:
                st.number_input(
                    field.fullname,
                    value=field.value,
                    placeholder="Type a number...",
                    key=f"{chamber}-{field.name}",
                )
        with cols[1]:
            for field in reader[n:]:
                st.number_input(
                    field.fullname,
                    value=field.value,
                    placeholder="Type a number...",
                    key=f"{chamber}-{field.name}",
                )
            st.selectbox(
                "Choose port",
                port_list,
                key=f"{chamber}-port",
                index=starting_index,
            )
        submitted = st.form_submit_button(
            "Save", on_click=callback_generator(chamber, reader)
        )
        if submitted:
            st.success("Settings saved successfully!", icon="✅")
