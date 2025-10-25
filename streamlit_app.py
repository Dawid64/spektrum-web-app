import logging
import os

import streamlit as st

from client.logic import get_shared

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)

get_shared()  # Required to initialize chamber object

st.logo(os.path.join("client", "static", "SpektrumLogoLight.svg"))

with open(os.path.join("client", "static", "style.css")) as f:
    st.markdown(f"<style id='vapor-css'>{f.read()}</style>", unsafe_allow_html=True)

pages = [
    st.Page(
        os.path.join("client", "pages", "dashboard.py"),
        title="Dashboard",
        icon="🌱",
    ),
    st.Page(
        os.path.join("client", "pages", "settings.py"),
        title="Chamber settings",
        icon="⚙️",
    ),
    st.Page(os.path.join("client", "pages", "labelling.py"), title="Labelling"),
    st.Page(os.path.join("client", "pages", "admin_panel.py"), title="Admin panel"),
    st.Page(os.path.join("client", "pages", "info.py"), title="Info"),
]

pg = st.navigation(pages, position="top")
pg.run()
