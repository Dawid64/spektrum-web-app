from __future__ import annotations
import threading
import os
import streamlit as st
from .chamber import Chamber, ChamberConfig

STATE_FILE = os.environ.get("STATE_FILE", "state.json")


def scheduler_loop(config: ChamberConfig):
    chamber = Chamber(config)
    chamber.scheduler_loop()


@st.cache_resource
def get_shared() -> ChamberConfig:
    config = ChamberConfig()
    config.load()
    if not hasattr(get_shared, "_started"):
        thread: threading.Thread = threading.Thread(
            target=scheduler_loop, args=(config,), daemon=True
        )
        thread.start()

        get_shared._started = True
    return config
