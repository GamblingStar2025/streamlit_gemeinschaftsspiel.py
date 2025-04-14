import streamlit as st
from supabase import create_client, Client

# Hole die Secrets
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def save_strategy(email: str, strategy_name: str, parameters: dict):
    data = {
        "email": email,
        "strategy_name": strategy_name,
        "parameters": parameters
    }
    response = supabase.table("Strategien").insert(data).execute()
    return response
