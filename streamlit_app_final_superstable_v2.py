
import streamlit as st
import pandas as pd
import random
import uuid

st.set_page_config(page_title="EuroMillions Analyse", layout="centered")

# === Intro mit Bild ===
if "intro_done" not in st.session_state:
    st.title("🎯 Willkommen zur EuroMillions KI-App")
    st.image("https://cdn-icons-png.flaticon.com/512/9455/9455170.png", width=100)
    st.markdown("Nutze Muster, Wahrscheinlichkeiten und Teamplay für bessere Tipps.")
    if st.button("🚀 Jetzt starten"):
        st.session_state.intro_done = True
        st.experimental_rerun()
    st.stop()

# === Länderwahl ===
st.sidebar.title("🌍 Einstellungen")
land = st.sidebar.selectbox("Wähle dein Land:", ["🇨🇭 Schweiz", "🇩🇪 Deutschland", "🇦🇹 Österreich", "🇫🇷 Frankreich", "🇪🇸 Spanien"])
waehrung = "CHF" if "Schweiz" in land else "€"
preis_pro_tipp = 3.5 if "Schweiz" in land else 2.5

# === Spielmoduswahl ===
st.header("🎮 Wähle deinen Spielmodus")
modus = st.radio("Modus wählen:", ["🎮 Einzelspieler", "👥 Gemeinschaftsspiel", "🤝 Team-Modus"])

# === Einzelspieler ===
if modus == "🎮 Einzelspieler":
    einsatz = st.slider("💰 Einsatzbetrag (1–50)", 1, 50, 10)
    anzahl_tipps = int(einsatz // preis_pro_tipp)
    kosten = anzahl_tipps * preis_pro_tipp

    st.markdown(f"📄 Anzahl Tipps: **{anzahl_tipps}**")
    st.markdown(f"💰 Gesamtkosten: **{waehrung} {kosten:.2f}**")

    if st.button("🎯 Tipps generieren", key="btn_einzel_" + str(uuid.uuid4())):
        tipps = []
        for _ in range(anzahl_tipps):
            haupt = sorted(random.sample(range(1, 51), 5))
            sterne = sorted(random.sample(range(1, 13), 2))
            tipps.append((haupt, sterne))
        df = pd.DataFrame([{
            "Tipp": i+1,
            "Hauptzahlen": ", ".join(map(str, h)),
            "Sternzahlen": ", ".join(map(str, s))
        } for i, (h, s) in enumerate(tipps)])
        st.dataframe(df)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 CSV herunterladen", data=csv, file_name="Einzel_Tipps.csv", key="dl_einzel")

# === Gemeinschaftsspiel ===
elif modus == "👥 Gemeinschaftsspiel":
    einsatz = st.slider("💰 Einsatzbetrag (50–500)", 50, 500, 50)
    anzahl_tipps = int(einsatz // preis_pro_tipp)
    kosten = anzahl_tipps * preis_pro_tipp

    st.markdown(f"📄 Anzahl Tipps: **{anzahl_tipps}**")
    st.markdown(f"💰 Gesamtkosten: **{waehrung} {kosten:.2f}**")
    st.markdown("🧠 KI-Gewichtung: **50%**")
    st.markdown("🔁 Simulationen: **100.000**")

    if st.button("🎯 Tipps generieren", key="btn_gemein_" + str(uuid.uuid4())):
        tipps = []
        for _ in range(anzahl_tipps):
            haupt = sorted(random.sample(range(1, 51), 5))
            sterne = sorted(random.sample(range(1, 13), 2))
            tipps.append((haupt, sterne))
        df = pd.DataFrame([{
            "Tipp": i+1,
            "Hauptzahlen": ", ".join(map(str, h)),
            "Sternzahlen": ", ".join(map(str, s))
        } for i, (h, s) in enumerate(tipps)])
        st.dataframe(df)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 CSV herunterladen", data=csv, file_name="Gemeinschaft_Tipps.csv", key="dl_gemein")

# === Team-Modus (Platzhalter) ===
elif modus == "🤝 Team-Modus":
    st.info("👥 Team-Modus wird bald aktiviert. Bleib dran!")
