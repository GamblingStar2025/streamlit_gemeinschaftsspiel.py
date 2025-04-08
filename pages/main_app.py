
import streamlit as st
import random

st.title("🎰 Tipp-Generator mit Strategie")

# Anzahl Tipps
anzahl = st.number_input("Anzahl Tipps", min_value=1, max_value=50, value=5)

# Strategie laden
strategie = st.session_state.get("strategie", {})
hot = strategie.get("hot", 100)
cluster = strategie.get("cluster", 100)
rad = strategie.get("rad", 100)
mc = strategie.get("mc", 100)
ki = strategie.get("ki", 100)

st.markdown("**Aktive Strategie:**")
st.json(strategie)

# Dummy Tippgenerierung basierend auf gewichteter Zufallsauswahl
tipps = []
for _ in range(anzahl):
    gewichtung = hot + cluster + rad + mc + ki
    basis_pool = list(range(1, 51))
    # Methode: Anzahl auswahl abhängig vom Gewichtungswert (je höher, desto wahrscheinlicher)
    random.shuffle(basis_pool)
    haupt = sorted(random.sample(basis_pool[:max(5, gewichtung // 20)], 5))
    sterne = sorted(random.sample(range(1, 13), 2))
    tipps.append((haupt, sterne))

# Tipps anzeigen
st.subheader("💡 Generierte Tipps:")
for i, (zahlen, sterne) in enumerate(tipps, 1):
    st.markdown(f"**Tipp {i}:** {zahlen} ⭐ {sterne}")

# Ergebnisse für spätere Auswertung speichern
st.session_state["generierte_tipps"] = tipps
