
import streamlit as st
import time
from PIL import Image

st.set_page_config(page_title="EuroGenius Start", layout="centered", initial_sidebar_state="collapsed")

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

# Logo laden mit aktuellem Parameter
try:
    logo = Image.open("logo_gold.png")
    st.image(logo, use_container_width=False)
except:
    st.warning("Logo konnte nicht geladen werden.")

st.markdown("## EuroGenius – KI trifft auf Glück ✨")

with st.spinner("App wird geladen..."):
    time.sleep(3)

st.markdown("**⬇️ Weiter zur App:**")
if st.button("➡️ Jetzt starten"):
    st.switch_page("pages/main_app")
