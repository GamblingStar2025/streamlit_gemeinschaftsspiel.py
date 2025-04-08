
import streamlit as st

st.title("💡 Strategien")
st.markdown("Hier findest du Erklärungen zu den angewendeten Methoden.")

strategien = {
    "Hot-Zahlen": "Häufig gezogene Zahlen.",
    "Cold-Zahlen": "Selten gezogene Zahlen.",
    "Rad-Prinzip": "Zahlen, die zyklisch wiederkehren.",
    "Monte-Carlo": "Simulation tausender Tipps.",
    "LSTM": "KI-Modell zur Vorhersage.",
}
for name, beschreibung in strategien.items():
    st.subheader(name)
    st.write(beschreibung)
