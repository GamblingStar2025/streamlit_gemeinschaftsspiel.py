
from supabase import Client

def save_strategy(client: Client, email: str, strategy_name: str, parameters: dict):
    data = {
        "email": email,
        "strategy_name": strategy_name,
        "parameters": parameters
    }
    return client.table("Strategien").insert(data).execute()
