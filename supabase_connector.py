from supabase import create_client, Client

SUPABASE_URL = "https://paxolsdymswbzrgadqie.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBheG9sc2R5bXN3YnpyZ2FkcWllIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQ0MDA1NjYsImV4cCI6MjA1OTk3NjU2Nn0.0_N4VTDd4ov29HI1PHR3nkwQsk6wiX3URBc1kv_HIzY"

def get_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)