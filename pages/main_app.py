
import streamlit as st

# 🔐 Temporärer Login-Bypass für Testzwecke
if "rolle" not in st.session_state:
    st.session_state["rolle"] = "premium"
    st.session_state["is_logged_in"] = True


import streamlit as st
import random
from custom_style import eurogenius_css

st.set_page_config(page_title="Tippgenerator", layout="centered")
st.markdown(eurogenius_css(), unsafe_allow_html=True)

rolle = st.session_state.get("rolle", "unknown")

if not st.session_state.get("is_logged_in"):
    st.warning("🚫 Bitte zuerst einloggen.")
    st.stop()

if rolle == "gast":
    st.info("🔓 Als Gast erhältst du 3 kostenlose Tipps!")
    anzahl = 3
elif rolle == "premium":
    anzahl = st.slider("Wie viele Tipps?", 1, 10, 3)
else:
    st.warning("🚫 Unbekannter Zugriff – bitte neu einloggen.")
    st.stop()

st.title("🎰 EuroGenius Tippgenerator")

tipps = []
for _ in range(anzahl):
    zahlen = sorted(random.sample(range(1, 51), 5))
    sterne = sorted(random.sample(range(1, 13), 2))
    tipps.append((zahlen, sterne))

if st.button("💾 Tipp speichern"):
    st.success("✅ Tipps gespeichert!")

for idx, (z, s) in enumerate(tipps, 1):
    st.markdown(f"**Tipp {idx}:** {z} ⭐ {s}")
