import streamlit as st
import os

pages = [
    st.Page(os.path.join("pages", "settings.py"), title="Settings"),
    st.Page(os.path.join("pages", "dashboard.py"), title="Dashboard"),
    st.Page(os.path.join("pages", "labelling.py"), title="Labelling"),
    st.Page(os.path.join("pages", "admin_panel.py"), title="Admin panel"),
]

pg = st.navigation(pages, position="top")
pg.run()
