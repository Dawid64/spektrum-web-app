from collections.abc import Callable
import streamlit as st
from client.utils import get_logger
from logic import get_shared
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
        logger.info(
            "Parameters has been changed to:\n\t"
            + "\n\t".join(
                f"{field.fullname}: {form_values[field.name]}" for field in reader
            )
        )

    return callback


def config_form(chamber: str):
    with st.form(f"{chamber}-settings"):
        current_config = get_shared()[chamber]
        with current_config:
            reader = current_config.reader()
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
        submitted = st.form_submit_button(
            "Save", on_click=callback_generator(chamber, reader)
        )
        if submitted:
            st.success("Settings saved successfully!", icon="✅")
