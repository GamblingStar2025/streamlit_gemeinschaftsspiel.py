
import streamlit as st
st.set_page_config(page_title="Strategie", layout="centered")
from ..supabase_connector import save_tipps  # wenn es ein Modul im Parent ist


st.title("🧠 Strategie")

if "email" not in st.session_state:
    st.warning("Bitte zuerst einloggen.")
else:
    strategie = st.selectbox("Strategie auswählen", ["Zufall", "Häufigkeit", "AI-Vorschlag"])
    zahlen = st.multiselect("Zahlen wählen (1–50)", list(range(1, 51)), max_selections=5)
    if st.button("💾 Tipp speichern"):
        response = save_tipps(
            user_email=st.session_state["email"],
            strategie=strategie,
            zahlen=zahlen
        )
        if response.status_code == 201:
            st.success("Tipp gespeichert!")
        else:
            st.error("Fehler beim Speichern.")
