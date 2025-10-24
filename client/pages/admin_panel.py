import streamlit as st
import pandas as pd

st.title("Admin Panel")


def get_users_dataset():
    columns = ["Imię", "Rola"]
    data = [("Mike", "Admin"), ("marta", "user")]
    a = pd.DataFrame(data, columns=columns)
    return a


data = get_users_dataset()


# TODO: Create Admin panel


st.subheader("Użytkownicy")
event = st.dataframe(
    data=data,
    hide_index=True,
    on_select="rerun",
    selection_mode="multi-row",
)


def set_admin():
    print(data.iloc(event.selection.rows))
    data.iloc(event.selection.rows)["Rola"] = "Admin"


def set_user():
    pass


col1, col2 = st.columns([1, 1])
with col1:
    st.button("Daj admina", on_click=set_admin)
with col2:
    st.button("Daj user'a", on_click=set_user)
