
import streamlit as st

# 🔢 Globale KI-Gewichtung (z.B. 135 % aus Slider)
ki_gewichtung_global = st.slider("🔮 KI-Gewichtung Gesamt (%)", 0, 200, 100)

# 📊 Basisgewichtung je Methode in Prozent (Verhältnis muss 100 ergeben)
basis_gewichte = {
    "Hot-Zahlen": 25,
    "Cold-Zahlen": 15,
    "Cluster": 20,
    "Monte Carlo": 25,
    "Zahlenrad (Rad)": 15
}

# 🔄 Berechnung der verstärkten Gewichtung
st.markdown("### 📈 Angewandte Gewichtungen der Analyse-Methoden")
for methode, basis in basis_gewichte.items():
    verstärkt = round(basis * (ki_gewichtung_global / 100), 2)
    st.progress(min(int(verstärkt), 100), text=f"{methode}: {verstärkt}%")
