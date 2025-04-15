import streamlit as st
from supabase_client import get_authenticated_client


def save_strategy(client, email: str, strategy_name: str, parameters: dict):
    data = {
        "email": email,
        "strategy_name": strategy_name,
        "parameters": parameters
    }

    # Debug-Ausgabe zur Fehleranalyse
    print("Daten zum Insert:", data)

    # Verwende den korrekten Tabellennamen (Case-sensitive!)
    response = client.table("Strategien").insert(data).execute()
    return response


# Hole den authentifizierten Supabase-Client
supabase = get_authenticated_client()
