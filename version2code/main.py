import streamlit as st
from version2code.rag import load_and_split_pdf   
st.set_page_config(
    layout="centered",
    page_title="HDB Resale Assistant"
)

st.title("HDB Resale Assistant")

if st.button("Load and Split PDF"):
    load_and_split_pdf()