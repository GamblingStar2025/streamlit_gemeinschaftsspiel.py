
import streamlit as st
import time
from PIL import Image

st.set_page_config(page_title="EuroGenius Start", layout="centered", initial_sidebar_state="collapsed")

# Design: dunkler Hintergrund
page_style = '''
<style>
body {
    background-color: #0c0c0c;
    color: #f1f1f1;
    text-align: center;
}
img {
    max-width: 250px;
    margin-top: 50px;
}
h1 {
    font-size: 2.5rem;
    margin-top: 1rem;
    color: gold;
}
</style>
'''
st.markdown(page_style, unsafe_allow_html=True)

# Logo laden
st.image("logo_gold.png", use_column_width=False)
st.markdown("## EuroGenius – KI trifft auf Glück ✨")

with st.spinner("App wird geladen..."):
    time.sleep(3)

st.switch_page("main.py")
