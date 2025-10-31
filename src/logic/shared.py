import threading
import streamlit as st
from logic.chamber import ChamberManager, ChamberConfig

CHAMBER_NAMES = ["Chamber-1", "Chamber-2"]


def _run_chamber_manager(configs: dict[str, ChamberConfig]):
    chamber_manager = ChamberManager(configs)
    chamber_manager.scheduler_loop()


def start_chamber_manager(configs: dict[str, ChamberConfig]):
    if not hasattr(start_chamber_manager, "_started"):
        thread: threading.Thread = threading.Thread(
            target=_run_chamber_manager, args=(configs,), daemon=True
        )
        thread.start()

        start_chamber_manager._started = True  # type: ignore


@st.cache_resource
def get_shared() -> dict[str, ChamberConfig]:
    configs: dict[str, ChamberConfig] = {
        name: ChamberConfig.load(name) for name in CHAMBER_NAMES
    }
    return configs
