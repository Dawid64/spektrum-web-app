import logging
from pathlib import Path
import streamlit as st

from logic.shared import get_shared, start_chamber_manager

logging.basicConfig(level=logging.DEBUG)

static = Path("client", "static")
pages = Path("client", "pages")

start_chamber_manager(get_shared())  # Required to initialize chamber object

st.logo(static / "SpektrumLogoLight.svg")

with open(static / "style.css") as f:
    st.markdown(f"<style id='vapor-css'>{f.read()}</style>", unsafe_allow_html=True)

pages = [
    st.Page(pages / "dashboard.py", title="Dashboard", icon="🌱"),
    st.Page(pages / "settings.py", title="Chamber settings", icon="⚙️"),
    st.Page(pages / "labelling.py", title="Labelling"),
    st.Page(pages / "admin_panel.py", title="Admin panel"),
    st.Page(pages / "info.py", title="Info"),
]

pg = st.navigation(pages, position="top")
pg.run()
