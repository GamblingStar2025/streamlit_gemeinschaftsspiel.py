import streamlit as st
from save_strategy import save_strategy
from supabase_connector import get_client

email = st.session_state.get("email")
if not email:
    st.warning("Bitte zuerst einloggen.")
else:
    st.title("🎯 Strategien speichern")
    supabase = get_client()

    with st.expander("🔥 Heiße Zahlen", expanded=False):
        hot = st.slider("Anteil heiße Zahlen (%)", 0, 100, 60, key="hot_slider")
        if st.button("💾 Strategie speichern", key="save_hot"):
            res = save_strategy(email, "Heiße Zahlen", {"anteil": hot})
            st.success("✅ Strategie gespeichert.")