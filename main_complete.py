import streamlit as st
from datetime import date
import pandas as pd
import random
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from collections import Counter
import json
import os
from fpdf import FPDF

# App-Konfiguration
st.set_page_config(page_title="EuroGenius", layout="centered")

# App-Header
st.markdown("""<style>
body { background-color: #0b1a2b; color: white; }
h1 { color: #FFD700; text-align: center; }
.stButton>button { background-color: #FFD700; color: #0b1a2b; font-weight: bold; }
</style>""", unsafe_allow_html=True)

st.image("https://chat.openai.com/cdn-cgi/image/width=256,quality=100/https://files.oaiusercontent.com/file-8ym196eg8EdEueSyg3X1fU", width=150)
st.markdown("# 🎯 EuroGenius\n### Die KI-basierte Lotto-App für Euromillionen")

# Nutzer-Login
st.markdown("## 🔐 Login")
user_type = st.radio("Nutzerrolle wählen", ["👤 Einzelspieler", "👥 Gemeinschaftsspiel"])
user_id = ""

def get_user_file(name):
    return f"/mnt/data/eurogenius_saved_{name}.json"

if user_type == "👥 Gemeinschaftsspiel":
    username = st.text_input("Benutzername")
    group_id = st.text_input("Gruppen-ID")
    if username and group_id:
        st.success(f"Willkommen, {username} in Gruppe {group_id}!")
        user_id = f"group_{group_id}_{username}"
    else:
        st.warning("Bitte Benutzername und Gruppen-ID eingeben.")
else:
    username = st.text_input("Dein Name")
    if username:
        st.success(f"Willkommen, {username}!")
        user_id = f"single_{username}"
    else:
        st.info("Bitte Namen eingeben.")

saved_tips_file = get_user_file(user_id) if user_id else ""

# Funktionen
@st.cache_data
def lade_historie():
    df = pd.read_csv("EuroMillion_Ziehungen.csv")
    haupt = df[[f"Hauptzahl {i}" for i in range(1, 6)]].values.flatten()
    stern = df[[f"Sternzahl {i}" for i in range(1, 3)]].values.flatten()
    return df, pd.Series(haupt).value_counts(), pd.Series(stern).value_counts()

df, h_count, s_count = lade_historie()
hot_haupt = list(h_count.sort_values(ascending=False).head(10).index)
cold_haupt = list(h_count.sort_values(ascending=True).head(10).index)
hot_stern = list(s_count.sort_values(ascending=False).head(5).index)
cold_stern = list(s_count.sort_values(ascending=True).head(5).index)

def generate_smart_tip(hot_weight=100):
    if hot_weight < 100:
        h_pool, s_pool = cold_haupt, cold_stern
    elif hot_weight > 100:
        h_pool, s_pool = hot_haupt, hot_stern
    else:
        h_pool, s_pool = list(range(1, 51)), list(range(1, 13))
    haupt = sorted(random.sample(h_pool, 5))
    stern = sorted(random.sample(s_pool, 2))
    return haupt, stern

def generate_cluster_tip():
    zahlen = df[[f"Hauptzahl {i}" for i in range(1, 6)]]
    X = zahlen.values
    kmeans = KMeans(n_clusters=5, random_state=0).fit(X)
    centers = kmeans.cluster_centers_.flatten()
    return sorted(random.sample(list(map(int, centers)), 5)), sorted(random.sample(range(1, 13), 2))

def generate_monte_tip(sim=100000):
    results = [tuple(sorted(random.sample(range(1, 51), 5))) for _ in range(sim)]
    most_common = pd.Series(results).value_counts().idxmax()
    return list(most_common), sorted(random.sample(range(1, 13), 2))

def generate_rad_tip():
    ring = list(range(1, 51))
    start = random.randint(0, 44)
    return sorted(ring[start:start+5]), sorted(random.sample(range(1, 13), 2))

# Nutzeroptionen
if user_id:
    modus = st.radio("Spielmodus wählen", ["👤 Einzelspieler", "👥 Gemeinschaftsspiel"])
    anzahl = st.slider("Anzahl Tipps", 1, 50 if modus == "👤 Einzelspieler" else 500)
    ki = st.slider("KI-Gewichtung", 0, 200, 100)
    sim = st.slider("Simulationen", 10000, 1000000, 100000, step=10000)

    use_hot = st.checkbox("🔥 Hot/Cold", value=True)
    use_cluster = st.checkbox("🧩 Cluster", value=True)
    use_rad = st.checkbox("♻️ Rad-Prinzip", value=True)
    use_monte = st.checkbox("🎲 Monte Carlo", value=True)

    ranking_counter = Counter()
    all_generated = []

    if st.button("🚀 Tipps generieren"):
        st.subheader("🧮 Generierte Tipps")
        tips_to_save = []
        for i in range(anzahl):
            if use_cluster:
                zahlen, sterne = generate_cluster_tip()
            elif use_monte:
                zahlen, sterne = generate_monte_tip(sim)
            elif use_rad:
                zahlen, sterne = generate_rad_tip()
            else:
                zahlen, sterne = generate_smart_tip(hot_weight=ki)

            tip = {'zahlen': zahlen, 'sterne': sterne}
            tips_to_save.append(tip)
            z = ", ".join(map(str, zahlen))
            s = " ⭐ ".join(map(str, sterne))
            st.success(f"Tipp {i+1}: {z} ⭐ {s}")
            all_generated.extend(zahlen + sterne)
            ranking_counter.update(zahlen + sterne)

        with open(saved_tips_file, 'w') as f:
            json.dump(tips_to_save, f)
        st.success("💾 Tipps gespeichert!")

        st.markdown("### 📈 Häufigkeit der generierten Zahlen")
        top = ranking_counter.most_common(10)
        zahlen, haeufigkeiten = zip(*top)
        fig, ax = plt.subplots()
        ax.bar(zahlen, haeufigkeiten)
        ax.set_title("Top 10 generierte Zahlen")
        st.pyplot(fig)

    # Wiederladen
    if os.path.exists(saved_tips_file):
        with open(saved_tips_file, 'r') as f:
            saved_tips = json.load(f)
        if st.checkbox("📂 Letzte Tipps anzeigen"):
            st.subheader("🗃️ Gespeicherte Tipps")
            for i, tip in enumerate(saved_tips, 1):
                zahlen = ", ".join(map(str, tip['zahlen']))
                sterne = " ⭐ ".join(map(str, tip['sterne']))
                st.info(f"Tipp {i}: {zahlen} ⭐ {sterne}")
        if st.button("📤 Exportiere Tipps als CSV"):
            df_export = pd.DataFrame([{**t, 'Tipp': i+1} for i, t in enumerate(saved_tips)])
            csv_path = f"/mnt/data/export_{user_id}.csv"
            df_export.to_csv(csv_path, index=False)
            st.download_button("⬇️ CSV herunterladen", data=open(csv_path, "rb"), file_name=f"eurogenius_tipps_{user_id}.csv")
        if st.button("📝 Exportiere Tipps als PDF"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="EuroGenius - Gespeicherte Tipps", ln=True, align='C')
            pdf.ln(10)
            for i, tip in enumerate(saved_tips, 1):
                zahlen = ", ".join(map(str, tip['zahlen']))
                sterne = " ⭐ ".join(map(str, tip['sterne']))
                pdf.cell(200, 10, txt=f"Tipp {i}: {zahlen} ⭐ {sterne}", ln=True)
            pdf_path = f"/mnt/data/export_{user_id}.pdf"
            pdf.output(pdf_path)
            st.download_button("⬇️ PDF herunterladen", data=open(pdf_path, "rb"), file_name=f"eurogenius_tipps_{user_id}.pdf")

st.caption(f"© {date.today().year} EuroGenius")
