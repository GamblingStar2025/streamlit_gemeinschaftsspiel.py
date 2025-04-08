
import streamlit as st

st.title("🏆 Auswertung")
st.markdown("Vergleicht eingegebene Tipps mit der Ziehung und zeigt den Gewinn.")

ziehung = {1, 14, 20, 30, 42}
tipp = set(st.multiselect("Dein Tipp (5 Zahlen)", list(range(1, 51)), max_selections=5))
treffer = ziehung.intersection(tipp)
st.success(f"Du hast {len(treffer)} Treffer: {sorted(treffer)}")
