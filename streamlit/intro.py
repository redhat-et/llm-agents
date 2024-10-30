import streamlit as st
from util import HIDE_MENU, read_markdown_file

st.set_page_config(page_title="Introduction")

st.markdown(HIDE_MENU, unsafe_allow_html=True)
st.image("streamlit/static/images/red_hat_banner_dark.png")
st.markdown(read_markdown_file("streamlit/static/markdown/introduction.md"))