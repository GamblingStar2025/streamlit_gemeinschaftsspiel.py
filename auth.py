import streamlit as st
from supabase import create_client, Client

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def register_user(email: str, password: str = None, user_type: str = "gast"):
    if user_type == "premium" and password:
        return supabase.auth.sign_up({"email": email, "password": password})
    return supabase.auth.sign_in_with_otp({"email": email})

def login_user(email: str, password: str = None, user_type: str = "gast"):
    if user_type == "premium" and password:
        return supabase.auth.sign_in_with_password({"email": email, "password": password})
    return supabase.auth.sign_in_with_otp({"email": email})

def get_user():
    return supabase.auth.get_user()