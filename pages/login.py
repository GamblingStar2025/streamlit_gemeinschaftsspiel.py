
import streamlit as st
from st_supabase_connection import SupabaseConnection
from custom_style import eurogenius_css

st.set_page_config(page_title="Login", layout="centered")
st.markdown(eurogenius_css(), unsafe_allow_html=True)

st.title("🔐 Login – EuroGenius")

conn = st.connection("supabase", type=SupabaseConnection)
supabase = conn.client

email = st.text_input("📧 E-Mail")

if st.button("🔐 Login mit Supabase"):
    response = supabase.table("users").select("role").eq("email", email).execute()
    if response.data:
        rolle = response.data[0]["role"]
        st.session_state["is_logged_in"] = True
        st.session_state["user_email"] = email
        st.session_state["rolle"] = rolle
        st.success(f"✅ Eingeloggt als {email} ({rolle})")
    else:
        st.error("❌ Benutzer nicht gefunden.")

if st.session_state.get("is_logged_in"):
    st.markdown(f"👤 Rolle: **{st.session_state['rolle']}**")
    if st.button("🚪 Logout"):
        st.session_state.clear()
        st.experimental_rerun()
