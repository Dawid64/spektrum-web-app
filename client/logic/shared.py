from __future__ import annotations
import threading
import streamlit as st
from .chamber import ChamberManager, Chamber, ChamberConfig

CHAMBER_NAMES = ["Chamber-1", "Chamber-2"]


def run_chamber_manager(configs: dict[str, ChamberConfig]):
    chambers = {name: Chamber(config) for name, config in configs.items()}
    chamber_manager = ChamberManager(chambers)
    chamber_manager.scheduler_loop()


@st.cache_resource
def get_shared() -> dict[str, ChamberConfig]:
    configs: dict[str, ChamberConfig] = {
        name: ChamberConfig.load(name) for name in CHAMBER_NAMES
    }
    if not hasattr(get_shared, "_started"):
        thread: threading.Thread = threading.Thread(
            target=run_chamber_manager, args=(configs,), daemon=True
        )
        thread.start()

        get_shared._started = True
    return configs
