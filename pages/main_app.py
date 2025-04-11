
import streamlit as st
import random

st.title("🎰 Tipp-Generator")

modus = st.radio("Wähle Spielmodus", ["Einzelspieler", "Gemeinschaftsspiel"])
anzahl = st.slider("Anzahl Tipps", 1, 50 if modus == "Einzelspieler" else 500, 5)

strategie = st.session_state.get("strategie", {})
ziehungen = st.session_state.get("ziehungen", [])
anzahl_ziehungen = len(ziehungen)
basisgröße = max(5, min(50, anzahl_ziehungen // 2 if anzahl_ziehungen >= 1000 else 25))

tipps = []
for _ in range(anzahl):
    basis = list(range(1, 51))
    random.shuffle(basis)
    zahlen = sorted(random.sample(basis[:basisgröße], 5))
    sterne = sorted(random.sample(range(1, 13), 2))
    tipps.append((zahlen, sterne))

st.subheader("📋 Deine Tipps:")
for i, (zahlen, sterne) in enumerate(tipps, 1):
    st.markdown(f"**Tipp {i}:** {zahlen} ⭐ {sterne}")

st.session_state["generierte_tipps"] = tipps

col1, col2 = st.columns(2)
with col1:
    if st.button("🔙 Zurück zur Strategie"):
        st.switch_page("pages/strategie.py")
with col2:
    if st.button("➡️ Weiter zur Auswertung"):
        st.switch_page("pages/auswertung.py")
