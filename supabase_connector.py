
import os
import requests

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

def add_user(email, rolle="gast", premium=False):
    import datetime
    payload = {
        "email": email,
        "rolle": rolle,
        "startdatum": datetime.datetime.utcnow().isoformat(),
        "premium": premium
    }
    return requests.post(f"{SUPABASE_URL}/rest/v1/users", headers=HEADERS, json=payload)

def get_user(email):
    return requests.get(f"{SUPABASE_URL}/rest/v1/users?email=eq.{email}", headers=HEADERS)

def save_tipps(user_email, strategie, zahlen):
    import datetime
    payload = {
        "user_email": user_email,
        "datum": datetime.datetime.utcnow().isoformat(),
        "strategie": strategie,
        "zahlen": zahlen
    }
    return requests.post(f"{SUPABASE_URL}/rest/v1/tipps", headers=HEADERS, json=payload)

def get_user_tipps(user_email):
    return requests.get(f"{SUPABASE_URL}/rest/v1/tipps?user_email=eq.{user_email}&order=datum.desc", headers=HEADERS)
