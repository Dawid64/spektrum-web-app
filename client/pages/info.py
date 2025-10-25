import streamlit as st
import toml

with open("pyproject.toml", "r", encoding="utf-8") as f:
    information = toml.load(f)["project"]
authors = [author["name"] for author in information["authors"]]

st.set_page_config(layout="centered")
st.title("Info")
st.markdown(f"""
### BADANIE WPŁYWU POLA ELEKTROMAGNETYCZNEGO NA POROST ROŚLIN.

            
Autorzy projektu: [#TODO: do uzupełnienia]

Autorzy strony: {", ".join(authors)}

Strona jest w wersji: {information["version"]}.
""")
