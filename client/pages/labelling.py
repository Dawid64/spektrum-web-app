import os
import streamlit as st
from client.components.label_image import image_labeler
# from client.components.authorization import after_login

st.title("Labelling")
st.set_page_config(layout="wide")


def main():
    image_labeler(os.path.join("data", "example"))


# after_login(main, "maintainer")
