
import requests
import streamlit as st

# Supabase Konfiguration – sichere Handhabung über secrets.toml
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_API_KEY = st.secrets["SUPABASE_API_KEY"]

HEADERS = {
    "apikey": SUPABASE_API_KEY,
    "Authorization": f"Bearer {SUPABASE_API_KEY}",
    "Content-Type": "application/json"
}

def get_user(email):
    """Benutzerdaten aus Supabase abrufen."""
    url = f"{SUPABASE_URL}/rest/v1/users?email=eq.{email}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        return data[0] if data else None
    else:
        st.error("Fehler beim Abrufen der Benutzerdaten.")
        return None

def add_user(email, role="Gast", startdatum=None, ablaufdatum=None):
    """Neuen Benutzer in Supabase einfügen."""
    payload = {
        "email": email,
        "rolle": role,
        "startdatum": startdatum,
        "ablaufdatum": ablaufdatum
    }
    response = requests.post(f"{SUPABASE_URL}/rest/v1/users", headers=HEADERS, json=payload)
    if response.status_code in (200, 201):
        return True
    else:
        st.error("Benutzer konnte nicht hinzugefügt werden.")
        return False
