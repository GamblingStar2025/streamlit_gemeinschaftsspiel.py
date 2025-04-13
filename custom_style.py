
def eurogenius_css():
    return """
<style>
    html, body, .main {
        background-color: #f4f9ff;
        font-family: 'Segoe UI', sans-serif;
    }
    h1, h2, h3 {
        color: #003366;
    }
    .stButton > button {
        background-color: #0057b8;
        color: white;
        font-weight: bold;
        border-radius: 12px;
        padding: 0.6em 1.2em;
        margin: 0.5em 0;
        transition: all 0.2s ease-in-out;
    }
    .stButton > button:hover {
        background-color: #003f8c;
        transform: scale(1.02);
    }
    .stTextInput > div > input {
        border-radius: 8px;
        border: 1px solid #aad4ff;
        padding: 0.5em;
        background-color: #ffffff;
    }
    .stSlider > div[data-testid="stSlider"] > div {
        background-color: #0057b8;
    }
    .stSelectbox > div {
        border-radius: 8px;
    }
    .stExpanderHeader {
        font-weight: bold;
        color: #003366;
    }
</style>
    """
