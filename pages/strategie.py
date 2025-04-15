
import streamlit as st
from save_strategy import save_strategy
from supabase_client import get_authenticated_client

email = st.session_state.get("email")
if not email:
    st.warning("Bitte zuerst einloggen.")
else:
    client = get_authenticated_client()

    st.title("🎯 Strategien speichern")

    with st.expander("🔥 Heiße Zahlen", expanded=False):
        hot = st.slider("Anteil heiße Zahlen (%)", 0, 100, 60, key="hot_slider")
        if st.button("💾 Strategie speichern", key="save_hot"):
            res = save_strategy(client, email, "Heiße Zahlen", {"anteil": hot})
            st.success("✅ Strategie gespeichert.")

    with st.expander("❄️ Kalte Zahlen", expanded=False):
        cold = st.slider("Anteil kalte Zahlen (%)", 0, 100, 30, key="cold_slider")
        if st.button("💾 Strategie speichern", key="save_cold"):
            res = save_strategy(client, email, "Kalte Zahlen", {"anteil": cold})
            st.success("✅ Strategie gespeichert.")

    with st.expander("🌀 Cluster-Strategie", expanded=False):
        cluster_level = st.slider("Cluster-Größe", 1, 5, 3, key="cluster_slider")
        if st.button("💾 Strategie speichern", key="save_cluster"):
            res = save_strategy(client, email, "Cluster", {"level": cluster_level})
            st.success("✅ Cluster-Strategie gespeichert.")

    with st.expander("🎰 Monaco Casino", expanded=False):
        mischg = st.slider("🔀 Durchmischung", 1000, 1_000_000, 50000, key="monaco_slider")
        st.markdown("Diese Strategie simuliert Extremszenarien wie im Casino.")
        if st.button("💾 Strategie speichern", key="save_monaco"):
            res = save_strategy(client, email, "Monaco Casino", {"durchmischung": mischg})
            st.success("✅ Monaco Casino-Strategie gespeichert.")

    with st.expander("📊 Radsystem", expanded=False):
        analyse_typ = st.selectbox("Analysetyp", ["Standard", "Fortgeschritten"], key="radsystem_typ")
        analyse_tiefe = st.slider("Anzahl Ziehungen", 10, 1000, 100, key="radsystem_tiefe")
        if st.button("💾 Strategie speichern", key="save_radsystem"):
            res = save_strategy(client, email, "Radsystem", {"analyse_typ": analyse_typ, "anzahl_ziehungen": analyse_tiefe})
            st.success("✅ Radsystem-Strategie gespeichert.")

    with st.expander("🤖 KI-Strategie", expanded=False):
        ki_power = st.slider("Anpassungsintensität (%)", 0, 200, 100, key="ki_power")
        st.markdown("Die KI-Strategie passt sich basierend auf historischen Daten automatisch an.")
        if st.button("💾 Strategie speichern", key="save_ki"):
            res = save_strategy(client, email, "KI-Strategie", {"intensität": ki_power})
            st.success("✅ KI-Strategie gespeichert.")
