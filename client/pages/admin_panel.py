import streamlit as st
import pandas as pd
from client.utils import after_login


st.set_page_config(
    layout="centered",
    initial_sidebar_state="expanded",
)
st.title("Admin Panel")


def get_users_dataset():
    columns = ["Imię", "Rola"]
    data = [("Mike", "Admin"), ("marta", "user")]
    a = pd.DataFrame(data, columns=columns)
    return a


def main():
    data = get_users_dataset()
    st.subheader("Użytkownicy")
    st.dataframe(
        data=data,
        hide_index=True,
        on_select="rerun",
        selection_mode="multi-row",
    )
    col1, col2 = st.columns([1, 1])
    with col1:
        st.button("Daj admina")
    with col2:
        st.button("Daj user'a")


after_login(main, "admin")
