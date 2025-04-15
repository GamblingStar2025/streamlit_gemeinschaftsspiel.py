from supabase_connector import get_client

def save_strategy(email, strategy_name, parameters):
    supabase = get_client()
    data = {
        "email": email,
        "strategy_name": strategy_name,
        "parameters": parameters
    }
    response = supabase.table("strategien").insert(data).execute()
    return response