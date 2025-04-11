
import streamlit as st
import random
from supabase_connector import save_tipps

st.set_page_config(page_title="Tippgenerator", layout="centered")
st.title("🎰 EuroGenius Tippgenerator")

anzahl = st.slider("Wie viele Tipps?", 1, 10, 3)

tipps = []
for _ in range(anzahl):
    zahlen = sorted(random.sample(range(1, 51), 5))
    sterne = sorted(random.sample(range(1, 13), 2))
    tipps.append((zahlen, sterne))

if st.button("💾 Tipp speichern"):
    email = st.session_state.get("user_email", "test@demo.ch")
    strategie = {"methode": "zufällig", "gewichtung": 100}
    save_tipps(user_email=email, strategie=strategie, zahlen=tipps)
    st.success("✅ Tipps wurden gespeichert!")

for idx, (z, s) in enumerate(tipps, 1):
    st.markdown(f"**Tipp {idx}:** {z} ⭐ {s}")
