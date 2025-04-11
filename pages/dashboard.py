
import streamlit as st

st.markdown("## 📊 EuroMillions Dashboard")
st.success("⭐ Letzte Ziehung: 5 - 23 - 28 - 44 - 48 | Sterne: 2 - 8")
st.markdown("🤑 **Nächster Superjackpot:** CHF 52.5 Mio")

tag = st.selectbox("Ziehungstag wählen:", ["Dienstag", "Freitag"])
st.markdown(f"🔍 Angezeigt: {tag}-Ziehungen")
