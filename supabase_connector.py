import streamlit as st
import requests

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_API_KEY = st.secrets["SUPABASE_API_KEY"]
HEADERS = {
    "apikey": SUPABASE_API_KEY,
    "Authorization": f"Bearer {SUPABASE_API_KEY}",
    "Content-Type": "application/json"
}

def add_user(email):
    return requests.post(f"{SUPABASE_URL}/rest/v1/users", json={"email": email}, headers=HEADERS)

def get_user(email):
    return requests.get(f"{SUPABASE_URL}/rest/v1/users?email=eq.{email}", headers=HEADERS)

def save_tipps(user_email, strategie, zahlen):
    return requests.post(f"{SUPABASE_URL}/rest/v1/tipps", json={
        "email": user_email,
        "strategie": strategie,
        "zahlen": zahlen
    }, headers=HEADERS)
