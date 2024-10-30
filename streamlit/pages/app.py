import json
import os
import requests
import streamlit as st
from util import HIDE_MENU

st.set_page_config(page_title="App")

st.markdown(HIDE_MENU, unsafe_allow_html=True)
st.image("streamlit/static/images/red_hat_banner_dark.png")

host = os.environ.get("APP_HOST", "0.0.0.0")
port = os.environ.get("APP_PORT", "2113")
api_root = f"http://{host}:{port}"

prompt = st.text_area("Prompt:")
url = api_root + "/react"
ask = st.button("Ask")

if ask:
    st.subheader("Answer")
    with st.spinner("Generating answer..."):
        request_json = {"prompt": prompt}
        response = requests.post(url=url, json=request_json)
        if response.status_code != 200:
            st.error("Request failed. Is the API running?")
            st.stop()
        response_json = response.json()
        answer = response_json["answer"]
        st.write(answer)