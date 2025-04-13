
def eurogenius_css():
    return """
    <style>
        html, body, .main {
            background-color: #0a1128;
            color: #ffffff;
            font-family: 'Segoe UI', sans-serif;
        }
        h1, h2, h3 {
            color: #FFD700;
        }
        .stButton>button {
            background-color: #003f8c;
            color: white;
            font-weight: bold;
            border-radius: 14px;
            padding: 0.8em 1.6em;
            font-size: 18px;
            transition: 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #0057b8;
            transform: scale(1.04);
        }
        .stTextInput>div>input, .stSelectbox>div, .stSlider {
            border-radius: 10px;
            border: 1px solid #0057b8;
            background-color: #f0f8ff;
            color: black;
        }
        .stProgress>div>div {
            background-color: #FFD700;
        }
        .stExpanderHeader {
            color: #FFD700;
            font-weight: bold;
        }
    </style>
    """
