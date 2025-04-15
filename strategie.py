import streamlit as st
from save_strategy import save_strategy
from supabase_client import get_authenticated_client

email = st.session_state.get("email")
if not email:
    st.warning("Bitte zuerst einloggen.")
    st.stop()
else:
    client = get_authenticated_client()

    st.title("🎯 Strategien speichern")

    with st.expander("🔥 Heiße Zahlen", expanded=False):
        hot = st.slider("Anteil heiße Zahlen (%)", 0, 100, 60, key="hot_slider")
        if st.button("💾 Strategie speichern", key="save_hot"):
            res = save_strategy(client, email, "Heiße Zahlen", {"anteil": hot})
            st.success("✅ Strategie gespeichert.")
