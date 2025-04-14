
import streamlit as st
from st_supabase_connection import SupabaseConnection

@st.cache_resource
def get_client():
    conn = st.connection("supabase", type=SupabaseConnection)
    return conn.client

def save_strategy(user_email, strategy_name, parameters):
    supabase = get_client()
    data = {
        "email": user_email,
        "strategy_name": strategy_name,
        "parameters": parameters
    }
    response = supabase.table("Strategien").insert(data).execute()
    return response
