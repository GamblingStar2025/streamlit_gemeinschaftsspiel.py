
import streamlit as st

st.set_page_config(page_title="EuroGenius App", page_icon="🎯", layout="wide")

st.title("🎯 Willkommen bei EuroGenius")

st.markdown("""
Herzlich willkommen zur EuroGenius-Community-App!  
Diese Plattform bietet dir:
- 🎰 **Tipp-Generator** für Lottozahlen
- 📊 **Analyse und Auswertung** deiner Strategien
- 💾 **Strategien speichern und verwalten**
- 🧠 **KI-gestützte Vorhersagen**
- 📈 **Dashboard mit Trends**
- 💸 **Bezahlmodelle für erweiterte Funktionen**

> Nutze die linke Navigation, um durch die App zu navigieren.
""")

# Zeige Anmeldehinweis, wenn nicht eingeloggt
if "email" not in st.session_state:
    st.warning("Bitte logge dich über die Login-Seite ein, um alle Funktionen zu nutzen.")
else:
    st.success(f"✅ Eingeloggt als: {st.session_state['email']}")
