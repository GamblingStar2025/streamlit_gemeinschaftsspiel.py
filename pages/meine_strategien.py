
import streamlit as st
from st_supabase_connection import SupabaseConnection
from custom_style import eurogenius_css
import pandas as pd

st.set_page_config(page_title="📂 Meine Strategien", layout="centered")
st.markdown(eurogenius_css(), unsafe_allow_html=True)
st.title("📂 Meine gespeicherten Strategien")

conn = st.connection("supabase", type=SupabaseConnection)
supabase = conn.client

email = st.session_state.get("user_email", None)

if not email:
    st.warning("Bitte zuerst einloggen.")
else:
    res = supabase.table("strategien").select("*").eq("email", email).execute()
    if res.data:
        df = pd.DataFrame(res.data)
        df["parameters"] = df["parameters"].apply(lambda x: str(x))
        st.dataframe(df[["strategy_name", "parameters"]], use_container_width=True)
    else:
        st.info("Noch keine Strategien gespeichert.")
