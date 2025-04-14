
import json
from supabase import create_client, Client

# Supabase-Verbindung (ersetzen durch deine Werte)
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-supabase-key"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def save_strategy(email, strategy_name, parameters):
    try:
        data = {
            "email": email,
            "strategy_name": strategy_name,
            "parameters": json.dumps(parameters)  # wichtig: als JSON-String speichern
        }

        response = supabase.table("Strategien").insert(data).execute()

        if response.status_code >= 400:
            raise Exception(f"Fehler bei Supabase: {response.json()}")

        return response

    except Exception as e:
        print("❌ Fehler beim Speichern der Strategie:", e)
        raise e
