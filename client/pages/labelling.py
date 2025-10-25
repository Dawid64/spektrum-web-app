import os
import streamlit as st
from client.components.label_image import image_labeler

st.title("Labelling")
st.set_page_config(layout="wide")

# TODO: Create labelling page

image_labeler(os.path.join("data", "example"))
