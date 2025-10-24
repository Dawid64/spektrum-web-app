from __future__ import annotations
import threading
import os
import streamlit as st
from .chamber import ChamberManager, Chamber, ChamberConfig

STATE_FILE = os.environ.get("STATE_FILE", "state.json")


def run_chamber_manager(configs: dict[str, ChamberConfig]):
    chambers = {name: Chamber(config) for name, config in configs.items()}
    chamber_manager = ChamberManager(chambers)
    chamber_manager.scheduler_loop()


@st.cache_resource
def get_shared() -> dict[str, ChamberConfig]:
    chamber_names = ["Chamber-1", "Chamber-2"]
    configs = {name: ChamberConfig(name) for name in chamber_names}
    for config in configs.values():
        config.load()
    if not hasattr(get_shared, "_started"):
        thread: threading.Thread = threading.Thread(
            target=run_chamber_manager, args=(configs,), daemon=True
        )
        thread.start()

        get_shared._started = True
    return configs
