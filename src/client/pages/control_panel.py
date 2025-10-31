import streamlit as st
from serial.tools.list_ports import comports
from serial.tools.list_ports_common import ListPortInfo

from logic.shared import CHAMBER_NAMES

st.set_page_config(layout="centered")
st.title("Control panel")


def main():
    port_map: dict[str, ListPortInfo | None] = {"None": None} | {
        str(port): port for port in comports()
    }
    for name, tab in zip(CHAMBER_NAMES, st.tabs(CHAMBER_NAMES)):
        with tab:
            st.selectbox(
                "Choose port",
                port_map.keys(),
                key=f"{name}-port",
                index=0,
            )
            st.write(st.session_state.get(f"{name}-port"))
            print([str(i) for i in comports()])


main()
