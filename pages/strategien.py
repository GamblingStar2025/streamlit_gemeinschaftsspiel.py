
import streamlit as st

st.title("🧠 Strategie & Gewichtung")

moduswahl = st.radio("🔧 Modus der Gewichtung", ["Automatisch", "Manuell"])

if moduswahl == "Manuell":
    st.markdown("### 🎛️ Methoden-Gewichtung (0–200 %)")
    hot_w = st.slider("🔥 Hot-Zahlen", 0, 200, 100)
    cold_w = st.slider("🧊 Cold-Zahlen", 0, 200, 100)
    rad_w = st.slider("♻️ Rad-Zahlen", 0, 200, 100)
    cluster_w = st.slider("🧩 Cluster-Bereiche", 0, 200, 100)
else:
    hot_w = cold_w = rad_w = cluster_w = 100

ki_w = st.slider("🤖 KI-Gewichtung", 0, 200, 100)

st.markdown("---")
st.subheader("📊 Aktuelle Einstellungen")
st.write(f"**Hot**: {hot_w}%")
st.write(f"**Cold**: {cold_w}%")
st.write(f"**Rad**: {rad_w}%")
st.write(f"**Cluster**: {cluster_w}%")
st.write(f"**KI-Gewichtung**: {ki_w}%")
