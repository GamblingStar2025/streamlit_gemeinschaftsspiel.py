
import streamlit as st
from custom_style import eurogenius_css

st.set_page_config(page_title="Upgrade auf Premium", layout="centered")
st.markdown(eurogenius_css(), unsafe_allow_html=True)

st.title("💳 Upgrade auf Premium")

st.markdown("**Nur CHF 5.99 / Monat für unbegrenzten Zugang**")
st.markdown("- 🔐 Zugriff auf alle Strategien")
st.markdown("- 🔄 Unbegrenzte Tippgenerierung")
st.markdown("- 📊 Analysen & Auswertungen freigeschaltet")

st.markdown("---")

st.markdown("### Zahlungsmethode wählen:")

option = st.radio("💰 Wähle:", ["🔵 Stripe (Kreditkarte)", "📨 Kontakt für Banküberweisung"])

if option == "🔵 Stripe (Kreditkarte)":
    st.markdown("[➡️ Hier über Stripe bezahlen](https://buy.stripe.com/test_4gwcNdgfe2HU8fK3cc)")
    st.info("Demo-Link. In der Live-Version erfolgt automatische Upgrade-Zuweisung nach Zahlung.")
else:
    st.markdown("📬 Schreib uns: **support@eurogenius.ch** für alternative Zahlungsarten.")

st.markdown("---")
st.page_link("pages/login.py", label="⬅️ Zurück zum Login", icon="🔐")
