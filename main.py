
import streamlit as st

st.set_page_config(page_title="EuroGenius", layout="wide")

# Reset Button
if st.sidebar.button("🔄 Reset"):
    st.session_state.clear()
    st.experimental_rerun()

# Manual Navigation
st.sidebar.title("Navigation")
st.sidebar.page_link("pages/1_Analyse.py", label="Analyse")
st.sidebar.page_link("pages/2_Strategie.py", label="Strategie")
st.sidebar.page_link("pages/3_Tippgenerator.py", label="Tippgenerator")
st.sidebar.page_link("pages/4_Auswertung.py", label="Auswertung")

st.title("🏁 Willkommen bei EuroGenius")
st.markdown("⬇️ Nutze die Seitenleiste für den strukturierten Ablauf der Tippgenerierung.")
