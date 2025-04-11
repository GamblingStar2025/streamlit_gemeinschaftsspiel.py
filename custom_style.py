
import streamlit as st

def eurogenius_css():
    st.markdown("""
    <style>
    body {
        background-color: #f0f2f6;
    }
    .main {
        background-color: white;
        padding: 2rem;
        border-radius: 2xl;
    }
    </style>
    """, unsafe_allow_html=True)
