
import streamlit as st

st.title("📊 Auswertung deiner Tipps")

gezogene_zahlen = st.multiselect("Gezogene Hauptzahlen (5)", list(range(1, 51)), max_selections=5)
gezogene_sterne = st.multiselect("Gezogene Sternzahlen (2)", list(range(1, 13)), max_selections=2)
tipps = st.session_state.get("generierte_tipps", [])

if gezogene_zahlen and gezogene_sterne and len(gezogene_zahlen) == 5 and len(gezogene_sterne) == 2:
    st.subheader("🏁 Trefferanalyse:")
    for i, (zahlen, sterne) in enumerate(tipps, 1):
        htreffer = set(zahlen).intersection(gezogene_zahlen)
        streffer = set(sterne).intersection(gezogene_sterne)
        st.markdown(f"**Tipp {i}:** {zahlen} ⭐ {sterne} — 🎯 {len(htreffer)} + {len(streffer)}")
else:
    st.info("Bitte die vollständige Ziehung eingeben.")
