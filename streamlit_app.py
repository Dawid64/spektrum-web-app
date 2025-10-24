import streamlit as st
import os
from client.logic.shared import get_shared

_ = get_shared()

pages = [
    st.Page(os.path.join("client", "pages", "settings.py"), title="Settings"),
    st.Page(os.path.join("client", "pages", "dashboard.py"), title="Dashboard"),
    st.Page(os.path.join("client", "pages", "labelling.py"), title="Labelling"),
    st.Page(os.path.join("client", "pages", "admin_panel.py"), title="Admin panel"),
]

pg = st.navigation(pages, position="top")
pg.run()
