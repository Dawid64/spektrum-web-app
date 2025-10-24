import logging
import os

import streamlit as st

from client.logic import get_shared

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)

get_shared()  # Required to initialize chamber object

pages = [
    st.Page(
        os.path.join("client", "pages", "dashboard.py"),
        title="Dashboard",
        icon="🌱",
    ),
    st.Page(os.path.join("client", "pages", "settings.py"), title="Settings", icon="⚙️"),
    st.Page(os.path.join("client", "pages", "labelling.py"), title="Labelling"),
    st.Page(os.path.join("client", "pages", "admin_panel.py"), title="Admin panel"),
]

pg = st.navigation(pages, position="top")
pg.run()
