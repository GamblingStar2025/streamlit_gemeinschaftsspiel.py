
from supabase import create_client
import os

SUPABASE_URL = "https://paxolsdymswbzrgadqie.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def add_user(email, rolle="gast", premium=False):
    from datetime import datetime
    return supabase.table("users").insert({
        "email": email,
        "rolle": rolle,
        "startdatum": datetime.utcnow().isoformat(),
        "premium": premium
    }).execute()

def get_user(email):
    return supabase.table("users").select("*").eq("email", email).single().execute()

def save_tipps(user_email, strategie, zahlen):
    from datetime import datetime
    return supabase.table("tipps").insert({
        "user_email": user_email,
        "datum": datetime.utcnow().isoformat(),
        "strategie": strategie,
        "zahlen": zahlen
    }).execute()

def get_user_tipps(user_email):
    return supabase.table("tipps").select("*").eq("user_email", user_email).order("datum", desc=True).execute()
