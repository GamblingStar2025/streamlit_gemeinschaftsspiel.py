def save_strategy(supabase, email, strategy_name, parameters):
    data = {
        "email": email,
        "strategy_name": strategy_name,
        "parameters": parameters
    }
    response = supabase.table("strategien").insert(data).execute()
    return response
