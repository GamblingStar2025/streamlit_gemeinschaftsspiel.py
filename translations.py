
def get_translations(lang):
    return {
        "de": {
            "welcome": "Willkommen bei EuroGenius",
            "login": "Einloggen",
            "start": "Jetzt starten",
            "numbers": "Zahlen",
            "stars": "Sternzahlen",
            "jackpot": "Nächster Jackpot",
        },
        "fr": {
            "welcome": "Bienvenue sur EuroGenius",
            "login": "Connexion",
            "start": "Commencer",
            "numbers": "Numéros",
            "stars": "Étoiles",
            "jackpot": "Prochain Jackpot",
        },
        "it": {
            "welcome": "Benvenuto su EuroGenius",
            "login": "Accesso",
            "start": "Inizia ora",
            "numbers": "Numeri",
            "stars": "Stelle",
            "jackpot": "Prossimo Jackpot",
        },
        "en": {
            "welcome": "Welcome to EuroGenius",
            "login": "Login",
            "start": "Start now",
            "numbers": "Numbers",
            "stars": "Stars",
            "jackpot": "Next Jackpot",
        }
    }.get(lang, {})
