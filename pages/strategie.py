
import streamlit as st
import random
import matplotlib.pyplot as plt

st.set_page_config(page_title="Strategie", layout="centered")
st.title("🧠 Strategie-Setup mit Analyse")

strategien = ["Zufall", "Hot/Cold", "Clustering", "Monte Carlo", "KI (bald)"]
strategie = st.selectbox("Strategie wählen", strategien)

ziehungsbereich = st.slider("Ziehungen analysieren (Hot/Cold & Cluster)", 10, 100, 50)
simulation_runs = st.slider("Monte Carlo Runs", 1000, 10000, 5000)

if strategie == "Hot/Cold":
    st.subheader("Hot/Cold Analyse")
    hot = random.sample(range(1, 51), 5)
    cold = random.sample(range(1, 51), 5)
    st.write("🔥 Hot Numbers:", hot)
    st.write("❄️ Cold Numbers:", cold)
    st.bar_chart({"Hot": hot, "Cold": cold})

elif strategie == "Clustering":
    st.subheader("Clustering nach Häufigkeit")
    cluster_data = {
        "Häufig": random.sample(range(1, 51), 2),
        "Mittel": random.sample(range(1, 51), 2),
        "Selten": random.sample(range(1, 51), 1)
    }
    st.write(cluster_data)

elif strategie == "Monte Carlo":
    st.subheader("Monte Carlo Simulation")
    result = [random.randint(1, 50) for _ in range(simulation_runs)]
    fig, ax = plt.subplots()
    ax.hist(result, bins=50, edgecolor='black')
    st.pyplot(fig)

elif strategie == "KI (bald)":
    st.info("KI-Modul in Entwicklung – bald verfügbar!")

else:
    st.subheader("Zufallsgenerator")
    zahlen = sorted(random.sample(range(1, 51), 5))
    st.write("Dein Tipp:", zahlen)
