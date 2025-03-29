
import streamlit as st

# Gemeinschaftsspiel-Logik
def gemeinschaftsspiel_strategie(einsatz):
    base_tips = 14
    multiplier = 8
    max_einsatz = 250
    stufen = [50, 100, 150, 200, 250]

    if einsatz not in stufen:
        raise ValueError("Einsatz muss 50, 100, 150, 200 oder 250 sein.")

    tipps = base_tips + ((einsatz - 50) // 50) * multiplier
    ki_gewichtung = 50 + ((einsatz - 50) // 50) * 10
    monte_carlo_iterationen = 100000 + ((einsatz - 50) // 50) * 50000

    return {
        "einsatz": einsatz,
        "tipps": tipps,
        "ki_gewichtung": ki_gewichtung,
        "simulationen": monte_carlo_iterationen,
        "stufe": f"Level {stufen.index(einsatz)+1}/5"
    }

# Streamlit App
st.set_page_config(page_title="Gemeinschaftsspiel Euromillions", layout="centered")
st.title("🎯 Gemeinschaftsspiel Euromillions")

st.markdown("""
Wähle deinen Beitrag zum Gemeinschaftsspiel und wir berechnen automatisch die optimale Anzahl Tipps, KI-Gewichtung und Simulationstiefe. Gemeinsam gewinnen wir cleverer! 💡
""")

einsatz = st.selectbox("💰 Einsatzbetrag wählen:", [50, 100, 150, 200, 250])

if einsatz:
    strategie = gemeinschaftsspiel_strategie(einsatz)

    st.subheader(f"🧮 Strategie für {strategie['einsatz']}€ Beitrag")
    st.metric("🎟️ Tipps insgesamt", f"{strategie['tipps']}")
    st.metric("🧠 KI-Gewichtung", f"{strategie['ki_gewichtung']}%")
    st.metric("🎲 Simulationen", f"{strategie['simulationen']:,}")
    st.metric("🔢 Stufe", strategie['stufe'])

    st.success("Tipp-Konfiguration erfolgreich berechnet!")
