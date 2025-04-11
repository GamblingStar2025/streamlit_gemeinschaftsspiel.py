
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Tipp-Historie", layout="centered")

st.title("📊 Tipp-Historie & Nutzerstatistik")

tipps = st.session_state.get("generierte_tipps", [])
strategie = st.session_state.get("strategie", {})
geschichte = st.session_state.get("tipps_history", [])

# Neue Tipps zur History hinzufügen (einmalig pro Sitzung)
if tipps and not st.session_state.get("history_saved"):
    eintrag = {
        "datum": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "strategie": strategie,
        "tipps": tipps
    }
    geschichte.append(eintrag)
    st.session_state["tipps_history"] = geschichte
    st.session_state["history_saved"] = True

if geschichte:
    st.subheader("📆 Übersicht deiner Tipps:")
    for eintrag in reversed(geschichte):
        st.markdown(f"**🗓️ Datum:** {eintrag['datum']}")
        st.markdown(f"🎯 Strategie: {eintrag['strategie']}")
        for idx, (zahlen, sterne) in enumerate(eintrag['tipps'], 1):
            st.markdown(f"• **Tipp {idx}:** {zahlen} ⭐ {sterne}")
        st.markdown("---")
else:
    st.info("Noch keine Tipps gespeichert.")
