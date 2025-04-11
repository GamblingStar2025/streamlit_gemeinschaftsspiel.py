
import streamlit as st
import requests

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}"
}

def get_user(email):
    url = f"{SUPABASE_URL}/rest/v1/users?email=eq.{email}"
    return requests.get(url, headers=HEADERS)
