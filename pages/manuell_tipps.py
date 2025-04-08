
import streamlit as st

st.title("✍️ Eigene Tipps")
st.markdown("Hier kannst du deine eigenen Tipps eingeben.")

zahlen = st.multiselect("Wähle 5 Hauptzahlen", list(range(1, 51)), max_selections=5)
sterne = st.multiselect("Wähle 2 Sternzahlen", list(range(1, 13)), max_selections=2)
if len(zahlen) == 5 and len(sterne) == 2:
    st.success(f"Dein Tipp: {zahlen} + Sterne: {sterne}")
